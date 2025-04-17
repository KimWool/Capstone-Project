# app/models/analysis_cases.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.session import Base

class AnalysisCase(Base):
    __tablename__ = "analysis_cases"
    
    analysis_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    main_address = Column(String(255), nullable=False)
    detail_address = Column(String(255), nullable=True)
    property_value = Column(Float, nullable=True)
    estimated_price = Column(Float, nullable=True)
    risk_summary = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    user = relationship("User", back_populates="analysis_cases")
