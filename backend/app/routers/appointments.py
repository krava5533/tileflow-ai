import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Lead, Appointment
from app.services.calendar_service import (
    create_measurement_event,
    cancel_measurement_event,
    list_busy_slots,
)

router = APIRouter()


class AppointmentIn(BaseModel):
    lead_id: uuid.UUID
    scheduled_for: datetime


@router.post("")
def book_appointment(payload: AppointmentIn, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == payload.lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    customer = lead.customer

    event_id = create_measurement_event(
        scheduled_for=payload.scheduled_for,
        customer_name=customer.name if customer else "",
        customer_address=customer.address if customer else "",
        customer_phone=customer.phone if customer else "",
        lead_id=str(lead.id),
    )
    # event_id is None if Google Calendar isn't configured yet -- booking
    # still works locally, it just won't show up on a real calendar until it is.

    appointment = Appointment(
        lead_id=lead.id,
        scheduled_for=payload.scheduled_for,
        google_calendar_event_id=event_id,
    )
    db.add(appointment)
    lead.status = "estimate_scheduled"
    db.commit()
    db.refresh(appointment)

    return {
        "appointment_id": str(appointment.id),
        "scheduled_for": appointment.scheduled_for.isoformat(),
        "status": lead.status,
        "calendar_connected": event_id is not None,
    }


@router.delete("/{appointment_id}")
def cancel_appointment(appointment_id: uuid.UUID, db: Session = Depends(get_db)):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appt.google_calendar_event_id:
        cancel_measurement_event(appt.google_calendar_event_id)

    db.delete(appt)
    db.commit()
    return {"cancelled": True}


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


@router.get("/availability/busy")
def get_busy_slots(days_ahead: int = 7):
    """Returns busy ranges on the business calendar for the next N days, so
    the booking UI can grey out unavailable times. Empty list if Calendar
    isn't connected yet."""
    start = datetime.utcnow()
    end = start + timedelta(days=days_ahead)
    return {"busy": list_busy_slots(start, end)}
