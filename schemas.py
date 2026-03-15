from pydantic import BaseModel
from typing import List, Optional, Any

class UserBase(BaseModel):
    student_id: str
    real_id: str
    name: str
    avatar: str
    class_name: str
    position: str
    gender: str
    ethnicity: str
    politics: str
    enrollment: str

    class Config:
        from_attributes = True

class News(BaseModel):
    tag: str
    title: str
    desc: str
    date: str
    circle_color_1: str
    circle_color_2: str

    class Config:
        from_attributes = True

class Archive(BaseModel):
    student_id: str
    category: str
    content: Any

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    student_id: str
    name: str
    avatar: str = "https://api.dicebear.com/7.x/notionists/svg?seed=default"
    real_id: str = "1100000000000"
    class_name: str = "体验班级"
    position: str = "体验用户"
    gender: str = "未知"
    ethnicity: str = "未知"
    politics: str = "群众"
    enrollment: str = "2024年"

class BorrowRequest(BaseModel):
    student_id: str
    title: str
    author: str
    cover: str

class VenueReservation(BaseModel):
    student_id: str
    venue_name: str
    date: str
    time_slot: str