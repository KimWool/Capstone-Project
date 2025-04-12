from fastapi import FastAPI
from app.api.endpoints import property

def create_app() -> FastAPI:
    app = FastAPI()
    # 엔드포인트 라우터 등록
    app.include_router(property.router, prefix="/properties", tags=["Properties"])
    return app

app = create_app()

# 간단한 홈 라우터
@app.get("/")
def read_root():
    return {"message": "Welcome Home!"}
