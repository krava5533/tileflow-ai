-- TileFlow AI — MVP schema (PostgreSQL)

CREATE TYPE lead_status AS ENUM (
  'new_lead',
  'contacted',
  'estimate_scheduled',
  'estimate_sent',
  'approved',
  'completed'
);

CREATE TYPE project_type AS ENUM (
  'bathroom',
  'kitchen',
  'floor',
  'shower',
  'backsplash',
  'outdoor_patio',
  'other'
);

-- Владелец / сотрудники компании (используют CRM)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'owner',   -- owner | staff
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Клиенты
CREATE TABLE customers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  phone TEXT NOT NULL,
  email TEXT,
  address TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Заявка (Lead) — центральная сущность
CREATE TABLE leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
  status lead_status NOT NULL DEFAULT 'new_lead',
  project_type project_type NOT NULL DEFAULT 'other',
  room_size_sqft NUMERIC(10,2),
  tile_type TEXT,
  budget_range TEXT,
  timeline TEXT,
  source TEXT,                 -- google_ads | facebook_ads | referral | organic ...
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- История переписки с AI-агентом
CREATE TABLE chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  role TEXT NOT NULL,           -- user | assistant
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Загруженные фото/видео объекта
CREATE TABLE project_media (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  media_type TEXT NOT NULL,     -- photo | video
  s3_url TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Результат AI-анализа фото (Project Report)
CREATE TABLE photo_analyses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  room_type TEXT,
  complexity TEXT,              -- low | medium | high
  surface_condition TEXT,
  waterproofing_needed BOOLEAN,
  estimated_sqft NUMERIC(10,2),
  estimated_material_units NUMERIC(10,2),
  raw_ai_response JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Сгенерированные сметы
CREATE TABLE estimates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  materials_cost NUMERIC(10,2) NOT NULL DEFAULT 0,
  labor_cost NUMERIC(10,2) NOT NULL DEFAULT 0,
  demolition_cost NUMERIC(10,2) NOT NULL DEFAULT 0,
  total_cost NUMERIC(10,2) NOT NULL DEFAULT 0,
  pdf_s3_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Записи на замер (appointments)
CREATE TABLE appointments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  scheduled_for TIMESTAMPTZ NOT NULL,
  google_calendar_event_id TEXT,
  reminder_sent BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_customer ON leads(customer_id);
CREATE INDEX idx_chat_lead ON chat_messages(lead_id);
CREATE INDEX idx_media_lead ON project_media(lead_id);
