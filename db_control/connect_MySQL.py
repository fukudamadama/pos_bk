from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

# 環境変数の読み込み
base_path = Path(__file__).parents[1]
env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

# 接続情報の取得
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME')

# SSL証明書
ssl_cert = str(base_path / 'DigiCertGlobalRootCA.crt.pem')

# DB URL構築
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# エンジンの作成
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {"ssl_ca": ssl_cert}
    },
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)

# セッションとベース
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# from sqlalchemy import create_engine
# import os
# from pathlib import Path
# from dotenv import load_dotenv

# # 環境変数の読み込み
# base_path = Path(__file__).parents[1]  # backendディレクトリへのパス
# # env_path = base_path / '.env'
# # load_dotenv(dotenv_path=env_path)

# # データベース接続情報
# DB_USER = os.getenv('DB_USER')
# DB_PASSWORD = os.getenv('DB_PASSWORD')
# DB_HOST = os.getenv('DB_HOST')
# DB_PORT = os.getenv('DB_PORT')
# DB_NAME = os.getenv('DB_NAME')

# # SSL証明書のパス
# ssl_cert = str(base_path / 'DigiCertGlobalRootCA.crt.pem')

# # MySQLのURL構築
# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# # エンジンの作成（SSL設定を追加）
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={
#         "ssl": {
#             "ssl_ca": ssl_cert
#         }
#     },
#     echo=True,
#     pool_pre_ping=True,
#     pool_recycle=3600
# )

# from sqlalchemy import create_engine

# import os
# from dotenv import load_dotenv

# # 環境変数の読み込み
# load_dotenv()

# # データベース接続情報
# DB_USER = os.getenv('DB_USER')
# DB_PASSWORD = os.getenv('DB_PASSWORD')
# DB_HOST = os.getenv('DB_HOST')
# DB_PORT = os.getenv('DB_PORT')
# DB_NAME = os.getenv('DB_NAME')

# # MySQLのURL構築
# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# # エンジンの作成
# engine = create_engine(
#     DATABASE_URL,
#     echo=True,
#     pool_pre_ping=True,
#     pool_recycle=3600
# )
