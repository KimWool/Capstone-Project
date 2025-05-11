### app/services/risk_scorer.py: 위험도 점수 계산기

# 위험 항목별 가중치
weights = {
    "명의불일치": 0.3,
    "근저당초과": 0.4,
    "비주거용": 0.2,
    "구조불량": 0.1
}

def calculate_risk_score(findings: str) -> dict:
    score = 0
    reasons = []
    if "소유자와 임대인 다름" in findings:
        score += weights["명의불일치"] * 100
        reasons.append("명의불일치")
    if "근저당이 보증금보다 높음" in findings:
        score += weights["근저당초과"] * 100
        reasons.append("근저당초과")
    if "비주거용" in findings:
        score += weights["비주거용"] * 100
        reasons.append("비주거용")
    if "오래된 건물" in findings or "철근 미사용" in findings:
        score += weights["구조불량"] * 100
        reasons.append("구조불량")

    return {
        "score": round(score, 1),
        "grade": "높음" if score > 70 else "보통" if score > 40 else "낮음",
        "reasons": reasons
    }
