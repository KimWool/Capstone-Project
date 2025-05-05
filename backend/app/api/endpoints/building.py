# app/api/endpoints/building.py

from fastapi import APIRouter, HTTPException
from app.clients.building_api import get_building_title_info
from app.schemas.building import TitleInfoItem
from typing import List

router = APIRouter(prefix="/building", tags=["건축물대장"])

@router.get(
    "/title-info/{plat_gb_cd}/{bun}/{ji}/{organization}/{loginType}/{type}/{address}",
    response_model=List[TitleInfoItem],
    summary="건축물대장 표제부 조회 (Path 파라미터 기반)"
)
async def title_info_path(
    plat_gb_cd: str,
    bun: str,
    ji: str,
    organization: str,
    loginType: str,
    type: str,
    address: str,
):
    real_estate_unique_number = f"{plat_gb_cd.zfill(10)}{bun.zfill(4)}{ji.zfill(4)}0"

    body = {
        "realEstateUniqueNumber": real_estate_unique_number,
        "organization": organization,
        "loginType": loginType,
        "type": type,
        "address": address,
    }

    try:
        data = await get_building_title_info(body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return [data]