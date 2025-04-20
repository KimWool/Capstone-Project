# app/schemas/registry.py
from pydantic import BaseModel

class RegistryData(BaseModel):
    ownerName:    str
    regDate:      str
    propertyKind: str
    # …응답 JSON 구조에 맞춰 추가 정의
