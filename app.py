from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
import shutil
import os
from adfi_inference import classify_hair
from db_control.crud import (
    get_db,
    create_hair_quality,
    get_hair_quality_by_id,
    get_all_hair_quality,
    update_hair_quality,
    delete_hair_quality
)

# フォームデータに合わせたPydanticモデル
class HairQuality(BaseModel):
    nickname: str
    age: int
    gender: str
    density: str
    hair_loss: str
    scalp: List[str]  # フロントから配列で受け取る想定
    thickness: str
    texture: List[str]  # フロントから配列で受け取る想定
    firmness: str

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "FastAPI top page!"}

# データ新規作成（CREATE）
@app.post("/hairQuality")
def create_hair_quality_data(hair_quality: HairQuality, db: Session = Depends(get_db)):
    return create_hair_quality(db, hair_quality.dict())

# 全データ取得（READ）
@app.get("/hairQuality")
def read_all_hair_quality_data(db: Session = Depends(get_db)):
    return get_all_hair_quality(db)

# ID指定データ取得（READ）
@app.get("/hairQuality/{hair_quality_id}")
def read_one_hair_quality_data(hair_quality_id: int, db: Session = Depends(get_db)):
    result = get_hair_quality_by_id(db, hair_quality_id)
    if not result:
        raise HTTPException(status_code=404, detail="HairQuality data not found")
    return result

# データ更新（UPDATE）
@app.put("/hairQuality/{hair_quality_id}")
def update_hair_quality_data(hair_quality_id: int, hair_quality: HairQuality, db: Session = Depends(get_db)):
    result = update_hair_quality(db, hair_quality_id, hair_quality.dict())
    if not result:
        raise HTTPException(status_code=404, detail="HairQuality data not found")
    return result

# データ削除（DELETE）
@app.delete("/hairQuality/{hair_quality_id}")
def delete_hair_quality_data(hair_quality_id: int, db: Session = Depends(get_db)):
    result = delete_hair_quality(db, hair_quality_id)
    if not result:
        raise HTTPException(status_code=404, detail="HairQuality data not found")
    return {"id": hair_quality_id, "status": "deleted"}

# adfiおはげモデルにファイルを送る
@app.post("/classify-hair/")
async def classify_hair_image(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = classify_hair(temp_path)

    os.remove(temp_path)  # ファイル削除
    return result