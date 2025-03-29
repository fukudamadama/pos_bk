from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
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

# from fastapi import FastAPI, HTTPException, Query
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import requests
# import json
# # from db_control import crud, mymodels
# from db_control import crud, mymodels
# # MySQLのテーブル作成
# # from db_control.create_tables import init_db

# # # アプリケーション初期化時にテーブルを作成
# # init_db()


# class Customer(BaseModel):
#     customer_id: str
#     customer_name: str
#     age: int
#     gender: str


# app = FastAPI()

# # CORSミドルウェアの設定
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def index():
#     return {"message": "FastAPI top page!"}


# @app.post("/customers")
# def create_customer(customer: Customer):
#     values = customer.dict()
#     tmp = crud.myinsert(mymodels.Customers, values)
#     result = crud.myselect(mymodels.Customers, values.get("customer_id"))

#     if result:
#         result_obj = json.loads(result)
#         return result_obj if result_obj else None
#     return None


# @app.get("/customers")
# def read_one_customer(customer_id: str = Query(...)):
#     result = crud.myselect(mymodels.Customers, customer_id)
#     if not result:
#         raise HTTPException(status_code=404, detail="Customer not found")
#     result_obj = json.loads(result)
#     return result_obj[0] if result_obj else None

# @app.get("/allcustomers")
# def read_all_customer():
#     result = crud.myselectAll(mymodels.Customers)
#     # 結果がNoneの場合は空配列を返す
#     if not result:
#         return []
#     # JSON文字列をPythonオブジェクトに変換
#     return json.loads(result)


# @app.put("/customers")
# def update_customer(customer: Customer):
#     values = customer.dict()
#     values_original = values.copy()
#     tmp = crud.myupdate(mymodels.Customers, values)
#     result = crud.myselect(mymodels.Customers, values_original.get("customer_id"))
#     if not result:
#         raise HTTPException(status_code=404, detail="Customer not found")
#     result_obj = json.loads(result)
#     return result_obj[0] if result_obj else None


# @app.delete("/customers")
# def delete_customer(customer_id: str = Query(...)):
#     result = crud.mydelete(mymodels.Customers, customer_id)
#     if not result:
#         raise HTTPException(status_code=404, detail="Customer not found")
#     return {"customer_id": customer_id, "status": "deleted"}


# @app.get("/fetchtest")
# def fetchtest():
#     response = requests.get('https://jsonplaceholder.typicode.com/users')
#     return response.json()
