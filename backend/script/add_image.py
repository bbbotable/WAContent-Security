import os
from flask_sqlalchemy import SQLAlchemy
import face_recognition

from sqlalchemy import Column, Integer, String, PickleType, LargeBinary, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库路径
db_path = 'sqlite:///backend/dataset/face.db'

# 初始化
Base = declarative_base()
engine = create_engine(db_path)
Session = sessionmaker(bind=engine)
session = Session()

# 模型定义
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    student_id = Column(String(20), unique=True)
    face_encoding = Column(PickleType)
    photo = Column(LargeBinary)  # 新增字段：用于存储图片内容
    mime_type = Column(String(50))  # 新增字段：存储 MIME 类型

# 创建表（如果没创建过）
Base.metadata.create_all(engine)

# ======== 你手动设定的用户数据 ========
name = "魏致博"
student_id = "2022302181282"
image_path = "backend/static/photo/2022302181282.jpg"  # 确保存在这张照片

# 加载图片并提取编码
if not os.path.exists(image_path):
    print(f"图片不存在：{image_path}")
    exit()

with open(image_path, 'rb') as f:
    photo_data = f.read()

image = face_recognition.load_image_file(image_path)
encodings = face_recognition.face_encodings(image)

if not encodings:
    print("未检测到人脸")
    exit()

encoding = encodings[0]

import mimetypes

# 获取 mime_type
mime_type, _ = mimetypes.guess_type(image_path)
if not mime_type:
    mime_type = "application/octet-stream"  # fallback 类型

# 插入数据库
new_user = User(
    name=name,
    student_id=student_id,
    face_encoding=encoding,
    photo=photo_data,
    mime_type=mime_type
)
session.add(new_user)
session.commit()

print(f"✅ 成功添加用户：{name}（{student_id},{mime_type}）")
