from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.jeonse_rate import fetch_rent_rate_with_risk

router = APIRouter()

class RentRateRequest(BaseModel):
  address: str

@router.post("/rent-rate")
async def get_rent_rate(data: RentRateRequest):
  try:
    result = fetch_rent_rate_with_risk(data.address)
    return result
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"전세가율 가져오기 실패: {str(e)}")
