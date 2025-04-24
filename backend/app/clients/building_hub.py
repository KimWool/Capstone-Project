# backend/app/clients/building_hub.py
# ─────────────────────────────────────────
# 건축물대장 공공 API client 모듈

import httpx
from fastapi import HTTPException
from app.config import SERVICE_KEY_BUILD, BASE_URL_BUILD

# 공통 파라미터
COMMON_PARAMS = {
    "serviceKey": SERVICE_KEY_BUILD,
    "_type":      "json",
    "pageNo":     1,
    "numOfRows":  10,
}

async def get_title_info(plat_gb_cd: str, bun: str, ji: str) -> list[dict]:
    """
    건축물대장 표제부 조회 (getBrTitleInfo)
    :param plat_gb_cd: 지번/관리구분코드("0"=지번)
    :param bun:        지번 본번
    :param ji:         지번 부번
    :return: List of item dicts
    """
    params = {
        **COMMON_PARAMS,
        "platGbCd": plat_gb_cd,
        "bun":       bun,
        "ji":        ji,
    }
    url = f"{BASE_URL_BUILD}/getBrTitleInfo"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    # 응답 구조 검증
    if "response" not in data or "body" not in data["response"]:
        raise HTTPException(
            status_code=502,
            detail=f"건축물대장 API 응답 오류: {data}"
        )

    items = data["response"]["body"].get("items")
    if not items:
        raise HTTPException(
            status_code=404,
            detail="건축물대장 조회 결과가 없습니다."
        )
    return items
