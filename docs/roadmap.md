# TileFlow AI — 90-Day Roadmap

## Phase 1 (Days 1-30) — MVP that lands a real lead
Goal: one tile company (yours) is actually getting and processing leads through
the system.

- Week 1: DB schema, backend skeleton (leads/estimates/appointments), staging deploy
- Week 2: website (Home, Portfolio, Reviews, Contact), "Get Free AI Estimate" CTA
- Week 3: AI chat agent (data collection), photo upload to S3, CRM dashboard
  (list + status changes)
- Week 4: Estimate Generator (calculation + PDF, CAD + tax), manual appointment
  booking, live test on real leads

**Phase 1 done means:** a lead comes in from an ad → goes through the chat →
uploads photos → gets a PDF quote → books a measurement → the owner sees all
of it in the dashboard.

## Phase 2 (Days 31-60) — automation and lead quality
- Google Calendar integration (real time slots, automatic reminders)
- Photo AI Analyzer on a real Vision API (room type, surface condition, area)
- AI Sales Assistant: objection handling ("your price is too high", etc.)
- Admin/analytics dashboard: leads, conversion rate, cost per lead, top sources
- Estimate Generator refinements: demolition, waterproofing, complex layouts,
  province-aware tax by customer address

## Phase 3 (Days 61-90) — scaling and Voice AI
- Voice AI agent (Twilio + Voice API): answers calls, creates a lead from the conversation
- Prepare the product to sell to other companies: multi-tenancy, Stripe billing, onboarding
- AI Interior Designer (bathroom photo → design/tile/layout options) as a premium feature
- Load testing, security review, legal pages (privacy policy, terms of service)

## After 90 days
- White-label version for partners
- Integration marketplace (competitor CRMs, ad platforms)
- Mobile app for the owner (push notifications on new leads)
