# Document Info Extractor Application


This application allows users to upload documents (Driving License, Passport, Vehicle CR Book) and extract information from them. It includes both a **frontend** built with React and a **backend** built with FastAPI and Python.

## Features

- Upload images of documents
- Extract information from Driving License, Passport, and CR Book
- Display extracted information

## Prerequisites

To run this project, you will need the following:

- Node.js (for running the React frontend).
- npm(Node.js package managers).
- Python 3.8+ (for running the FastAPI backend).
- pip (Python package manager).
- Virtualenv (optional, but recommended to manage Python dependencies).

# Frontend Setup

The frontend is built using React and allows users to upload documents and view extracted information.

1. Navigate to frontend Directory:

cd cv-ocr-app
cd ocr-frontend

2. Then start the frontend server,

npm start

3. Then it will start on http://localhost:3000.

# Backend Setup

1. First install necessary dependencies.

pip install -r requirements.txt

2. Navigate to backend directory.

cd cv-ocr-app
cd ocr-backend
cd python-ocr

3. Then start the backend server running(FastAPI backend server) 

uvicorn main:app --reload --host 0.0.0.0 --port 8000
