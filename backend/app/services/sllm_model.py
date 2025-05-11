# services/sllm_model.py

import os
from pathlib import Path
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# ─── 1) .env 파일 경로 지정 & 로드 ───────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent   # .../backend/app/services → .../backend
env_path = BASE_DIR / ".env"
if not env_path.is_file():
    raise FileNotFoundError(f".env 파일이 없습니다: {env_path}")
load_dotenv(env_path)

hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError(f"HF_TOKEN이 .env에서 로드되지 않았습니다: {env_path}")

# ─── 2) 모델명 설정 ───────────────────────────────────────────
model_name = "beomi/KoAlpaca-llama-1-7b"

# ─── 3) 토크나이저 & 모델 로드 ─────────────────────────────────
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    token=hf_token,
    use_fast=False     # 느린 SP 토크나이저만 쓰도록 강제
)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    token=hf_token
)

# ─── 4) 파이프라인 구성 ───────────────────────────────────────
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=64,
    temperature=0.7,
    do_sample=True,
    repetition_penalty=1.1,
    device=-1         # CPU
)
llm = HuggingFacePipeline(pipeline=pipe)

# ─── 5) 위험도 예측용 Chain ───────────────────────────────────
risk_prompt = PromptTemplate(
    input_variables=["deposit", "period", "address"],
    template="""
당신은 부동산 전문가 AI입니다. 아래 정보를 바탕으로 전세계약의 사기 위험 가능성을 판단하세요.

전세보증금: {deposit}원
계약기간: {period}개월
건물 주소: {address}

예측 결과:
"""
)
risk_chain = LLMChain(prompt=risk_prompt, llm=llm)

def predict_risk(deposit: str, period: str, address: str) -> str:
    return risk_chain.run({
        "deposit": deposit,
        "period": period,
        "address": address
    })

# ─── 6) 메타데이터 요약용 Chain ────────────────────────────────
metadata_prompt = PromptTemplate(
    input_variables=["raw_text"],
    template="""
다음은 전세계약과 관련된 등기부등본 및 건축물대장 데이터입니다.
해당 데이터를 기반으로 의미 있는 핵심 정보만 요약해 주세요.

데이터:
{raw_text}

요약 결과:
"""
)
metadata_chain = LLMChain(prompt=metadata_prompt, llm=llm)

def extract_metadata(raw_text: str) -> str:
    return metadata_chain.run({"raw_text": raw_text})

# ─── 7) 불일치 항목 추출용 Chain ─────────────────────────────
compare_prompt = PromptTemplate(
    input_variables=["registry", "building"],
    template="""
당신은 부동산 계약 분석 전문가입니다.

[등기부등본]
{registry}

[건축물대장]
{building}

두 문서를 비교하여 다음 항목들의 불일치 여부를 판단하고, 사기 위험 요소가 있는 항목을 표 형태로 정리해주세요.

항목:
1. 소유자와 임대인 일치 여부
2. 근저당 설정 여부 (보증금보다 높을 경우)
3. 건축물 용도 (주거용/비주거용 여부)
4. 구조 안전성 (오래된 건물, 철근 미사용 등)

결과:
"""
)

compare_chain = LLMChain(prompt=compare_prompt, llm=llm)

def compare_documents(registry: str, building: str) -> str:
    return compare_chain.run({"registry": registry, "building": building})