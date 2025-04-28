# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String(255), primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), nullable=True)
    provider = Column(String(50), default="email")  # 예: email, kakao, naver
    provider_id = Column(String(255), nullable=True)  # 소셜 로그인 시 사용
    hashed_password = Column(String(255), nullable=True)  # 이메일 로그인용
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User id={self.user_id} email={self.email}>"
