# app/services/vector_db.py
# ─────────────────────────────────────────
# Chroma VectorDB 연동 모듈

import os
import chromadb
from chromadb.utils import embedding_functions

# ┌─ 1) 임베디드(in-process) 모드로 Chroma Client 초기화
client = chromadb.Client()

# ┌─ 2) 임베딩 함수 설정
# OpenAI 키가 있으면 OpenAI 사용, 없으면 Sentence-Transformers 사용
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_key,
        model_name="text-embedding-ada-002"
    )
else:
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

# ┌─ 3) 컬렉션 생성 또는 가져오기
collection = client.get_or_create_collection(
    name="property_docs",
    embedding_function=embedding_function
)

# ┌─ 4) Upsert 함수
# docs: list of {id, text, metadata}
def upsert_property_docs(docs: list[dict]):
    ids = [d["id"] for d in docs]
    texts = [d["text"] for d in docs]
    metadatas = [d["metadata"] for d in docs]
    collection.upsert(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )

# ┌─ 5) Query 함수
# query_similar_documents: 텍스트 질의로 top-n 유사 문서 반환
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
