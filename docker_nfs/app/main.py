from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FILES_DIR = "/app/files/media_files"
FOLDERS = ["2d", "3d", "record"]

def get_folder_path(folder_name: str):
    if folder_name not in FOLDERS:
        raise HTTPException(status_code=404, detail="Folder not found")
    folder_path = os.path.join(FILES_DIR, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

@app.get("/list/{folder_name}", response_model=List[str])
async def list_files(folder_name: str):
    folder_path = get_folder_path(folder_name)
    return os.listdir(folder_path)

@app.get("/download/{folder_name}/{file_name}")
async def download_file(folder_name: str, file_name: str):
    folder_path = get_folder_path(folder_name)
    file_path = os.path.join(folder_path, file_name)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=file_name)

@app.post("/upload/{folder_name}")
async def upload_file(folder_name: str, file: UploadFile = File(...)):
    folder_path = get_folder_path(folder_name)
    file_path = os.path.join(folder_path, file.filename)
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    return {"filename": file.filename, "message": "Upload successful"}
