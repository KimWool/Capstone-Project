# app/clients/building_hub.py

import httpx
from fastapi import HTTPException
from app.config import SERVICE_KEY_BUILD, BASE_URL_BUILD

COMMON = {
    "serviceKey": SERVICE_KEY_BUILD,
    "_type":      "json",
    "pageNo":     1,
    "numOfRows":  10,
}

async def get_br_title_info(plat_gb_cd: str, bun: str, ji: str) -> list[dict]:
    params = {
        **COMMON,
        "platGbCd": plat_gb_cd,
        "bun":       bun,
        "ji":        ji,
    }
    url = f"{BASE_URL_BUILD}/getBrTitleInfo"
    async with httpx.AsyncClient() as cli:
        resp = await cli.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    # 디버그용: 실제 반환된 전체 JSON 구조를 확인하고 싶으면
    # print("DEBUG building API response:", data)

    # 올바른 키가 있는지 검사
    if "response" not in data or "body" not in data["response"]:
        raise HTTPException(
            status_code=502,
            detail=f"건축물대장 API 오류: 예상과 다른 응답 구조입니다. 전체 응답: {data}"
        )

    items = data["response"]["body"].get("items")
    # items가 없거나 빈 리스트면 404 처리
    if not items:
        raise HTTPException(status_code=404, detail="건축물대장 조회 결과가 없습니다.")
    return items
