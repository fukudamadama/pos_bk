from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn

from db_control import crud, models, schemas
from db_control.connect import SessionLocal, engine, Base

# ─── データベーステーブルをすべて作成（開発時のみ） ───
#    本番環境では Alembic 等でマイグレーションを行うことを推奨します。
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mobile POS Backend", version="1.0")

# ─── CORS 設定 ───
origins = [
    "http://localhost:3000",       # Next.js がローカルで動く場合
    "https://localhost:3000",       # Next.js がローカルで動く場合その２
    "https://app-step4-73.azurewebsites.net",  # 実際にホストした Next.js のURL
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── DB セッションを取得する依存関数 ───
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─── 1. 商品マスタ検索エンドポイント ───
@app.get("/products/{code}", response_model=schemas.ProductRead)
def read_product_by_code(code: str, db: Session = Depends(get_db)):
    # 前後の空白・タブを取り除いて厳密に検索
    code = code.strip()
    product = crud.get_product_by_code(db, code)
    if not product:
        raise HTTPException(status_code=404, detail=f"商品コード {code} は存在しません")
    return product


# ─── 2. 取引ヘッダ作成エンドポイント ───
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


# ─── 3. 明細作成エンドポイント ───
@app.post("/transactions/{trd_id}/details/", response_model=schemas.TransactionDetailRead)
def create_detail(
    trd_id: int,
    detail_in: schemas.TransactionDetailCreate,
    db: Session = Depends(get_db)
):
    # URL の trd_id とボディの trd_id が一致するかチェック
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


# ─── uvicorn で起動する場合 ───
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
