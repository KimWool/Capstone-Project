# api/endpoints/prediction.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.sllm_model import predict_risk

router = APIRouter()

class RiskInput(BaseModel):
    deposit: str
    period: str
    address: str

@router.post("/predict-risk/")
def predict_risk_api(input: RiskInput):
    result = predict_risk(input.deposit, input.period, input.address)
    return {"result": result}
