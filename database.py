import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 核心适配：使用你提供的 Neon PostgreSQL 链接作为默认连接
DEFAULT_DB_URL = "postgresql://neondb_owner:npg_ZEGxm6Szt9Mk@ep-plain-cell-abittstm-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

# SQLite 需要特定的参数，而云端 PostgreSQL 不需要
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

# 针对 Serverless 环境开启 pool_pre_ping（防止数据库连接休眠断开报错）
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args=connect_args,
    pool_pre_ping=True if not SQLALCHEMY_DATABASE_URL.startswith("sqlite") else False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()