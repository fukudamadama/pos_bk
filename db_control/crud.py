# db_control/crud.py

# ──────── 先頭で「相対インポート」を使って models と schemas を読み込む ────────
from . import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

# ※もし SessionLocal や Base も必要なら、connect から相対インポート↓
# from .connect import SessionLocal  

# ─────────────────────────────────────────────────────────────────────────────
# ① JANコードをキーにした商品マスタ検索
# ─────────────────────────────────────────────────────────────────────────────
def get_product_by_code(db: Session, code: str) -> schemas.ProductRead:
    """
    ProductMaster テーブルから JAN コード (code) に一致するレコードを取得する。
    見つからなければ None を返す。
    """
    product = db.query(models.ProductMaster).filter(models.ProductMaster.code == code).first()
    if not product:
        return None
    # Pydantic の schemas.ProductRead に変換して返す
    return schemas.ProductRead.from_orm(product)


# ─────────────────────────────────────────────────────────────────────────────
# ② 取引レコードの作成 (sales_transaction)
# ─────────────────────────────────────────────────────────────────────────────
def create_sales_transaction(
    db: Session,
    transaction_in: schemas.SalesTransactionCreate
) -> schemas.SalesTransactionRead:
    """
    SalesTransaction テーブルに新しい取引ヘッダを挿入する。
    """
    db_trd = models.SalesTransaction(
        emp_cd=transaction_in.emp_cd,
        store_cd=transaction_in.store_cd,
        pos_no=transaction_in.pos_no,
        total_amt=transaction_in.total_amt,
        ttl_amt_ex_tax=transaction_in.ttl_amt_ex_tax
        # transaction_dt はサーバー側で自動設定
    )
    db.add(db_trd)
    db.commit()
    db.refresh(db_trd)
    return schemas.SalesTransactionRead.from_orm(db_trd)


# ─────────────────────────────────────────────────────────────────────────────
# ③ 明細レコードの作成 (transaction_detail)
# ─────────────────────────────────────────────────────────────────────────────
def create_transaction_detail(
    db: Session,
    detail_in: schemas.TransactionDetailCreate
) -> schemas.TransactionDetailRead:
    """
    TransactionDetail テーブルに新しい取引明細を挿入する。
    - detail_in.trd_id: どの取引ヘッダ（SalesTransaction.trd_id）に紐づけるか
    - detail_in.prd_id: どの ProductMaster.prd_id と紐づけるか
    """
    # 1) 取引ヘッダ (SalesTransaction) が存在するかチェック
    try:
        db.query(models.SalesTransaction).filter(
            models.SalesTransaction.trd_id == detail_in.trd_id
        ).one()
    except NoResultFound:
        raise ValueError(f"取引 ID {detail_in.trd_id} は存在しません")

    # 2) 商品マスタ (ProductMaster) が存在するかチェック
    try:
        db.query(models.ProductMaster).filter(
            models.ProductMaster.prd_id == detail_in.prd_id
        ).one()
    except NoResultFound:
        raise ValueError(f"商品 ID {detail_in.prd_id} は存在しません")

    # 3) TransactionDetail レコードを作成してコミット
    db_detail = models.TransactionDetail(
        trd_id=detail_in.trd_id,
        prd_id=detail_in.prd_id,
        prd_code=detail_in.prd_code,
        prd_name=detail_in.prd_name,
        prd_price=detail_in.prd_price,
        tax_cd=detail_in.tax_cd
    )
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)

    return schemas.TransactionDetailRead.from_orm(db_detail)
