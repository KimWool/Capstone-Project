# app/schemas/building.py
from pydantic import BaseModel

class TitleInfoItem(BaseModel):
    platGbCd:  str  # 지번/관리구분코드
    bun:       str  # 지번 본번
    ji:        str  # 지번 부번
    bldNm:     str  # 건축물명
    ownerNm:   str  # 소유자명
    # … 필요에 따라 필드 추가
