import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Lead, ChatMessage
from app.ai.customer_agent import get_agent_reply

router = APIRouter()


class ChatIn(BaseModel):
    lead_id: uuid.UUID
    message: str


class ChatOut(BaseModel):
    reply: str
    collected_fields: dict


@router.post("", response_model=ChatOut)
def send_message(payload: ChatIn, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == payload.lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    db.add(ChatMessage(lead_id=lead.id, role="user", content=payload.message))
    db.commit()

    history = (
        db.query(ChatMessage)
        .filter(ChatMessage.lead_id == lead.id)
        .order_by(ChatMessage.created_at)
        .all()
    )
    history_pairs = [{"role": m.role, "content": m.content} for m in history]

    reply, collected = get_agent_reply(history_pairs, lead)

    db.add(ChatMessage(lead_id=lead.id, role="assistant", content=reply))

    # Обновляем поля лида по мере того, как AI их собирает
    for field, value in collected.items():
        if hasattr(lead, field) and value:
            setattr(lead, field, value)
    if lead.status == "new_lead" and collected:
        lead.status = "contacted"

    db.commit()
    return ChatOut(reply=reply, collected_fields=collected)


@router.get("/{lead_id}/history", response_model=List[dict])
def get_history(lead_id: uuid.UUID, db: Session = Depends(get_db)):
    history = (
        db.query(ChatMessage)
        .filter(ChatMessage.lead_id == lead_id)
        .order_by(ChatMessage.created_at)
        .all()
    )
    return [{"role": m.role, "content": m.content} for m in history]
