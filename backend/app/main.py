# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, property, users
from app.db.session import init_db

app = FastAPI(
    title="Capstone Backend API",
    description="API for Capstone Project Backend with User & Property management and OAuth login",
    version="1.0.0"
)

# CORS 미들웨어 설정 (필요에 따라 origin 변경)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 예: ["http://localhost:3000", "http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 앱 시작 시 DB 테이블 생성 (ORM 모델 기반)
@app.on_event("startup")
def on_startup():
    init_db()

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(property.router, prefix="/api/property", tags=["Property"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Capstone Backend API"}
