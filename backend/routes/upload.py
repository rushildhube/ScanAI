import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List
from uuid import uuid4
from config.settings import settings
from routes.auth import get_current_user
from datetime import datetime
from config.database import db

router = APIRouter()

@router.post("/upload")
async def upload_images(files: List[UploadFile] = File(...), user: dict = Depends(get_current_user)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    if len(files) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 files can be uploaded")

    user_email = user.get("email")
    user_uploads_dir = os.path.join(settings.UPLOADS_DIR, user_email, "images")
    os.makedirs(user_uploads_dir, exist_ok=True)
    
    saved_files = []
    for file in files:
        file_extension = os.path.splitext(file.filename)[1]
        file_path = os.path.join(user_uploads_dir, f"{uuid4()}{file_extension}")
        try:
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            saved_files.append({"path": file_path, "filename": file.filename})
        except Exception:
            raise HTTPException(status_code=500, detail="Could not save file")
    
    # Create an analysis record and return its ID
    analysis_record = {
        "user_id": str(user["_id"]),
        "status": "uploaded",
        "timestamp": datetime.now(),
        "image_paths": [f["path"] for f in saved_files]
    }
    result = await db.db["analyses"].insert_one(analysis_record)
    return {"message": "Files uploaded successfully", "analysis_id": str(result.inserted_id)}