from services.sllm_model import extract_metadata

raw_text = """
[등기부등본]
소유자: 김철수
근저당: 2억 (신한은행, 2021-01-01)
임대인: 김철수

[건축물대장]
용도: 다세대주택
구조: 철근콘크리트
준공일: 2001-03-01
"""

print("🧠 KoAlpaca + LangChain 테스트 중...")

summary = extract_metadata(raw_text)

print("✅ 요약 결과:")
print(summary)
