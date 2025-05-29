# app/api/endpoints/jeonse_price.py
from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.clients.jeonse_price_api import fetch_jeonse_price_data
from app.schemas.jeonse_price import (
  AptJeonsePrice,
  OffiJeonsePrice,
  RhJeonsePrice,
  ShJeonsePrice
)

router = APIRouter(prefix="/transaction-price", tags=["부동산 전월세 실거래가 조회"])

@router.get("/apt", response_model=List[AptJeonsePrice], tags=["부동산 전월세 실거래가 조회"], summary="아파트 전월세 실거래가 조회")
async def get_apt_transaction_price(
    region_code: str = Query(..., description="법정동 코드 앞 5자리 (예: 11110)"),
    deal_ym: str = Query(..., description="거래 년월 (예: 202401)")
):
  try:
    return await fetch_jeonse_price_data(region_code, deal_ym, "apt")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/offi", response_model=List[OffiJeonsePrice], tags=["부동산 전월세 실거래가 조회"], summary="오피스텔 전월세 실거래가 조회")
async def get_offi_transaction_price(
    region_code: str = Query(..., description="법정동 코드 앞 5자리 (예: 11110)"),
    deal_ym: str = Query(..., description="거래 년월 (예: 202401)")
):
  try:
    return await fetch_jeonse_price_data(region_code, deal_ym, "offi")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/rh", response_model=List[RhJeonsePrice], tags=["부동산 전월세 실거래가 조회"], summary="연립/다세대 전월세 실거래가 조회")
async def get_rh_transaction_price(
    region_code: str = Query(..., description="법정동 코드 앞 5자리 (예: 11110)"),
    deal_ym: str = Query(..., description="거래 년월 (예: 202401)")
):
  try:
    return await fetch_jeonse_price_data(region_code, deal_ym, "rh")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@router.get("/sh", response_model=List[ShJeonsePrice], tags=["부동산 전월세 실거래가 조회"], summary="단독/다가구 전월세 실거래가 조회")
async def get_sh_transaction_price(
    region_code: str = Query(..., description="법정동 코드 앞 5자리 (예: 11110)"),
    deal_ym: str = Query(..., description="거래 년월 (예: 202401)")
):
  try:
    return await fetch_jeonse_price_data(region_code, deal_ym, "sh")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))