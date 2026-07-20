# Going Live — Step by Step

This is the part I can't do for you (no internet access from where I build),
but it's mostly clicking "Deploy" and pasting keys — not writing code.

## 1. Accounts you need (all have Canadian billing support)

| Service | What it's for | Free tier? |
|---|---|---|
| [Anthropic Console](https://console.anthropic.com) | AI chat + photo analysis | Pay-as-you-go, no monthly minimum |
| [AWS](https://aws.amazon.com) | S3 storage for photos + PDFs | Free tier covers early usage |
| [Vercel](https://vercel.com) | Hosts the Next.js frontend | Free for this scale |
| [Render](https://render.com) or [Railway](https://railway.app) | Hosts FastAPI backend + Postgres | Free/low-cost starter tier |
| A domain registrar (Namecheap, Google Domains successor, or a `.ca` registrar like CIRA-accredited ones) | Your public URL | ~$15-20 CAD/year |

## 2. Backend deploy (Render example)

1. Push this repo to a GitHub repository.
2. In Render: **New → Web Service** → connect the repo → root directory `backend`.
3. Build command: `pip install -r requirements.txt`
   Start command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
4. **New → PostgreSQL** in Render, copy the connection string.
5. In the web service's environment variables, set everything from
   `backend/.env.example` — paste the Postgres URL into `DATABASE_URL`, your
   Anthropic key into `ANTHROPIC_API_KEY`, AWS keys, etc.
6. Once deployed, run the schema once against the new database:
   `psql <DATABASE_URL> < database/schema.sql`

## 3. Frontend deploy (Vercel)

1. In Vercel: **New Project** → import the same repo → root directory `frontend`.
2. Add environment variable `NEXT_PUBLIC_API_URL` = your Render backend URL
   (e.g. `https://tileflow-api.onrender.com`).
3. Deploy. Vercel gives you a `*.vercel.app` URL immediately.
4. In Vercel project settings → Domains, add your purchased domain and follow
   the DNS instructions from your registrar.

## 4. Connect the AI

- `backend/app/ai/customer_agent.py` and `backend/app/services/photo_analyzer.py`
  both have the exact Anthropic API call written out in a comment — uncomment
  it and remove the placeholder return once `ANTHROPIC_API_KEY` is set.

## 4b. Connect Google Calendar (so bookings show up on a real calendar)

1. In [Google Cloud Console](https://console.cloud.google.com), create a
   project and enable the **Google Calendar API**.
2. Create a **Service Account** (IAM & Admin → Service Accounts), then create
   a JSON key for it and download it.
3. Open Google Calendar as the business owner → the calendar to book into →
   **Settings and sharing** → **Share with specific people** → add the service
   account's email (looks like `xxx@xxx.iam.gserviceaccount.com`) with
   **"Make changes to events"** permission.
4. Set two environment variables on the backend:
   - `GOOGLE_CALENDAR_ID` — the calendar's ID (usually the owner's Gmail
     address, or a dedicated calendar's ID from its settings page)
   - `GOOGLE_SERVICE_ACCOUNT_JSON` — paste the entire downloaded JSON key as
     one string
5. That's it — no OAuth consent screen needed, since this books into one
   fixed business calendar rather than each customer's own calendar.

Until these are set, appointment booking still works (stored in the
database), it just won't create a real calendar event — useful for testing
before Google Cloud setup is done.

## 5. Canadian business basics (not code, but worth flagging)

- If you plan to invoice customers, you'll want a **GST/HST number** from the
  CRA once you're past the small-supplier threshold — the tax rates are
  already wired into `estimate_engine.py` by province.
- If reselling this to other tile companies as a subscription, Stripe Billing
  handles CAD subscriptions natively — that's Phase 3 in the roadmap.

## 6. What "done" looks like

Once steps 1-3 are done, you'll have a real public URL, a real database, and a
real AI — at that point this stops being a demo and becomes the actual
product. Everything past that (more leads, better copy, real portfolio photos,
Voice AI) is iteration, not a blocker to going live.
