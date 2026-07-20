from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import leads, chat, uploads, estimates, appointments, admin, content
from app.database import engine, Base
from app.models import models  # noqa: F401 -- registers models on Base.metadata

app = FastAPI(title="TileFlow AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # сузить до домена фронтенда в проде
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leads.router, prefix="/api/leads", tags=["leads"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(uploads.router, prefix="/api/uploads", tags=["uploads"])
app.include_router(estimates.router, prefix="/api/estimates", tags=["estimates"])
app.include_router(appointments.router, prefix="/api/appointments", tags=["appointments"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(content.router, prefix="/api/content", tags=["content"])


@app.on_event("startup")
def create_tables():
    # Creates any tables that don't exist yet, based on the SQLAlchemy models.
    # Safe to run on every startup -- it never drops or alters existing tables.
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}
