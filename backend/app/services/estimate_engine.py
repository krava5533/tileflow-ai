"""
Estimate Generator — calculates a preliminary quote based on square footage,
tile type, surface condition (demolition/waterproofing) and labor complexity.

All rates below are placeholder starter values in CAD for the MVP — replace
them with the company's real price book (move to a `price_book` DB table in
Phase 2 so the owner can edit rates without a code change).

Canadian sales tax varies by province (GST 5% federal only in AB/territories,
HST 13-15% in ON/Atlantic provinces, GST+PST elsewhere). TAX_RATE_BY_PROVINCE
below covers the common cases — wire up PROVINCE from the lead's address once
that's available; defaults to Ontario HST.
"""

from typing import Dict

MATERIAL_COST_PER_SQFT = {
    "ceramic": 3.5,
    "porcelain": 5.0,
    "natural_stone": 9.0,
    "mosaic": 12.0,
}
DEFAULT_MATERIAL_COST = 5.0

LABOR_COST_PER_SQFT = {
    "low": 6.0,
    "medium": 9.0,
    "high": 14.0,
}

DEMOLITION_COST_PER_SQFT = 4.0
WATERPROOFING_COST_PER_SQFT = 3.5

TAX_RATE_BY_PROVINCE = {
    "ON": 0.13,  # HST
    "NB": 0.15, "NS": 0.15, "PE": 0.15, "NL": 0.15,  # HST
    "BC": 0.12, "SK": 0.11, "MB": 0.12,  # GST + PST (approximate combined)
    "AB": 0.05, "NT": 0.05, "NU": 0.05, "YT": 0.05,  # GST only
    "QC": 0.14975,  # GST + QST
}
DEFAULT_PROVINCE = "ON"


def calculate_estimate(
    sqft: float,
    tile_type: str = "porcelain",
    complexity: str = "medium",
    needs_demolition: bool = True,
    needs_waterproofing: bool = False,
    province: str = DEFAULT_PROVINCE,
) -> Dict[str, float]:
    material_rate = MATERIAL_COST_PER_SQFT.get(
        (tile_type or "").lower(), DEFAULT_MATERIAL_COST
    )
    labor_rate = LABOR_COST_PER_SQFT.get(complexity, LABOR_COST_PER_SQFT["medium"])

    materials_cost = round(sqft * material_rate, 2)
    labor_cost = round(sqft * labor_rate, 2)
    demolition_cost = round(sqft * DEMOLITION_COST_PER_SQFT, 2) if needs_demolition else 0.0
    waterproofing_cost = round(sqft * WATERPROOFING_COST_PER_SQFT, 2) if needs_waterproofing else 0.0

    subtotal = materials_cost + labor_cost + demolition_cost + waterproofing_cost
    tax_rate = TAX_RATE_BY_PROVINCE.get((province or "").upper(), TAX_RATE_BY_PROVINCE[DEFAULT_PROVINCE])
    tax_amount = round(subtotal * tax_rate, 2)

    return {
        "materials_cost": materials_cost,
        "labor_cost": labor_cost,
        "demolition_cost": demolition_cost + waterproofing_cost,
        "subtotal": round(subtotal, 2),
        "tax_rate": tax_rate,
        "tax_amount": tax_amount,
        "total_cost": round(subtotal + tax_amount, 2),
        "currency": "CAD",
    }
