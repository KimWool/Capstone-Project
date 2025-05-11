# backend/app/clients/building_api.py
# ─────────────────────────────────────────
# CODEF 기반 건축물대장(표제부) 조회 API client

import httpx
from fastapi import HTTPException
from app.config import CODEF_API_HOST
from app.clients.codef_auth import get_second_codef_token

# CODEF 개발 서버 엔드포인트
CODEF_BUILDING_URL = f"{CODEF_API_HOST}/v1/kr/public/mw/building-register/general"

async def get_building_info(body: dict) -> dict:
    """
    CODEF 건축물대장 표제부 API 호출
    :param body: 요청에 필요한 전체 파라미터 (realEstateUniqueNumber 포함)
    :return: dict 응답 데이터
    """
    token = await get_second_codef_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("[요청 보냄] body:", body)
    print("[요청 보냄] headers:", headers)

    resp = None
    try:
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.post(CODEF_BUILDING_URL, headers=headers, json=body)
            if resp is not None:
                print("[응답 수신] status:", resp.status_code)
                print("[응답 수신] body:", resp.text)
            resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        detail = f"CODEF HTTP 오류: {e.response.status_code}, 내용: {e.response.text}"
        raise HTTPException(status_code=502, detail=detail)
    except Exception as e:
        detail = f"CODEF 요청 실패: {str(e)}"
        if resp is not None:
            detail += f"\n응답 내용: {resp.text}"
        raise HTTPException(status_code=502, detail=detail)

    try:
        data = resp.json()
    except Exception:
        raise HTTPException(status_code=502, detail=f"CODEF 응답 JSON 파싱 실패: {resp.text if resp else 'No response'}")

    if "data" not in data:
        raise HTTPException(status_code=502, detail=f"CODEF 응답 데이터 이상: {data}")

    return data["data"]