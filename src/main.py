from typing import Optional, List
from fastapi import FastAPI, Form, UploadFile, File
import shutil
import os
from .routers.image_routes import img_router
from .routers.pdf_routes import pdf_router
from .routers.user_routes import user_router
from .database import create_tables
# from . import models



app = FastAPI(title="Imani", summary="Image Manipulation Tools", version="1.0")

# Create database tables
create_tables()

app.include_router(router=img_router)
app.include_router(router=pdf_router)
app.include_router(router=user_router)

@app.get("/")
async def home():
    return "Healthy"

