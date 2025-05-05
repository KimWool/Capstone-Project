# app/schemas/building.py
from pydantic import BaseModel
from typing import Optional

class TitleInfoItem(BaseModel):
    platGbCd: str              # 지번/관리구분코드
    bun: str                   # 지번 본번
    ji: str                    # 지번 부번
    bldNm: Optional[str]       # 건축물명
    mainPurpsCdNm: Optional[str]   # 주요 용도
    mainpurpsArea: Optional[str]   # 용도별 면적 (㎡)
    ownerNm: Optional[str]     # 소유자명
    strctCdNm: Optional[str]   # 구조코드명
    totArea: Optional[float]   # 연면적 (전체 바닥 면적)
    archArea: Optional[float]  # 건축면적 (건물 외곽 기준 면적)
    bcRat: Optional[float]     # 건폐율 (%)
    vlRat: Optional[float]     # 용적률 (%)
    grndFlrCnt: Optional[int]  # 지상 층수
    ugrndFlrCnt: Optional[int] # 지하 층수
    useAprDay: Optional[str]   # 사용 승인일 (YYYYMMDD 형식)
    platPlc: Optional[str]     # 대지 위치 (도로명 주소 또는 지번 주소)
    mgmBldrgstPk: Optional[str]# 관리건축물대장PK (건물 고유 식별자)
    # … 필요에 따라 필드 추가
