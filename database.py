import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. 定义源数据库和目标（云端可写）数据库路径
LOCAL_DB_PATH = "./campuslife_data.db"
TMP_DB_PATH = "/tmp/campuslife_data.db"

# 2. 动态判断当前环境的写权限
# os.W_OK 用于检查当前目录是否可写。如果不具备写权限，说明部署在 Vercel/EdgeOne 等 Serverless 云端
if not os.access(".", os.W_OK):
    # 将带有预设数据的数据库完整复制到云端唯一可写的 /tmp 目录
    if not os.path.exists(TMP_DB_PATH) and os.path.exists(LOCAL_DB_PATH):
        shutil.copy2(LOCAL_DB_PATH, TMP_DB_PATH)
    # 数据库连接指向 /tmp 中的副本
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{TMP_DB_PATH}"
else:
    # 如果在本地开发环境（Windows/Mac），直接使用根目录的数据库
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{LOCAL_DB_PATH}"

# 预留环境变量覆盖接口（未来若接入 PostgreSQL 也能直接兼容）
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", SQLALCHEMY_DATABASE_URL)

# SQLite 专属参数
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()