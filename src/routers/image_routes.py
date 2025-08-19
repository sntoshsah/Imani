from typing import List, Optional
from fastapi import APIRouter, Form, UploadFile, File
from ..tools import ImageEditor
import os
import shutil



img_router =  APIRouter(tags=["Image"])


UPLOAD_FOLDER = "uploaded_images"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

OUTPUT_FOLDER = "processed_pdfs"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)




@img_router.post("/upload/", tags=["Image"])
def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "File uploaded successfully", "file_path": file_path}

@img_router.post("/resize/")
def resize_image(file_path: str = Form(...), width: Optional[int] = Form(None), height: Optional[int] = Form(None)):
    editor = ImageEditor(file_path)
    editor.resize(width=width, height=height)
    output_path = os.path.join(UPLOAD_FOLDER, "resized_" + os.path.basename(file_path))
    editor.save_image(output_path)
    return {"message": "Image resized successfully", "output_path": output_path}

@img_router.post("/rotate/")
def rotate_image(file_path: str = Form(...), angle: float = Form(...)):
    editor = ImageEditor(file_path)
    editor.rotate(angle=angle)
    output_path = os.path.join(UPLOAD_FOLDER, "rotated_" + os.path.basename(file_path))
    editor.save_image(output_path)
    return {"message": "Image rotated successfully", "output_path": output_path}

@img_router.post("/filter/")
def apply_filter(file_path: str = Form(...), filter_type: str = Form(...)):
    editor = ImageEditor(file_path)
    editor.apply_filter(filter_type=filter_type)
    output_path = os.path.join(UPLOAD_FOLDER, "filtered_" + os.path.basename(file_path))
    editor.save_image(output_path)
    return {"message": "Filter applied successfully", "output_path": output_path}

@img_router.post("/extract_text_from_image/")
def extract_text_from_image(file: UploadFile = File(...)):
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    editor = ImageEditor(image_path)
    text = editor.extract_text_from_image()
    return {"message": "Text extracted from image successfully", "text": text}

@img_router.post("/reset/")
def reset_image(file_path: str = Form(...)):
    editor = ImageEditor(file_path)
    editor.reset()
    output_path = os.path.join(UPLOAD_FOLDER, "reset_" + os.path.basename(file_path))
    editor.save_image(output_path)
    return {"message": "Image reset successfully", "output_path": output_path}

