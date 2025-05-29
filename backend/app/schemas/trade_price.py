# app/schemas/jeonse_price.py

from pydantic import BaseModel
from typing import Optional, List, Union

#공통 스키마
class TradePriceBase(BaseModel):
  sggCd: Optional[str]                 # 지역 코드
  umdNm: Optional[str]                 # 법정동 명칭
  jibun: Optional[str]                 # 지번
  dealYear: int                        # 계약 연도
  dealMonth: int                       # 계약 월
  dealDay: int                         # 계약 일
  dealAmount: Union[float, str]        # 거래 금액(만원)
  dealingGbn: Optional[str]            # 거래 유형(중개 및 직거래 여부)
  buildYear: Optional[Union[int, str]] # 건축 년도

#아파트
class AptTradePrice(TradePriceBase):
  aptNm: Optional[str]                        # 아파트명
  excluUseAr: Optional[Union[str, float]]     # 전용면적 (㎡)
  floor: Optional[Union[int, str]]            # 층수

# 오피스텔
class OffiTradePrice(TradePriceBase):
  sggNm: Optional[str]
  offiNm: Optional[str]
  excluUseAr: Optional[Union[str, float]]
  floor: Optional[Union[int, str]]

# 연립다세대
class RhTradePrice(TradePriceBase):
  mhouseNm: Optional[str]
  excluUseAr: Optional[Union[str, float]]
  floor: Optional[Union[int, str]]

# 단독/다가구
class ShTradePrice(TradePriceBase):
  houseType: Optional[str]
  totalFloorAr: Optional[Union[str, float]]