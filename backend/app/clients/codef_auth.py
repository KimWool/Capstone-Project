# app/clients/codef_auth.py
# codef 토큰 발급 모듈
import httpx
from app.config import CODEF_CLIENT_ID, CODEF_CLIENT_SECRET, CODEF_API_HOST_DEV

AUTH_URL = f"{CODEF_API_HOST_DEV}/v2/auth/authenticate"

async def get_codef_token() -> str:
    """Codef 에서 Bearer 토큰을 발급받는다."""
    payload = {
        "client_id":     CODEF_CLIENT_ID,
        "client_secret": CODEF_CLIENT_SECRET,
    }
    async with httpx.AsyncClient() as cli:
        r = await cli.post(AUTH_URL, json=payload)
        r.raise_for_status()
        return r.json()["data"]["token"]
