from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from summerize import process_pdf_and_query
import os
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure uploads directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/answer")
async def get_answer(
    file: UploadFile = File(...),
    text: str = Form(...)
):
    """
    Dynamically process any PDF uploaded by user
    """
    # Save the uploaded PDF
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process this specific PDF with LangChain (dynamic!)
    answer = process_pdf_and_query(file_path, text)
    
    return {"text": answer}

@app.get("/hello")
def read_root():
    return {"message": "Hello, World!"}