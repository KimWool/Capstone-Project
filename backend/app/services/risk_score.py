### risk_scorer.py: 위험도 점수 계산기

def calculate_risk(meta):
    score = 0
    if meta.get("근저당권") == "있음":
        score += 5
    if meta.get("전세권") == "없음":
        score += 3
    return {
        "score": score,
        "level": "높음" if score >= 8 else ("보통" if score >= 4 else "낮음")
    }