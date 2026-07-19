"""
Generates a client-ready PDF estimate document. Uses reportlab (pure Python,
no external binary dependency, works in any Docker/Vercel/Render environment).
"""

import os
from datetime import datetime
from typing import Dict

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas

COMPANY_NAME = os.getenv("COMPANY_NAME", "TileFlow AI")
COMPANY_TAGLINE = os.getenv("COMPANY_TAGLINE", "Tile & Remodeling")


def generate_estimate_pdf(
    output_path: str,
    customer_name: str,
    customer_address: str,
    project_type: str,
    costs: Dict,
) -> str:
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(0.75 * inch, height - 1 * inch, COMPANY_NAME)
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.grey)
    c.drawString(0.75 * inch, height - 1.2 * inch, COMPANY_TAGLINE)
    c.setFillColor(colors.black)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.75 * inch, height - 1.7 * inch, "Preliminary Estimate")
    c.setFont("Helvetica", 10)
    c.drawString(0.75 * inch, height - 1.95 * inch, f"Date: {datetime.now().strftime('%B %d, %Y')}")

    # Customer block
    c.setFont("Helvetica-Bold", 11)
    c.drawString(0.75 * inch, height - 2.4 * inch, "Prepared for:")
    c.setFont("Helvetica", 10)
    c.drawString(0.75 * inch, height - 2.6 * inch, customer_name or "Prospective Customer")
    c.drawString(0.75 * inch, height - 2.8 * inch, customer_address or "")
    c.drawString(0.75 * inch, height - 3.0 * inch, f"Project type: {project_type or 'N/A'}")

    # Cost table
    y = height - 3.6 * inch
    rows = [
        ("Materials", costs.get("materials_cost", 0)),
        ("Labor", costs.get("labor_cost", 0)),
        ("Demolition / prep / waterproofing", costs.get("demolition_cost", 0)),
        ("Subtotal", costs.get("subtotal", 0)),
        (f"Tax ({round(costs.get('tax_rate', 0) * 100, 2)}%)", costs.get("tax_amount", 0)),
    ]
    c.setFont("Helvetica", 10)
    for label, value in rows:
        c.drawString(0.75 * inch, y, label)
        c.drawRightString(width - 0.75 * inch, y, f"${value:,.2f} CAD")
        y -= 0.28 * inch

    c.line(0.75 * inch, y, width - 0.75 * inch, y)
    y -= 0.3 * inch
    c.setFont("Helvetica-Bold", 13)
    c.drawString(0.75 * inch, y, "Total (estimated)")
    c.drawRightString(width - 0.75 * inch, y, f"${costs.get('total_cost', 0):,.2f} CAD")

    y -= 0.6 * inch
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.grey)
    c.drawString(
        0.75 * inch, y,
        "This is a preliminary AI-generated estimate based on submitted photos and information.",
    )
    y -= 0.15 * inch
    c.drawString(
        0.75 * inch, y,
        "Final pricing is confirmed after an in-person measurement.",
    )

    c.showPage()
    c.save()
    return output_path
