# app/api/endpoints/chatbot.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import or_
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import Keyword

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    source: str = "input"

@router.post("/chat")
async def chatbot_response(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    query = req.message.strip()

    if req.source == "button":
        # 정확히 일치하는 키워드만 조회
        stmt = select(Keyword).where(Keyword.keyword == query)
    else:
        # LIKE 검색 (부분 포함된 키워드까지 검색)
        stmt = select(Keyword).where(Keyword.keyword.ilike(f"%{query}%"))

    result = await db.execute(stmt)
    keyword_entry = result.scalars().first()

    if keyword_entry:
        return {
            "keyword": keyword_entry.keyword,
            "answer": keyword_entry.description
        }

    return {
        "keyword": None,
        "answer": "해당 키워드와 관련된 정보를 찾을 수 없습니다."
    }
