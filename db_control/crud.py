# uname() error回避
import platform
print("platform", platform.uname())

from sqlalchemy.orm import Session
from db_control.connect_MySQL import SessionLocal
from db_control.mymodels_MySQL import HairQuality
# ★★★hairQuestionYouからインポートするので追加
from db_control.mymodels_MySQL import HairQuestionYou


# DB接続用（FastAPI依存関数）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE処理（新規登録）
def create_hair_quality(db: Session, hair_quality_data: dict):
    db_hair_quality = HairQuality(**hair_quality_data)
    db.add(db_hair_quality)
    db.commit()
    db.refresh(db_hair_quality)
    return db_hair_quality

# CREATE処理（新規登録）　ここいらないかな
# ★★★hairQuestionYouのデータベース
def create_hair_questionyou(db: Session, hair_questionyou_data: dict):
    db_hair_questionyou = HairQuestionYou(**hair_questionyou_data)
    db.add(db_hair_questionyou)
    db.commit()
    db.refresh(db_hair_questionyou)
    return db_hair_questionyou

# READ処理（全件取得）
def get_all_hair_quality(db: Session):
    return db.query(HairQuality).all()

# READ処理（全件取得）
# ★★★hairQuestionYouのデータベース
def get_all_hair_questionyou(db: Session):
    return db.query(HairQuestionYou).all()

# READ処理（特定IDのデータ取得）
def get_hair_quality_by_id(db: Session, hair_quality_id: int):
    return db.query(HairQuality).filter(HairQuality.id == hair_quality_id).first()

# READ処理（特定IDのデータ取得）
# ★★★hairQuestionYouのデータベース
def get_hair_questionyou_by_id(db: Session, hair_questionyou_id: int):
    return db.query(HairQuestionYou).filter(HairQuestionYou.id == hair_questionyou_id).first()

# READ処理（hair_quality_idから問診データ取得）
# hairQualityと紐づいたhairQuestionYouを取得
def get_questionyou_by_hair_quality_id(db: Session, hair_quality_id: int):
    return db.query(HairQuestionYou).filter(HairQuestionYou.hair_quality_id == hair_quality_id).first()

# UPDATE処理（特定IDのデータ更新）
def update_hair_quality(db: Session, hair_quality_id: int, update_data: dict):
    db_hair_quality = db.query(HairQuality).filter(HairQuality.id == hair_quality_id).first()
    if db_hair_quality:
        for key, value in update_data.items():
            setattr(db_hair_quality, key, value)
        db.commit()
        db.refresh(db_hair_quality)
    return db_hair_quality


# UPDATE処理（特定IDのデータ更新）
# ★★★hairQuestionYouのデータベース
def update_hair_questionyou(db: Session, hair_questionyou_id: int, update_data: dict):
    db_hair_questionyou = db.query(HairQuestionYou).filter(HairQuestionYou.id == hair_questionyou_id).first()
    if db_hair_questionyou:
        for key, value in update_data.items():
            setattr(db_hair_questionyou, key, value)
        db.commit()
        db.refresh(db_hair_questionyou)
    return db_hair_questionyou

# DELETE処理（特定IDのデータ削除）
def delete_hair_quality(db: Session, hair_quality_id: int):
    db_hair_quality = db.query(HairQuality).filter(HairQuality.id == hair_quality_id).first()
    if db_hair_quality:
        db.delete(db_hair_quality)
        db.commit()
    return db_hair_quality


# DELETE処理（特定IDのデータ削除）
# ★★★hairQuestionYouのデータベース
def delete_hair_questionyou(db: Session, hair_questionyou_id: int):
    db_hair_questionyou = db.query(HairQuestionYou).filter(HairQuestionYou.id == hair_questionyou_id).first()
    if db_hair_questionyou:
        db.delete(db_hair_questionyou)
        db.commit()
    return db_hair_questionyou