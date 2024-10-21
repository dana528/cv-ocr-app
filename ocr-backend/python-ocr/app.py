import logging
from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, ImageOps
import io
import numpy as np
import os
from paddleocr import PaddleOCR


# Import individual document type processing modules
from dl_ocr import process_dl_ocr  # Ensure this module is available
from passport import process_passport_ocr  # Ensure this module is available

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Directory to store uploaded images
UPLOAD_DIRECTORY = "./uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

app = FastAPI()
# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize PaddleOCR once for all document types
ocr = PaddleOCR(lang='en', use_gpu=False)

def correct_orientation(image):
    """Correct the orientation of the image based on EXIF data."""
    try:
        image = ImageOps.exif_transpose(image)
    except Exception as e:
        logging.error(f"Orientation correction failed: {e}")
    return image

@app.post("/process")
async def process_image(image: UploadFile = File(...), doc_type: str = Form(...)):
    """Process the uploaded image and extract information based on the document type."""
    
    logging.info(f"Received a request to process a document of type {doc_type}")
    
    # Check if image is uploaded
    if not image:
        logging.error("No image uploaded")
        raise HTTPException(status_code=400, detail="No image uploaded")
    
    # Check if the uploaded file is an image
    if not image.content_type.startswith('image/'):
        logging.error("Uploaded file is not an image. Content type: %s", image.content_type)
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")
    
    try:
        logging.info(f"Processing document of type {doc_type} with file: {image.filename}")

        # Read the uploaded image file
        image_bytes = await image.read()
        logging.info(f"Image bytes length: {len(image_bytes)}")

        # Save the uploaded image to the specified directory
        try:
            image_path = os.path.join(UPLOAD_DIRECTORY, image.filename)
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            logging.info(f"Image successfully saved at: {image_path}")
        except Exception as e:
            logging.error(f"Error saving image: {str(e)}")
            raise HTTPException(status_code=500, detail="Error saving image")

        # Try opening the image and converting it to RGB
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            logging.info("Image successfully opened and converted to RGB.")
        except Exception as e:
            logging.error(f"Error opening image: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Correct image orientation if necessary
        image = correct_orientation(image)
        logging.info("Image orientation corrected.")

        # Convert image to numpy array
        image_np = np.array(image)
        logging.info(f"Image successfully converted to NumPy array. Shape: {image_np.shape}")

        # Perform OCR
        logging.info("Starting OCR process...")
        ocr_results = ocr.ocr(image_np, rec=True)
        logging.info(f"OCR results: {ocr_results}")

        # Route the OCR results to the appropriate function based on document type
        if doc_type == 'DL':
            logging.info("Processing OCR results for DL document.")
            extracted_info = process_dl_ocr(ocr_results)
        elif doc_type == 'Passport':
            logging.info("Processing OCR results for Passport document.")
            
            # Add detailed logging of the OCR results before processing
            logging.debug(f"OCR results passed to process_passport_ocr: {ocr_results}")
            
            extracted_info = process_passport_ocr(ocr_results)
            logging.info(f"Extracted Passport Info: {extracted_info}")
        else:
            logging.error(f"Invalid document type: {doc_type}")
            raise HTTPException(status_code=400, detail="Invalid document type")

        # Return the extracted info
        logging.info(f"Successfully extracted info: {extracted_info}")
        return JSONResponse(content={'extracted_info': extracted_info})

    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail="Image processing failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_config="logging_config.yaml")
