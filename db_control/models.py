# db_control/models.py

# ── 先頭で相対インポートに修正 ──
from .connect import Base

from sqlalchemy import Column, Integer, String, CHAR, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

class ProductMaster(Base):
    __tablename__ = "product_master"

    prd_id = Column(Integer, primary_key=True, index=True)
    code   = Column(CHAR(13), unique=True, nullable=False, comment="商品コード(JAN)")
    name   = Column(String(50), nullable=False, comment="商品名")
    price  = Column(Integer, nullable=False, comment="価格(円)")

    # 明細とのリレーション
    transaction_details = relationship(
        "TransactionDetail",
        back_populates="product",
        cascade="all, delete-orphan"
    )

class SalesTransaction(Base):
    __tablename__ = "sales_transaction"

    trd_id         = Column(Integer, primary_key=True, index=True)
    transaction_dt = Column(
        TIMESTAMP,
        nullable=False,
        server_default="CURRENT_TIMESTAMP",
        comment="取引日時"
    )
    emp_cd         = Column(CHAR(10), nullable=False, comment="社員コード")
    store_cd       = Column(CHAR(5),  nullable=False, comment="店舗コード")
    pos_no         = Column(CHAR(3),  nullable=False, comment="POS機番")
    total_amt      = Column(Integer, nullable=False, comment="税込合計金額")
    ttl_amt_ex_tax = Column(Integer, nullable=False, comment="税抜合計金額")

    # 明細とのリレーション
    details = relationship(
        "TransactionDetail",
        back_populates="transaction",
        cascade="all, delete-orphan"
    )

class TransactionDetail(Base):
    __tablename__ = "transaction_detail"

    dtl_id    = Column(Integer, primary_key=True, index=True)
    trd_id    = Column(Integer, ForeignKey("sales_transaction.trd_id"), nullable=False)
    prd_id    = Column(Integer, ForeignKey("product_master.prd_id"), nullable=False)
    prd_code  = Column(CHAR(13), nullable=False, comment="商品コード(JAN)")
    prd_name  = Column(String(50), nullable=False, comment="商品名")
    prd_price = Column(Integer, nullable=False, comment="販売単価(円)")
    tax_cd    = Column(CHAR(2), nullable=False, comment="税区分コード")

    # リレーション：ヘッダと商品マスターに結ぶ
    transaction = relationship("SalesTransaction", back_populates="details")
    product     = relationship("ProductMaster",    back_populates="transaction_details")
