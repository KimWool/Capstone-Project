### sllm_model.py: 메타데이터 추출용 sLLM 분석기
from transformers import pipeline

classifier = pipeline("text-classification", model="monologg/koelectra-small-v3-discriminator")

# 실제 사용 시에는 Few-shot Prompting이나 custom 모델 적용 추천
def analyze_documents(registry_text, building_text):
    combined_text = registry_text + "\n" + building_text
    # 프롬프트 방식 또는 파싱기 적용
    meta = {
        "근저당권": "있음" if "근저당" in combined_text else "없음",
        "전세권": "없음" if "전세권 없음" in combined_text else "있음",
        "소유자": "홍길동"  # 추후 LLM이 자동 추출하도록 개선
    }
    return meta