from dotenv import load_dotenv
import os

load_dotenv()  # 프로젝트 루트 .env 읽음

BASE_URL_BUILD = "https://apis.data.go.kr/1613000/BldRgstHubService"
SERVICE_KEY_BUILD = os.getenv("BUILDING_SERVICE_KEY")

# Codef 등기부 API
CODEF_CLIENT_ID       = os.getenv("CODEF_CLIENT_ID")
CODEF_CLIENT_SECRET   = os.getenv("CODEF_CLIENT_SECRET")
CODEF_PUBLIC_KEY      = os.getenv("CODEF_PUBLIC_KEY")
CODEF_API_HOST_DEV    = os.getenv("CODEF_API_HOST_DEV")
CODEF_API_HOST        = os.getenv("CODEF_API_HOST")
