# backend/app/models/user.py

from sqlalchemy import Column, String, DateTime, func
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String(255), primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), nullable=True)
    hashed_password = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)  # ✅ 추가됨
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User id={self.user_id} email={self.email}>"
