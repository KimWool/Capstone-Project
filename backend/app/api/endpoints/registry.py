# app/api/endpoints/registry.py
from fastapi import APIRouter, HTTPException
from app.clients.registry_api import fetch_registry
from app.schemas.registry import RegistryData

router = APIRouter(prefix="/registry", tags=["등기부등본"])

@router.get("/{jibun}", response_model=RegistryData,
            summary="등기부등본 조회 (jibun)")
async def get_registry(jibun: str):
    data = await fetch_registry(jibun)
    if not data:
        raise HTTPException(status_code=404, detail="데이터 없음")
    return RegistryData(**data)
