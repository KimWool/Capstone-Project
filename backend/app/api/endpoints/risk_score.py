# app/api/endpoints/risk_score.py
import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from run_analysis import analyze_by_address

router = APIRouter()

class AnalysisRequest(BaseModel):
  full_address: str
  deposit: int

@router.post("/risk/address")
async def analyze_risk(req: AnalysisRequest):
  try:
    transaction_data = analyze_by_address(req.full_address, req.deposit)
    with open("latest_transaction_data.json", "w", encoding="utf-8") as f:
      json.dump(transaction_data, f, ensure_ascii=False, indent=2)
    return transaction_data
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
