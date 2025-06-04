import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from pathlib import Path
import os
from dotenv import load_dotenv

# ── 1) 환경 설정 (프로젝트 루트 .env 로드)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_path = BASE_DIR / ".env"
if not env_path.is_file():
    raise FileNotFoundError(f".env 파일이 없습니다: {env_path}")
load_dotenv(env_path)

# ── 2) OpenAI API 키 로딩 및 임베딩 함수 설정
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다")

embedding_function = OpenAIEmbeddingFunction(api_key=api_key)

# ── 3) Chroma Client 초기화 및 컬렉션 준비
client = chromadb.Client()
collection = client.get_or_create_collection(
    name="property_docs",
    embedding_function=embedding_function
)

# ── 4) Upsert 함수
def upsert_property_docs(docs: list[dict]):
    ids = [d["id"] for d in docs]
    texts = [d["text"] for d in docs]
    metadatas = [d["metadata"] for d in docs]
    collection.upsert(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )

# ── 5) Query 함수
def query_similar_documents(query: str, n_results: int = 5) -> list[dict]:
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    ids = results["ids"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    return [
        {"id": iid, "metadata": meta, "distance": dist}
        for iid, meta, dist in zip(ids, metadatas, distances)
    ]

# ── 6) 분석 결과 저장 함수
def store_full_analysis(case_id: str, summary: str, score: dict, address: str):
    collection.upsert(
        documents=[summary],
        metadatas=[{
            "score": score["score"],
            "grade": score["grade"],
            "reasons": ", ".join(score.get("reasons", [])) if isinstance(score.get("reasons"), list) else "",
            "address": address
        }],
        ids=[f"analyzed-{case_id}"]
    )

# ── 7) 등기부 + 건축물대장 메타데이터 정리
def build_vector_docs(registry_list, building_list):
    docs = []
    for reg, bld in zip(registry_list, building_list):
        case_id = reg["case_id"]
        text = (
            f"[등기부등본] 소유자: {reg['owner_name']}, 용도: {reg['building_purpose']}, 구조: {reg['building_structure']}, "
            f"전용면적: {reg['area_exclusive']}, 공유면적: {reg['area_shared']}, 연면적: {reg['area_total']}, "
            f"준공년도: {reg['construction_year']}, 권리사항: {reg.get('rights', [])}. "
            f"[건축물대장] 소유자: {bld['owner_name']}, 용도: {bld['building_purpose']}, 구조: {bld['building_structure']}, "
            f"전용면적: {bld['area_exclusive']}, 공유면적: {bld['area_shared']}, 연면적: {bld['area_total']}, "
            f"준공년도: {bld['construction_year']}, 승인일: {bld['approval_date']}."
        )
        docs.append({
            "id": case_id,
            "text": text,
            "metadata": {"address": reg["address"]}
        })
    upsert_property_docs(docs)
