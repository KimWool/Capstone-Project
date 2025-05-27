from fastapi import APIRouter
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.clients.registry_api import get_registry_info
from app.clients.building_api import get_building_title_info
#from app.services.sllm_model import extract_metadata
#from app.services.vector_db import store_metadata

router = APIRouter()

@router.post("/analyze/", response_model=AnalyzeResponse)
def analyze_property(data: AnalyzeRequest):
    registry_data = get_registry_info(data.address)
    building_data = get_building_title_info(data.address)

    raw_text = f"""
    [등기부등본]
    소유자: {registry_data['owner']}
    근저당: {registry_data['mortgage']}
    임대인 정보: {registry_data['lessor']}

    [건축물대장]
    건축물 용도: {building_data['usage']}
    준공일: {building_data['completion']}
    구조: {building_data['structure']}
    """

    summary = extract_metadata(raw_text)
    #store_metadata(data.address, summary)

    return AnalyzeResponse(address=data.address, summary=summary)
