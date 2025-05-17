# backend/run_analysis.py
import json
from pathlib import Path
from app.services.sllm_model import extract_fields, get_match_flags, generate_explanations, compile_report
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

        # 위험 권리 유형 리스트
        risk_types = {"경매개시결정", "압류", "가압류", "가등기", "신탁", "전세권", "임차권"}

        rights_raw = reg.get("rights", [])
        if isinstance(rights_raw, list):
            if rights_raw and isinstance(rights_raw[0], dict):
                filtered = [r.get("type", "알수없음") for r in rights_raw if r.get("type") in risk_types]
                rights_str = ", ".join(filtered) if filtered else "없음"
            elif rights_raw and isinstance(rights_raw[0], str):
                filtered = [r for r in rights_raw if r in risk_types]
                rights_str = ", ".join(filtered) if filtered else "없음"
            else:
                rights_str = "없음"
        else:
            rights_str = "없음"

        amount = 0
        for r in reg.get("rights", []):
            if r["type"] == "근저당권":
                amount = r["amount"]
                break
        amount_str = f"{amount}" if amount > 0 else "없음"

        reg_text = (
            f"소유자: {reg['owner_name']}, 용도: {reg['building_purpose']}, 구조: {reg['building_structure']}, "
            f"전용면적: {reg['area_exclusive']}㎡, 공유면적: {reg['area_shared']}㎡, 연면적: {reg['area_total']}㎡, "
            f"준공년도: {reg['construction_year']}, 채권최고액: {amount_str}"
            f"권리: {rights_str}"
        )
        bld_text = (
            f"소유자: {bld['owner_name']}, 용도: {bld['building_purpose']}, 구조: {bld['building_structure']}, "
            f"전용면적: {bld['area_exclusive']}㎡, 공유면적: {bld['area_shared']}㎡, 연면적: {bld['area_total']}㎡, "
            f"준공년도: {bld['construction_year']}, 승인일자: {bld.get('approval_date', '없음')}"
        )

        # 3) 필드 추출 및 일치/불일치 플래그
        reg_fields = extract_fields(reg_text)
        bld_fields = extract_fields(bld_text)
        flags = get_match_flags(reg_fields, bld_fields)

        # 4) KoAlpaca로 설명 생성
        explanations = generate_explanations(flags, reg_fields, bld_fields)

        # 5) 비교 테이블 출력
        print("\n비교 요약 결과 (표):")
        print("항목           | 일치 유무 | 설명")
        print("--------------|----------|----------------")
        for k in flags:
            print(f"{k:<14} | {flags[k]:<8} | {explanations.get(k, '')}")

        # 6) GPT-4로 최종 보고서
        #report = compile_report(case_id, address, flags, explanations)
        #print("\n=== 최종 보고서 ===\n", report)

        # 7) 메타데이터 & 위험도 분석
        meta = {
            "등기부_소유자": reg_fields.get("소유자명"),
            "건축물대장_소유자": bld_fields.get("소유자명"),
            "채권최고액": reg.get("채권최고액"),
            "위험_권리_목록": reg_fields.get("위험 권리 목록", []),
            "건물 용도": reg_fields.get("건물 용도")
        }
        score = calculate_risk_score(meta)
        print("\n위험도 분석 결과")
        print("=" * 40)
        print(f"위험 점수 총합: {score['score']}점")
        print(f"위험도 원인: {score['reasons']}")
        print(f"등급: {score['grade']}")

        # 8) 분석 결과 저장
        """try:
            store_full_analysis(case_id, report, score, address)
        except Exception as e:
            print(f"저장 실패: {e}")"""

if __name__ == "__main__":
    main()
