"""
Generic key/value settings store (the `settings` table), used for the price
book, portfolio items, and reviews -- anything the owner should be able to
edit from /admin without a code change.
"""

from sqlalchemy.orm import Session
from app.models.models import Setting
from app.services import estimate_engine as defaults

PRICE_BOOK_KEY = "price_book"
PORTFOLIO_KEY = "portfolio"
REVIEWS_KEY = "reviews"
SITE_CONTENT_KEY = "site_content"

DEFAULT_SITE_CONTENT = {
    "site_name": "TileFlow AI",
    "hero_title_line1": "Tile estimates,",
    "hero_title_line2": "without the wait.",
    "hero_subtitle": (
        "Describe your project to our AI, upload a few photos, and get a real "
        "estimate before you've finished your coffee. Then book your on-site "
        "measurement -- no phone tag required."
    ),
    "contact_phone": "",
    "contact_email": "",
    "accent_color": "#3F6E64",
}

DEFAULT_PORTFOLIO = [
    {"title": "Master Bath Remodel", "tag": "Bathroom · Porcelain", "image_url": ""},
    {"title": "Kitchen Backsplash Refresh", "tag": "Kitchen · Mosaic", "image_url": ""},
    {"title": "Whole-Home Floor Replacement", "tag": "Floor · Large-format", "image_url": ""},
]

DEFAULT_REVIEWS = [
    {"text": "Placeholder review #1 -- replace with real customer feedback.", "author": "Verified customer"},
    {"text": "Placeholder review #2 -- replace with real customer feedback.", "author": "Verified customer"},
    {"text": "Placeholder review #3 -- replace with real customer feedback.", "author": "Verified customer"},
]


def get_setting(db: Session, key: str, default):
    row = db.query(Setting).filter(Setting.key == key).first()
    if row and row.value is not None:
        return row.value
    return default


def save_setting(db: Session, key: str, value):
    row = db.query(Setting).filter(Setting.key == key).first()
    if row:
        row.value = value
    else:
        row = Setting(key=key, value=value)
        db.add(row)
    db.commit()
    return value


def get_price_book(db: Session) -> dict:
    return get_setting(db, PRICE_BOOK_KEY, {
        "material_cost_per_sqft": dict(defaults.MATERIAL_COST_PER_SQFT),
        "labor_cost_per_sqft": dict(defaults.LABOR_COST_PER_SQFT),
        "demolition_cost_per_sqft": defaults.DEMOLITION_COST_PER_SQFT,
        "waterproofing_cost_per_sqft": defaults.WATERPROOFING_COST_PER_SQFT,
        "default_province": defaults.DEFAULT_PROVINCE,
    })


def save_price_book(db: Session, data: dict) -> dict:
    return save_setting(db, PRICE_BOOK_KEY, data)


def get_portfolio(db: Session) -> list:
    return get_setting(db, PORTFOLIO_KEY, DEFAULT_PORTFOLIO)


def save_portfolio(db: Session, data: list) -> list:
    return save_setting(db, PORTFOLIO_KEY, data)


def get_reviews(db: Session) -> list:
    return get_setting(db, REVIEWS_KEY, DEFAULT_REVIEWS)


def save_reviews(db: Session, data: list) -> list:
    return save_setting(db, REVIEWS_KEY, data)


def get_site_content(db: Session) -> dict:
    stored = get_setting(db, SITE_CONTENT_KEY, {})
    return {**DEFAULT_SITE_CONTENT, **stored}


def save_site_content(db: Session, data: dict) -> dict:
    return save_setting(db, SITE_CONTENT_KEY, data)
