import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Lead, ProjectMedia, PhotoAnalysis
from app.services.storage import upload_to_s3
from app.services.photo_analyzer import analyze_photo

router = APIRouter()


@router.post("")
async def upload_media(
    lead_id: uuid.UUID = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    media_type = "video" if file.content_type.startswith("video") else "photo"
    contents = await file.read()
    s3_url = upload_to_s3(contents, filename=file.filename, lead_id=str(lead_id))

    media = ProjectMedia(lead_id=lead.id, media_type=media_type, s3_url=s3_url)
    db.add(media)
    db.commit()

    analysis_result = None
    if media_type == "photo":
        analysis_result = analyze_photo(s3_url)
        db.add(PhotoAnalysis(lead_id=lead.id, **analysis_result))
        db.commit()

    return {
        "media_id": str(media.id),
        "s3_url": s3_url,
        "analysis": analysis_result,
    }
