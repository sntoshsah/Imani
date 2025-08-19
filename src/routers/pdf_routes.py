from typing import List, Optional
from fastapi import APIRouter, Form, UploadFile, File
from ..tools import PDFEditor
import os
import shutil

pdf_router = APIRouter(tags=["pdf"])



UPLOAD_FOLDER = "uploaded_images"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

OUTPUT_FOLDER = "processed_pdfs"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@pdf_router.post("/upload_pdf/", tags=["pdf"])
def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "PDF uploaded successfully", "file_path": file_path}

@pdf_router.post("/convert_to_images/")
def convert_pdf_to_images(file_path: str = Form(...)):
    editor = PDFEditor(file_path)
    image_paths = editor.convert_to_images(output_folder=OUTPUT_FOLDER)
    return {"message": "PDF converted to images successfully", "image_paths": image_paths}

@pdf_router.post("/split_pdf/")
def split_pdf(file_path: str = Form(...)):
    editor = PDFEditor(file_path)
    pdf_paths = editor.split_pdf(output_folder=OUTPUT_FOLDER)
    return {"message": "PDF split into pages successfully", "pdf_paths": pdf_paths}



@pdf_router.post("/merge_pdfs/")
def merge_pdfs(file_paths: List[str] = Form(...)):
    output_path = os.path.join(OUTPUT_FOLDER, "merged.pdf")
    print(file_paths)
    PDFEditor.merge_pdfs(pdf_paths=file_paths, output_path=output_path)
    return {"message": "PDFs merged successfully", "output_path": output_path}


@pdf_router.post("/extract_text/")
def extract_pdf_text(file_path: str = Form(...)):
    editor = PDFEditor(file_path)
    text = editor.extract_text()
    return {"message": "Text extracted successfully", "text": text}
