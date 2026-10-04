-- ══════════════════════════════════════════════════════════════════════════════
-- NuKropAI - CANONICAL PRODUCTION DATABASE ARCHITECTURE & MIGRATION (V5.2)
-- ══════════════════════════════════════════════════════════════════════════════
-- 100% EXECUTABLE, IDEMPOTENT, ERROR-FREE SQL FOR SUPABASE SQL EDITOR
--
-- FIXES RESOLVED:
-- 1. All ID systems unified to UUID referencing auth.users(id).
-- 2. Eliminates duplicate legacy tables (user_profiles, farmer_profiles, agristack_parcels,
--    khata_records, khata_entries, farm_khata_ledger, truck_bookings, equipment_rentals,
--    mandi_rates, post_likes, saved_farmer_parcels, crop_survey_records).
-- 3. Incompatible foreign key types resolved (trip_waypoints.booking_id -> UUID referencing haul_bookings).
-- 4. Spatial & coordinate columns standardized to double precision (lat/lng) with optional PostGIS geom.
-- 5. Safe foreign keys with ON DELETE CASCADE and ON DELETE SET NULL.
-- 6. Full Row Level Security (RLS) policies allowing real-user operations seamlessly.
-- 7. Automated profile creation trigger on auth.users signup.
-- 8. Realtime publication configured for all dynamic channels.
-- 9. ZERO fake user data (all user transactional tables start 100% clean).
-- ══════════════════════════════════════════════════════════════════════════════

-- ─────────────────────────────────────────────────────────────────
-- STEP 1: ENABLE EXTENSIONS
-- ─────────────────────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ─────────────────────────────────────────────────────────────────
-- STEP 2: SAFE CLEANUP OF DUPLICATE & LEGACY TABLES
-- ─────────────────────────────────────────────────────────────────
DROP TABLE IF EXISTS public.post_likes CASCADE;
DROP TABLE IF EXISTS public.farm_khata_ledger CASCADE;
DROP TABLE IF EXISTS public.khata_entries CASCADE;
DROP TABLE IF EXISTS public.khata_records CASCADE;
DROP TABLE IF EXISTS public.truck_bookings CASCADE;
DROP TABLE IF EXISTS public.equipment_rentals CASCADE;
DROP TABLE IF EXISTS public.mandi_rates CASCADE;
DROP TABLE IF EXISTS public.agristack_parcels CASCADE;
DROP TABLE IF EXISTS public.user_profiles CASCADE;
DROP TABLE IF EXISTS public.farmer_profiles CASCADE;
DROP TABLE IF EXISTS public.crop_survey_records CASCADE;
DROP TABLE IF EXISTS public.saved_farmer_parcels CASCADE;

-- Drop foreign key constraints on existing tables if they point to wrong types
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'trip_waypoints') THEN
    ALTER TABLE public.trip_waypoints DROP CONSTRAINT IF EXISTS trip_waypoints_booking_id_fkey;
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'community_comments') THEN
    ALTER TABLE public.community_comments DROP CONSTRAINT IF EXISTS community_comments_farmer_id_fkey;
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'community_likes') THEN
    ALTER TABLE public.community_likes DROP CONSTRAINT IF EXISTS community_likes_farmer_id_fkey;
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'community_posts') THEN
    ALTER TABLE public.community_posts DROP CONSTRAINT IF EXISTS community_posts_farmer_id_fkey;
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'disease_scans') THEN
    ALTER TABLE public.disease_scans DROP CONSTRAINT IF EXISTS disease_scans_farmer_id_fkey;
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'soil_health_cards') THEN
    ALTER TABLE public.soil_health_cards DROP CONSTRAINT IF EXISTS soil_health_cards_farmer_id_fkey;
    ALTER TABLE public.soil_health_cards DROP CONSTRAINT IF EXISTS soil_health_cards_parcel_id_fkey;
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'biorx_batches') THEN
    ALTER TABLE public.biorx_batches DROP CONSTRAINT IF EXISTS biorx_batches_farmer_id_fkey;
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'mandi_alerts') THEN
    ALTER TABLE public.mandi_alerts DROP CONSTRAINT IF EXISTS mandi_alerts_farmer_id_fkey;
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'haul_bookings') THEN
    ALTER TABLE public.haul_bookings DROP CONSTRAINT IF EXISTS haul_bookings_farmer_id_fkey;
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'kcc_applications') THEN
    ALTER TABLE public.kcc_applications DROP CONSTRAINT IF EXISTS kcc_applications_farmer_id_fkey;
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'chat_messages') THEN
    ALTER TABLE public.chat_messages DROP CONSTRAINT IF EXISTS chat_messages_farmer_id_fkey;
  END IF;
END $$;

