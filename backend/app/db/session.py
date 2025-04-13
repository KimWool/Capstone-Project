# backend/app/db/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 환경 변수 로드

# .env 파일에 정의된 DATABASE_URL 사용
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    # 모델에 정의된 모든 테이블을 생성
    from app.models import user, property  # 임포트해 모든 모델 모듈이 로드되게 함
    Base.metadata.create_all(bind=engine)
