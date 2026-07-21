import os

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import settings_service

router = APIRouter()


def require_admin(x_admin_password: str = Header(default="")):
    expected = os.getenv("ADMIN_PASSWORD")
    if not expected:
        raise HTTPException(status_code=503, detail="Admin panel not configured (ADMIN_PASSWORD not set)")
    if x_admin_password != expected:
        raise HTTPException(status_code=401, detail="Invalid admin password")


@router.post("/login")
def login(x_admin_password: str = Header(default="")):
    """Just validates the password so the frontend can show/hide the panel."""
    require_admin(x_admin_password)
    return {"ok": True}


@router.get("/price-book")
def get_price_book(db: Session = Depends(get_db), x_admin_password: str = Header(default="")):
    require_admin(x_admin_password)
    return settings_service.get_price_book(db)


@router.put("/price-book")
def update_price_book(
    price_book: dict,
    db: Session = Depends(get_db),
    x_admin_password: str = Header(default=""),
):
    require_admin(x_admin_password)
    return settings_service.save_price_book(db, price_book)


@router.get("/portfolio")
def get_portfolio(db: Session = Depends(get_db), x_admin_password: str = Header(default="")):
    require_admin(x_admin_password)
    return settings_service.get_portfolio(db)


@router.put("/portfolio")
def update_portfolio(
    items: list,
    db: Session = Depends(get_db),
    x_admin_password: str = Header(default=""),
):
    require_admin(x_admin_password)
    return settings_service.save_portfolio(db, items)


@router.get("/reviews")
def get_reviews(db: Session = Depends(get_db), x_admin_password: str = Header(default="")):
    require_admin(x_admin_password)
    return settings_service.get_reviews(db)


@router.put("/reviews")
def update_reviews(
    items: list,
    db: Session = Depends(get_db),
    x_admin_password: str = Header(default=""),
):
    require_admin(x_admin_password)
    return settings_service.save_reviews(db, items)


@router.get("/site-content")
def get_site_content(db: Session = Depends(get_db), x_admin_password: str = Header(default="")):
    require_admin(x_admin_password)
    return settings_service.get_site_content(db)


@router.put("/site-content")
def update_site_content(
    content: dict,
    db: Session = Depends(get_db),
    x_admin_password: str = Header(default=""),
):
    require_admin(x_admin_password)
    return settings_service.save_site_content(db, content)
