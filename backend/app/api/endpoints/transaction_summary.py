# app/api/endpoints/transaction_summary.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.transaction_data_parser import summarize_transaction_by_address

router = APIRouter()

class SummaryRequest(BaseModel):
  address: str
  house_type: str  # 예: "아파트", "다가구", "오피스텔" 등

@router.post("/transaction/summary")
async def get_transaction_summary(request: SummaryRequest):
  try:
    result = await summarize_transaction_by_address(request.address, request.house_type)
    return result
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"요약 실패: {str(e)}")
