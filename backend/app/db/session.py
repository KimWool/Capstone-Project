# backend/app/db/session.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# ✅ .env에 DATABASE_URL 없을 시 기본값 사용
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://capstone_user:1234@localhost:5432/capstone")
engine = create_async_engine(DATABASE_URL, echo=True)

# ✅ 먼저 정의
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# ✅ 필요한 경우 임시로도 사용 가능
SessionLocal = AsyncSessionLocal  

Base = declarative_base()

print(f"💥 현재 사용 중인 DATABASE_URL: {DATABASE_URL}")

# ✅ async generator for FastAPI Depends
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
