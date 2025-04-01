# uname() error回避
import platform
print("platform", platform.uname())

from sqlalchemy.orm import Session
from db_control.connect_MySQL import SessionLocal
from db_control.mymodels_MySQL import HairQuality

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

# READ処理（全件取得）
def get_all_hair_quality(db: Session):
    return db.query(HairQuality).all()

# READ処理（特定IDのデータ取得）
def get_hair_quality_by_id(db: Session, hair_quality_id: int):
    return db.query(HairQuality).filter(HairQuality.id == hair_quality_id).first()

# UPDATE処理（特定IDのデータ更新）
def update_hair_quality(db: Session, hair_quality_id: int, update_data: dict):
    db_hair_quality = db.query(HairQuality).filter(HairQuality.id == hair_quality_id).first()
    if db_hair_quality:
        for key, value in update_data.items():
            setattr(db_hair_quality, key, value)
        db.commit()
        db.refresh(db_hair_quality)
    return db_hair_quality

# DELETE処理（特定IDのデータ削除）
def delete_hair_quality(db: Session, hair_quality_id: int):
    db_hair_quality = db.query(HairQuality).filter(HairQuality.id == hair_quality_id).first()
    if db_hair_quality:
        db.delete(db_hair_quality)
        db.commit()
    return db_hair_quality


# # uname() error回避
# import platform
# print("platform", platform.uname())


# from sqlalchemy import create_engine, insert, delete, update, select
# import sqlalchemy
# from sqlalchemy.orm import sessionmaker
# import json
# import pandas as pd

# from db_control.connect_MySQL import engine
# from db_control.mymodels import Customers


# def myinsert(mymodel, values):
#     # session構築
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     query = insert(mymodel).values(values)
#     try:
#         # トランザクションを開始
#         with session.begin():
#             # データの挿入
#             result = session.execute(query)
#     except sqlalchemy.exc.IntegrityError:
#         print("一意制約違反により、挿入に失敗しました")
#         session.rollback()

#     # セッションを閉じる
#     session.close()
#     return "inserted"


# def myselect(mymodel, customer_id):
#     # session構築
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = session.query(mymodel).filter(mymodel.customer_id == customer_id)
#     try:
#         # トランザクションを開始
#         with session.begin():
#             result = query.all()
#         # 結果をオブジェクトから辞書に変換し、リストに追加
#         result_dict_list = []
#         for customer_info in result:
#             result_dict_list.append({
#                 "customer_id": customer_info.customer_id,
#                 "customer_name": customer_info.customer_name,
#                 "age": customer_info.age,
#                 "gender": customer_info.gender
#             })
#         # リストをJSONに変換
#         result_json = json.dumps(result_dict_list, ensure_ascii=False)
#     except sqlalchemy.exc.IntegrityError:
#         print("一意制約違反により、挿入に失敗しました")

#     # セッションを閉じる
#     session.close()
#     return result_json


# def myselectAll(mymodel):
#     # session構築
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = select(mymodel)
#     try:
#         # トランザクションを開始
#         with session.begin():
#             df = pd.read_sql_query(query, con=engine)
#             result_json = df.to_json(orient='records', force_ascii=False)

#     except sqlalchemy.exc.IntegrityError:
#         print("一意制約違反により、挿入に失敗しました")
#         result_json = None

#     # セッションを閉じる
#     session.close()
#     return result_json


# def myupdate(mymodel, values):
#     # session構築
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     customer_id = values.pop("customer_id")

#     query = "お見事！E0002の原因はこのクエリの実装ミスです。正しく実装しましょう"
#     try:
#         # トランザクションを開始
#         with session.begin():
#             result = session.execute(query)
#     except sqlalchemy.exc.IntegrityError:
#         print("一意制約違反により、挿入に失敗しました")
#         session.rollback()
#     # セッションを閉じる
#     session.close()
#     return "put"


# def mydelete(mymodel, customer_id):
#     # session構築
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = delete(mymodel).where(mymodel.customer_id == customer_id)
#     try:
#         # トランザクションを開始
#         with session.begin():
#             result = session.execute(query)
#     except sqlalchemy.exc.IntegrityError:
#         print("一意制約違反により、挿入に失敗しました")
#         session.rollback()

#     # セッションを閉じる
#     session.close()
#     return customer_id + " is deleted"