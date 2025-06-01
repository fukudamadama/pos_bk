from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import text                              # ← 追加
from sqlalchemy.exc import SQLAlchemyError               # ← 追加
import shutil
import os
from db_control.crud import (
    get_db,
    create_hair_quality,
    get_hair_quality_by_id,
    get_all_hair_quality,
    update_hair_quality,
    delete_hair_quality
)   
# ★★★hairquestionyouをデータベースから持ってくる
from db_control.crud import (
    create_hair_questionyou,
    get_hair_questionyou_by_id,
    get_all_hair_questionyou,   
    update_hair_questionyou,
    delete_hair_questionyou
)

# HairQuestionYou を mymodels_MySQL からインポート
from db_control.mymodels_MySQL import HairQuestionYou
from db_control.connect_MySQL import engine 

# フォームデータに合わせたPydanticモデル
class HairQuality(BaseModel):
    density: str
    hair_loss: str
    scalp: List[str]  # フロントから配列で受け取る想定
    thickness: str
    texture: List[str]  # フロントから配列で受け取る想定
    firmness: str

# ★★★HairQuestionYouをクラスに文字列を定義
class HairQuestionYou(BaseModel):
    nickname: str
    age: int # 数字なのでint
    gender: str
    bloodtype: str
    occupation: str
    familyhage: str
    eatinghabits: str
    sleep: str
    stress: str
    undo: str
    drink: str
    smoke: str
    usugemotivation: str
    usugeexperience: str
    futureaga: str
    sindan: str


app = FastAPI()


# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # ローカル（Next.js開発環境）
        "https://app-002-step3-2-node-oshima2.azurewebsites.net"  # 本番
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"message": "FastAPI top page!"}

## DB接続テスト用
@app.get("/dbtest", tags=["Health Check"])
async def db_connection_test():
    """
    <!--
        このエンドポイントを叩くと、
        - engine.connect() で接続を試み
        - SELECT 1 を実行
        - 正常なら {"db_status": "ok"} を返す
        - 失敗したら例外を吐いて 500 返却
    -->
    """
    try:
        # 1) engine.connect() を使って生の Connection を取得し、直接クエリを実行
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1;"))
            # 結果を取得（[(1,)] のように返るはず）
            fetched = result.fetchone()
            if fetched and fetched[0] == 1:
                return {"db_status": "ok"}
            else:
                # もしなにか想定外なら明示的にエラーを返す
                raise HTTPException(status_code=500, detail="Unexpected DB response")
    except SQLAlchemyError as e:
        # SQLAlchemy／DB 接続まわりで何か SQLException が起きた場合
        raise HTTPException(status_code=500, detail=f"DB connection failed: {str(e)}")
    except Exception as e:
        # その他のエラー
        raise HTTPException(status_code=500, detail=f"Unknown error: {str(e)}")



# データ新規作成（CREATE）
@app.post("/kamokamo/hairQuality")
def create_hair_quality_data(hair_quality: HairQuality, db: Session = Depends(get_db)):
    return create_hair_quality(db, hair_quality.dict())

# データ新規作成（CREATE）
# ★★★hairQuestionYouについて追加
@app.post("/kamokamo/hairQuality/hairQuestionYou")
def create_hair_questionyou_data(hair_questionyou: HairQuestionYou, db: Session = Depends(get_db)):
    return create_hair_questionyou(db, hair_questionyou.dict())

# hair_quality_idで指定してhairQuestionYouを新規登録するPOSTルート（新規追加！）
# ★★★hairQualityに紐づくhairQuestionYouを新規登録
@app.post("/kamokamo/hairQuality/{hair_quality_id}/hairQuestionYou")
def create_hair_questionyou_with_quality_id(
    hair_quality_id: int,
    hair_questionyou: HairQuestionYou,
    db: Session = Depends(get_db)
):
    data = hair_questionyou.dict()
    data["hair_quality_id"] = hair_quality_id
    return create_hair_questionyou(db, data)

# 全データ取得（READ）
@app.get("/kamokamo/hairQuality")
def read_all_hair_quality_data(db: Session = Depends(get_db)):
    return get_all_hair_quality(db)


