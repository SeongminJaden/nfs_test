from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List
import yaml
from urllib.parse import quote

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

@app.get("/image-meta/{image_id}")
def get_image_meta(image_id: str):
    folder_path = get_folder_path("2d")  # 2d 폴더 경로 가져오기
    yaml_path = os.path.join(folder_path, f"{image_id}.yaml")  # quote()는 필요없음, 파일명 그대로 사용 가능

    if not os.path.isfile(yaml_path):
        raise HTTPException(status_code=404, detail="YAML metadata not found")

    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"YAML read error: {str(e)}")

    return metadata