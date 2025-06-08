# app.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn

# 📌 ここを絶対インポートにする
#  db_control パッケージの中に models.py, schemas.py, crud.py がある
from db_control import crud, models, schemas

# 📌 connect.py の中に SessionLocal, engine, Base を定義しているので、これも絶対インポート
from db_control.connect import SessionLocal, engine, Base

# （もし database.py に Base があればそちらからインポートしても OK です）
# from database import SessionLocal, engine, Base

# ここで「テーブルがなければ作成する」を呼び出す
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mobile POS API", version="1.0")


# DB セッションを取得する Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products/{code}", response_model=schemas.ProductRead)
def read_product_by_code(code: str, db: Session = Depends(get_db)):
    product = crud.get_product_by_code(db, code)
    if not product:
        raise HTTPException(status_code=404, detail=f"商品コード {code} は存在しません")
    return product


@app.post("/transactions/", response_model=schemas.SalesTransactionRead)
def create_transaction(
    transaction_in: schemas.SalesTransactionCreate,
    db: Session = Depends(get_db)
):
    try:
        trd = crud.create_sales_transaction(db, transaction_in)
        return trd
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/transactions/{trd_id}/details/", response_model=schemas.TransactionDetailRead)
def create_detail(
    trd_id: int,
    detail_in: schemas.TransactionDetailCreate,
    db: Session = Depends(get_db)
):
    if detail_in.trd_id != trd_id:
        raise HTTPException(
            status_code=400,
            detail="URL の trd_id とリクエストボディの trd_id が一致しません"
        )
    try:
        new_detail = crud.create_transaction_detail(db, detail_in)
        return new_detail
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="明細作成中にエラーが発生しました")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
