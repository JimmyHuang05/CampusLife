import json
from database import SessionLocal, engine, Base
import models

print("正在初始化数据库表...")
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed_data():
    print("正在清理旧数据...")
    db.query(models.Archive).delete()
    db.query(models.News).delete()
    db.query(models.User).delete()

    print("正在导入学生资料...")

    students_raw = {
        'male': { 'name': 'MALE', 'id': '1100120210624', 'class': '高二 (6) 班', 'gender': '男', 'ethnicity': '汉族', 'position': '校学生会 主席', 'enrollment': '2021年9月', 'politics': '共青团员', 'avatar': 'https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBVSFpLx0DumrKPjuUA5dWWQhQIO_i5QACGAtrG2S7eUU0zdRez_Kk0wEAAwIAA3gAAzYE.png' },
        'female': { 'name': 'FEMALE', 'id': '1100120210608', 'class': '高二 (6) 班', 'gender': '女', 'ethnicity': '汉族', 'position': '公共服务部 部员', 'enrollment': '2021年9月', 'politics': '共青团员', 'avatar': 'https://im.gurl.eu.org/file/AgACAgEAAxkDAAEBVDBpJI184gfBdDEcTaQb3nlF7TJaKAACkwtrG49XKEW3y6h_dCzaCgEAAwIAA3gAAzYE.png' },
    }

    for s_id, info in students_raw.items():
        db.add(models.User(
            student_id=s_id, real_id=info['id'], name=info['name'], avatar=info['avatar'],
            class_name=info['class'], position=info['position'], gender=info['gender'],
            ethnicity=info['ethnicity'], politics=info['politics'], enrollment=info['enrollment']
        ))

    print("正在导入考试成绩...")

    exam_data = {
        'male': [
            { 'title': '全市第一次模拟考', 'date': '2023.01', 'tag': '一模', 'totalScore': 566, 'totalMax': 660, 'gradeRank': 7, 
              'subjects': [
                  { 'name': '语文', 'score': 119, 'avg': 106, 'change': '↑ 2', 'changeColor': 'text-accentRed' },
                  { 'name': '数学', 'score': 133, 'avg': 121, 'change': '↑ 2', 'changeColor': 'text-accentRed' },
                  { 'name': '英语', 'score': 128, 'avg': 115, 'change': '↑ 3', 'changeColor': 'text-accentRed' },
                  { 'name': '历史', 'score': 61, 'avg': 52, 'change': '↑ 1', 'changeColor': 'text-accentRed' },
                  { 'name': '地理', 'score': 67, 'avg': 58, 'change': '↑ 1', 'changeColor': 'text-accentRed' },
                  { 'name': '生物', 'score': 58, 'avg': 53, 'change': '↑ 9', 'changeColor': 'text-accentRed' }
              ] 
            },
            { 'title': '高二年级第二次质量监测', 'date': '2022.11', 'tag': '月考', 'totalScore': 512, 'totalMax': 660, 'gradeRank': 30,
              'subjects': [
                  { 'name': '语文', 'score': 115, 'avg': 98, 'change': '↓ 3', 'changeColor': 'text-accentGreen' },
                  { 'name': '数学', 'score': 120, 'avg': 113, 'change': '↑ 2', 'changeColor': 'text-accentRed' }
              ]
            }
        ],
        'female': [
            { 'title': '全市第一次模拟考', 'date': '2023.01', 'tag': '一模', 'totalScore': 581, 'totalMax': 660, 'gradeRank': 2,
              'subjects': [
                  { 'name': '语文', 'score': 128, 'avg': 106, 'change': '↑ 1', 'changeColor': 'text-accentRed' },
                  { 'name': '英语', 'score': 141, 'avg': 115, 'change': '↑ 1', 'changeColor': 'text-accentRed' }
              ]
            }
        ]
    }

    for s_id, content in exam_data.items():
        db.add(models.Archive(student_id=s_id, category='academic', content=content))

    print("正在导入体检数据...")

    health_data = {
        'male': [
            { 'title': '2022年秋季体检报告', 'date': '2022.11.10', 'result_summary': '体质良好，无明显异常。', 
              'details': [
                  { 'item': '身高 (cm)', 'value': '180.5', 'status': '正常', 'color': 'text-accentGreen' },
                  { 'item': '体重 (kg)', 'value': '62.2', 'status': '正常', 'color': 'text-accentGreen' },
                  { 'item': '双眼视力', 'value': '5.0 / 5.1', 'status': '正常', 'color': 'text-accentGreen' },
                  { 'item': '肺活量 (ml)', 'value': '4500', 'status': '正常', 'color': 'text-accentGreen' }
              ]
            }
        ],
        'female': [
            { 'title': '2022年秋季体检报告', 'date': '2022.11.10', 'result_summary': '体质轻盈。视力优秀。', 
              'details': [
                  { 'item': '身高 (cm)', 'value': '168.0', 'status': '正常', 'color': 'text-accentGreen' },
                  { 'item': '体重 (kg)', 'value': '48.9', 'status': '正常', 'color': 'text-accentGreen' },
                  { 'item': '双眼视力', 'value': '4.5 / 4.7', 'status': '近视', 'color': 'text-accentRed' }
              ]
            }
        ],
    }

    for s_id, content in health_data.items():
        db.add(models.Archive(student_id=s_id, category='health', content=content))

    print("正在导入新闻数据...")

    news_list = [
        models.News(tag="⭐ 头条新闻", title="我校科技创新小组在全国<br>青少年大赛中荣获金奖", desc="11月25日，我校“星火”科技创新小组荣获金奖。", date="2025-11-26", circle_color_1="bg-accentRed", circle_color_2="bg-accentYellow"),
        models.News(tag="🎨 校园文化", title="第十五届“光影之韵”<br>校园艺术节正式开幕", desc="本次艺术节涵盖了绘画、摄影、短视频及舞台剧等多种形式。", date="2025-12-01", circle_color_1="bg-accentGreen", circle_color_2="bg-accentBlue")
    ]
    db.add_all(news_list)

    print("正在导入图书馆数据...")
    
    db.add(models.Archive(student_id="male", category="library", content=[
        { "title": "三体：死神永生", "author": "刘慈欣", "borrow_date": "2025.02.01", "due_date": "2025.03.01", "status": "借阅中", "days_left": 26, "cover": "https://img1.doubanio.com/view/subject/s/public/s26012670.jpg" },
        { "title": "Python编程：从入门到实践", "author": "Eric Matthes", "borrow_date": "2025.01.15", "due_date": "2025.02.15", "status": "即将到期", "days_left": 3, "cover": "https://img2.doubanio.com/view/subject/s/public/s34848323.jpg" }
    ]))

    db.add(models.Archive(student_id="female", category="library", content=[
        { "title": "杀死一只知更鸟", "author": "哈珀·李", "borrow_date": "2025.01.20", "due_date": "2025.02.20", "status": "借阅中", "days_left": 14, "cover": "https://img3.doubanio.com/view/subject/s/public/s29662862.jpg" },
        { "title": "百年孤独", "author": "加西亚·马尔克斯", "borrow_date": "2024.12.01", "due_date": "2025.01.01", "status": "已逾期", "days_left": -35, "cover": "https://img1.doubanio.com/view/subject/s/public/s6384944.jpg" }
    ]))

    db.commit()
    print("数据更新完成！")

if __name__ == "__main__":
    seed_data()
    db.close()