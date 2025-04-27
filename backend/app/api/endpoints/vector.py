from fastapi import APIRouter
from app.services.vector_db import query_similar_documents

router = APIRouter(prefix="/vector", tags=["VectorDB"])

@router.get("/search")
async def vector_search(q: str, top: int = 5):
    """
    질의(q)에 대해 상위(top)개의 유사 문서 반환
    """
    results = query_similar_documents(q, top)
    return {"query": q, "results": results}
