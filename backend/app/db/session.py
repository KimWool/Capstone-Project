# backend/app/db/session.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # .env에서 DATABASE_URL 불러오기

# URL 예시: postgresql+asyncpg://user:pw@localhost:5432/dbname
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)

Base = declarative_base()

# <-- 이 부분만 교체: async def로 정의하고, 호출하지 마세요!
async def get_db():
    """
    FastAPI 의존성 주입 함수.
    비동기 세션을 yield 후 자동으로 닫습니다.
    """
    async with SessionLocal() as session:
        yield session
