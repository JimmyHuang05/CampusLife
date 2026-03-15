from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)
    real_id = Column(String)
    name = Column(String)
    avatar = Column(String)
    class_name = Column(String)
    position = Column(String)
    gender = Column(String)
    ethnicity = Column(String)
    politics = Column(String)
    enrollment = Column(String)

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String)
    title = Column(String)
    desc = Column(Text)
    date = Column(String)
    circle_color_1 = Column(String)
    circle_color_2 = Column(String)

class Archive(Base):
    __tablename__ = "archives"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, index=True)
    category = Column(String)
    content = Column(JSON)