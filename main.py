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

# --- 新增的 POST 写入接口 ---

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
    archive = db.query(models.Archive).filter(models.Archive.student_id == req.student_id, models.Archive.category == 'library').first()
    
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
        # SQLite JSON column needs reassignment to trigger update
        new_content = list(archive.content) if isinstance(archive.content, list) else [archive.content]
        new_content.insert(0, new_book)
        archive.content = new_content
        flag_modified(archive, "content")
    else:
        archive = models.Archive(student_id=req.student_id, category='library', content=[new_book])
        db.add(archive)
        
    db.commit()
    return {"message": "借阅成功", "book": new_book}

# 3. 预约场地 (预留功能)
@app.post("/api/venues/reserve")
def reserve_venue(req: schemas.VenueReservation, db: Session = Depends(database.get_db)):
    archive = db.query(models.Archive).filter(models.Archive.student_id == req.student_id, models.Archive.category == 'venue').first()
    new_res = {
        "venue_name": req.venue_name,
        "date": req.date,
        "time_slot": req.time_slot,
        "status": "预约成功"
    }
    
    if archive:
        new_content = list(archive.content) if isinstance(archive.content, list) else [archive.content]
        new_content.insert(0, new_res)
        archive.content = new_content
        flag_modified(archive, "content")
    else:
        archive = models.Archive(student_id=req.student_id, category='venue', content=[new_res])
        db.add(archive)
        
    db.commit()
    return {"message": "场地预约成功", "reservation": new_res}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)