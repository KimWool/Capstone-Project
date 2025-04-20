# app/api/endpoints/building.py
from fastapi import APIRouter, Query, HTTPException
from typing import List
from app.clients.building_hub import get_title_info
from app.schemas.building import TitleInfoItem

router = APIRouter(prefix="/building", tags=["건축물대장"])

@router.get(
    "/title-info",
    response_model=List[TitleInfoItem],
    summary="건축물대장 표제부 조회 (getBrTitleInfo)"
)
async def title_info(
    plat_gb_cd: str = Query(..., description="지번/관리구분코드"),
    bun:        str = Query(..., description="지번 본번"),
    ji:         str = Query(..., description="지번 부번")
):
    items = await get_title_info(plat_gb_cd, bun, ji)
    if not items:
        raise HTTPException(status_code=404, detail="데이터 없음")
    return items
