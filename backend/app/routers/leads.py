import uuid
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Lead, Customer

router = APIRouter()


class CustomerIn(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None


class LeadCreate(BaseModel):
    customer: CustomerIn
    project_type: Optional[str] = "other"
    room_size_sqft: Optional[float] = None
    tile_type: Optional[str] = None
    budget_range: Optional[str] = None
    timeline: Optional[str] = None
    source: Optional[str] = None


class LeadStatusUpdate(BaseModel):
    status: str


class LeadOut(BaseModel):
    id: uuid.UUID
    status: str
    project_type: str
    customer_name: str
    customer_phone: str

    class Config:
        from_attributes = True


VALID_STATUSES = {
    "new_lead", "contacted", "estimate_scheduled",
    "estimate_sent", "approved", "completed",
}


@router.post("", response_model=dict)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)):
    """Создаётся, когда клиент проходит форму / AI-чат на сайте."""
    customer = Customer(**payload.customer.dict())
    db.add(customer)
    db.flush()

    lead = Lead(
        customer_id=customer.id,
        project_type=payload.project_type,
        room_size_sqft=payload.room_size_sqft,
        tile_type=payload.tile_type,
        budget_range=payload.budget_range,
        timeline=payload.timeline,
        source=payload.source,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return {"lead_id": str(lead.id), "status": lead.status}


@router.get("", response_model=List[dict])
def list_leads(status: Optional[str] = None, db: Session = Depends(get_db)):
    """Для CRM Dashboard владельца — список лидов, опционально фильтр по статусу."""
    query = db.query(Lead)
    if status:
        query = query.filter(Lead.status == status)
    leads = query.order_by(Lead.created_at.desc()).all()
    return [
        {
            "id": str(l.id),
            "status": l.status,
            "project_type": l.project_type,
            "customer_name": l.customer.name if l.customer else None,
            "customer_phone": l.customer.phone if l.customer else None,
            "created_at": l.created_at.isoformat() if l.created_at else None,
        }
        for l in leads
    ]


@router.get("/{lead_id}")
def get_lead(lead_id: uuid.UUID, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {
        "id": str(lead.id),
        "status": lead.status,
        "project_type": lead.project_type,
        "room_size_sqft": lead.room_size_sqft,
        "tile_type": lead.tile_type,
        "budget_range": lead.budget_range,
        "timeline": lead.timeline,
        "notes": lead.notes,
        "customer": {
            "name": lead.customer.name,
            "phone": lead.customer.phone,
            "email": lead.customer.email,
            "address": lead.customer.address,
        } if lead.customer else None,
    }


@router.patch("/{lead_id}/status")
def update_status(lead_id: uuid.UUID, payload: LeadStatusUpdate, db: Session = Depends(get_db)):
    if payload.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {VALID_STATUSES}")
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.status = payload.status
    db.commit()
    return {"lead_id": str(lead.id), "status": lead.status}
