# app/services/sllm_model.py
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# └── 1) .env 설정 로드
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
if not env_path.is_file():
    raise FileNotFoundError(f".env 파일이 없습니다: {env_path}")
load_dotenv(env_path)

hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError("HF_TOKEN이 로드되지 않았습니다")

# └── 2) KoAlpaca 모델 로드
model_name = "beomi/KoAlpaca-llama-1-7b"
tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_name, token=hf_token)

# └── 2.5) 프롬프트 길이 초과 방지를 위한 유틸 함수
def truncate_prompt(prompt: str, max_length: int = 512) -> str:
    """
    주어진 프롬프트 문자열을 tokenizer 기준 최대 토큰 수 이하로 잘라냄.
    모델 입력 시 길이 초과로 인한 오류 또는 경고 방지를 위해 추가.
    """
    tokens = tokenizer(prompt, truncation=True, max_length=max_length, return_tensors="pt")
    return tokenizer.decode(tokens["input_ids"][0], skip_special_tokens=True)


# └── 3) 프라이프와 Chain 구성
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512, temperature=0.7, do_sample=True, repetition_penalty=1.1, device=-1)
llm = HuggingFacePipeline(pipeline=pipe)

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
risk_chain =risk_prompt | llm

def predict_risk(deposit: str, period: str, address: str) -> str:
    prompt = risk_prompt.format(deposit=deposit, period=period, address=address)
    return llm.invoke(truncate_prompt(prompt))


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
    return llm.invoke(truncate_prompt(prompt))


compare_prompt = PromptTemplate(
    input_variables=["registry", "building"],
    template="""
당신은 부동산 계약 방문 전문가입니다.

[등기부등본]
{registry}

[건축물대장]
{building}

아래 항목들과 같이 두 문서를 비교하여 불일치 유무를 확인하고, 불일치 시 이유를 설명해주세요:

1. 소유자명
2. 건물 용도
3. 구조 유형
4. 전용면적
5. 공유면적
6. 연면적
7. 준공년도
8. 근저당 설정 유무

결과를 표 형식으로 제공하세요. 예시:
항목 | 일치 유무 | 설명
------|------------|------
소유자명 | 일치 | 동일함
건물 용도 | 불일치 | 등기부는 "상업용", 건축물대장은 "주거용"

등기부_소유자: OOO  
건축물대장_소유자: OOO  
...
..."""
)
compare_chain = compare_prompt | llm

def compare_documents(registry: str, building: str) -> str:
    prompt = compare_prompt.format(registry=registry, building=building)
    return llm.invoke(truncate_prompt(prompt))


def parse_summary_to_meta(summary: str) -> dict:
    meta = {}
    meta["등기부_소유자"] = re.search(r"등기부\s*소유자[:：]?\s*(\S+)", summary)
    meta["건축물대장_소유자"] = re.search(r"건축물대장\s*소유자[:：]?\s*(\S+)", summary)
    meta["계약_임대인"] = re.search(r"계약\s*임대인[:：]?\s*(\S+)", summary)

    for k in list(meta):
        if isinstance(meta[k], re.Match):
            meta[k] = meta[k].group(1)
        else:
            meta[k] = None
    keywords = [
        "경매가시결정", "압류", "가압류", "가등기", "신택",
        "전세권_다수", "보증금_장기미반환", "전세권말소청권가등기",
        "임찰권등기명령", "이전세입자_전세권", "정상_전세권",
        "불복용도변경", "위반건축물", "건물용도"
    ]
    for key in keywords:
        if re.search(fr"{key}[:：]?\s*있음", summary):
            meta[key] = "있음"
        elif re.search(fr"{key}[:：]?\s*없음", summary):
            meta[key] = "없음"
        elif re.search(fr"{key}[:：]?\s*중대", summary):
            meta[key] = "중대"
        elif re.search(fr"{key}[:：]?\s*경미", summary):
            meta[key] = "경미"
        elif re.search(fr"{key}[:：]?\s*의심됩", summary):
            meta[key] = "의심됩"
    for k, p in {"채권최고액": r"채권최고액[:：]?\s*(\d+)", "기존_보증금": r"보증금[:：]?\s*(\d+)", "주택_시세": r"시세[:：]?\s*(\d+)"}.items():
        m = re.search(p, summary)
        if m:
            meta[k] = int(m.group(1))
    return meta