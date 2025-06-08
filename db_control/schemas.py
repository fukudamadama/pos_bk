# db_control/schemas.py

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# ───────────────
# ProductMaster 用スキーマ
# ───────────────
class ProductBase(BaseModel):
    code: str = Field(..., min_length=13, max_length=13, description="商品コード(JAN、13桁)")
    name: str = Field(..., max_length=50, description="商品名")
    price: int = Field(..., ge=0, description="価格(円)")

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    prd_id: int

    class Config:
        # Pydantic v2 では orm_mode の代わりに from_attributes=True を指定する
        from_attributes = True


# ───────────────
# SalesTransaction 用スキーマ
# ───────────────
class SalesTransactionBase(BaseModel):
    emp_cd: str = Field(..., max_length=10, description="社員コード")
    store_cd: str = Field(..., max_length=5, description="店舗コード")
    pos_no: str = Field(..., max_length=3, description="POS機番")
    total_amt: int = Field(..., ge=0, description="税込合計金額")
    ttl_amt_ex_tax: int = Field(..., ge=0, description="税抜合計金額")

class SalesTransactionCreate(SalesTransactionBase):
    pass

class SalesTransactionRead(SalesTransactionBase):
    trd_id: int
    transaction_dt: datetime

    class Config:
        from_attributes = True


# ───────────────
# TransactionDetail 用スキーマ
# ───────────────
class TransactionDetailBase(BaseModel):
    prd_id: int = Field(..., description="商品マスタID")
    prd_code: str = Field(..., min_length=13, max_length=13, description="商品コード(JAN)")
    prd_name: str = Field(..., max_length=50, description="商品名")
    prd_price: int = Field(..., ge=0, description="販売単価(円)")
    tax_cd: str = Field(..., max_length=2, description="税区分コード")

class TransactionDetailCreate(TransactionDetailBase):
    trd_id: int  # どの取引ヘッダに紐づけるか

class TransactionDetailRead(TransactionDetailBase):
    dtl_id: int
    trd_id: int

    class Config:
        from_attributes = True
