# app/schemas/transaction_price.py

from pydantic import BaseModel
from typing import Optional, List, Union

#공통 스키마
class TransactionPriceBase(BaseModel):
  dealYear: int                        # 계약 연도
  dealMonth: int                       # 계약 월
  dealDay: int                         # 계약 일
  deposit: Union[float, str]           # 보증금 (만원)
  monthlyRent: Union[float, str]       # 월세 (만원)
  contractTerm: Optional[str]          # 계약 기간
  contractType: Optional[str]          # 계약 유형
  useRRRight: Optional[str]            # 갱신요구권 사용 여부
  preDeposit: Optional[str]            # 종전 보증금
  preMonthlyRent: Optional[str]        # 종전 월세

#아파트
class AptTransactionPrice(TransactionPriceBase):
  sggCd: Optional[str]                        # 지역(시군구) 코드
  umdNm: Optional[str]                        # 법정동 명칭
  aptNm: Optional[str]                        # 아파트명
  jibun: Optional[str]                        # 지번
  excluUseAr: Optional[Union[str, float]]     # 전용면적 (㎡)
  floor: Optional[Union[int, str]]            # 층수
  buildYear: Optional[Union[int, str]]        # 건축년도

# 오피스텔
class OffiTransactionPrice(TransactionPriceBase):
  sggCd: Optional[str]
  sggNm: Optional[str]
  umdNm: Optional[str]
  jibun: Optional[str]
  offiNm: Optional[str]
  excluUseAr: Optional[Union[str, float]]
  floor: Optional[Union[int, str]]
  buildYear: Optional[Union[int, str]]


# 연립다세대
class RhTransactionPrice(TransactionPriceBase):
  sggCd: Optional[str]
  umdNm: Optional[str]
  mhouseNm: Optional[str]
  jibun: Optional[str]
  excluUseAr: Optional[Union[str, float]]
  floor: Optional[Union[int, str]]
  buildYear: Optional[Union[int, str]]


# 단독/다가구
class ShTransactionPrice(TransactionPriceBase):
  sggCd: Optional[str]
  umdNm: Optional[str]
  totalFloorAr: Optional[Union[str, float]]
  buildYear: Optional[Union[int, str]]
