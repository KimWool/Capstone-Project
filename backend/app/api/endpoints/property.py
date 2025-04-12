from fastapi import APIRouter, Depends
from typing import Any
# from app.services.external_api import fetch_registry_data, fetch_building_data
# from app.db.session import SessionLocal

router = APIRouter()

@router.get("/")
def get_properties() -> Any:
    # DB에서 매물 정보를 조회하거나, 외부 API 호출 로직 등을 실행
    return {"message": "list of properties"}

@router.post("/")
def create_property(address: str) -> Any:
    # 외부 API 등기부등본, 건축물대장 데이터 호출
    # registry_data = fetch_registry_data(address)
    # building_data = fetch_building_data(address)
    
    # DB에 저장 로직 (예시)
    # db = SessionLocal()
    # property_model = Property(address=address, registry_data=registry_data, ...)
    # db.add(property_model)
    # db.commit()
    # db.refresh(property_model)
    
    return {"message": f"Property created for address: {address}"}
