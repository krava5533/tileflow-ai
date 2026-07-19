import os
import tempfile
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Lead, PhotoAnalysis, Estimate
from app.services.estimate_engine import calculate_estimate
from app.services.pdf_generator import generate_estimate_pdf
from app.services.storage import upload_to_s3

router = APIRouter()


@router.post("/{lead_id}/generate")
def generate_estimate(lead_id: uuid.UUID, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    analysis = (
        db.query(PhotoAnalysis)
        .filter(PhotoAnalysis.lead_id == lead_id)
        .order_by(PhotoAnalysis.created_at.desc())
        .first()
    )

    sqft = float(analysis.estimated_sqft) if analysis and analysis.estimated_sqft else (
        float(lead.room_size_sqft) if lead.room_size_sqft else 50.0
    )
    complexity = analysis.complexity if analysis else "medium"
    needs_waterproofing = analysis.waterproofing_needed if analysis else False

    costs = calculate_estimate(
        sqft=sqft,
        tile_type=lead.tile_type or "porcelain",
        complexity=complexity,
        needs_demolition=True,
        needs_waterproofing=bool(needs_waterproofing),
    )

    # DB row only stores the columns that exist on the model
    db_costs = {
        "materials_cost": costs["materials_cost"],
        "labor_cost": costs["labor_cost"],
        "demolition_cost": costs["demolition_cost"],
        "total_cost": costs["total_cost"],
    }
    estimate = Estimate(lead_id=lead.id, **db_costs)
    db.add(estimate)
    db.flush()

    with tempfile.TemporaryDirectory() as tmp_dir:
        pdf_path = os.path.join(tmp_dir, f"estimate_{estimate.id}.pdf")
        generate_estimate_pdf(
            output_path=pdf_path,
            customer_name=lead.customer.name if lead.customer else "",
            customer_address=lead.customer.address if lead.customer else "",
            project_type=lead.project_type,
            costs=costs,
        )
        with open(pdf_path, "rb") as f:
            pdf_url = upload_to_s3(
                f.read(), filename=f"estimate_{estimate.id}.pdf", lead_id=str(lead.id)
            )

    estimate.pdf_s3_url = pdf_url
    lead.status = "estimate_sent"
    db.commit()
    db.refresh(estimate)

    return {
        "estimate_id": str(estimate.id),
        "sqft_used": sqft,
        "pdf_url": pdf_url,
        **costs,
    }


@router.get("/{lead_id}")
def list_estimates(lead_id: uuid.UUID, db: Session = Depends(get_db)):
    estimates = (
        db.query(Estimate)
        .filter(Estimate.lead_id == lead_id)
        .order_by(Estimate.created_at.desc())
        .all()
    )
    return [
        {
            "id": str(e.id),
            "materials_cost": float(e.materials_cost),
            "labor_cost": float(e.labor_cost),
            "demolition_cost": float(e.demolition_cost),
            "total_cost": float(e.total_cost),
            "created_at": e.created_at.isoformat(),
        }
        for e in estimates
    ]
