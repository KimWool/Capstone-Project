# app/services/risk_score.py

weights = {
    # 세부항목 기준 가중치 (AHP 분석 기반 최종 가중치)
    "소유자불일치": 0.14717,
    "소유권침해요소": 0.07250,
    "임차권등기명령": 0.13841,
    "전세권설정": 0.06896,
    "위반건축물": 0.07233,
    "불법용도": 0.06324,

    # AHP에서 항목 단일로 판단된 위험 요소
    "근저당권": 0.24652,
    "깡통위험": 0.19086
}

def calculate_risk_score(findings: dict) -> dict:
    score = 0
    reasons = []

    # 1. 소유권 관련 위험
    if findings.get("건축물대장_소유자") != findings.get("등기부_소유자"):
        score += weights["소유자불일치"] * 100
        reasons.append("소유자 불일치")
    elif findings.get("등기부_소유자") != findings.get("계약_임대인"):
        score += weights["소유자불일치"] * 80
        reasons.append("임대인과 소유자 다름")
    if any(findings.get(k) == "있음" for k in ["경매개시결정", "압류", "가압류", "가등기", "신탁"]):
        score += weights["소유권침해요소"] * 100
        reasons.append("소유권 침해 요소 있음")

    # 2. 기존 전세권 및 임차권 위험(복합적인 요인, 실제 위험 낮음)
    if findings.get("임차권등기명령") == "있음":
        score += weights["임차권등기명령"] * 100
        reasons.append("임차권 등기명령 존재")
    if findings.get("전세권_다수") == "있음" or findings.get("보증금_장기미반환") == "있음":
        score += weights["전세권설정"] * 80
        reasons.append("전세권 다수/보증금 미반환")
    elif findings.get("전세권말소청구권가등기") == "있음" or findings.get("이전세입자_전세권") == "있음":
        score += weights["전세권설정"] * 60
        reasons.append("이전 전세권 관련 문제")

    # 3. 근저당권 설정 위험 (단일 항목이면서 실질 위험도 높음)
    pledge = findings.get("채권최고액", 0)
    price = findings.get("주택_시세", 1)
    pledge_ratio = (pledge / price) * 100
    if pledge_ratio >= 60:
        score += weights["근저당권"] * 100
        reasons.append("근저당이 시세 대비 과다")
    elif pledge_ratio >= 45:
        score += weights["근저당권"] * 60 #기존보다 간격 확대
        reasons.append("근저당이 다소 높음")
    elif pledge_ratio >= 30:
        score += weights["근저당권"] * 30
        reasons.append("근저당 있음")

    # 4. 깡통주택 위험도 (단일 항목이면서 높지만 근저당보다 변동성이 큼)
    deposit = findings.get("기존_보증금", 0)
    margin_ratio = ((pledge + deposit) / price) * 100
    if price <= 0:
        price = 1; # ZeroDivisionError 방지
    if margin_ratio >= 90:
        score += weights["깡통위험"] * 100
        reasons.append("깡통주택 가능성 매우 높음")
    elif margin_ratio >= 80:
        score += weights["깡통위험"] * 65 #중간값 낮춤
        reasons.append("깡통 위험 있음")

    # 5. 건축물 적법성/용도
    if findings.get("위반건축물") == "중대":
        score += weights["위반건축물"] * 100
        reasons.append("위반건축물 중대")
    if findings.get("불법용도변경") == "의심됨" or findings.get("건물용도") == "비주거":
        score += weights["불법용도"] * 100
        reasons.append("불법용도 또는 비주거 건물")

    # 점수 등급
    HIGH_RISK = 70
    MEDIUM_RISK = 40
    LOW_RISK = 20

    if score > HIGH_RISK:
        grade = "매우 위험"
    elif score > MEDIUM_RISK:
        grade = "위험"
    elif score > LOW_RISK:
        grade = "주의"
    else:
        grade = "안전"

    return {
        "score": round(score, 1),
        "grade": grade,
        "reasons": reasons
    }
