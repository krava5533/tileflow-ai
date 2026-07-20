import uuid
from sqlalchemy import (
    Column, String, Text, Numeric, Boolean, ForeignKey, TIMESTAMP, Enum, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


def uuid_col():
    return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class Customer(Base):
    __tablename__ = "customers"

    id = uuid_col()
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String)
    address = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    leads = relationship("Lead", back_populates="customer")


class Lead(Base):
    __tablename__ = "leads"

    id = uuid_col()
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))
    status = Column(
        Enum(
            "new_lead", "contacted", "estimate_scheduled",
            "estimate_sent", "approved", "completed",
            name="lead_status",
        ),
        default="new_lead",
        nullable=False,
    )
    project_type = Column(String, default="other")
    room_size_sqft = Column(Numeric(10, 2))
    tile_type = Column(String)
    budget_range = Column(String)
    timeline = Column(String)
    source = Column(String)
    notes = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    customer = relationship("Customer", back_populates="leads")
    messages = relationship("ChatMessage", back_populates="lead")
    media = relationship("ProjectMedia", back_populates="lead")
    estimates = relationship("Estimate", back_populates="lead")
    appointments = relationship("Appointment", back_populates="lead")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = uuid_col()
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"))
    role = Column(String, nullable=False)  # user | assistant
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    lead = relationship("Lead", back_populates="messages")


class ProjectMedia(Base):
    __tablename__ = "project_media"

    id = uuid_col()
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"))
    media_type = Column(String, nullable=False)  # photo | video
    s3_url = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    lead = relationship("Lead", back_populates="media")


class PhotoAnalysis(Base):
    __tablename__ = "photo_analyses"

    id = uuid_col()
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"))
    room_type = Column(String)
    complexity = Column(String)
    surface_condition = Column(String)
    waterproofing_needed = Column(Boolean)
    estimated_sqft = Column(Numeric(10, 2))
    estimated_material_units = Column(Numeric(10, 2))
    raw_ai_response = Column(JSON)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Estimate(Base):
    __tablename__ = "estimates"

    id = uuid_col()
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"))
    materials_cost = Column(Numeric(10, 2), default=0)
    labor_cost = Column(Numeric(10, 2), default=0)
    demolition_cost = Column(Numeric(10, 2), default=0)
    total_cost = Column(Numeric(10, 2), default=0)
    pdf_s3_url = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    lead = relationship("Lead", back_populates="estimates")


class Setting(Base):
    __tablename__ = "settings"

    key = Column(String, primary_key=True)
    value = Column(JSON, nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


class Appointment(Base):
    __tablename__ = "appointments"

    id = uuid_col()
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"))
    scheduled_for = Column(TIMESTAMP(timezone=True), nullable=False)
    google_calendar_event_id = Column(String)
    reminder_sent = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    lead = relationship("Lead", back_populates="appointments")