# 全データ取得（READ）
# ★★★hairQuestionYouについて追加
@app.get("/kamokamo/hairQuality/hairQuestionYou")
def read_all_hair_questionyou_data(db: Session = Depends(get_db)):
    return get_all_hair_questionyou(db)


# ID指定データ取得（READ）
@app.get("/kamokamo/hairQuality/{hair_quality_id}")
def read_one_hair_quality_data(hair_quality_id: int, db: Session = Depends(get_db)):
    result = get_hair_quality_by_id(db, hair_quality_id)
    if not result:
        raise HTTPException(status_code=404, detail="HairQuality data not found")
    return result


# ID指定データ取得（READ）
# ★★★hairQuestionYouについて追加
@app.get("/kamokamo/hairQuality/hairQuestionYou/{hair_questionyou_id}")
def read_one_hair_questionyou_data(hair_questionyou_id: int, db: Session = Depends(get_db)):
    result = get_hair_questionyou_by_id(db, hair_questionyou_id)
    if not result:
        raise HTTPException(status_code=404, detail="HairQuestionYou data not found")
    return result

# hair_quality_idで指定してhairQuestionYouを取得するGETルート（新規追加！）
# ★★★hairQualityに紐づくhairQuestionYouを取得
@app.get("/kamokamo/hairQuality/{hair_quality_id}/hairQuestionYou")
def read_questionyou_by_hair_quality(hair_quality_id: int, db: Session = Depends(get_db)):
    result = db.query(HairQuestionYou).filter(HairQuestionYou.hair_quality_id == hair_quality_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="HairQuestionYou (by hair_quality_id) not found")
    return result

# データ更新（UPDATE）
@app.put("/kamokamo/hairQuality/{hair_quality_id}")
def update_hair_quality_data(hair_quality_id: int, hair_quality: HairQuality, db: Session = Depends(get_db)):
    result = update_hair_quality(db, hair_quality_id, hair_quality.dict())
    if not result:
        raise HTTPException(status_code=404, detail="HairQuality data not found")
    return result


# データ更新（UPDATE）
# # ★★★hairQuestionYouについて追加
@app.put("/kamokamo/hairQuality/hairQuestionYou/{hair_questionyou_id}")
def update_hair_questionyou_data(hair_questionyou_id: int, hair_questionyou: HairQuestionYou, db: Session = Depends(get_db)):
    result = update_hair_questionyou(db, hair_questionyou_id, hair_questionyou.dict())
    if not result:
        raise HTTPException(status_code=404, detail="HairQuestionYou data not found")
    return result


# データ削除（DELETE）
@app.delete("/kamokamo/hairQuality/{hair_quality_id}")
def delete_hair_quality_data(hair_quality_id: int, db: Session = Depends(get_db)):
    result = delete_hair_quality(db, hair_quality_id)
    if not result:
        raise HTTPException(status_code=404, detail="HairQuality data not found")
    return {"id": hair_quality_id, "status": "deleted"}


# データ削除（DELETE）
# ★★★hairQuestionYouについて追加
@app.delete("/kamokamo/hairQuestionYou/{hair_questionyou_id}")
def delete_hair_questionyou_data(hair_questionyou_id: int, db: Session = Depends(get_db)):
    result = delete_hair_questionyou(db, hair_questionyou_id)
    if not result:
        raise HTTPException(status_code=404, detail="hairQuestionYou data not found")
    return {"id": hair_questionyou_id, "status": "deleted"}



# adfiおはげモデルにファイルを送る
@app.post("/classify-hair/")
async def classify_hair_image(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = classify_hair(temp_path)

    os.remove(temp_path)  # ファイル削除
    return result

#髪質診断＋おハゲモデルでOpenAIに診断してもらう
class Question(BaseModel):
    hageLevel: str

@app.post("/diagnostic_kamo/")
async def ask_diagnostic(question: Question):
    """
    髪質診断＋おハゲモデルでOpenAIに診断してもらう
    """
    try:
        # かも先生の診断コメント関数を呼び出す
        answer = diagnostic_kamo(question.hageLevel)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
