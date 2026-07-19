import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Lead, Appointment

router = APIRouter()


class AppointmentIn(BaseModel):
    lead_id: uuid.UUID
    scheduled_for: datetime


@router.post("")
def book_appointment(payload: AppointmentIn, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == payload.lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    appointment = Appointment(lead_id=lead.id, scheduled_for=payload.scheduled_for)
    db.add(appointment)
    lead.status = "estimate_scheduled"
    db.commit()
    db.refresh(appointment)

    # Google Calendar integration hooks in here (Phase 2):
    #   - create event via Calendar API, store event id
    #   - send SMS/email reminder 24h before via a scheduled job

    return {
        "appointment_id": str(appointment.id),
        "scheduled_for": appointment.scheduled_for.isoformat(),
        "status": lead.status,
    }


@router.get("/{lead_id}")
def get_appointments(lead_id: uuid.UUID, db: Session = Depends(get_db)):
    appts = (
        db.query(Appointment)
        .filter(Appointment.lead_id == lead_id)
        .order_by(Appointment.scheduled_for)
        .all()
    )
    return [
        {"id": str(a.id), "scheduled_for": a.scheduled_for.isoformat()}
        for a in appts
    ]