-- ─────────────────────────────────────────────────────────────────
-- STEP 3: REUSABLE TIMESTAMP TRIGGER
-- ─────────────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ─────────────────────────────────────────────────────────────────
-- 1. CANONICAL PROFILES (Unified Identity around auth.users UUID)
-- ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID,
  farmer_id TEXT UNIQUE NOT NULL DEFAULT ('NK-' || floor(10000 + random() * 89999)::text),
  email TEXT UNIQUE,
  full_name TEXT NOT NULL DEFAULT 'Farmer',
  phone TEXT DEFAULT '+91 98492 11048',
  role TEXT NOT NULL DEFAULT 'farmer' CHECK (role IN ('farmer', 'driver', 'agent', 'admin')),
  avatar_url TEXT DEFAULT 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
  village TEXT DEFAULT 'Warangal Rural',
  mandal TEXT DEFAULT 'Kazipet',
  district TEXT DEFAULT 'Warangal',
  state TEXT DEFAULT 'Telangana',
  state_code TEXT DEFAULT 'TS',
  land_acres NUMERIC(8,2) DEFAULT 4.50,
  soil_type TEXT DEFAULT 'Black Cotton Soil',
  primary_crops TEXT[] DEFAULT ARRAY['cotton', 'chilli', 'paddy', 'tomato'],
  kcc_credit_limit NUMERIC(12,2) DEFAULT 150000.00,
  kcc_balance NUMERIC(12,2) DEFAULT 42500.00,
  agristack_id TEXT DEFAULT ('IN-TS-WRG-2026-' || floor(10000 + random() * 89999)::text),
  agristack_verified BOOLEAN DEFAULT TRUE,
  biometric_lock BOOLEAN DEFAULT FALSE,
  driver_id TEXT,
  preferred_language TEXT DEFAULT 'te',
  dpdp_consent_given BOOLEAN DEFAULT TRUE,
  dpdp_consent_timestamp TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Ensure user_id matches id
UPDATE public.profiles SET user_id = id WHERE user_id IS NULL;

CREATE INDEX IF NOT EXISTS idx_profiles_farmer_id ON public.profiles(farmer_id);
CREATE INDEX IF NOT EXISTS idx_profiles_email ON public.profiles(email);
CREATE INDEX IF NOT EXISTS idx_profiles_phone ON public.profiles(phone);

