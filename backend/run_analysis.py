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

        # 1) 헤더 출력
        print(f"\n케이스 ID: {case_id} ({address})")
        print("🔍 문서 비교 분석 중...")

        # 2) 비교용 텍스트 구성
        reg_text = (
            f"소유자: {reg['owner_name']}, 용도: {reg['building_purpose']}, 구조: {reg['building_structure']}, "
            f"전용면적: {reg['area_exclusive']}㎡, 공유면적: {reg['area_shared']}㎡, 연면적: {reg['area_total']}㎡, "
            f"준공년도: {reg['construction_year']}, 채권최고액: {reg.get('채권최고액', '없음')}, "
            f"권리: {', '.join(reg.get('rights', [])) or '없음'}"
        )
        bld_text = (
            f"소유자: {bld['owner_name']}, 용도: {bld['building_purpose']}, 구조: {bld['building_structure']}, "
            f"전용면적: {bld['area_exclusive']}㎡, 공유면적: {bld['area_shared']}㎡, 연면적: {bld['area_total']}㎡, "
            f"준공년도: {bld['construction_year']}, 승인일자: {bld.get('approval_date', '없음')}"
        )

        # 3) 하이브리드 비교 호출
        summary_text = compare_documents(reg_text, bld_text)

        # 4) 결과 출력
        print("\n비교 요약 결과 (표):")
        print(summary_text)

        # 5) 메타데이터 추출
        meta = parse_summary_to_meta(summary_text)
        print("\n메타데이터 추출 결과:")
        for k, v in meta.items():
            print(f"{k}: {v}")

        # 6) 위험도 점수 계산
        score = calculate_risk_score(meta)
        print("\n위험도 분석 결과")
        print("=" * 40)
        print(f"위험 점수 총합: {score['score']}점")
        print(f"등급: {score['grade']}")

        # 7) 벡터 DB 저장
        try:
            store_full_analysis(case_id, summary_text, score, address)
        except Exception as e:
            print(f"저장 실패: {e}")


if __name__ == "__main__":
    main()
