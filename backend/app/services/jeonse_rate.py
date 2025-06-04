import os
import re

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
from threading import Lock

def parse_korean_address(address: str):
  """
  '서울특별시 강남구 역삼동' 같은 주소를 시/도, 시/군/구, 읍/면/동으로 분리
  """
  parts = address.strip().split()
  sido = parts[0] if len(parts) > 0 else ''
  sigungu = parts[1] if len(parts) > 1 else '전체'
  dong = parts[2] if len(parts) > 2 else '전체'
  return sido, sigungu, dong


def find_available_search_month(wait, max_lookback=6):
  """
  현재 월부터 max_lookback 개월 전까지 순차적으로 시도하며
  전세가율 데이터가 있는 월을 찾는 함수.
  """
  now = datetime.now()
  for i in range(max_lookback):
    # 월을 하나씩 감소시키되, 1월 이전이면 전년도 12월 등으로 이동
    search_month = now.month - i - 1
    if search_month <= 0:
      year = now.year - 1
      month = 12 + search_month
    else:
      year = now.year
      month = search_month

    year_text = f"{year}년"
    month_text = f"{month}월"

    print(f"[시도 중] {year_text} {month_text} 데이터 검색 시도")

    try:
      # 셀렉트박스 선택 시도
      search_period_year = Select(wait.until(EC.presence_of_element_located((By.ID, "yearFrom"))))
      search_period_year.select_by_visible_text(year_text)

      search_period_month = Select(wait.until(EC.presence_of_element_located((By.ID, "monthFrom"))))
      search_period_month.select_by_visible_text(month_text)

      return year_text, month_text
    except Exception as e:
      print(f"해당 날짜 선택 실패: {year_text} {month_text} → {str(e)}")
      continue

  raise ValueError(f"{max_lookback}개월 전까지 데이터가 존재하지 않습니다.")


def fetch_rent_rate(address: str):
  # Selenium WebDriver 설정
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')  # 브라우저 창을 띄우지 않음
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')

  # 크롬 드라이버 실행
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
  driver.get("https://rtech.or.kr/board/rentRateView.do#")

  try:
    wait = WebDriverWait(driver, 10)

    # 주소 분리
    sido, sigungu, dong = parse_korean_address(address)

    # 통계구분 선택: 전세가율
    stat_select = Select(wait.until(EC.presence_of_element_located((By.ID, "stastics_gbn"))))
    stat_select.select_by_visible_text("전세가율")

    # 지역구분 선택: 시군구별
    region_select = Select(wait.until(EC.presence_of_element_located((By.ID, "addr_part"))))
    region_select.select_by_visible_text("시군구별")

    # 시도 선택
    sido_select = Select(wait.until(EC.presence_of_element_located((By.ID, "do_code"))))
    sido_select.select_by_visible_text(sido)

    # 시군구 선택
    sigungu_select = Select(wait.until(EC.presence_of_element_located((By.ID, "city_code"))))
    sigungu_select.select_by_visible_text(sigungu)

    dong_select_element = None
    # 동 리스트 로딩 대기 및 선택 (최대 5초 대기)
    try:
      # 동 셀렉트박스 로딩 대기
      dong_select_element = wait.until(EC.presence_of_element_located((By.ID, "dong_code")))

      # 최대 5초 동안 dong 옵션 중 우리가 원하는 값이 뜰 때까지 대기
      WebDriverWait(driver, 5).until(
          lambda d: dong in [opt.text.strip() for opt in Select(d.find_element(By.ID, "dong_code")).options]
      )

      # 동 선택
      dong_select = Select(dong_select_element)
      dong_select.select_by_visible_text(dong)

    except TimeoutException:
      print(f"[경고] '{dong}' 동을 찾을 수 없어 '전체'로 대체합니다.")
      if dong_select_element:
        dong_select = Select(dong_select_element)
        dong_select.select_by_visible_text("전체")
      else:
        print("[오류] dong_select_element를 찾을 수 없습니다.")
        return None

    # 현재 년월 가져 오기
    now = datetime.now()
    current_year, current_month = find_available_search_month(wait)
    if now.month == 1:
      current_year = f"{now.year -1}년"
      current_month = "12월"
    else:
      current_year = f"{now.year}년"
      current_month = f"{now.month - 1}월"

    # 검색 기간 선택: 현재 날짜(년월)
    search_period_year = Select(wait.until(EC.presence_of_element_located((By.ID, "yearFrom"))))
    search_period_year.select_by_visible_text(current_year)
    search_period_month = Select(wait.until(EC.presence_of_element_located((By.ID, "monthFrom"))))
    search_period_month.select_by_visible_text(current_month)

    # 검색 버튼 클릭
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="rateSearchtbl"]/tbody/tr[1]/td[7]/button[2]')))
    search_button.click()

    # 결과 로딩 대기
    time.sleep(5)  # 필요에 따라 조정

    # 결과 테이블 추출
    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rent_rate_table")))
    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    # 의미 있는 마지막 행에서 실거래값만 추출
    last_row = rows[-1]
    last_row_text = last_row.text
    raw_values = re.findall(r"\d+\.\d+|-", last_row_text)
    if len(raw_values) == 4:
      # '-'는 None으로 변환하고 숫자는 float로 변환
      parsed_values = [float(val) if val != '-' else None for val in raw_values]
      result = {
        "status": "ok",
        "아파트_최근1년": parsed_values[0],
        "아파트_최근3개월": parsed_values[1],
        "연립다세대_최근1년": parsed_values[2],
        "연립다세대_최근3개월": parsed_values[3],
      }
      return result
    else:
      print("[디버그] 마지막 행 텍스트:", last_row_text)
      print("[디버그] 추출된 값:", raw_values)
      print("[오류] 전세가율 값이 4개가 아닙니다:", raw_values)
      return None
  except Exception as e:
    print(f"오류 발생: {e}")
    return None

  finally:
    driver.quit()

# 전세가율 기반 위험도 판단 함수
def assess_risk_by_jeonse_rate(rate: float) -> str:
  if rate is None:
    risk_result = "데이터 없음"
  try:
    rate_float = float(rate)
  except (ValueError, TypeError):
    return "데이터 오류"
  if rate >= 80:
    risk_result = "위험"
  elif rate >= 70:
    risk_result = "주의"
  else:
    risk_result = "안전"
  return risk_result

driver_lock = Lock()

def fetch_rent_rate_with_risk(address: str):
  with driver_lock:
    rent_rates = fetch_rent_rate(address)
  if not rent_rates:
    return None

  result_with_risk = {}
  for key, value in rent_rates.items():
    result_with_risk[key] = {
      "rate": value,
      "risk": assess_risk_by_jeonse_rate(value)
    }
  return result_with_risk

# __main__에서 실행
if __name__ == "__main__":
  address = "서울특별시 송파구 석촌동"
  jeonse_rates = fetch_rent_rate(address)
  if jeonse_rates:
    print("전세가율 요약:")
    for k, v in jeonse_rates.items():
      print(f"{k}: {'데이터 없음' if v is None else f'{v}%'}")
  else:
    print("전세가율 데이터를 불러올 수 없습니다.")

