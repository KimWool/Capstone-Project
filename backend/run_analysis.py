import json
from app.services.sllm_model import compare_documents
from app.services.risk_score import calculate_risk_score
from app.services.vector_db import store_full_analysis


def load_data():
    with open("registry_data.json", encoding="utf-8") as f:
        registry_list = json.load(f)
    with open("building_data.json", encoding="utf-8") as f:
        building_list = json.load(f)
    return registry_list, building_list

def main():
    registry_data, building_data = load_data()
    for reg, bld in zip(registry_data, building_data):
        case_id = reg["case_id"]
        address = reg["address"]

        # 1. 텍스트 구성
        reg_text = f"소유자: {reg['owner_name']}, 용도: {reg['building_purpose']}, 구조: {reg['building_structure']}, 권리사항: {reg.get('rights', [])}"
        bld_text = f"소유자: {bld['owner_name']}, 용도: {bld['building_purpose']}, 구조: {bld['building_structure']}, 승인일: {bld['approval_date']}"

        # 2. LLM 분석
        print(f"\n 케이스 ID: {case_id} ({address})")
        print("LLM 분석 중...")
        summary = compare_documents(reg_text, bld_text)
        print("요약 결과:")
        print(summary)

        # 3. 점수 계산
        score = calculate_risk(summary)
        print("위험 점수:", score["score"], f"({score['grade']})")
        print("사유:", ", ".join(score["reasons"]))

        # 4. Vector DB 저장
        store_full_analysis(case_id, summary, score, address)

if __name__ == "__main__":
    main()
