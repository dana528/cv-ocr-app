from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import cv2
import logging
import numpy as np
from PIL import Image, ImageDraw
from dl_ocr2 import load_and_process_image, process_ocr_results
from passport_ocr2 import extract_text_from_image,extract_mrz_data
from cr_book_ocr2 import(
    process_ocr_result_reg_no,
    process_ocr_result_chassis_no,
    process_ocr_result_engine_no,
    process_ocr_result_cylinder_capacity,
    process_ocr_result_class_of_vehicle, 
    process_ocr_result_taxation_class, 
    process_ocr_result_status_when_reg,
    process_ocr_result_fuel_type, 
    combined_pipeline_all_fields
)

from io import BytesIO

app = FastAPI()

# Configure CORS and logging
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIRECTORY = "./uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


field_params = {
    "REGISTRATION_NO": ([9, 14, 12, 10], 12.5, process_ocr_result_reg_no),
    "CHASSIS_NO": ([55, 12, 69, 10], 11, process_ocr_result_chassis_no),
    "ENGINE_NO": ([9, 49, 13, 45], 10, process_ocr_result_engine_no),
    "CYLINDER_CAPACITY": ([56, 49, 61, 45], 6, process_ocr_result_cylinder_capacity),
    "CLASS_OF_VEHICLE": ([10, 52, 16, 47], 8, process_ocr_result_class_of_vehicle),
    "TAXATION_CLASS": ([56, 52, 64, 48], 10, process_ocr_result_taxation_class),
    "STATUS_WHEN_REGISTERED": ([10, 55, 14, 50], 7, process_ocr_result_status_when_reg),
    "FUEL_TYPE": ([56, 55, 58, 50], 7, process_ocr_result_fuel_type)
}


@app.post("/process")
async def process_image(image: UploadFile = File(...), doc_type: str = Form(...)):
    """Process the uploaded image and extract information based on the document type."""
    
    logging.info(f"Received request to process a document of type: {doc_type}")
    
    if not image:
        raise HTTPException(status_code=400, detail="No image uploaded")
    
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")
    
    try:
        # Read and save the uploaded image
        image_bytes = await image.read()
        image_path = os.path.join(UPLOAD_DIRECTORY, image.filename)
        with open(image_path, "wb") as f:
            f.write(image_bytes)

        extracted_info = None  # Initialize the variable for extracted info

        # Load and process the image only if it's a Driving License
        if doc_type == 'DL':
            ocr_results = load_and_process_image(image_path)  # Call only for DL
            if ocr_results is None:
                logging.error("load_and_process_image returned None.")
                raise HTTPException(status_code=500, detail="Image processing failed in DL.")        
            
            extracted_info = process_ocr_results(ocr_results)
            # Return extracted information as JSON response
        elif doc_type == 'Passport':
            # Call process_passport_ocr directly if it's a passport
            image2 = Image.open(image.file)
            # Save the image temporarily if extract_mrz_data needs a file path
            temp_image_path = os.path.join(UPLOAD_DIRECTORY, 'temp_passport_image.jpg')
            image2.save(temp_image_path)  # Save the image as a file
            
            mrz_data = extract_mrz_data(temp_image_path)  # Adjust this if you have a specific method
            
            if mrz_data is None:
                logging.error("extract_mrz_data returned None.")
                raise HTTPException(status_code=500, detail="Image processing failed in Passport.")

            extracted_text = extract_text_from_image(image2)
            extracted_info = {'mrz_data': mrz_data, 'text': extracted_text}
            
            # Return extracted information as JSON response
        elif doc_type == 'CRBook':  
            logging.info("Starting CR Book image processing...")

            try:
                # Open the image from the uploaded file
                uploaded_image = Image.open(image.file)
                logging.info("Image opened successfully.")
        
                # Convert the image to OpenCV format
                image_np = np.array(uploaded_image.convert('RGB'))
                image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
                # Define a path to save the processed image
                image_path = os.path.join(UPLOAD_DIRECTORY, 'temp_crbook_image.jpg')
        
                # Save the image in OpenCV format
                cv2.imwrite(image_path, image_cv)
                logging.info("Image converted and saved successfully.")
        
                # Call the CR Book OCR processing pipeline
                extracted_info = combined_pipeline_all_fields(image_path, field_params)
                logging.info("CR Book OCR processing completed.")
        
            except Exception as e:
                logging.error(f"Error during CR Book processing: {str(e)}")
                raise HTTPException(status_code=500, detail="Image processing failed in CR Book.")

        else:
            raise HTTPException(status_code=400, detail="Invalid document type")

        # Return the extracted info
        return JSONResponse(content={'extracted_info': extracted_info})

    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail="Image processing failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)


