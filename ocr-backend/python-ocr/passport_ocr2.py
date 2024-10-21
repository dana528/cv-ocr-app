import logging
import re
import numpy as np
import pandas as pd
from paddleocr import PaddleOCR
from PIL import Image
from passporteye import read_mrz  # Make sure you have this import if you use PassportEye

# Initialize PaddleOCR
ocr = PaddleOCR(lang='en', use_gpu=False)

# Load the countries data from CSV to create a mapping of ISO codes to country names
country_df = pd.read_csv('countries.csv')
country_dict = dict(zip(country_df['ISO Code'], country_df['Country']))

# Function to extract MRZ data from the uploaded image using PassportEye
def extract_mrz_data(image):
    mrz = read_mrz(image, save_roi=True)
    if mrz is None:
        return {}
    
    mrz_data = mrz.to_dict()
    # Rename keys and clean up data for clarity
    mrz_data['nic_number'] = mrz_data.pop('personal_number', '').replace('<', '')
    mrz_data['passport_number'] = mrz_data.pop('number', '').replace('<', '')
    mrz_data['mrz_code'] = mrz_data.pop('raw_text', '')
    mrz_data['sex'] = 'Female' if mrz_data.get('sex', '') == 'F' else 'Male'
    mrz_data['country_code'] = mrz_data.pop('nationality', '').replace('<', '')
    mrz_data['country'] = country_dict.get(mrz_data['country_code'], '')  # Get country name from country code

    # Format the expiration date and calculate issue date
    expiration = mrz_data.get('expiration_date', '')
    if len(expiration) == 6:
        year, month, day = expiration[:2], expiration[2:4], expiration[4:]
        mrz_data['expiration_date'] = f"20{year}-{month}-{day}"
        issue_year = str(int("20" + year) - 10)
        mrz_data['issue_date'] = f"{issue_year}-{month}-{day}"
    else:
        mrz_data['issue_date'] = ''

    # Format the date_of_birth and determine year prefix
    dob = mrz_data.get('date_of_birth', '')
    if len(dob) == 6:
        year, month, day = dob[:2], dob[2:4], dob[4:]
        year_prefix = "19" if "V" in mrz_data['nic_number'] else "20"
        mrz_data['date_of_birth'] = f"{year_prefix}{year}-{month}-{day}"
    else:
        mrz_data['date_of_birth'] = ''

    return mrz_data

# Function to extract text from image using PaddleOCR
def extract_text_from_image(image):
    image_array = np.array(image)
    result = ocr.ocr(image_array, rec=True)  # Call OCR
    extracted_text = " ".join([line[1][0] for line in result[0]])  # Extract text
    return extracted_text
