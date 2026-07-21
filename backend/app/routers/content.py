from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import settings_service

router = APIRouter()


@router.get("/portfolio")
def public_portfolio(db: Session = Depends(get_db)):
    return settings_service.get_portfolio(db)


@router.get("/reviews")
def public_reviews(db: Session = Depends(get_db)):
    return settings_service.get_reviews(db)


@router.get("/site")
def public_site_content(db: Session = Depends(get_db)):
    return settings_service.get_site_content(db)