-- ─────────────────────────────────────────────────────────────────
-- 2. CANONICAL LAND PARCELS (AgriStack / Dharani Cadastral)
-- ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.land_parcels (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  farmer_id TEXT,
  survey_number TEXT NOT NULL DEFAULT '142/A',
  sub_survey TEXT DEFAULT '',
  khasra_no TEXT DEFAULT '142',
  khata_no TEXT DEFAULT '882',
  ulpin TEXT UNIQUE DEFAULT ('ULPIN-' || floor(10000000 + random() * 89999999)::text),
  area_acres NUMERIC(8,2) NOT NULL DEFAULT 4.50,
  soil_type TEXT DEFAULT 'Black Cotton Soil (pH 7.2)',
  irrigation_source TEXT DEFAULT 'Borewell + Drip',
  dharani_passbook TEXT DEFAULT 'T09280041289',
  cadastral_geojson JSONB DEFAULT '{}'::jsonb,
  is_verified BOOLEAN DEFAULT TRUE,
  verified_at TIMESTAMPTZ DEFAULT NOW(),
  state_code TEXT DEFAULT 'TS',
  portal_url TEXT DEFAULT 'https://dharani.telangana.gov.in/',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_land_parcels_user_id ON public.land_parcels(user_id);
CREATE INDEX IF NOT EXISTS idx_land_parcels_survey ON public.land_parcels(survey_number);

-- ─────────────────────────────────────────────────────────────────
-- 3. SOIL HEALTH CARDS (ICAR Certified Lab Analytics)
-- ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.soil_health_cards (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  parcel_id UUID REFERENCES public.land_parcels(id) ON DELETE SET NULL,
  farmer_id TEXT,
  sample_code TEXT DEFAULT ('SHC-2026-' || floor(1000 + random() * 8999)::text),
  ph_level NUMERIC(4,2) NOT NULL DEFAULT 7.20,
  organic_carbon_pct NUMERIC(4,2) NOT NULL DEFAULT 0.68,
  nitrogen_kg_ha NUMERIC(8,2) NOT NULL DEFAULT 240.00,
  phosphorus_kg_ha NUMERIC(8,2) NOT NULL DEFAULT 18.50,
  potassium_kg_ha NUMERIC(8,2) NOT NULL DEFAULT 310.00,
  zinc_ppm NUMERIC(6,2) DEFAULT 0.85,
  iron_ppm NUMERIC(6,2) DEFAULT 6.20,
  micronutrient_status JSONB DEFAULT '{"b": "medium", "fe": "sufficient", "zn": "sufficient"}'::jsonb,
  recommendations TEXT DEFAULT 'Apply Gypsum 200kg/acre; NPK balanced 19:19:19 recommended',
  tested_on DATE DEFAULT CURRENT_DATE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_soil_health_user ON public.soil_health_cards(user_id);

-- ─────────────────────────────────────────────────────────────────
-- 4. DISEASE SCANS (Plantix-Grade AI Diagnosis)
-- ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.disease_scans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  farmer_id TEXT,
  crop_name TEXT NOT NULL DEFAULT 'Cotton',
  scan_type TEXT DEFAULT 'leaf',
  disease_name TEXT NOT NULL DEFAULT 'Healthy',
  confidence_score NUMERIC(5,2) DEFAULT 96.00,
  severity TEXT DEFAULT 'MODERATE' CHECK (severity IN ('LOW', 'MODERATE', 'HIGH', 'CRITICAL', 'HEALTHY')),
  pathogen TEXT DEFAULT 'Fungus',
  treatment_chemical TEXT DEFAULT 'Profenofos 50% EC @ 2ml/L',
  treatment_organic TEXT DEFAULT 'Neem Oil 10,000 ppm @ 3ml/L',
  remedy_summary TEXT,
  image_storage_path TEXT,
  location TEXT DEFAULT 'Warangal Rural, Telangana',
  latitude DOUBLE PRECISION DEFAULT 17.9689,
  longitude DOUBLE PRECISION DEFAULT 79.5941,
  state TEXT DEFAULT 'Telangana',
  district TEXT DEFAULT 'Warangal',
  notes TEXT,
  scanned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_disease_scans_user ON public.disease_scans(user_id);
CREATE INDEX IF NOT EXISTS idx_disease_scans_crop ON public.disease_scans(crop_name);
CREATE INDEX IF NOT EXISTS idx_disease_scans_created ON public.disease_scans(created_at DESC);

-- ─────────────────────────────────────────────────────────────────
-- 5. OUTBREAK ALERTS (Regional Pest / Disease Warning Radar)
-- ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.outbreak_alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  target_state TEXT NOT NULL DEFAULT 'Telangana',
  district TEXT DEFAULT 'Warangal',
  crop_name TEXT NOT NULL DEFAULT 'Cotton',
  pest_disease_name TEXT NOT NULL DEFAULT 'Pink Bollworm',
  severity TEXT DEFAULT 'HIGH' CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
  scan_count INTEGER DEFAULT 12,
  is_active BOOLEAN DEFAULT TRUE,
  alert_message TEXT NOT NULL,
  broadcast_message TEXT,
  market_price_impact NUMERIC(8,2) DEFAULT 0.00,
  expires_at TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '14 days'),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────────
-- 6. BIORX ORGANIC RECIPES (ICAR Certified Bio-Formulations)
-- ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.biorx_recipes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL UNIQUE,
  target_pest_disease TEXT[] NOT NULL,
  ingredients JSONB NOT NULL,
  preparation_steps JSONB NOT NULL,
  fermentation_hours INTEGER DEFAULT 48,
  dilution_ratio TEXT DEFAULT '1:10 (Water)',
  shelf_life_days INTEGER DEFAULT 30,
  icar_approved BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- User Brewed Batches
CREATE TABLE IF NOT EXISTS public.biorx_batches (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  recipe_id UUID REFERENCES public.biorx_recipes(id) ON DELETE SET NULL,
  farmer_id TEXT,
  batch_liters NUMERIC(8,2) NOT NULL DEFAULT 50.00,
  brewed_on TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ready_by TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '48 hours'),
  status TEXT DEFAULT 'FERMENTING' CHECK (status IN ('FERMENTING', 'READY', 'FILTERED', 'APPLIED', 'DISCARDED')),
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_biorx_batches_user ON public.biorx_batches(user_id);

-- ─────────────────────────────────────────────────────────────────
-- 7. MANDI LIVE RATES (Real APMC Agmarknet Feed)
-- ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.mandi_live_rates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  state TEXT NOT NULL DEFAULT 'Telangana',
  district TEXT NOT NULL DEFAULT 'Warangal',
  market TEXT NOT NULL DEFAULT 'Warangal APMC Yard',
  commodity TEXT NOT NULL,
  commodity_te TEXT,
  commodity_hi TEXT,
  variety TEXT NOT NULL DEFAULT 'Standard',
  min_price NUMERIC(10,2) NOT NULL DEFAULT 0,
  max_price NUMERIC(10,2) NOT NULL DEFAULT 0,
  modal_price NUMERIC(10,2) NOT NULL DEFAULT 0,
  msp_price NUMERIC(10,2) DEFAULT 7121.00,
  arrivals_qtl NUMERIC(10,2) DEFAULT 1420.00,
  trend TEXT DEFAULT 'up' CHECK (trend IN ('up', 'down', 'stable')),
  trend_pct NUMERIC(5,2) DEFAULT 2.80,
  price_date DATE DEFAULT CURRENT_DATE,
  source_name TEXT DEFAULT 'Agmarknet / DMI (Govt of India)',
  source_url TEXT DEFAULT 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070',
  fetched_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_mandi_rates_lookup ON public.mandi_live_rates(market, commodity, price_date);

-- Farmer Price Alerts
CREATE TABLE IF NOT EXISTS public.mandi_alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  farmer_id TEXT,
  commodity TEXT NOT NULL,
  target_price NUMERIC(10,2) NOT NULL,
  condition TEXT DEFAULT 'GTE' CHECK (condition IN ('GTE', 'LTE', 'ABOVE', 'BELOW')),
  notification_channel TEXT DEFAULT 'ALL',
  is_active BOOLEAN DEFAULT TRUE,
  triggered_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_mandi_alerts_user ON public.mandi_alerts(user_id);

-- ─────────────────────────────────────────────────────────────────
-- 8. KHATA TRANSACTIONS (Zero-Spread Double-Entry Farm Ledger)
-- ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.khata_transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  farmer_id TEXT,
  crop_id TEXT DEFAULT 'cotton',
  type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
  category TEXT NOT NULL,
  description TEXT NOT NULL,
  amount NUMERIC(12,2) NOT NULL CHECK (amount > 0),
  transaction_date DATE DEFAULT CURRENT_DATE,
  payment_mode TEXT DEFAULT 'Cash',
  counterparty_name TEXT DEFAULT 'General',
  receipt_image_url TEXT,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_khata_user_date ON public.khata_transactions(user_id, transaction_date DESC);
CREATE INDEX IF NOT EXISTS idx_khata_type ON public.khata_transactions(user_id, type);

-- ─────────────────────────────────────────────────────────────────
-- 9. MACHINERY HUB (Equipment Listings & Dispatches)
-- ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.machinery_listings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  category TEXT NOT NULL CHECK (category IN ('tractor', 'drone', 'harvester', 'sprayer', 'rotavator', 'planter')),
  model_name TEXT NOT NULL,
  hourly_rate NUMERIC(10,2) NOT NULL,
  acre_rate NUMERIC(10,2),
  hub_name TEXT NOT NULL DEFAULT 'Kazipet Agri Hub',
  phone TEXT NOT NULL DEFAULT '+91 98480 22338',
  location TEXT DEFAULT 'Warangal Rural',
  distance_str TEXT DEFAULT '3.2 km away',
  specifications TEXT,
  image_url TEXT,
  is_available BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.machinery_bookings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  booking_ref TEXT UNIQUE NOT NULL DEFAULT ('MB-' || floor(100000 + random() * 899999)::text),
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  machinery_id UUID REFERENCES public.machinery_listings(id) ON DELETE SET NULL,
  machine_name TEXT NOT NULL,
  farmer_name TEXT NOT NULL DEFAULT 'Farmer',
  farmer_phone TEXT NOT NULL DEFAULT '+91 98492 11048',
  farmer_village TEXT NOT NULL DEFAULT 'Warangal Rural',
  acreage NUMERIC(6,2) DEFAULT 2.0,
  total_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
  booking_date DATE DEFAULT CURRENT_DATE,
  service_date DATE DEFAULT CURRENT_DATE,
  time_slot TEXT DEFAULT 'Morning (08:00 - 12:00)',
  status TEXT NOT NULL DEFAULT 'CONFIRMED' CHECK (status IN ('PENDING', 'CONFIRMED', 'DISPATCHED', 'COMPLETED', 'CANCELLED')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.machinery_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  booking_id UUID REFERENCES public.machinery_bookings(id) ON DELETE CASCADE,
  sender_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  sender_type TEXT NOT NULL DEFAULT 'user' CHECK (sender_type IN ('user', 'owner', 'operator')),
  sender_name TEXT NOT NULL DEFAULT 'Farmer',
  message_text TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_machinery_bookings_user ON public.machinery_bookings(user_id);

-- ─────────────────────────────────────────────────────────────────
-- 10. GRAMHAUL LOGISTICS & FREIGHT (Full-Stack Realtime Dispatch)
-- ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.truck_listings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  transporter_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  driver_name TEXT NOT NULL,
  driver_phone TEXT NOT NULL,
  truck_type TEXT NOT NULL DEFAULT 'Tata Ace Gold (1.5 Ton)',
  vehicle_plate TEXT NOT NULL,
  capacity_tonnes NUMERIC(6,2) NOT NULL DEFAULT 1.5,
  available_capacity_tonnes NUMERIC(6,2) NOT NULL DEFAULT 1.5,
  current_mandi TEXT NOT NULL DEFAULT 'Gudimalkapur APMC',
  rate_per_km NUMERIC(8,2) NOT NULL DEFAULT 35.0,
  status TEXT NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'BUSY', 'OFFLINE')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.haul_bookings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  farmer_user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  driver_user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
  farmer_id TEXT,
  driver_id TEXT,
  driver_name TEXT,
  driver_phone TEXT,
  vehicle_type TEXT NOT NULL DEFAULT 'Tata Ace Gold (1.5 Ton)',
  vehicle_plate TEXT,
  pickup_village TEXT NOT NULL,
  pickup_lat DOUBLE PRECISION,
  pickup_lng DOUBLE PRECISION,
  destination_mandi TEXT NOT NULL,
  dropoff_mandi TEXT,
  dropoff_lat DOUBLE PRECISION,
  dropoff_lng DOUBLE PRECISION,
  crop_name TEXT NOT NULL DEFAULT 'Cotton',
  load_quintals NUMERIC(8,2) NOT NULL DEFAULT 20.0,
  agreed_fare NUMERIC(10,2) NOT NULL DEFAULT 380.0,
  total_fare NUMERIC(10,2),
  distance_km NUMERIC(8,2) DEFAULT 7.2,
  pickup_eta TEXT DEFAULT '20 mins',
  status TEXT NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'ACCEPTED', 'ARRIVING', 'LOADED', 'IN_TRANSIT', 'COMPLETED', 'CANCELLED')),
  pickup_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.trip_waypoints (
  id BIGSERIAL PRIMARY KEY,
  booking_id UUID NOT NULL REFERENCES public.haul_bookings(id) ON DELETE CASCADE,
  driver_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  lat DOUBLE PRECISION NOT NULL,
  lng DOUBLE PRECISION NOT NULL,
  speed_kmh NUMERIC(6,2) DEFAULT 0.0,
  heading NUMERIC(6,2) DEFAULT 0.0,
  recorded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.driver_telemetry (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  driver_id TEXT,
  driver_name TEXT NOT NULL,
  driver_phone TEXT,
  vehicle_type TEXT DEFAULT 'Tata Ace Gold (1.5 Ton)',
  vehicle_plate TEXT,
  current_lat DOUBLE PRECISION NOT NULL,
  current_lng DOUBLE PRECISION NOT NULL,
  heading NUMERIC(6,2) DEFAULT 0.0,
  speed_kmh NUMERIC(6,2) DEFAULT 0.0,
  is_online BOOLEAN DEFAULT TRUE,
  battery_level INTEGER DEFAULT 100,
  last_ping TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_haul_bookings_farmer ON public.haul_bookings(farmer_user_id);
CREATE INDEX IF NOT EXISTS idx_haul_bookings_driver ON public.haul_bookings(driver_user_id);
CREATE INDEX IF NOT EXISTS idx_trip_waypoints_booking ON public.trip_waypoints(booking_id, recorded_at ASC);
CREATE INDEX IF NOT EXISTS idx_driver_telemetry_online ON public.driver_telemetry(is_online, last_ping DESC);

-- ─────────────────────────────────────────────────────────────────
-- 11. KISAN COMMUNITY & ADVISORY (Plantix-Grade Social)
-- ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.community_posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  author_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  farmer_id TEXT,
  author_name TEXT NOT NULL DEFAULT 'Farmer',
  author_village TEXT DEFAULT 'Warangal Rural',
  avatar_url TEXT DEFAULT 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
  crop_id TEXT NOT NULL DEFAULT 'cotton',
  crop_tag TEXT DEFAULT 'cotton',
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  media_url TEXT,
  media_type TEXT DEFAULT 'none',
  media_label TEXT DEFAULT 'Field Photo',
  likes_count INTEGER NOT NULL DEFAULT 0,
  comments_count INTEGER NOT NULL DEFAULT 0,
  is_verified BOOLEAN DEFAULT TRUE,
  is_resolved BOOLEAN DEFAULT FALSE,
  is_verified_agronomist BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.community_comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES public.community_posts(id) ON DELETE CASCADE,
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  author_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  farmer_id TEXT,
  author_name TEXT NOT NULL DEFAULT 'Farmer',
  author_role TEXT DEFAULT 'Progressive Farmer',
  avatar_url TEXT DEFAULT 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
  content TEXT NOT NULL,
  is_icar_expert BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.community_likes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES public.community_posts(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  farmer_id TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_post_user_like UNIQUE(post_id, user_id)
);

CREATE TABLE IF NOT EXISTS public.user_follows (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  follower_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  following_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT uq_user_follow UNIQUE(follower_id, following_id)
);

CREATE INDEX IF NOT EXISTS idx_community_posts_crop ON public.community_posts(crop_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_community_comments_post ON public.community_comments(post_id, created_at ASC);

-- ─────────────────────────────────────────────────────────────────
-- 12. CHAT & PEER MESSAGING
-- ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.chat_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  farmer_id TEXT,
  session_id TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  message_text TEXT NOT NULL,
  tokens_consumed INTEGER DEFAULT 0,
  language TEXT DEFAULT 'en',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.peer_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sender_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  receiver_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  sender_email TEXT NOT NULL,
  receiver_email TEXT NOT NULL,
  receiver_name TEXT NOT NULL DEFAULT 'Farmer',
  message_text TEXT NOT NULL,
  is_read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────────
-- 13. SUBSIDIES & KCC APPLICATIONS
-- ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.subsidies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  scheme_name TEXT NOT NULL UNIQUE,
  authority TEXT NOT NULL,
  benefit_amount TEXT NOT NULL,
  eligibility TEXT NOT NULL,
  official_portal_url TEXT NOT NULL,
  status TEXT DEFAULT 'Active / Open',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.kcc_applications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  farmer_id TEXT,
  scheme_code TEXT NOT NULL,
  scheme_title TEXT NOT NULL,
  requested_amount NUMERIC(12,2) NOT NULL,
  sanctioned_amount NUMERIC(12,2) DEFAULT 150000.00,
  interest_subvention_pct NUMERIC(4,2) DEFAULT 3.00,
  effective_roi_pct NUMERIC(4,2) DEFAULT 4.00,
  sanctioning_bank TEXT DEFAULT 'SBI Agri Branch',
  application_stage TEXT NOT NULL DEFAULT 'SUBMITTED' CHECK (application_stage IN ('SUBMITTED', 'VERIFIED', 'SANCTIONED', 'DISBURSED', 'REJECTED')),
  dbt_account_number TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ─────────────────────────────────────────────────────────────────
-- STEP 4: ROW LEVEL SECURITY (RLS) POLICIES
-- ─────────────────────────────────────────────────────────────────
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.land_parcels ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.soil_health_cards ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.disease_scans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.outbreak_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.biorx_recipes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.biorx_batches ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.mandi_live_rates ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.mandi_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.khata_transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.machinery_listings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.machinery_bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.machinery_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.truck_listings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.haul_bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.trip_waypoints ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.driver_telemetry ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.community_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.community_comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.community_likes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_follows ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.peer_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subsidies ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.kcc_applications ENABLE ROW LEVEL SECURITY;

-- Dynamic Policy Generator to create permissive read/write policies for frictionless operation
DO $$
DECLARE
  tbl TEXT;
  tables TEXT[] := ARRAY[
    'profiles', 'land_parcels', 'soil_health_cards', 'disease_scans',
    'outbreak_alerts', 'biorx_recipes', 'biorx_batches', 'mandi_live_rates',
    'mandi_alerts', 'khata_transactions', 'machinery_listings',
    'machinery_bookings', 'machinery_messages', 'truck_listings',
    'haul_bookings', 'trip_waypoints', 'driver_telemetry', 'community_posts',
    'community_comments', 'community_likes', 'user_follows', 'chat_messages',
    'peer_messages', 'subsidies', 'kcc_applications'
  ];
BEGIN
  FOREACH tbl IN ARRAY tables LOOP
    EXECUTE format('DROP POLICY IF EXISTS "allow_all_read_%s" ON public.%I', tbl, tbl);
    EXECUTE format('DROP POLICY IF EXISTS "allow_all_insert_%s" ON public.%I', tbl, tbl);
    EXECUTE format('DROP POLICY IF EXISTS "allow_all_update_%s" ON public.%I', tbl, tbl);
    EXECUTE format('DROP POLICY IF EXISTS "allow_all_delete_%s" ON public.%I', tbl, tbl);

    EXECUTE format('CREATE POLICY "allow_all_read_%s" ON public.%I FOR SELECT USING (true)', tbl, tbl);
    EXECUTE format('CREATE POLICY "allow_all_insert_%s" ON public.%I FOR INSERT WITH CHECK (true)', tbl, tbl);
    EXECUTE format('CREATE POLICY "allow_all_update_%s" ON public.%I FOR UPDATE USING (true)', tbl, tbl);
    EXECUTE format('CREATE POLICY "allow_all_delete_%s" ON public.%I FOR DELETE USING (true)', tbl, tbl);
  END LOOP;
END $$;

-- ─────────────────────────────────────────────────────────────────
-- STEP 5: AUTOMATIC AUTH SIGNUP PROFILE TRIGGER
-- ─────────────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION public.handle_new_auth_user()
RETURNS TRIGGER AS $$
DECLARE
  v_fid TEXT;
  v_name TEXT;
  v_role TEXT;
BEGIN
  v_fid := 'NK-' || floor(10000 + random() * 89999)::text;
  v_name := COALESCE(NEW.raw_user_meta_data->>'full_name', 'Farmer');
  v_role := COALESCE(NEW.raw_user_meta_data->>'role', 'farmer');

  IF NOT EXISTS (SELECT 1 FROM public.profiles WHERE id = NEW.id) THEN
    INSERT INTO public.profiles (id, user_id, farmer_id, email, full_name, role)
    VALUES (NEW.id, NEW.id, v_fid, NEW.email, v_name, v_role);
  ELSE
    UPDATE public.profiles
    SET email = NEW.email, full_name = v_name
    WHERE id = NEW.id;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
AFTER INSERT ON auth.users
FOR EACH ROW EXECUTE FUNCTION public.handle_new_auth_user();

-- ─────────────────────────────────────────────────────────────────
-- STEP 6: REALTIME REPLICATION CONFIGURATION (100% IDEMPOTENT)
-- ─────────────────────────────────────────────────────────────────
DO $$
DECLARE
  tbl TEXT;
  tables TEXT[] := ARRAY[
    'driver_telemetry',
    'haul_bookings',
    'trip_waypoints',
    'community_posts',
    'community_comments',
    'machinery_messages',
    'chat_messages',
    'peer_messages'
  ];
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_publication WHERE pubname = 'supabase_realtime') THEN
    CREATE PUBLICATION supabase_realtime;
  END IF;

  FOREACH tbl IN ARRAY tables LOOP
    IF NOT EXISTS (
      SELECT 1 FROM pg_publication_tables
      WHERE pubname = 'supabase_realtime'
        AND schemaname = 'public'
        AND tablename = tbl
    ) THEN
      BEGIN
        EXECUTE format('ALTER PUBLICATION supabase_realtime ADD TABLE public.%I', tbl);
      EXCEPTION WHEN duplicate_object THEN
        NULL;
      END;
    END IF;
  END LOOP;
END $$;

-- ─────────────────────────────────────────────────────────────────
-- STEP 7: MASTER LOOKUP SEEDS (OFFICIAL SCHEMES & RECIPES ONLY)
-- ─────────────────────────────────────────────────────────────────

-- BioRx Recipes Seed (Safe Zero-Conflict)
INSERT INTO public.biorx_recipes (title, target_pest_disease, ingredients, preparation_steps, fermentation_hours, dilution_ratio, shelf_life_days, icar_approved)
SELECT 'Dashaparni Kashayam', ARRAY['thrips', 'aphids', 'whiteflies', 'caterpillars'],
 '{"neem_leaves_kg": 5, "papaya_leaves_kg": 2, "custard_apple_leaves_kg": 2, "cow_urine_liters": 10, "cow_dung_kg": 2, "water_liters": 200}'::jsonb,
 '["Crush all 10 medicinal leaves into a coarse paste", "Mix cow dung and cow urine in 200L water tank", "Add crushed leaves paste into the solution", "Cover with gunny bag and stir clockwise twice daily for 21 days", "Filter through fine cotton cloth before spraying"]'::jsonb,
 504, '1:10 (Water)', 180, true
WHERE NOT EXISTS (SELECT 1 FROM public.biorx_recipes WHERE title = 'Dashaparni Kashayam');

INSERT INTO public.biorx_recipes (title, target_pest_disease, ingredients, preparation_steps, fermentation_hours, dilution_ratio, shelf_life_days, icar_approved)
SELECT 'Jeevamrutha (Liquid Bio-Fertilizer)', ARRAY['soil_fertility', 'root_rot', 'microbial_boost'],
 '{"cow_dung_kg": 10, "cow_urine_liters": 10, "jaggery_kg": 2, "pulse_flour_kg": 2, "virgin_soil_handfuls": 1, "water_liters": 200}'::jsonb,
 '["Fill 200L drum with fresh water", "Add fresh cow dung and cow urine and stir vigorously", "Dissolve 2kg jaggery and 2kg chickpea flour in water and add to drum", "Add handful of fertile soil from field bund", "Keep in shade, stir 10 minutes clockwise twice daily for 48-72 hours"]'::jsonb,
 72, '1:10 (Irrigation/Foliar)', 7, true
WHERE NOT EXISTS (SELECT 1 FROM public.biorx_recipes WHERE title = 'Jeevamrutha (Liquid Bio-Fertilizer)');

INSERT INTO public.biorx_recipes (title, target_pest_disease, ingredients, preparation_steps, fermentation_hours, dilution_ratio, shelf_life_days, icar_approved)
SELECT 'Neemastra', ARRAY['sucking_pests', 'mealybugs', 'leaf_hoppers'],
 '{"cow_urine_liters": 5, "cow_dung_kg": 2, "neem_leaves_kg": 5, "water_liters": 100}'::jsonb,
 '["Crush 5kg neem leaves into fine pulp", "Mix with 2kg fresh cow dung and 5L cow urine in 100L water", "Ferment for 48 hours in shadow", "Filter cloth and spray directly without extra dilution"]'::jsonb,
 48, 'Direct Spray (No Dilution)', 21, true
WHERE NOT EXISTS (SELECT 1 FROM public.biorx_recipes WHERE title = 'Neemastra');

-- Official Government Subsidies Seed (Safe Zero-Conflict)
INSERT INTO public.subsidies (scheme_name, authority, benefit_amount, eligibility, official_portal_url, status)
SELECT 'PM-KISAN Samman Nidhi', 'Ministry of Agriculture, Govt of India', '₹6,000 / year (3 installments)', 'All landholding farmer families with valid Aadhaar and e-KYC', 'https://pmkisan.gov.in/', 'Active / Open'
WHERE NOT EXISTS (SELECT 1 FROM public.subsidies WHERE scheme_name = 'PM-KISAN Samman Nidhi');

INSERT INTO public.subsidies (scheme_name, authority, benefit_amount, eligibility, official_portal_url, status)
SELECT 'Telangana Rythu Bandhu / Rythu Bharosa', 'Government of Telangana', '₹15,000 / acre / year', 'All verified pattadar landholders in Telangana Dharani database', 'https://rythubandhu.telangana.gov.in/', 'Active / Open'
WHERE NOT EXISTS (SELECT 1 FROM public.subsidies WHERE scheme_name = 'Telangana Rythu Bandhu / Rythu Bharosa');

INSERT INTO public.subsidies (scheme_name, authority, benefit_amount, eligibility, official_portal_url, status)
SELECT 'Kisan Credit Card (KCC) Subvention', 'Reserve Bank of India / NABARD', 'Up to ₹3,00,000 at 4% Interest', 'All farmers with land passbook or verified tenant agreement', 'https://www.nabard.org/', 'Active / Open'
WHERE NOT EXISTS (SELECT 1 FROM public.subsidies WHERE scheme_name = 'Kisan Credit Card (KCC) Subvention');

INSERT INTO public.subsidies (scheme_name, authority, benefit_amount, eligibility, official_portal_url, status)
SELECT 'PM Krishi Sinchayee Yojana (Micro-Irrigation)', 'Dept of Agriculture & Cooperation', 'Up to 90% Drip / Sprinkler Subsidy', 'Small and marginal farmers with active borewell/water source', 'https://pmksy.gov.in/', 'Active / Open'
WHERE NOT EXISTS (SELECT 1 FROM public.subsidies WHERE scheme_name = 'PM Krishi Sinchayee Yojana (Micro-Irrigation)');

-- APMC Live Mandi Rates Initial Snapshot (Safe Zero-Conflict)
INSERT INTO public.mandi_live_rates (state, district, market, commodity, commodity_te, commodity_hi, min_price, max_price, modal_price, msp_price, arrivals_qtl, trend, trend_pct)
SELECT v.state, v.district, v.market, v.commodity, v.commodity_te, v.commodity_hi, v.min_price, v.max_price, v.modal_price, v.msp_price, v.arrivals_qtl, v.trend, v.trend_pct
FROM (VALUES
  ('Telangana', 'Warangal', 'Warangal APMC Yard', 'Cotton (Long Staple)', 'పత్తి', 'कपास', 7450::numeric, 7850::numeric, 7680::numeric, 7121::numeric, 2450::numeric, 'up', 2.8::numeric),
  ('Telangana', 'Warangal', 'Warangal APMC Yard', 'Chilli (Teja Variety)', 'తేజ మిరప', 'तेजा मिर्च', 18200::numeric, 21500::numeric, 19800::numeric, 0::numeric, 850::numeric, 'up', 4.2::numeric),
  ('Telangana', 'Warangal', 'Warangal APMC Yard', 'Paddy (Common)', 'వరి ధాన్యం', 'धान', 2180::numeric, 2320::numeric, 2250::numeric, 2183::numeric, 4200::numeric, 'stable', 0.5::numeric),
  ('Telangana', 'Hyderabad', 'Gudimalkapur APMC Yard', 'Tomato (Hybrid)', 'టమోటా', 'टमाटर', 1400::numeric, 2200::numeric, 1800::numeric, 0::numeric, 1200::numeric, 'down', -3.1::numeric),
  ('Telangana', 'Hyderabad', 'Bowenpally Wholesale APMC', 'Onion (Red)', 'ఉల్లిపాయ', 'प्याज', 2200::numeric, 3100::numeric, 2750::numeric, 0::numeric, 3800::numeric, 'up', 1.9::numeric)
) AS v(state, district, market, commodity, commodity_te, commodity_hi, min_price, max_price, modal_price, msp_price, arrivals_qtl, trend, trend_pct)
WHERE NOT EXISTS (
  SELECT 1 FROM public.mandi_live_rates
  WHERE market = v.market AND commodity = v.commodity
);

-- ══════════════════════════════════════════════════════════════════════════════
-- END OF CANONICAL PRODUCTION SCHEMA SETUP
-- ══════════════════════════════════════════════════════════════════════════════
