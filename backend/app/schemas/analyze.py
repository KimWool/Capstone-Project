from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    address: str

class AnalyzeResponse(BaseModel):
    address: str
    summary: str
