# app/api/endpoints/jeonse_price.py
from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.clients.trade_price_api import fetch_trade_price_data
from app.schemas.trade_price import (
  AptTradePrice,
  OffiTradePrice,
  RhTradePrice,
  ShTradePrice
)

router = APIRouter(prefix="/transaction-price", tags=["부동산 전월세 실거래가 조회"])

@router.get("/apt", response_model=List[AptTradePrice], tags=["부동산 전월세 실거래가 조회"], summary="아파트 전월세 실거래가 조회")
async def get_apt_trade_price(
    region_code: str = Query(..., description="법정동 코드 앞 5자리 (예: 11110)"),
    deal_ym: str = Query(..., description="거래 년월 (예: 202401)")
):
  try:
    return await fetch_trade_price_data(region_code, deal_ym, "apt")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/offi", response_model=List[OffiTradePrice], tags=["부동산 전월세 실거래가 조회"], summary="오피스텔 전월세 실거래가 조회")
async def get_offi_trade_price(
    region_code: str = Query(..., description="법정동 코드 앞 5자리 (예: 11110)"),
    deal_ym: str = Query(..., description="거래 년월 (예: 202401)")
):
  try:
    return await fetch_trade_price_data(region_code, deal_ym, "offi")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/rh", response_model=List[RhTradePrice], tags=["부동산 전월세 실거래가 조회"], summary="연립/다세대 전월세 실거래가 조회")
async def get_rh_trade_price(
    region_code: str = Query(..., description="법정동 코드 앞 5자리 (예: 11110)"),
    deal_ym: str = Query(..., description="거래 년월 (예: 202401)")
):
  try:
    return await fetch_trade_price_data(region_code, deal_ym, "rh")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/sh", response_model=List[ShTradePrice], tags=["부동산 전월세 실거래가 조회"], summary="단독/다가구 전월세 실거래가 조회")
async def get_sh_trade_price(
    region_code: str = Query(..., description="법정동 코드 앞 5자리 (예: 11110)"),
    deal_ym: str = Query(..., description="거래 년월 (예: 202401)")
):
  try:
    return await fetch_trade_price_data(region_code, deal_ym, "sh")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))