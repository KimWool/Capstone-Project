# backend/app/api/endpoints/auth.py
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

load_dotenv()

router = APIRouter()

# 이메일 회원가입 엔드포인트
@router.post("/signup/email")
async def signup_email(
    body: SignupEmailRequest,  # ← JSON 바디가 이 모델로 파싱됩니다
    db: AsyncSession = Depends(get_db)
):
    
    email    = body.email
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
        email=email,
        username=username,
        hashed_password=hashed_pw,
        provider="email"
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # JWT 토큰 반환
    token = create_access_token({"sub": str(new_user.user_id)})
    return {"access_token": token, "user": new_user.email}

# 이메일 로그인 엔드포인트
@router.post("/login/email")
async def login_email(
    email: str,
    password: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(User.email == email, User.provider == "email")
    )
    user = result.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.user_id)})
    return {"access_token": token, "user": user.email}

# 카카오 로그인 URL 반환
@router.get("/login/kakao")
async def get_kakao_login_url():
    key = os.getenv("KAKAO_REST_API_KEY")
    uri = os.getenv("KAKAO_REDIRECT_URI")
    url = (
        f"https://kauth.kakao.com/oauth/authorize"
        f"?client_id={key}&redirect_uri={uri}&response_type=code"
    )
    return {"authorization_url": url}

# 카카오 로그인 콜백
@router.get("/login/kakao/callback")
async def kakao_callback(
    code: str,
    db: AsyncSession = Depends(get_db)
):
    key = os.getenv("KAKAO_REST_API_KEY")
    uri = os.getenv("KAKAO_REDIRECT_URI")
    token_url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": key,
        "redirect_uri": uri,
        "code": code,
    }
    token_resp = requests.post(
        token_url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    ).json()
    access_token = token_resp.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Kakao token error")

    user_info = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()
    kakao_id = user_info.get("id")
    acct = user_info.get("kakao_account", {})
    email = acct.get("email")

    result = await db.execute(
        select(User).where(User.provider == "kakao", User.provider_id == str(kakao_id))
    )
    user = result.scalars().first()
    if not user:
        user = User(
            email=email,
            provider="kakao",
            provider_id=str(kakao_id),
            username=acct.get("profile", {}).get("nickname", "")
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    token = create_access_token({"sub": str(user.user_id)})
    return {"access_token": token, "user": user.email}

# 네이버 로그인 URL 반환
@router.get("/login/naver")
async def get_naver_login_url():
    cid = os.getenv("NAVER_CLIENT_ID")
    uri = os.getenv("NAVER_REDIRECT_URI")
    state = "random_state"
    url = (
        f"https://nid.naver.com/oauth2.0/authorize"
        f"?response_type=code&client_id={cid}&redirect_uri={uri}&state={state}"
    )
    return {"authorization_url": url}

# 네이버 로그인 콜백
@router.get("/login/naver/callback")
async def naver_callback(
    code: str,
    state: str,
    db: AsyncSession = Depends(get_db)
):
    cid = os.getenv("NAVER_CLIENT_ID")
    secret = os.getenv("NAVER_CLIENT_SECRET")
    uri = os.getenv("NAVER_REDIRECT_URI")
    token_url = "https://nid.naver.com/oauth2.0/token"
    params = {
        "grant_type": "authorization_code",
        "client_id": cid,
        "client_secret": secret,
        "code": code,
        "state": state,
    }
    token_resp = requests.get(token_url, params=params).json()
    access_token = token_resp.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="Naver token error")

    profile_resp = requests.get(
        "https://openapi.naver.com/v1/nid/me",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()
    if profile_resp.get("resultcode") != "00":
        raise HTTPException(status_code=400, detail="Naver user info error")
    info = profile_resp.get("response", {})
    naver_id = info.get("id")
    email = info.get("email")

    result = await db.execute(
        select(User).where(User.provider == "naver", User.provider_id == str(naver_id))
    )
    user = result.scalars().first()
    if not user:
        user = User(
            email=email,
            provider="naver",
            provider_id=str(naver_id),
            username=info.get("name", "")
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    token = create_access_token({"sub": str(user.user_id)})
    return {"access_token": token, "user": user.email}
