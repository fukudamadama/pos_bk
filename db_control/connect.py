# db_control/connect.py

import os
from pathlib import Path
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base   # ← ここで declarative_base を追加でインポート

# ─── 1) 環境変数の読み込み ───
base_path = Path(__file__).parents[1]
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

# ─── 2) データベース接続情報 取得 ───
DB_USER     = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST     = os.getenv('DB_HOST')
DB_PORT     = os.getenv('DB_PORT', '3306')    # デフォルト 3306
DB_NAME     = os.getenv('DB_NAME')

# ─── 3) SSL 証明書パス (必要なら) ───
ssl_cert = str(base_path / 'DigiCertGlobalRootCA.crt.pem')

# ─── 4) SQLAlchemy エンジン作成 ───
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {"ssl_ca": ssl_cert}
    },
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)

# ─── 5) SessionLocal 定義 ───
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ─── 6) Base を定義 ───
Base = declarative_base()
