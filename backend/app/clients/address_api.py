# backend/app/clients/address_api.py

import os

import requests
from dotenv import load_dotenv

load_dotenv()

JUSO_API_URL = os.getenv("JUSO_API_URL")
CONFM_KEY = os.getenv("CONFM_KEY")

async def fetch_juso_data(keyword: str, current_page: int, count_per_page: int) -> dict:
  params = {
    "confmKey": CONFM_KEY,
    "keyword": keyword,
    "currentPage": current_page,
    "countPerPage": count_per_page,
    "resultType": "json"
  }
  resp = requests.get(JUSO_API_URL, params=params)
  resp.raise_for_status()
  return resp.json()
