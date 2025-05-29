# backend/app/api/endpoints/auth.py
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os
import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

from app.db.session import get_db
from app.models.user import User
from app.services.auth import create_access_token, get_password_hash, verify_password



class SignupEmailRequest(BaseModel):
    email: str
    password: str
    username: Optional[str] = None

class LoginEmailRequest(BaseModel):
    email: str
    password: str


load_dotenv()

router = APIRouter()

# 이메일 회원가입 엔드포인트
@router.post("/signup/email")
async def signup_email(
    body: SignupEmailRequest,
    db: AsyncSession = Depends(get_db)
):
    email = body.email
    password = body.password
    username = body.username

    # 중복 이메일 확인
    result = await db.execute(
        select(User).where(User.email == email, User.provider == "email")
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 비밀번호 해시 및 사용자 생성
    hashed_pw = get_password_hash(password)
    new_user = User(
        user_id=str(uuid.uuid4()),  # ✅ UUID 문자열로 직접 생성
        email=email,
        username=username,
        hashed_password=hashed_pw,
        provider="email"
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # JWT 토큰 발급
    token = create_access_token({"sub": str(new_user.user_id)})
    return {
    "success": True,
    "access_token": token,
    "user": {
        "user_id": str(new_user.user_id),
        "email": new_user.email,
        "username": new_user.username
    }
}




# 이메일 로그인 엔드포인트
@router.post("/login/email")
async def login_email(
    body: LoginEmailRequest,
    db: AsyncSession = Depends(get_db)
):
    email = body.email
    password = body.password

    result = await db.execute(
        select(User).where(User.email == email, User.provider == "email")
    )
    user = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.user_id)})

    # ✅ Flutter가 기대하는 구조로 반환
    return {
        "success": True,
        "access_token": token,
        "user": {
            "user_id": str(user.user_id),
            "email": user.email,
            "username": user.username
        }
    }


