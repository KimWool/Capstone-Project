# run.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",     # FastAPI 앱 import 경로
        host="0.0.0.0",
        port=10010,
        reload=True,        # 코드 수정 시 자동 재시작
        reload_dirs=["app"] # 변경 감지할 디렉토리
    )
