# app/services/risk_scorer.py

weights = {
    "소유권_문제": 0.25,
    "기존임차권_설정": 0.20,
    "근저당권_설정": 0.20,
    "깡통주택_위험도": 0.20,
    "건축물_용도/위반": 0.15
}

def calculate_risk_score(findings: dict) -> dict:
    score = 0
    reasons = []

    # 1. 소유권 관련 위험
    if findings.get("경매개시결정") == "있음" or findings.get("압류") == "있음":
        score += weights["소유권_문제"] * 100
        reasons.append("경매/압류 있음")
    elif findings.get("건축물대장_소유자") != findings.get("등기부_소유자"):
        score += weights["소유권_문제"] * 80
        reasons.append("소유자 불일치")
    elif findings.get("등기부_소유자") != findings.get("계약_임대인"):
        score += weights["소유권_문제"] * 60
        reasons.append("임대인과 소유자 다름")
    elif any(findings.get(k) == "있음" for k in ["가압류", "가등기", "신탁"]):
        score += weights["소유권_문제"] * 40
        reasons.append("기타 권리 제한 있음")

    # 2. 기존 전세권 및 임차권 위험
    if findings.get("전세권_다수") == "있음" or findings.get("보증금_장기미반환") == "있음":
        score += weights["기존임차권_설정"] * 100
        reasons.append("다수 전세권 또는 장기미반환")
    elif findings.get("전세권말소청구권가등기") == "있음" or findings.get("임차권등기명령") == "있음":
        score += weights["기존임차권_설정"] * 75
        reasons.append("전세권말소/임차권등기 존재")
    elif findings.get("이전세입자_전세권") == "있음":
        score += weights["기존임차권_설정"] * 50
        reasons.append("이전 세입자 전세권 있음")

    # 3. 근저당권 위험
    pledge = findings.get("채권최고액", 0)
    price = findings.get("주택_시세", 1)
    pledge_ratio = (pledge / price) * 100
    if pledge_ratio >= 60:
        score += weights["근저당권_설정"] * 100
        reasons.append("근저당이 시세 대비 과다")
    elif pledge_ratio >= 45:
        score += weights["근저당권_설정"] * 75
        reasons.append("근저당이 다소 높음")
    elif pledge_ratio >= 30:
        score += weights["근저당권_설정"] * 50
        reasons.append("근저당 있음")

    # 4. 깡통주택 위험
    deposit = findings.get("기존_보증금", 0)
    margin_ratio = ((pledge + deposit) / price) * 100
    if margin_ratio >= 90:
        score += weights["깡통주택_위험도"] * 100
        reasons.append("깡통주택 가능성 매우 높음")
    elif margin_ratio >= 80:
        score += weights["깡통주택_위험도"] * 75
        reasons.append("깡통 위험 있음")

    # 5. 건축물 적법성/용도
    if findings.get("불법용도변경") == "의심됨" or findings.get("위반건축물") == "중대":
        score += weights["건축물_용도/위반"] * 100
        reasons.append("위반건축물 중대")
    elif findings.get("건물용도") == "비주거":
        score += weights["건축물_용도/위반"] * 60
        reasons.append("비주거용 건물")

    # 점수 등급
    grade = "매우 위험" if score > 70 else "위험" if score > 40 else "주의" if score > 20 else "안전"

    return {
        "score": round(score, 1),
        "grade": grade,
        "reasons": reasons
    }
