# run.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",     # FastAPI 앱 import 경로
        host="127.0.0.1",
        port=8000,
        reload=True,        # 코드 수정 시 자동 재시작
        reload_dirs=["app"] # 변경 감지할 디렉토리
    )
