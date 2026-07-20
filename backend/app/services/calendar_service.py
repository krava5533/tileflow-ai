"""
Google Calendar integration for booking on-site measurements.

Uses a Google service account instead of per-user OAuth — appropriate here
because there's exactly one business calendar to write to, not one calendar
per end customer. Setup (also documented in docs/deployment.md):

1. In Google Cloud Console, create a project (or reuse one) and enable the
   "Google Calendar API".
2. Create a Service Account, download its JSON key.
3. Open Google Calendar (as the business owner) → the calendar you want to
   book into → Settings and sharing → "Share with specific people" → add the
   service account's email (looks like xxx@xxx.iam.gserviceaccount.com) with
   "Make changes to events" permission.
4. Set env vars:
   - GOOGLE_SERVICE_ACCOUNT_JSON = the full JSON key content (as one line/string)
   - GOOGLE_CALENDAR_ID = the calendar's ID (the owner's email address, or a
     dedicated calendar's ID from its settings page)

If those env vars aren't set, functions here no-op and return None so the
rest of the app (appointments, reminders) keeps working without Calendar
connected — useful for local dev before you've done the Google Cloud setup.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional

CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")
SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def _get_calendar_client():
    if not (CALENDAR_ID and SERVICE_ACCOUNT_JSON):
        return None

    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    info = json.loads(SERVICE_ACCOUNT_JSON)
    credentials = service_account.Credentials.from_service_account_info(
        info, scopes=SCOPES
    )
    return build("calendar", "v3", credentials=credentials)


def create_measurement_event(
    scheduled_for: datetime,
    customer_name: str,
    customer_address: str,
    customer_phone: str,
    lead_id: str,
    duration_minutes: int = 45,
) -> Optional[str]:
    """Creates a calendar event for the on-site measurement. Returns the
    Google Calendar event ID, or None if Calendar isn't configured yet."""
    service = _get_calendar_client()
    if service is None:
        return None

    end_time = scheduled_for + timedelta(minutes=duration_minutes)

    event = {
        "summary": f"Measurement — {customer_name}",
        "location": customer_address or "",
        "description": (
            f"Lead ID: {lead_id}\n"
            f"Phone: {customer_phone}\n"
            f"Booked automatically via TileFlow AI."
        ),
        "start": {"dateTime": scheduled_for.isoformat(), "timeZone": "America/Toronto"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "America/Toronto"},
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 60},
            ],
        },
    }

    created = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return created.get("id")


def cancel_measurement_event(event_id: str) -> bool:
    service = _get_calendar_client()
    if service is None or not event_id:
        return False
    try:
        service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
        return True
    except Exception:
        return False


def list_busy_slots(start: datetime, end: datetime) -> list:
    """Returns busy time ranges on the business calendar between start/end,
    so the frontend can show only free slots when booking."""
    service = _get_calendar_client()
    if service is None:
        return []

    body = {
        "timeMin": start.isoformat(),
        "timeMax": end.isoformat(),
        "items": [{"id": CALENDAR_ID}],
    }
    result = service.freebusy().query(body=body).execute()
    return result.get("calendars", {}).get(CALENDAR_ID, {}).get("busy", [])
