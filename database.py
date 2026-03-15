import os
import shutil
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

TMP_DB_PATH = "/tmp/campuslife_data.db"
LOCAL_DB_PATH = "./campuslife_data.db"

# 1. 寻找真实数据源 (EdgeOne 的工作路径可能与本地环境不同)
source_db = LOCAL_DB_PATH
if not os.path.exists(source_db):
    alt_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "campuslife_data.db")
    if os.path.exists(alt_db):
        source_db = alt_db

# 2. 真实写入测试：判断当前是否是 Serverless 只读环境
is_writable = False
try:
    with open("./.write_test", "w") as f:
        f.write("test")
    os.remove("./.write_test")
    is_writable = True
except Exception:
    pass

# 默认让连接指向真实的源文件（保证不管怎样，GET 接口/看新闻绝对不会挂）
db_url_path = source_db 

# 3. 如果环境不可写，尝试将数据库转移到云端唯一的读写区 /tmp
if not is_writable and os.path.exists(source_db):
    # 【关键修复】清理上个版本由于异常导致的 0 字节废弃空数据库
    if os.path.exists(TMP_DB_PATH) and os.path.getsize(TMP_DB_PATH) < 1024:
        try:
            os.remove(TMP_DB_PATH)
        except:
            pass
            
    # 将包含数据的真实数据库拷贝到 /tmp
    if not os.path.exists(TMP_DB_PATH):
        try:
            shutil.copy2(source_db, TMP_DB_PATH)
        except Exception:
            pass # 如果复制失败，安全退回到只读模式，不阻断程序
            
    # 再次验证：只有 /tmp 中的数据库真实存在且体积正常，才切换路径开启写入功能！
    if os.path.exists(TMP_DB_PATH) and os.path.getsize(TMP_DB_PATH) > 1024:
        db_url_path = TMP_DB_PATH

# 4. 初始化引擎
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_url_path}"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", SQLALCHEMY_DATABASE_URL)

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()