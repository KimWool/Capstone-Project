# backend/app/clients/transaction_price_api.py

import os
import httpx
from typing import List, Union
from fastapi import HTTPException
from dotenv import load_dotenv
from app.schemas.transaction_price import (
  AptTransactionPrice,
  OffiTransactionPrice,
  RhTransactionPrice,
  ShTransactionPrice
)
import logging
import xmltodict

# 환경 변수 로드
load_dotenv()

APT_TRANSACTION_PRICE_URL = os.getenv("APT_TRANSACTION_PRICE_URL")
OFFI_TRANSACTION_PRICE_URL = os.getenv("OFFI_TRANSACTION_PRICE_URL")
RH_TRANSACTION_PRICE_URL = os.getenv("RH_TRANSACTION_PRICE_URL")
SH_TRANSACTION_PRICE_URL = os.getenv("SH_TRANSACTION_PRICE_URL")
SERVICE_KEY = os.getenv("SERVICE_KEY")

# 로거 설정
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# 환경 변수 검증
if not all([APT_TRANSACTION_PRICE_URL, OFFI_TRANSACTION_PRICE_URL, RH_TRANSACTION_PRICE_URL, SH_TRANSACTION_PRICE_URL, SERVICE_KEY]):
  raise RuntimeError("필수 환경 변수가 누락되었습니다.")

# API URL 선택 함수
def get_url_by_property_type(property_type: str) -> str:
  if property_type == "apt":
    return APT_TRANSACTION_PRICE_URL
  elif property_type == "offi":
    return OFFI_TRANSACTION_PRICE_URL
  elif property_type == "rh":
    return RH_TRANSACTION_PRICE_URL
  elif property_type == "sh":
    return SH_TRANSACTION_PRICE_URL
  else:
    raise ValueError("지원하지 않는 부동산 유형입니다. (apt, offi, rh, sh 중 하나)")

# 안전한 숫자 변환 함수
def safe_int(val, default=0):
  try:
    return int(val)
  except (TypeError, ValueError):
    return default

def safe_float(val, default=0.0):
  try:
    return float(val.replace(",", "").replace(" ", ""))
  except (AttributeError, ValueError):
    return default


# API 요청 및 파싱 함수
async def fetch_transaction_price_data(region_code: str, deal_ym: str, property_type: str = "apt") -> List[Union[AptTransactionPrice, OffiTransactionPrice, RhTransactionPrice, ShTransactionPrice]]:
  """
  아파트/오피스텔/연립다세대/단독다가구 전월세 실거래가 조회
  :param region_code: 법정동 코드
  :param deal_ym: 계약 년월
  :param property_type: 'apt', 'offi', 'rh', 'sh' 중 하나
  """
  url = get_url_by_property_type(property_type)
  params = {
    "serviceKey": SERVICE_KEY,
    "LAWD_CD": region_code,
    "DEAL_YMD": deal_ym,
    "numOfRows": "100",
    "pageNo": "1",
  }

  logger.info(f"[국토부 API 요청] {property_type.upper()} params: {params}")

  try:
    async with httpx.AsyncClient() as client:
      resp = await client.get(url, params=params)
      resp.raise_for_status()
    logger.info(f"[국토부 API 응답] {property_type.upper()} 응답: {resp.text[:500]}")
  except httpx.HTTPStatusError as e:
    detail = f"{property_type.upper()} API HTTP 오류: {e.response.status_code}, 내용: {e.response.text}"
    logger.error(detail)
    raise HTTPException(status_code=502, detail=detail)
  except httpx.RequestError as e:
    logger.error(f"{property_type.upper()} API 요청 오류: {str(e)}")
    raise HTTPException(status_code=502, detail=f"API 요청 실패: {str(e)}")

  try:
    data = xmltodict.parse(resp.text)
    body = data.get("response", {}).get("body", {})
    items = body.get("items", {}).get("item")

    if not items:
      return []

    # 단일 item일 경우 리스트로 변환
    if not isinstance(items, list):
      items = [items]

    # 항목에 따라 적절한 모델로 변환
    if property_type == "apt":
      return [AptTransactionPrice(**item) for item in items]
    elif property_type == "offi":
      return [OffiTransactionPrice(**item) for item in items]
    elif property_type == "rh":
      return [RhTransactionPrice(**item) for item in items]
    elif property_type == "sh":
      return [ShTransactionPrice(**item) for item in items]
    else:
      raise ValueError(f"지원하지 않는 유형입니다: {property_type}")

  except Exception as e:
    logger.error(f"XML 파싱 또는 변환 실패: {e}")
    raise HTTPException(status_code=502, detail="XML → JSON 파싱 실패")
