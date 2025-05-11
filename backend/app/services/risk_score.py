# app/services/risk_scorer.py: 위험도 점수 계산기

def calculate_risk(meta):
    score = 0
    """if meta.get("근저당권") == "있음":
        score += 5
    if meta.get("전세권") == "없음":
        score += 3
    return {
        "score": score,
        "level": "높음" if score >= 8 else ("보통" if score >= 4 else "낮음")"""
    # 1. 소유권 관련 위험 (최대 25점)
    if meta.get("경매개시결정") == "있음" or meta.get("압류") == "있음":
        score += 25
    elif meta.get("건축물대장_소유자") != meta.get("등기부_소유자"):
        score += 20
    elif meta.get("등기부_소유자") != meta.get("계약_임대인"):
        score += 15 # 계약 임대인 필수 입력 필요
    elif any(meta.get(key) == "있음" for key in ["가압류", "가등기", "신탁"]):
        score += 10

    # 2. 기존 전세권 및 임차권 위험 (최대 20점)
    if meta.get("전세권_다수") == "있음" or meta.get("보증금_장기미반환") == "있음":
        score += 20
    elif meta.get("전세권말소청구권가등기") == "있음" or meta.get("임차권등기명령") == "있음":
        score += 15
    elif meta.get("이전세입자_전세권") == "있음":
        score += 10
    elif meta.get("정상_전세권") == "있음":
        score += 5

    # 3. 근저당권 설정 위험 (최대 20점)
    MaxPledgeAmount = meta.get("채권최고액", 0)
    MarketPrice = meta.get("주택_시세", 1)  # 0으로 나누지 않기 위해 최소 1 설정
    MortgageRatio = (MaxPledgeAmount / MarketPrice) * 100

    if MortgageRatio >= 60:
        score += 20
    elif MortgageRatio >= 45:
        score += 15
    elif MortgageRatio >= 30:
        score += 10
    elif MortgageRatio > 0:
        score += 5

    # 4. 깡통주택 위험도 (최대 20점)
    deposit = meta.get("기존_보증금", 0)
    marginRatio = ((MaxPledgeAmount + deposit) / MarketPrice) * 100
    if marginRatio >= 90:
        score += 20
    elif marginRatio >= 80:
        score += 15
    elif marginRatio >= 70:
        score += 10
    elif marginRatio >= 60:
        score += 5

    # 5. 건축물 적법성 위험 (최대 15점)
    if meta.get("불법용도변경") == "의심됨" or meta.get("위반건축물") == "중대":
        score += 15
    elif meta.get("건물용도") == "비주거":
        score += 10
    elif meta.get("위반건축물") == "경미":
        score += 5

    # 위험도 등급
    if score <= 20:
        level = "안전"
    elif score <= 40:
        level = "주의"
    elif score <= 60:
        level = "위험"
    else:
        level = "매우 위험"

    return {
        "score": score,
        "level": level
    }