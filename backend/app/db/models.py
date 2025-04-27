# app/db/models.py
from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone = Column(String)

