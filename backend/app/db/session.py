# backend/app/db/session.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://capstone_user:1234@localhost:5432/capstone")
engine = create_async_engine(DATABASE_URL, echo=True)

# ✅ 이름 일치
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

Base = declarative_base()

print(f"💥 현재 사용 중인 DATABASE_URL: {DATABASE_URL}")

# ✅ async generator for dependency injection
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
