# app/clients/registry_api.py
import httpx
from app.config import CODEF_API_HOST
from app.clients.codef_auth import get_codef_token

# 데모전; 운영 시 CODEF_API_HOST로 교체
REG_URL = f"{CODEF_API_HOST}/v1/real-estate/register/jibun"

async def fetch_registry(jibun: str) -> dict:
    """
    등기부등본 조회
    :param jibun: "123-45" 와 같은 지번(본번-부번) 문자열
    """
    token = await get_codef_token()
    headers = {"Authorization": f"Bearer {token}"}
    params  = {"jibun": jibun}
    async with httpx.AsyncClient() as cli:
        r = await cli.get(REG_URL, headers=headers, params=params)
        r.raise_for_status()
        # 실제 response 구조: {"data": { … }}
        return r.json()["data"]
