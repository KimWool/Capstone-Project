import json
from app.services.sllm_model import compare_documents, parse_summary_to_meta
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

    if len(registry_data) != len(building_data):
        print("데이터 수가 일치하지 않습니다.")
        return

    for reg, bld in zip(registry_data, building_data):
        case_id = reg["case_id"]
        address = reg["address"]

        # 1. 텍스트 요약 구성 (길이 초과 방지)
        reg_text = f"소유자: {reg['owner_name']}, 용도: {reg['building_purpose']}, 구조: {reg['building_structure']}, 준공년도: {reg['construction_year']}"
        bld_text = f"소유자: {bld['owner_name']}, 용도: {bld['building_purpose']}, 구조: {bld['building_structure']}, 준공년도: {bld['construction_year']}"

        print(f"\n케이스 ID: {case_id} ({address})")
        print("🔍 LLM 비교 분석 중...")

        # 2. LLM 분석
        summary = compare_documents(reg_text, bld_text)

        # LangChain invoke 결과가 dict일 경우 text 필드만 추출
        if isinstance(summary, dict) and "text" in summary:
            summary_text = summary["text"]
        else:
            summary_text = str(summary)

        lines = summary_text.strip().splitlines()


        # 전체 결과 로그 출력
        print("\n비교 요약 전체 결과:\n", summary)

        # 3. 표 출력
        print("비교 요약 결과 (표):")
        print("=" * 40)
        lines = summary_text.strip().splitlines()
        inside_table = False
        for line in lines:
            if "항목" in line and "설명" in line:
                inside_table = True
                print(f"{'항목':<12} | {'일치 유무':<10} | 설명")
                print("-" * 40)
                continue
            if inside_table:
                if not line.strip():
                    break
                parts = line.split("|")
                if len(parts) == 3:
                    항목 = parts[0].strip()
                    일치 = parts[1].strip()
                    설명 = parts[2].strip()
                    print(f"{항목:<12} | {일치:<10} | {설명}")

        # 4. 메타데이터 추출
        meta = parse_summary_to_meta(summary_text)
        print("\n메타데이터 추출 결과:")
        for k, v in meta.items():
            print(f"{k}: {v}")

        # 5. 위험도 점수 계산
        score = calculate_risk_score(meta)
        print("\n위험도 분석 결과")
        print("=" * 40)
        print(f"위험 점수 총합: {score['score']}점")
        print(f"등급: {score['level']}")

        # 6. 분석 결과 벡터 DB 저장 (OpenAI API 사용 가능성 있음)
        if score:
            try:
                store_full_analysis(case_id, summary_text, score, address)
            except Exception as e:
                print(f"저장 실패: {e}")

if __name__ == "__main__":
    main()
