# app/services/external_api.py
import os
import requests
from dotenv import load_dotenv

from app.clients.transaction_price_api import SERVICE_KEY

load_dotenv()

REGISTRY_API_URL = os.getenv("REGISTRY_API_URL")
BUILDING_API_URL = os.getenv("BUILDING_API_URL")
APT_TRANSACTION_PRICE_URL = os.getenv("APT_TRANSACTION_PRICE_URL")
OFFI_TRANSACTION_PRICE_URL = os.getenv("OFFI_TRANSACTION_PRICE_URL")
RH_TRANSACTION_PRICE_URL = os.getenv("RH_TRANSACTION_PRICE_URL")
SH_TRANSACTION_PRICE_URL = os.getenv("SH_TRANSACTION_PRICE_URL")
JUSO_API_URL = os.getenv("JUSO_API_URL")

API_KEY = os.getenv("API_KEY")
SERVICE_KEY = os.getenv("SERVICE_KEY")
CONFM_KEY = os.getenv("CONFM_KEY")

def fetch_registry_data(query_params: dict) -> dict:
    """등기부등본 API 호출"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    resp = requests.get(REGISTRY_API_URL, params=query_params, headers=headers)
    resp.raise_for_status()
    return resp.json()

def fetch_building_data(query_params: dict) -> dict:
    """건축물대장 API 호출"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    resp = requests.get(BUILDING_API_URL, params=query_params, headers=headers)
    resp.raise_for_status()
    return resp.json()

def fetch_apt_transaction_price_data(query_params: dict) -> dict:
    """아파트_전월세_실거래가 API 호출"""
    params = {
        "serviceKey": SERVICE_KEY,
        "_type": "json",
        **query_params
    }
    resp = requests.get(APT_TRANSACTION_PRICE_URL, params=params)
    resp.raise_for_status()
    return resp.json()

def fetch_offi_transaction_price_data(query_params: dict) -> dict:
    """오피스텔_전월세_실거래가 API 호출"""
    params = {
        "serviceKey": SERVICE_KEY,
        "_type": "json",
        **query_params
    }
    resp = requests.get(OFFI_TRANSACTION_PRICE_URL, params=params)
    resp.raise_for_status()
    return resp.json()

def fetch_rh_transaction_price_data(query_params: dict) -> dict:
    """연립다세대_전월세_실거래가 API 호출(row house)"""
    params = {
        "serviceKey": SERVICE_KEY,
        "_type": "json",
        **query_params
    }
    resp = requests.get(RH_TRANSACTION_PRICE_URL, params=params)
    resp.raise_for_status()
    return resp.json()

def fetch_sh_transaction_price_data(query_params: dict) -> dict:
    """단독/다가구_전월세_실거래가 API 호출(single house)"""
    params = {
        "serviceKey": SERVICE_KEY,
        "_type": "json",
        **query_params
    }
    resp = requests.get(SH_TRANSACTION_PRICE_URL, params=params)
    resp.raise_for_status()
    return resp.json()

def fetch_juso_data(query_params: dict) -> dict:
    "도로명주소 검색 API 호출"
    params = {
        "confmKey": JUSO_API_URL,
        "_type": "json",
        **query_params
    }
    resp = requests.get(JUSO_API_URL, params=params)
    resp.raise_for_status()
    return resp.json()

def extract_metadata(api_response: dict) -> dict:
    """
    API 응답에서 핵심 메타데이터(예: 소유자, 주소, 세부내용 등)를 뽑아
    새로운 dict 형태로 리턴합니다.
    """
    # **여기에는 실제 API 스펙에 맞춘 필드 매핑을 넣으세요.**
    return {
        "owner": api_response.get("ownerName") or api_response.get("owner"),
        "address": api_response.get("address"),
        "details": api_response.get("detailInfo") or api_response.get("details"),
    }
