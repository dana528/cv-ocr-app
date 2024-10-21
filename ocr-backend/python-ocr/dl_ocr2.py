import logging
import re
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image

# Initialize PaddleOCR
ocr = PaddleOCR(lang='en', use_gpu=False)

def load_and_process_image(image_file):
    """Load the image file and perform OCR."""
    image = Image.open(image_file).convert('RGB')
    image_np = np.array(image)
    if image_np is None:
        logging.error("Image conversion to NumPy array failed.")
        return None
    result = ocr.ocr(image_np, rec=True)

    return result  # Return OCR results

def process_ocr_results(ocr_results):
    """Extract relevant information from the OCR results for Driving Licenses."""
    extracted_info = {
        "Driving_Licence_No": None,
        "National_Identification_Card_No": None,
        "Name": None,
        "Address": None,
        "Data_Of_Birth": None,
        "Date_Of_Issue": None,
        "Date_Of_Expiry": None,
        "Blood_Group": None
    }

    for page in ocr_results:
        for i, line in enumerate(page):
            text = line[1][0]
            if re.search(r'^5\.(B|8)\d+', text):
                match = re.sub(r'^5\.', '', text)
                extracted_info["Driving_Licence_No"] = "B" + match[1:]

            elif re.search(r'^B\d{7}', text):
                extracted_info["Driving_Licence_No"] = text

            elif re.search(r'\d{9,}', text):
                match = re.search(r'\d{9,}[A-Za-z]*', text)
                if match:
                    extracted_info["National_Identification_Card_No"] = match.group()
                else:
                    extracted_info["National_Identification_Card_No"] = text

            elif re.search(r"^(1,2\.|\.2|1\.2\.|12\.|1,2,|1\.2,|,2).+$", text):
                match = re.sub(r'\d+', '', text)  # Remove numbers from the text
                match = re.sub(r'[,.]', '', match)  # Remove commas and periods from the text
                # Check if there's another line to process
                if i + 1 < len(page):
                    temp = page[i + 1][1][0]
                    if temp == "SL":
                        temp = ""
                    if re.search(r'^(8|B)\.', temp):
                        temp = ""
                else:
                    temp = ""  # No further line to process
                merge_name = f"{match} {temp}".strip()  # Merge and strip any extra spaces
                extracted_info["Name"] = merge_name

            elif re.search(r'^(8|B)\.', text):
                match = text[2:]  # Remove prefix and capture the rest of the text
                temp_list = [page[j][1][0] for j in range(i + 1, min(i + 3, len(page)))] if i + 2 < len(page) else [page[j][1][0] for j in range(i + 1, len(page))] if i + 1 < len(page) else []

                # Remove 'SL' from temp_list
                temp_list = [line for line in temp_list if 'SL' not in line]

                # Remove any strings that match the date pattern
                temp_list = [line for line in temp_list if not re.match(r'^(3|5)\.\d{2}\.\d{2}\.\d{4}', line)]

                # Merge 'match' with the remaining values in temp_list
                merge = ' '.join([match] + temp_list)

                extracted_info["Address"] = merge

            elif re.search(r'^(3|5)\.\d{2}\.\d{2}\.\d{4}', text):
                extracted_info["Data_Of_Birth"] = text.split('.', 1)[1].strip()

            elif re.search(r'^4(a|s)\.\d{2}\.\d{2}\.\d{4}', text):
                extracted_info["Date_Of_Issue"] = text.split('.', 1)[1].strip()

            elif re.search(r'^4(b|6)\.\d{2}\.\d{2}\.\d{4}', text):
                extracted_info["Date_Of_Expiry"] = text.split('.', 1)[1].strip()

            elif re.search(r'^Blood', text, re.IGNORECASE):
                match = text  # Current line
                # Check if there's another line to process
                if i + 1 < len(page):
                    temp = page[i + 1][1][0]
                    # Check if the next line contains '+' 
                    if '+' not in temp:
                        temp = ""
                else:
                    temp = ""  # No further line to process

                # Merge 'match' with 'temp' if 'temp' is not empty
                merge = f"{match} {temp}".strip() if temp else match.strip()
                # Extract the blood group information
                extracted_info["Blood_Group"] = merge.split(None, 2)[-1]

    logging.info(f"Extracted Driving License Info: {extracted_info}")

    return extracted_info
