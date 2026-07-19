# TileFlow AI — MVP

An AI platform for tile installation & remodeling companies: a customer submits
a request → an AI agent collects project details and photos → a preliminary
quote is generated → an on-site measurement gets booked → everything lands in
the owner's CRM automatically.

Built for the Canadian market (CAD pricing, provincial sales tax handling).

## Repository structure

```
tileflow-ai/
├── backend/            FastAPI application
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── models/      SQLAlchemy models
│       ├── routers/     leads, estimates, appointments, chat, uploads
│       ├── services/    estimate_engine, photo_analyzer, storage, pdf_generator
│       └── ai/          system prompts for the AI customer agent
├── frontend/           Next.js 14 (App Router) + Tailwind
│   └── app/
│       ├── page.tsx           Home
│       ├── estimate/page.tsx   AI Estimate flow (chat + photo + quote)
│       ├── dashboard/page.tsx  Owner CRM dashboard
│       ├── portfolio/page.tsx
│       ├── reviews/page.tsx
│       └── contact/page.tsx
├── database/
│   └── schema.sql       Full Postgres schema
└── docs/
    ├── roadmap.md        90-day plan
    └── deployment.md      How to actually go live in Canada
```

## Tech stack

- **Frontend:** Next.js 14, React, Tailwind CSS
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **AI:** Anthropic API (chat agent + vision for photo analysis)
- **Storage:** AWS S3 (project photos/videos, generated PDF estimates)
- **Payments:** Stripe (only needed if you resell this to other companies)
- **Auth:** Auth.js (owner/staff login — customers never need an account)
- **Deploy:** Docker → Vercel (frontend) + Render/Railway/AWS (backend + DB)

## Run it locally

### 1. Database
```bash
createdb tileflow
psql tileflow < database/schema.sql
```

### 2. Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in DATABASE_URL, ANTHROPIC_API_KEY, AWS keys
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend
```bash
cd frontend
npm install
cp .env.local.example .env.local   # NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```

Visit `http://localhost:3000` for the site, `/estimate` for the AI flow, and
`/dashboard` for the owner CRM.

## What's in this MVP release

- ✅ Website (Home / Portfolio / Reviews / AI Estimate / Contact)
- ✅ AI chat agent that collects Name / Phone / Address / Project type / Room
  size / Tile type / Budget / Timeline
- ✅ Photo upload with AI analysis hook (stubbed until a Vision API key is added)
- ✅ Estimate Generator with Canadian sales tax (GST/HST/PST by province) → PDF
- ✅ Lead CRM dashboard with status pipeline (New Lead → Contacted → Estimate
  Scheduled → Estimate Sent → Approved → Completed)
- ✅ Appointment booking (structure ready for Google Calendar API)

Voice AI, price-objection handling, and the AI Interior Designer are Phase 2/3
— see `docs/roadmap.md` — so the MVP stays shippable instead of half-built
everywhere at once.

## What YOU need to do to make this a live, sellable product

This repo is the whole engineering side. Going live also needs a few things
only you can do (see `docs/deployment.md` for the exact steps):

1. Get an **Anthropic API key** (for the chat + photo analysis) and an **AWS
   account** (for S3 photo/PDF storage).
2. **Register a domain** and a **Canadian business number** (for invoicing/tax).
3. **Deploy**: push `frontend/` to Vercel, `backend/` + Postgres to
   Render/Railway — both take about 10 minutes with the walkthrough in
   `docs/deployment.md`.
4. Fill in real prices in `backend/app/services/estimate_engine.py` — the
   numbers there are placeholders.
5. Replace the placeholder Portfolio/Reviews copy with real project photos and
   testimonials.

Nothing above requires touching code beyond step 4 — it's account setup and
following the deploy guide.
