# app/db/models.py

from sqlalchemy import Column, Integer, String
from app.db.base_class import Base  # 이미 정의되어 있다면 그대로 사용

# ✅ 기존 사용자 테이블
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone = Column(String)

# ✅ 키워드 설명 테이블
class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, unique=True, index=True)
    description = Column(String)
