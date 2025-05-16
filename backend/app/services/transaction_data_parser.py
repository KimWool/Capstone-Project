# backend/app/services/transaction_data_parser.py
import PublicDataReader as pdr
import xml.etree.ElementTree as ET
import json
from collections import defaultdict, OrderedDict

def parse_real_estate_xml(xml_str: str, house_type: str):
  """
  XML 문자열을 파싱하여 시/도 코드별로 데이터를 분류
  :param xml_str: XML 형식 문자열
  :param house_type: "아파트", "오피스텔", "연립다세대", "단독다가구"
  :return: 시/도 코드별 데이터 dict
  """
  root = ET.fromstring(xml_str)
  grouped_data = defaultdict(list)

  bdong_df = pdr.code_bdong()

  for item in root.findall(".//item"):
    # 공통 필드 추출
    try:
      deal_year = item.findtext("dealYear")
      deal_month = item.findtext("dealMonth")
      deal_day = item.findtext("dealDay")
      deposit = item.findtext("deposit")
      rent = item.findtext("monthlyRent")
      area = item.findtext("excluUseAr") or item.findtext("totalFloorAr")
      sgg_code = item.findtext("sggCd")
      jibun = item.findtext("jibun")
      floor = item.findtext("floor")
      umdNm = item.findtext("umdNm")

      # 건물 이름 (유형별 다름)
      if house_type == "아파트":
        name = item.findtext("aptNm")
      elif house_type == "오피스텔":
        name = item.findtext("offiNm")
      elif house_type == "연립다세대":
        name = item.findtext("mhouseNm")
      elif house_type == "단독다가구":
        name = item.findtext("houseType")  # "다가구" 또는 "단독"
      else:
        name = "unknown"

      sido_code = sgg_code[:2]  # 시/도 코드 추출

      # 법정동코드 앞 5자리가 sgg_code와 일치하는 행을 찾기
      match_row = bdong_df[bdong_df["법정동코드"].astype(str).str.startswith(sgg_code)]

      if not match_row.empty:
        sido_name = match_row.iloc[0]["시도명"]
        sgg_name = match_row.iloc[0]["시군구명"]
      else:
        sido_name = "알수없음"
        sgg_name = "알수없음"

      grouped_data[sido_code].append(OrderedDict([
        ("sgg_code", sgg_code),
        ("sido_name", sido_name),
        ("sgg_name", sgg_name),
        ("umdNm", umdNm),
        ("jibun", jibun),
        ("name", name),
        ("deal_date", f"{deal_year}-{deal_month.zfill(2)}-{deal_day.zfill(2)}"),
        ("deposit", int(deposit.replace(",", "")) if deposit else 0),
        ("monthly_rent", int(rent.replace(",", "")) if rent else 0),
        ("area", float(area) if area else 0),
        ("floor", int(floor) if floor and floor.isdigit() else None),
      ]))
    except Exception as e:
      print("Error parsing item:", e)

  return grouped_data

import asyncio
from app.clients.transaction_price_api import fetch_transaction_price_data
from app.schemas.transaction_price import AptTransactionPrice, OffiTransactionPrice, RhTransactionPrice, ShTransactionPrice
import xmltodict
import pprint

async def test_with_api():
  region_code = "41135"  # 예: 경기 성남시 분당구
  deal_ym = "202501"
  property_type = "offi"  # "apt", "offi", "rh", "sh" 중 선택

  print(f"🔍 {deal_ym} / {region_code} / {property_type} 데이터 요청 중...")

  try:
    # Step 1: API로 데이터를 받아옴 (Pydantic 객체 리스트)
    items = await fetch_transaction_price_data(region_code, deal_ym, property_type)

    if not items:
      print("❌ 가져온 데이터가 없습니다.")
      return

    # Step 2: 객체를 dict로 변환 후 다시 XML 문자열로 직렬화
    dict_items = [item.dict() for item in items]
    xml_dict = {
      "response": {
        "body": {
          "items": {
            "item": dict_items
          }
        }
      }
    }
    xml_str = xmltodict.unparse(xml_dict, pretty=True)

    # Step 3: XML 파싱 함수에 전달
    parsed = parse_real_estate_xml(xml_str, house_type="오피스텔")

    # Step 4: 출력
    print("🔍 시/도 코드별 오피스텔 전월세 실거래가:")
    for sido, records in parsed.items():
      print(f"\n📁 시도 코드 {sido} - 건수: {len(records)}")
      pprint.pprint(records)

  except Exception as e:
    print(f"🚨 테스트 중 오류 발생: {e}")

# __main__에서 실행
if __name__ == "__main__":
  asyncio.run(test_with_api())

