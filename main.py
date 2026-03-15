from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from typing import List
from datetime import datetime, timedelta

import models
import database
import schemas 

app = FastAPI(title="Edu.Space API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 获取所有学生列表
@app.get("/api/users", response_model=List[schemas.UserBase])
def get_users(db: Session = Depends(database.get_db)):
    return db.query(models.User).all()

# 搜索学生
@app.get("/api/users/search", response_model=List[schemas.UserBase])
def search_users(q: str, db: Session = Depends(database.get_db)):
    return db.query(models.User).filter(
        (models.User.name.contains(q)) | (models.User.real_id.contains(q))
    ).all()

# 获取特定学生资料
@app.get("/api/users/{user_id}", response_model=schemas.UserBase)
def get_user(user_id: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.student_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 获取首页新闻
@app.get("/api/news", response_model=List[schemas.News])
def get_news(db: Session = Depends(database.get_db)):
    return db.query(models.News).all()

# 获取档案详情
@app.get("/api/archives/{user_id}")
def get_archives(user_id: str, category: str = "all", db: Session = Depends(database.get_db)):
    query = db.query(models.Archive).filter(models.Archive.student_id == user_id)
    if category != "all":
        query = query.filter(models.Archive.category == category)
    
    records = query.all()
    result = {"academic": [], "health": [], "awards": [], "library": [], "venue": []}
    
    for r in records:
        content = r.content
        if not isinstance(content, list):
            content = [content]

        if r.category in result:
            result[r.category].extend(content)
        
    return result

# --- POST 写入接口 ---

# 1. 注册新用户
@app.post("/api/users/register", response_model=schemas.UserBase)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.student_id == user.student_id).first():
        raise HTTPException(status_code=400, detail="User already exists")
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 2. 借阅图书
@app.post("/api/library/borrow")
def borrow_book(req: schemas.BorrowRequest, db: Session = Depends(database.get_db)):
    # 查找该用户的图书档案
    archive = db.query(models.Archive).filter(
        models.Archive.student_id == req.student_id, 
        models.Archive.category == 'library'
    ).first()
    
    new_book = {
        "title": req.title,
        "author": req.author,
        "borrow_date": datetime.now().strftime("%Y.%m.%d"),
        "due_date": (datetime.now() + timedelta(days=30)).strftime("%Y.%m.%d"),
        "status": "借阅中",
        "days_left": 30,
        "cover": req.cover
    }
    
    if archive:
        # 如果已有档案，向列表顶部插入新书
        new_content = list(archive.content) if isinstance(archive.content, list) else [archive.content]
        new_content.insert(0, new_book)
        archive.content = new_content
        # 必须标记修改，否则 SQLAlchemy 无法监测到 JSON 内部变化
        flag_modified(archive, "content")
    else:
        # 如果没有档案，新建一条记录
        archive = models.Archive(student_id=req.student_id, category='library', content=[new_book])
        db.add(archive)
        
    db.commit()
    return {"message": "借阅成功", "book": new_book}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)