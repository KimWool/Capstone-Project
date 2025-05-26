# app/services/risk_score.py

risk_factor = {
    # 세부항목 기준 가중치 (AHP 분석 기반 최종 가중치)
    "소유자불일치": {"weight": 0.1471, "severity": "심각"},
    "소유권침해요소": {"weight": 0.0725, "severity": "심각"},
    "임차권등기명령": {"weight": 0.1384, "severity": "주의"},
    "전세권설정": {"weight": 0.0690, "severity": "주의"},
    "위반건축물": {"weight": 0.0723, "severity": "심각"},
    "불법용도": {"weight": 0.0633, "severity": "심각"},

    # AHP에서 항목 단일로 판단된 위험 요소
    "근저당권": {"weight": 0.2465, "severity": "심각"},
    "깡통위험": {"weight": 0.1909, "severity": "심각"}
}

def safe_divide(a, b, default=1):
    try:
        return a / b if b else default
    except (TypeError, ValueError):
        return default

# 가중치 계산
def apply_risk(score, reasons, severities, key, factor=1.0, reason_text=""):
    info = risk_factor[key]
    score += info["weight"] * 100 * factor
    reasons.append(reason_text or key)
    severities.append(info["severity"])
    return score

# 리스트를 기반으로 위험 등급 판단, 점수는 보조 지표로 사용
def classify_risk_by_severity(score, severities):
    severe = severities.count("심각")
    caution = severities.count("주의")

    if severe >= 3:
        return "매우 위험"
    elif severe >= 2:
        return "위험"
    elif severe >= 1 or caution >= 2:
        return "주의"
    else:
        if score >= 70:
            return "매우 위험"
        elif score >= 40:
            return "위험"
        elif score >= 20:
            return "주의"
        else:
            return "안전"

def calculate_risk_score(findings: dict) -> dict:
    score = 0
    reasons = []
    severities = []
    #print("🔎 전달된 findings:", findings)

    # 1. 소유권 관련 위험
    if findings.get("건축물대장_소유자") != findings.get("등기부_소유자"):
        score = apply_risk(score, reasons, severities, "소유자불일치", 1.0, "소유자 불일치")
    elif findings.get("등기부_소유자") != findings.get("계약_임대인"):
        score = apply_risk(score, reasons, severities, "소유자불일치", 0.8, "임대인과 소유자 다름")
    if any(findings.get(k) == "있음" for k in ["경매개시결정", "압류", "가압류", "가등기", "신탁"]):
        score = apply_risk(score, reasons, severities, "소유권침해요소", 1.0, "소유권 침해 요소 있음")

    # 2. 기존 전세권 및 임차권 위험(복합적인 요인, 실제 위험 낮음)
    if findings.get("임차권"):
        score = apply_risk(score, reasons, severities, "임차권등기명령", 1.0, "임차권 등기명령 존재")
    owner_name = findings.get("등기부_소유자", "").strip()
    if check_defaulter(owner_name):
        score = apply_risk(score, reasons, severities, "전세권설정", 1.0, "상습 채무불이행자 공개 내역에 포함됨")
    elif findings.get("전세권"):
        score = apply_risk(score, reasons, severities, "전세권설정", 0.6, "이전 전세권 설정")

    # 3. 근저당권 설정 위험 (단일 항목이면서 실질 위험도 높음)
    pledge = int(findings.get("채권최고액", 0) or 0)
    price = int(findings.get("주택_시세", 1) or 1) #실제 사용자에게 주소를
    pledge_ratio = safe_divide(pledge, price) * 100

    if pledge_ratio >= 60:
        score = apply_risk(score, reasons, severities, "근저당권", 1.0, "근저당이 시세 대비 과다")
    elif pledge_ratio >= 45:
        score = apply_risk(score, reasons, severities, "근저당권", 0.6, "근저당이 다소 높음")
    elif pledge_ratio >= 30:
        score = apply_risk(score, reasons, severities, "근저당권", 0.3, "근저당 있음")

    # 4. 깡통주택 위험도 (단일 항목이면서 높지만 근저당보다 변동성이 큼)
    deposit = int(findings.get("계약_보증금", 0) or 0)
    margin_ratio = safe_divide(pledge + deposit, price) * 100

    if margin_ratio >= 90:
        score = apply_risk(score, reasons, severities, "깡통위험", 1.0, "깡통주택 가능성 매우 높음")
    elif margin_ratio >= 80:
        score = apply_risk(score, reasons, severities, "깡통위험", 0.65, "깡통 위험 있음")

    # 5. 건축물 적법성/용도
    if findings.get("위반건축물"):
        score = apply_risk(score, reasons, severities, "위반건축물", 1.0, "위반건축물 중대")
    if findings.get("불법용도변경") or findings.get("건물 용도") != "주거용":
        score = apply_risk(score, reasons, severities, "불법용도", 1.0, "불법용도 또는 비주거 건물")
    elif findings.get("근린생활시설"):
        score = apply_risk(score, reasons, severities, "불법용도", 1.0, "불법개조 의심됨")

    # 최종 등급 판단
    grade = classify_risk_by_severity(score, severities);

    return {
        "score": round(score, 1),
        "grade": grade,
        "reasons": reasons
    }

import requests
from bs4 import BeautifulSoup
# 상습 채무불이행자 명단 조회
def check_defaulter(name_to_check):
    url = "https://www.molit.go.kr/USR/WPGE0201/m_37180/DTL.jsp"
    response = requests.get(url)
    if response.status_code != 200:
        print("페이지를 불러오는 데 실패했습니다.")
        return False

    soup = BeautifulSoup(response.text, 'html.parser')
    # 페이지 구조에 따라 적절한 선택자 사용
    table = soup.find('table')
    if not table:
        print("명단 테이블을 찾을 수 없습니다.")
        return False

    rows = table.find_all('tr')[1:]  # 헤더를 제외한 행들
    for row in rows:
        cols = row.find_all('td')
        if cols:
            name = cols[0].get_text(strip=True)
            if name == name_to_check:
                print(f"'{name_to_check}'님은 상습 채무불이행자 명단에 포함되어 있습니다.")
                return True

    print(f"'{name_to_check}'는 명단에 포함되어 있지 않습니다.")
    return False
