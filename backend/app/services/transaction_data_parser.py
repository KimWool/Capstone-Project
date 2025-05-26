# backend/app/services/transaction_data_parser.py
import PublicDataReader as pdr
import xml.etree.ElementTree as ET
import asyncio
import xmltodict
from datetime import datetime
from collections import defaultdict, OrderedDict
from dateutil.relativedelta import relativedelta
from app.clients.transaction_price_api import fetch_transaction_price_data
from app.clients.address_api import fetch_juso_data

def resolve_region_code_from_address(address: str) -> str:
  """
  PublicDataReader를 통해 주소 문자열에서 시군구 코드를 추출
  :param address: 예) "서울특별시 강남구 청담동"
  :return: 시군구 코드 문자열 (예: "11680")
  """
  bdong_df = pdr.code_bdong()

  for _, row in bdong_df.iterrows():
    sido = str(row['시도명']).strip()
    sigungu = str(row['시군구명']).strip()

    # 시군구가 비어있거나 의미 없는 경우 건너뜀
    if not sigungu or sigungu.lower() == 'nan':
      continue

    full_region = f"{sido} {sigungu}"

    # 주소에서 시군구 코드 추출
    if full_region in address:
      region_code = str(row["법정동코드"])[:5]
      print(f"주소: {address} / 지역 코드: {region_code} / 시군구명: {sigungu}")
      return region_code

  raise ValueError("주소에서 시군구 코드를 찾을 수 없습니다.")

# 주소를 입력받아 가장 최근 실거래가 반환
async def get_latest_transaction_by_address(address: str, house_type: str):

  region_code = resolve_region_code_from_address(address)
  current_ym = datetime.today()

  print(f"주소: {address} / 지역 코드: {region_code}")

  # 도로명주소 상세 검색
  jibun = None
  try:
    juso_response = await fetch_juso_data(keyword=address, current_page=1, count_per_page=1)
    juso_list = juso_response.get("results", {}).get("juso", [])
    if juso_list:
      juso_info = juso_list[0]
      road_address = juso_info.get("roadAddr")
      building_name = juso_info.get("bdNm")
      jibun_main = juso_info.get("lnbrMnnm", "").strip()  # 본번
      jibun_sub = juso_info.get("lnbrSlno", "").strip()   # 부번

      if jibun_main:
        if jibun_sub and jibun_sub != "0":
          jibun = f"{jibun_main}-{jibun_sub}"
        else:
          jibun = jibun_main
        print(f"📌 최종 지번: {jibun}")
      else:
        raise ValueError("지번 본번(lnbrMnnm)이 없습니다.")

      print(f"도로명주소: {road_address} / 건물명: {building_name} / 지번: {jibun}")
    else:
      print("도로명주소 검색 결과가 없습니다.")
  except Exception as e:
    print(f"도로명주소 API 호출 중 오류: {e}")

    if not jibun:
      raise ValueError("지번을 확인할 수 없습니다.")

  type_map = {
    "아파트": "apt",
    "오피스텔": "offi",
    "연립다세대": "rh",
    "단독다가구": "sh"
  }
  property_code = type_map.get(house_type)

  if not property_code:
    raise ValueError("지원하지 않는 주택 유형입니다.")

  MAX_RETRIES = 12
  matched_records = []

  for i in range(MAX_RETRIES):
    deal_ym = current_ym.strftime("%Y%m")
    print(f"🔍 {i+1}회차 시도: {deal_ym} 조회 중...")
    items = await fetch_transaction_price_data(region_code, deal_ym, property_code)
    if not items:
      current_ym -= relativedelta(months=1)
      continue

    print(f"✅ {deal_ym} 데이터 {len(items)}건 확인됨")

    # dict → xml 변환
    dict_items = [item.model_dump() for item in items]
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
    # XML 파싱
    parsed = parse_real_estate_xml(xml_str, house_type=house_type)

    # 최근 날짜 순으로 정렬
    all_records = []
    for records in parsed.values():
      all_records.extend(records)
    # 건물명이 일치하는 레코드만 필터링
    jibun_matched = [r for r in all_records if r.get("jibun", "") == jibun]
    if jibun_matched:
      print(f"🏢 '{jibun}' 과(와) 일치하는 지번 {len(jibun_matched)}건 발견됨")
      jibun_matched.sort(key=lambda x: x["deal_date"], reverse=True)
      matched_records = jibun_matched[:5]
      break
    else:
      print(f"⚠️ '{jibun}' 과 일치하는 거래 없음, 이전 달로 이동")
      current_ym -= relativedelta(months=1)

  if not matched_records:
    print("❌ 해당 주소의 실거래 데이터(지번 일치 기준)가 없습니다.")
    return []

  return [record["deposit"] for record in matched_records]

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

# __main__에서 실행
if __name__ == "__main__":
  address = "서울특별시 성동구 금호로 15"
  house_type = "아파트"
  latest_data = asyncio.run(get_latest_transaction_by_address(address, house_type))

  print("\n 최신 거래 보증금 목록:")
  for record in latest_data:
    print(record)