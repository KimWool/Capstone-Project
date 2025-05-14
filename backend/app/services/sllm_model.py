import os
import re
import json
from pathlib import Path
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate

# └── 1) .env 설정 로드
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
if not env_path.is_file():
    raise FileNotFoundError(f".env 파일이 없습니다: {env_path}")
load_dotenv(env_path)

hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError("HF_TOKEN이 로드되지 않았습니다")

# └── 2) KoAlpaca 모델 로드 및 LLM 파이프라인 구성
model_name = "beomi/KoAlpaca-llama-1-7b"
tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_name, token=hf_token)
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=64,
    temperature=0.7,
    do_sample=True,
    repetition_penalty=1.1,
    device=-1
)
llm = HuggingFacePipeline(pipeline=pipe)

# └── 3) 전세계약 위험도 예측
risk_prompt = PromptTemplate(
    input_variables=["deposit", "period", "address"],
    template="""
당신은 부동산 전문가 AI입니다. 아래 정보를 바탕으로 전세계약의 사기 위험 가능성을 판단하세요.

전세보주금: {deposit}원
계약기간: {period}개월
건물 주소: {address}

예측 결과:
"""
)
risk_chain = risk_prompt | llm

def predict_risk(deposit: str, period: str, address: str) -> str:
    prompt = risk_prompt.format(deposit=deposit, period=period, address=address)
    return llm.invoke(prompt)

# └── 4) 메타데이터 요약
metadata_prompt = PromptTemplate(
    input_variables=["raw_text"],
    template="""
다음은 전세계약과 관련된 등기부등본 및 건축물대장 데이터입니다.
해당 데이터를 기반으로 의미 있는 헌정 정보만 요약해 주세요.

데이터:
{raw_text}

요약 결과:
"""
)
metadata_chain = metadata_prompt | llm

def extract_metadata(raw_text: str) -> str:
    prompt = metadata_prompt.format(raw_text=raw_text)
    return llm.invoke(prompt)

# └── 5) 정규식 기반 필드 추출

def extract_fields(text: str) -> dict:
    """
    등기부등본/건축물대장 텍스트에서 주요 필드를 뽑아 dict으로 반환
    """
    patterns = {
        "소유자명":        r"소유자[:：]?\s*([^,]+)",
        "건물 용도":      r"용도[:：]?\s*([^,]+)",
        "구조 유형":      r"구조[:：]?\s*([^,]+)",
        "전용면적":       r"전용면적[:：]?\s*([^,]+)",
        "공유면적":       r"공유면적[:：]?\s*([^,]+)",
        "연면적":         r"연면적[:：]?\s*([^,]+)",
        "준공년도":       r"준공년도[:：]?\s*([^,]+)",
        "근저당 설정 유무": r"채권최고액[:：]?(\d+|없음)"
    }
    fields = {}
    for name, pat in patterns.items():
        m = re.search(pat, text)
        fields[name] = m.group(1).strip() if m else None
    return fields

# └── 6) LLM 판정을 이용한 하이브리드 비교

def compare_documents_llm_decision(registry: str, building: str) -> dict:
    """
    LLM에게 few-shot + temperature=0 으로 일치/불일치 판정만 JSON으로 요청
    """
    reg = extract_fields(registry)
    bld = extract_fields(building)
    items = ["소유자명","건물 용도","구조 유형","전용면적","공유면적","연면적","준공년도","근저당 설정 유무"]

    # few-shot prompt
    prompt = (
        "다음은 등기부(reg)와 건축물대장(bld)에서 추출된 필드 값입니다.\n"
        "문자열을 정확히 비교하여, 같으면 \"일치\", 다르면 \"불일치\"로 JSON으로 반환하세요.\n"
        "예시: { \"소유자명\": \"불일치\", \"전용면적\": \"일치\" }\n\n값:\n"
    )
    for key in items:
        prompt += f"{key}: reg='{reg.get(key) or ''}', bld='{bld.get(key) or ''}'\n"
    prompt += "\n결과:"

    # 온도 0으로 호출
    resp = llm.invoke(prompt, params={"temperature":0, "max_new_tokens":128})
    text = resp if isinstance(resp, str) else resp.get("text", "")
    # JSON 파싱
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        decision = {}
        for key in items:
            m = re.search(fr'"{key}"\s*:\s*"(일치|불일치)"', text)
            decision[key] = m.group(1) if m else "불일치"
        return decision


def compare_documents(registry: str, building: str) -> str:
    """
    Hybrid: LLM이 판정, Python이 설명+표 포맷팅
    """
    reg = extract_fields(registry)
    bld = extract_fields(building)
    decision = compare_documents_llm_decision(registry, building)

    header = [
        "항목 | 일치 유무 | 설명",
        "------|------------|------"
    ]
    rows = []
    for key in ["소유자명","건물 용도","구조 유형","전용면적","공유면적","연면적","준공년도","근저당 설정 유무"]:
        flag = decision.get(key, "불일치")
        if flag == "일치":
            desc = "동일함"
        else:
            rv = reg.get(key) or "없음"
            bv = bld.get(key) or "없음"
            desc = f'등기부는 "{rv}", 건축물대장은 "{bv}"'
        rows.append(f"{key} | {flag} | {desc}")

    table = "\n".join(header + rows)
    meta_lines = [
        f"등기부_소유자: {reg.get('소유자명') or '미상'}",
        f"건축물대장_소유자: {bld.get('소유자명') or '미상'}",
        "계약_임대인: 미상",
        f"채권최고액: {reg.get('근저당 설정 유무') or 0}"
    ]
    return table + "\n\n" + "\n".join(meta_lines)


def parse_summary_to_meta(summary: str) -> dict:
    """
    compare_documents 출력의 메타데이터 부분을 파싱해 dict으로 반환
    """
    meta = {}
    for key in ["등기부_소유자", "건축물대장_소유자", "계약_임대인", "채권최고액"]:
        m = re.search(fr"{key}[:：]?\s*(\S+)", summary)
        meta[key] = m.group(1) if m else None
    return meta
