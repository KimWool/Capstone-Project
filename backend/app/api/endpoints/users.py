# backend/app/api/endpoints/users.py
import uuid 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, EmailStr
from app.db.session import SessionLocal
from app.models.user import User
from app.services.auth import get_password_hash
from pydantic import BaseModel
from fastapi import HTTPException, Depends
from app.services.auth import verify_password, get_password_hash


router = APIRouter()

# Pydantic 모델 (요청/응답 스키마)
class UserCreate(BaseModel):
    email: EmailStr
    username: str = None
    password: str


class UserUpdate(BaseModel):
    username: str = None
    password: str = None
    email: EmailStr = None
    phone: str = None  # 새로 추가


class UserOut(BaseModel):
    user_id: str  # ✅ int → str로 수정
    email: EmailStr
    username: str = None
    provider: str

    class Config:
        from_attributes = True

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  일반 사용자 생성 (예: 관리자용 API)
@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = get_password_hash(user.password)
    new_user = User(
        user_id=str(uuid.uuid4()),  # ✅ UUID 문자열로 직접 생성
        email=user.email,
        username=user.username,
        hashed_password=hashed_pw,
        provider="email"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Read all users
@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# Read single user by ID
@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user
@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.password is not None:
        user.hashed_password = get_password_hash(user_update.password)
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.phone is not None:
        user.phone = user_update.phone

    db.commit()
    db.refresh(user)
    return user

# Delete user
@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}


# 비밀번호 변경 (전용 API)
class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

@router.put("/change-password/{user_id}")
def change_password(
    user_id: str,
    payload: PasswordChangeRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = get_password_hash(payload.new_password)
    db.commit()

    return {"message": "비밀번호가 성공적으로 변경되었습니다."}

