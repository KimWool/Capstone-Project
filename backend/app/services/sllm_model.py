import os
import sys
import re
import json
from pathlib import Path
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from openai import OpenAI
from typing import Dict

# ── 1) 환경 설정 (프로젝트 루트 .env 로드)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"
if not env_path.is_file():
    raise FileNotFoundError(f".env 파일이 없습니다: {env_path}")
load_dotenv(env_path)

# PYTHONPATH에 프로젝트 루트 추가
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# ── 2) KoAlpaca sLLM 설정
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError("HF_TOKEN이 로드되지 않았습니다")
model_name = "beomi/KoAlpaca-llama-1-7b"
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    token=hf_token,
    use_fast=False,
    cache_dir="/mnt/model_cache"
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    token=hf_token,
    cache_dir="E:/huggingface_cache"
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=128,
    temperature=0.7,
    do_sample=True,
    repetition_penalty=1.1,
    device=-1
)
llm = HuggingFacePipeline(pipeline=pipe)

# ── 3) OpenAI GPT-4 설정
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다")
openai_client = OpenAI(api_key=api_key)

# ── 4) 필드 추출 정규표현식 패턴
patterns = {
    "소유자명":        r"소유자[:：]?\s*([^,]+)",
    "건물 용도":      r"용도[:：]?\s*([^,]+)",
    "구조 유형":      r"구조[:：]?\s*([^,]+)",
    "전용면적":       r"전용면적[:：]?\s*([^,]+)",
    "공유면적":       r"공유면적[:：]?\s*([^,]+)",
    "연면적":         r"연면적[:：]?\s*([^,]+)",
    "준공년도":       r"준공년도[:：]?\s*([^,]+)",
    "근저당 설정 유무": r"채권최고액[:：]?(\d+|없음)",
    "위험 권리 존재 여부": r"권리[:：]?\s*([^,]+)"
}

# ── 5) 텍스트에서 필드 값 추출
def extract_fields(text: str) -> dict:
    fields = {}
    risk_types = {"경매개시결정", "압류", "가압류", "가등기", "신탁", "전세권", "임차권"}
    for name, pat in patterns.items():
        m = re.search(pat, text)
        value = m.group(1).strip() if m else None
        if name == "위험 권리 존재 여부":
            if value:
                rights = [s.strip() for s in re.split(r"[,\s]+", value)]
                filtered = [r for r in rights if r in risk_types]
                fields["위험 권리 목록"] = filtered
            else:
                fields["위험 권리 목록"] = []
        elif value is not None:
            fields[name] = value
    return fields

# ── 6) GPT-4로 플래그(일치/불일치) 판정
def compare_flags_gpt4(reg: dict, bld: dict) -> Dict[str, str]:
    prompt = f"""
다음은 두 개의 문서에서 추출된 필드 값입니다.

[등기부등본]
{json.dumps(reg, ensure_ascii=False, indent=2)}

[건축물대장]
{json.dumps(bld, ensure_ascii=False, indent=2)}

다음 형식을 그대로 유지하여, JSON만 응답하세요. 설명이나 문장은 포함하지 마세요.
반드시 아래 예시처럼 응답하세요:
{{
  "소유자명": "불일치",
  "건물 용도": "일치"
}}

필드 목록: {', '.join(patterns.keys())}

출력 예시:
{{
  "소유자명": "불일치",
  "건물 용도": "일치"
}}
"""
    resp = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = resp.choices[0].message.content.strip()
    
    if not content:
        raise ValueError("❌ GPT 응답이 비어 있습니다.")

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("❌ GPT 응답이 JSON이 아님:", content)
        raise

# ── 7) KoAlpaca로 설명 생성 (기존 코드 재사용)
def generate_explanations(flags: Dict[str, str], reg: dict, bld: dict) -> Dict[str, str]:
    lines = []
    for k, flag in flags.items():
        rv = reg.get(k) or "없음"
        bv = bld.get(k) or "없음"
        lines.append(f"{k}: flag={flag}, reg='{rv}', bld='{bv}'")
    prompt = (
        "아래는 비교 대상 항목의 판정 결과와 원본 값입니다.\n"
        "각 항목마다 ‘동일함’ 또는 ‘왜 다른지’ 한 줄 설명만 생성하세요.\n\n" + "\n".join(lines)
    )
    raw = llm.invoke(prompt)
    explanations = {}
    for line in str(raw).splitlines():
        if ':' in line:
            key, desc = line.split(':', 1)
            explanations[key.strip()] = desc.strip()
    return explanations

# ── 8) GPT-4로 최종 보고서 컴파일
def compile_report(case_id: str, address: str, flags: Dict[str, str], explanations: Dict[str, str]) -> str:
    table = "\n".join([
        "항목 | 일치 유무 | 설명",
        "------|---------|------",
        *[f"{k} | {flags[k]} | {explanations.get(k, '')}" for k in flags]
    ])
    prompt = f"""
다음은 전세계약 비교 결과입니다.\n\n케이스: {case_id} ({address})\n\n{table}\n\n이 표를 바탕으로 요약 보고서를 한 단락으로 작성해주세요.
"""
    resp = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7
    )
    return resp.choices[0].message.content

# ── 9) 엔트리 포인트 예시
if __name__ == '__main__':
    # 예시 사용 흐름
    sample_reg = extract_fields("[등기부등본] 소유자: 김철수, 용도: 주거용")
    sample_bld = extract_fields("[건축물대장] 소유자: 고예지, 용도: 주거용")
    flags = compare_flags_gpt4(sample_reg, sample_bld)
    explanations = generate_explanations(flags, sample_reg, sample_bld)
    report = compile_report("case_001", "서울시 강남구", flags, explanations)
    print(report)
