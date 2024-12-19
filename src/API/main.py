from typing import Optional, List
from fastapi import FastAPI, Form, UploadFile, File
import shutil
import os
from tools import ImageEditor, PDFEditor


app = FastAPI(title="Imani", summary="Image Manipulation Tools", version="1.0")



@app.get("/")
async def home():
    return "Healthy"


UPLOAD_FOLDER = "uploaded_images"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

OUTPUT_FOLDER = "processed_pdfs"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


@app.post("/upload/")
def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "File uploaded successfully", "file_path": file_path}

@app.post("/resize/")
def resize_image(file_path: str = Form(...), width: Optional[int] = Form(None), height: Optional[int] = Form(None)):
    editor = ImageEditor(file_path)
    editor.resize(width=width, height=height)
    output_path = os.path.join(UPLOAD_FOLDER, "resized_" + os.path.basename(file_path))
    editor.save_image(output_path)
    return {"message": "Image resized successfully", "output_path": output_path}

@app.post("/rotate/")
def rotate_image(file_path: str = Form(...), angle: float = Form(...)):
    editor = ImageEditor(file_path)
    editor.rotate(angle=angle)
    output_path = os.path.join(UPLOAD_FOLDER, "rotated_" + os.path.basename(file_path))
    editor.save_image(output_path)
    return {"message": "Image rotated successfully", "output_path": output_path}

@app.post("/filter/")
def apply_filter(file_path: str = Form(...), filter_type: str = Form(...)):
    editor = ImageEditor(file_path)
    editor.apply_filter(filter_type=filter_type)
    output_path = os.path.join(UPLOAD_FOLDER, "filtered_" + os.path.basename(file_path))
    editor.save_image(output_path)
    return {"message": "Filter applied successfully", "output_path": output_path}

@app.post("/reset/")
def reset_image(file_path: str = Form(...)):
    editor = ImageEditor(file_path)
    editor.reset()
    output_path = os.path.join(UPLOAD_FOLDER, "reset_" + os.path.basename(file_path))
    editor.save_image(output_path)
    return {"message": "Image reset successfully", "output_path": output_path}


@app.post("/upload_pdf/")
def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "PDF uploaded successfully", "file_path": file_path}

@app.post("/convert_to_images/")
def convert_pdf_to_images(file_path: str = Form(...)):
    editor = PDFEditor(file_path)
    image_paths = editor.convert_to_images(output_folder=OUTPUT_FOLDER)
    return {"message": "PDF converted to images successfully", "image_paths": image_paths}

@app.post("/split_pdf/")
def split_pdf(file_path: str = Form(...)):
    editor = PDFEditor(file_path)
    pdf_paths = editor.split_pdf(output_folder=OUTPUT_FOLDER)
    return {"message": "PDF split into pages successfully", "pdf_paths": pdf_paths}


@app.post("/merge_pdfs/")
def merge_pdfs(file_paths: List[str] = Form(...)):
    output_path = os.path.join(OUTPUT_FOLDER, "merged.pdf")
    PDFEditor.merge_pdfs(pdf_paths=file_paths.split(","), output_path=output_path)
    return {"message": "PDFs merged successfully", "output_path": output_path}

@app.post("/extract_text/")
def extract_pdf_text(file_path: str = Form(...)):
    editor = PDFEditor(file_path)
    text = editor.extract_text()
    return {"message": "Text extracted successfully", "text": text}
