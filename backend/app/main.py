# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import auth, property, users, building, registry, vector, analyze,  chatbot, transaction_price, address
from app.db.session import engine, Base  # init_db 대신 engine, Base를 가져옵니다

app = FastAPI()

# CORS 설정 예시
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# startup 이벤트에서 테이블 생성
@app.on_event("startup")
async def on_startup():
    # 비동기 엔진으로 Base.metadata를 이용해 테이블을 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 라우터 등록
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(property.router, prefix="/property", tags=["property"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(building.router)
app.include_router(registry.router)
app.include_router(vector.router)
app.include_router(analyze.router, prefix="/analyze", tags=["Analyze"])
#clude_router(prediction.router, prefix="/prediction", tags=["prediction"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
app.include_router(transaction_price.router)
app.include_router(address.router)