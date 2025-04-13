# backend/app/api/endpoints/properties.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.db.session import SessionLocal
from app.models.property import Property

router = APIRouter()

# Pydantic 모델
class PropertyCreate(BaseModel):
    address: str
    detail_address: str = None
    property_value: float = None
    estimated_price: float = None
    risk_summary: str = None

class PropertyUpdate(BaseModel):
    detail_address: str = None
    property_value: float = None
    estimated_price: float = None
    risk_summary: str = None

class PropertyOut(BaseModel):
    property_id: int
    address: str
    detail_address: str = None
    property_value: float = None
    estimated_price: float = None
    risk_summary: str = None

    class Config:
        orm_mode = True

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create property
@router.post("/", response_model=PropertyOut)
def create_property(property: PropertyCreate, db: Session = Depends(get_db)):
    new_property = Property(**property.dict())
    db.add(new_property)
    db.commit()
    db.refresh(new_property)
    return new_property

# Read all properties
@router.get("/", response_model=List[PropertyOut])
def read_properties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    props = db.query(Property).offset(skip).limit(limit).all()
    return props

# Read property by ID
@router.get("/{property_id}", response_model=PropertyOut)
def read_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop

# Update property
@router.put("/{property_id}", response_model=PropertyOut)
def update_property(property_id: int, prop_update: PropertyUpdate, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.property_id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    update_data = prop_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(prop, key, value)
    db.commit()
    db.refresh(prop)
    return prop
