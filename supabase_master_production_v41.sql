-- =================================================================================================
-- NUKROPAI ENTERPRISE AGRARIAN INTELLIGENCE OS — MASTER PRODUCTION SCHEMA v5.1
-- Architect: Senior Supabase Database Architect
-- Fixes: Eliminates all "column farmer_id does not exist" and foreign key type mismatches.
-- Compatible with: Web emulator (nukrop_emulator.html), Mobile WebView (index.html), and API
-- =================================================================================================

-- STEP 0: EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- STEP 1: CLEAN SLATE (Safely drops all older conflicting tables with CASCADE)
DROP TABLE IF EXISTS public.machinery_messages CASCADE;
DROP TABLE IF EXISTS public.machinery_bookings CASCADE;
DROP TABLE IF EXISTS public.community_likes CASCADE;
DROP TABLE IF EXISTS public.post_likes CASCADE;
DROP TABLE IF EXISTS public.user_follows CASCADE;
DROP TABLE IF EXISTS public.community_comments CASCADE;
DROP TABLE IF EXISTS public.community_posts CASCADE;
DROP TABLE IF EXISTS public.equipment_rentals CASCADE;
DROP TABLE IF EXISTS public.khata_records CASCADE;
DROP TABLE IF EXISTS public.khata_entries CASCADE;
DROP TABLE IF EXISTS public.farm_khata_ledger CASCADE;
DROP TABLE IF EXISTS public.disease_scans CASCADE;
DROP TABLE IF EXISTS public.outbreak_alerts CASCADE;
DROP TABLE IF EXISTS public.mandi_live_rates CASCADE;
DROP TABLE IF EXISTS public.mandi_rates CASCADE;
DROP TABLE IF EXISTS public.mandi_alerts CASCADE;
DROP TABLE IF EXISTS public.truck_listings CASCADE;
DROP TABLE IF EXISTS public.truck_bookings CASCADE;
DROP TABLE IF EXISTS public.haul_bookings CASCADE;
DROP TABLE IF EXISTS public.subsidies CASCADE;
DROP TABLE IF EXISTS public.kcc_applications CASCADE;
DROP TABLE IF EXISTS public.biorx_recipes CASCADE;
DROP TABLE IF EXISTS public.biorx_batches CASCADE;
DROP TABLE IF EXISTS public.agristack_parcels CASCADE;
DROP TABLE IF EXISTS public.soil_health_cards CASCADE;
DROP TABLE IF EXISTS public.chat_messages CASCADE;
DROP TABLE IF EXISTS public.user_profiles CASCADE;
DROP TABLE IF EXISTS public.profiles CASCADE;
DROP TABLE IF EXISTS public.users CASCADE;

-- STEP 2: CREATE CORE PROFILE TABLES
CREATE TABLE public.profiles (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id TEXT,
    farmer_id TEXT DEFAULT 'NK-87621',
    email TEXT,
    full_name TEXT NOT NULL DEFAULT 'Farmer',
    phone TEXT DEFAULT '+91 98492 11048',
    phone_number TEXT DEFAULT '+91 98492 11048',
    avatar_url TEXT DEFAULT 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
    village TEXT DEFAULT 'Warangal Rural',
    district TEXT DEFAULT 'Warangal',
    mandal TEXT DEFAULT 'Kazipet',
    state TEXT DEFAULT 'Telangana',
    land_acres NUMERIC(6,2) DEFAULT 4.50,
    total_land_acres NUMERIC(6,2) DEFAULT 4.50,
    soil_type TEXT DEFAULT 'Black Cotton Soil',
    primary_crops TEXT[] DEFAULT ARRAY['cotton', 'chilli', 'paddy', 'tomato'],
    kcc_credit_limit NUMERIC(10,2) DEFAULT 150000.00,
    kcc_balance NUMERIC(10,2) DEFAULT 42500.00,
    agristack_id TEXT DEFAULT 'IN-TS-WRG-2026-88914',
    agristack_verified BOOLEAN DEFAULT true,
    biometric_lock BOOLEAN DEFAULT false,
    role TEXT DEFAULT 'farmer',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE public.user_profiles (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id TEXT,
    farmer_id TEXT DEFAULT 'NK-87621',
    email VARCHAR NOT NULL UNIQUE,
    full_name VARCHAR NOT NULL,
    phone_number VARCHAR DEFAULT '+91 98492 11048',
    state VARCHAR NOT NULL DEFAULT 'Telangana',
    district VARCHAR NOT NULL DEFAULT 'Warangal Rural',
    mandal VARCHAR DEFAULT 'Kazipet',
    village VARCHAR DEFAULT 'Kadipikonda',
    primary_crop VARCHAR DEFAULT 'Cotton & Chilli',
    farm_size_acres NUMERIC(6,2) DEFAULT 4.50,
    latitude DOUBLE PRECISION DEFAULT 18.5204,
    longitude DOUBLE PRECISION DEFAULT 73.8567,
    dharani_passbook TEXT DEFAULT 'T09280041289',
    kcc_active BOOLEAN DEFAULT true,
    kcc_sanctioned_limit NUMERIC(10,2) DEFAULT 150000.00,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- STEP 3: AGRISTACK & SOIL HEALTH
CREATE TABLE public.agristack_parcels (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    farmer_id TEXT DEFAULT 'NK-87621',
    user_id TEXT,
    survey_number VARCHAR(32) NOT NULL DEFAULT '142/A',
    khasra_number VARCHAR(32),
    khata_number VARCHAR(32),
    land_area_acres NUMERIC(8,2) NOT NULL DEFAULT 4.50,
    soil_classification VARCHAR(64) DEFAULT 'Black Cotton Soil',
    irrigation_source VARCHAR(64) DEFAULT 'Borewell + Drip',
    dharani_passbook_id VARCHAR(64) DEFAULT 'T09280041289',
    cadastral_geojson JSONB DEFAULT '{}'::jsonb,
    is_ror_verified BOOLEAN DEFAULT true,
    verified_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE TABLE public.soil_health_cards (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    farmer_id TEXT DEFAULT 'NK-87621',
    user_id TEXT,
    parcel_id TEXT,
    sample_code VARCHAR(32) DEFAULT 'SHC-2026-9921',
    ph_level NUMERIC(4,2) NOT NULL DEFAULT 7.20,
    organic_carbon_pct NUMERIC(4,2) NOT NULL DEFAULT 0.68,
    nitrogen_kg_ha NUMERIC(6,2) NOT NULL DEFAULT 240.00,
    phosphorus_kg_ha NUMERIC(6,2) NOT NULL DEFAULT 18.50,
    potassium_kg_ha NUMERIC(6,2) NOT NULL DEFAULT 310.00,
    zinc_ppm NUMERIC(5,2) DEFAULT 0.85,
    iron_ppm NUMERIC(5,2) DEFAULT 6.20,
    micronutrient_status JSONB DEFAULT '{"zn":"sufficient","fe":"sufficient","b":"medium"}'::jsonb,
    recommendations TEXT DEFAULT 'Apply Gypsum 200kg/acre; NPK balanced 19:19:19 recommended',
    tested_on DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- STEP 4: BIOSHIELD AI CROP DISEASE SCANS & OUTBREAKS
CREATE TABLE public.disease_scans (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    scan_id TEXT DEFAULT gen_random_uuid()::text,
    farmer_id TEXT DEFAULT 'NK-87621',
    user_id TEXT,
    crop_name TEXT NOT NULL DEFAULT 'Cotton',
    scan_type TEXT DEFAULT 'leaf',
    disease_name TEXT NOT NULL DEFAULT 'Healthy',
    disease_detected TEXT DEFAULT 'Healthy',
    confidence TEXT DEFAULT '96%',
    confidence_score NUMERIC(5,2) DEFAULT 96.00,
    severity TEXT DEFAULT 'MODERATE',
    pathogen TEXT DEFAULT 'Fungus',
    pathogen_type VARCHAR(32) DEFAULT 'Fungus',
    vector TEXT,
    treatment_chemical TEXT DEFAULT 'Profenofos 50% EC @ 2ml/L',
    treatment_organic TEXT DEFAULT 'Neem Oil 10,000 ppm @ 3ml/L',
    chemical_solution TEXT DEFAULT 'Profenofos 50% EC @ 2ml/L',
    organic_solution TEXT DEFAULT 'Neem Oil 10,000 ppm @ 3ml/L',
    remedy_summary TEXT,
    image_storage_path TEXT,
    location TEXT DEFAULT 'Warangal Rural, Telangana',
    latitude DOUBLE PRECISION DEFAULT 17.9689,
    longitude DOUBLE PRECISION DEFAULT 79.5941,
    gps_latitude NUMERIC(10,7) DEFAULT 17.9689,
    gps_longitude NUMERIC(10,7) DEFAULT 79.5941,
    notes TEXT,
    scanned_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE public.outbreak_alerts (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    target_state TEXT NOT NULL DEFAULT 'Telangana',
    crop_name TEXT NOT NULL DEFAULT 'Cotton',
    disease_name TEXT NOT NULL DEFAULT 'Pink Bollworm',
    severity TEXT DEFAULT 'HIGH',
    scan_count INT DEFAULT 12,
    is_active BOOLEAN DEFAULT true,
    alert_message TEXT DEFAULT 'High risk of Pink Bollworm outbreak detected in Warangal & Karimnagar districts.',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- STEP 5: BIORX ORGANIC FORMULATIONS & BATCH BREWS
CREATE TABLE public.biorx_recipes (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    title VARCHAR(128) NOT NULL,
    target_pest_disease TEXT[] NOT NULL,
    ingredients JSONB NOT NULL,
    preparation_steps JSONB NOT NULL,
    fermentation_hours INT DEFAULT 48,
    dilution_ratio VARCHAR(32) DEFAULT '1:10 (Water)',
    shelf_life_days INT DEFAULT 30,
    icar_approved BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE TABLE public.biorx_batches (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    farmer_id TEXT DEFAULT 'NK-87621',
    user_id TEXT,
    recipe_id TEXT,
    batch_liters NUMERIC(6,2) NOT NULL DEFAULT 50.00,
    brewed_on TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    ready_by TIMESTAMPTZ NOT NULL DEFAULT (NOW() + interval '48 hours'),
    current_status VARCHAR(32) DEFAULT 'FERMENTING',
    notes TEXT
);

-- STEP 6: MANDI APMC MARKET RATES & ALERTS
CREATE TABLE public.mandi_live_rates (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    state VARCHAR NOT NULL DEFAULT 'Telangana',
    district VARCHAR NOT NULL DEFAULT 'Warangal',
    market VARCHAR NOT NULL DEFAULT 'Warangal APMC Yard',
    commodity VARCHAR NOT NULL,
    commodity_te TEXT,
    commodity_hi TEXT,
    variety VARCHAR NOT NULL DEFAULT 'Standard',
    arrival_date DATE DEFAULT CURRENT_DATE,
    min_price NUMERIC(10,2) NOT NULL DEFAULT 0,
    max_price NUMERIC(10,2) NOT NULL DEFAULT 0,
    modal_price NUMERIC(10,2) NOT NULL DEFAULT 0,
    msp_price NUMERIC(10,2) DEFAULT 7121.00,
    arrivals_qtl NUMERIC(10,2) DEFAULT 1420.00,
    trend TEXT DEFAULT 'up',
    trend_pct NUMERIC(4,2) DEFAULT 2.80,
    price_date DATE DEFAULT CURRENT_DATE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE public.mandi_rates (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    mandi_name VARCHAR(64) NOT NULL DEFAULT 'Warangal APMC Yard',
    state VARCHAR(64) NOT NULL DEFAULT 'Telangana',
    district VARCHAR(64) NOT NULL DEFAULT 'Warangal',
    commodity VARCHAR(64) NOT NULL,
    variety VARCHAR(64) DEFAULT 'Common',
    modal_price NUMERIC(10,2) NOT NULL,
    min_price NUMERIC(10,2) NOT NULL,
    max_price NUMERIC(10,2) NOT NULL,
    arrival_tonnes NUMERIC(8,2) DEFAULT 0,
    recorded_date DATE DEFAULT CURRENT_DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE TABLE public.mandi_alerts (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    farmer_id TEXT DEFAULT 'NK-87621',
    user_id TEXT,
    commodity VARCHAR(64) NOT NULL,
    target_price NUMERIC(10,2) NOT NULL,
    condition VARCHAR(8) DEFAULT 'GTE',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- STEP 7: GRAMHAUL LOGISTICS & FLEET POOLING
CREATE TABLE public.truck_listings (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    transporter_id TEXT,
    driver_name VARCHAR(64) NOT NULL,
    driver_phone VARCHAR(16) NOT NULL,
    truck_type VARCHAR(32) NOT NULL,
    vehicle_plate VARCHAR(32) NOT NULL,
    capacity_tonnes NUMERIC(5,2) NOT NULL,
    available_capacity_tonnes NUMERIC(5,2) NOT NULL,
    current_mandi VARCHAR(64) NOT NULL,
    rate_per_km NUMERIC(6,2) NOT NULL,
    status VARCHAR(16) DEFAULT 'ACTIVE' NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE TABLE public.truck_bookings (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    farmer_id TEXT DEFAULT 'NK-87621',
    user_id TEXT,
    driver_name TEXT NOT NULL,
    driver_phone TEXT NOT NULL,
    vehicle TEXT NOT NULL DEFAULT 'Tata Ace (1.5 Ton)',
    from_loc TEXT NOT NULL,
    to_mandi TEXT NOT NULL,
    crop_name TEXT NOT NULL,
    quantity_qtl NUMERIC(8,2) NOT NULL DEFAULT 10,
    total_cost NUMERIC(10,2) NOT NULL DEFAULT 600,
    status TEXT DEFAULT 'confirmed',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE public.haul_bookings (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    farmer_id TEXT DEFAULT 'NK-87621',
    user_id TEXT,
    truck_id TEXT,
    pickup_village VARCHAR(64) NOT NULL,
    destination_mandi VARCHAR(64) NOT NULL,
    crop_name VARCHAR(64) NOT NULL,
    load_quintals NUMERIC(6,2) NOT NULL,
    agreed_fare NUMERIC(10,2) NOT NULL,
    status VARCHAR(32) DEFAULT 'PENDING' NOT NULL,
    pickup_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- STEP 8: FARM KHATA LEDGERS
CREATE TABLE public.khata_records (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    farmer_id TEXT DEFAULT 'NK-87621',
    user_id TEXT,
    crop_id TEXT NOT NULL DEFAULT 'cotton',
    type TEXT NOT NULL DEFAULT 'expense',
    category TEXT NOT NULL DEFAULT 'general',
    title TEXT NOT NULL,
    amount NUMERIC(10,2) NOT NULL DEFAULT 0,
    notes TEXT,
    record_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE public.khata_entries (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    farmer_id TEXT DEFAULT 'NK-87621',
    user_id TEXT,
    flow VARCHAR(16) NOT NULL DEFAULT 'EXPENSE',
    category VARCHAR(64) NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    counterparty_name VARCHAR(64) DEFAULT 'General',
    payment_mode VARCHAR(32) DEFAULT 'CASH' NOT NULL,
    receipt_image_url TEXT,
    notes TEXT,
    entry_date DATE DEFAULT CURRENT_DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

CREATE TABLE public.farm_khata_ledger (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    farmer_id TEXT DEFAULT 'NK-87621',
    user_id TEXT,
    transaction_type TEXT NOT NULL DEFAULT 'expense',
    category TEXT NOT NULL,
    amount NUMERIC(10,2) NOT NULL DEFAULT 0,
    description TEXT,
    transaction_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- STEP 9: KISAN CREDIT CARD & SUBSIDIES
CREATE TABLE public.subsidies (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    scheme_name TEXT NOT NULL,
    authority TEXT NOT NULL,
    benefit_amount TEXT NOT NULL,
    eligibility TEXT NOT NULL,
    official_portal_url TEXT NOT NULL,
    status TEXT DEFAULT 'Active / Open',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE public.kcc_applications (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    farmer_id TEXT DEFAULT 'NK-87621',
    user_id TEXT,
    scheme_code VARCHAR(32) NOT NULL,
    scheme_title VARCHAR(128) NOT NULL,
    requested_amount NUMERIC(12,2) NOT NULL,
    sanctioned_amount NUMERIC(12,2) DEFAULT 150000.00,
    interest_subvention_pct NUMERIC(4,2) DEFAULT 3.00,
    effective_roi_pct NUMERIC(4,2) DEFAULT 4.00,
    sanctioning_bank VARCHAR(64) DEFAULT 'SBI Agri Branch',
    application_stage VARCHAR(32) DEFAULT 'DISBURSED' NOT NULL,
    dbt_account_number VARCHAR(32),
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- STEP 10: MACHINERY & EQUIPMENT SHARING
CREATE TABLE public.equipment_rentals (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    owner_id TEXT,
    name TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'tractor',
    rate NUMERIC(10,2) NOT NULL DEFAULT 850,
    owner_name TEXT NOT NULL DEFAULT 'Balaji Agri Rentals',
    phone_number TEXT NOT NULL DEFAULT '+91 98480 22338',
    location TEXT NOT NULL DEFAULT 'Kazipet / Warangal',
    distance_str TEXT DEFAULT '2.5 km away',
    specs TEXT DEFAULT 'Verified Agrarian Implement · Available in Hub with certified operator',
    image_url TEXT,
    is_available BOOLEAN DEFAULT true,
    owner_email TEXT DEFAULT 'beyondtheearth75@gmail.com',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE public.machinery_messages (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    item_id TEXT NOT NULL,
    sender_type TEXT NOT NULL DEFAULT 'user',
    sender_name TEXT NOT NULL DEFAULT 'Farmer',
    recipient_name TEXT,
    message_text TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE public.machinery_bookings (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    booking_ref TEXT NOT NULL UNIQUE,
    machine_id TEXT NOT NULL,
    machine_name TEXT NOT NULL,
    farmer_name TEXT NOT NULL DEFAULT 'Farmer',
    farmer_phone TEXT NOT NULL DEFAULT '+91 98492 11048',
    farmer_village TEXT NOT NULL DEFAULT 'Warangal Rural',
    acreage NUMERIC(6,2) DEFAULT 2.0,
    total_amount NUMERIC(10,2) NOT NULL DEFAULT 0,
    booking_date DATE DEFAULT CURRENT_DATE,
    status TEXT NOT NULL DEFAULT 'DISPATCHED',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- STEP 11: KISAN COMMUNITY & SOCIAL Q&A
CREATE TABLE public.community_posts (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    author_id TEXT,
    user_id TEXT,
    farmer_id TEXT DEFAULT 'NK-87621',
    author_name TEXT NOT NULL DEFAULT 'Farmer',
    author_village TEXT DEFAULT 'Warangal, Telangana',
    avatar_url TEXT DEFAULT 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
    crop_id TEXT NOT NULL DEFAULT 'cotton',
    crop_tag VARCHAR(32) DEFAULT 'cotton',
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    body TEXT,
    media_url TEXT,
    media_type TEXT DEFAULT 'none',
    media_label TEXT DEFAULT 'Field Photo',
    likes_count INTEGER NOT NULL DEFAULT 0,
    comments_count INTEGER NOT NULL DEFAULT 0,
    upvotes INT DEFAULT 0,
    is_verified BOOLEAN DEFAULT true,
    is_resolved BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE public.community_comments (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    post_id TEXT NOT NULL REFERENCES public.community_posts(id) ON DELETE CASCADE,
    author_id TEXT,
    user_id TEXT,
    farmer_id TEXT,
    author_name TEXT NOT NULL DEFAULT 'Farmer',
    author_role TEXT DEFAULT 'Progressive Farmer',
    avatar_url TEXT DEFAULT 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
    content TEXT NOT NULL,
    comment_body TEXT,
    is_icar_expert BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE public.community_likes (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    post_id TEXT NOT NULL REFERENCES public.community_posts(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL,
    farmer_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT unique_post_user_like UNIQUE (post_id, user_id)
);

CREATE TABLE public.post_likes (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    post_id TEXT NOT NULL REFERENCES public.community_posts(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT unique_post_likes UNIQUE (post_id, user_id)
);

CREATE TABLE public.user_follows (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    follower_id TEXT NOT NULL,
    following_id TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT unique_user_follows UNIQUE (follower_id, following_id)
);

-- STEP 12: CHAT MESSAGES
CREATE TABLE public.chat_messages (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    farmer_id TEXT DEFAULT 'NK-87621',
    user_id TEXT,
    session_id VARCHAR(64) NOT NULL,
    role VARCHAR(16) NOT NULL,
    message_text TEXT NOT NULL,
    tokens_consumed INT DEFAULT 0,
    language VARCHAR(8) DEFAULT 'en',
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- STEP 13: AUTOMATED ATOMIC RPC FUNCTIONS
CREATE OR REPLACE FUNCTION public.increment_post_likes(post_id TEXT)
RETURNS void AS $$
BEGIN
    UPDATE public.community_posts
    SET likes_count = COALESCE(likes_count, 0) + 1,
        upvotes = COALESCE(upvotes, 0) + 1,
        updated_at = NOW()
    WHERE id = post_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION public.increment_post_likes(p_post_id TEXT, p_delta INT)
RETURNS INT AS $$
DECLARE
    v_new_likes INT;
BEGIN
    UPDATE public.community_posts
    SET likes_count = GREATEST(0, COALESCE(likes_count, 0) + p_delta),
        upvotes = GREATEST(0, COALESCE(upvotes, 0) + p_delta),
        updated_at = NOW()
    WHERE id = p_post_id
    RETURNING likes_count INTO v_new_likes;

    RETURN COALESCE(v_new_likes, 0);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION public.get_farmer_dashboard_summary(p_farmer_id TEXT)
RETURNS JSONB AS $$
DECLARE
    v_total_income NUMERIC(12,2) := 0;
    v_total_expense NUMERIC(12,2) := 0;
    v_total_scans INT := 0;
    v_active_kcc NUMERIC(12,2) := 0;
    v_land_acres NUMERIC(8,2) := 0;
BEGIN
    SELECT COALESCE(SUM(amount), 0) INTO v_total_income
    FROM public.khata_records
    WHERE type = 'income' AND (farmer_id = p_farmer_id OR user_id = p_farmer_id);

    SELECT COALESCE(SUM(amount), 0) INTO v_total_expense
    FROM public.khata_records
    WHERE type = 'expense' AND (farmer_id = p_farmer_id OR user_id = p_farmer_id);

    SELECT COUNT(*) INTO v_total_scans
    FROM public.disease_scans
    WHERE farmer_id = p_farmer_id OR user_id = p_farmer_id;

    SELECT COALESCE(MAX(sanctioned_amount), 150000.00) INTO v_active_kcc
    FROM public.kcc_applications;

    SELECT COALESCE(SUM(land_area_acres), 4.50) INTO v_land_acres
    FROM public.agristack_parcels;

    RETURN jsonb_build_object(
        'total_income', v_total_income,
        'total_expense', v_total_expense,
        'net_khata_balance', (v_total_income - v_total_expense),
        'total_scans_performed', v_total_scans,
        'kcc_sanctioned_limit', v_active_kcc,
        'verified_acres', v_land_acres
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- STEP 14: ROW LEVEL SECURITY (RLS) OPEN ACCESS POLICIES
DO $$ 
DECLARE
    tbl text;
BEGIN
    FOR tbl IN 
        SELECT tablename FROM pg_tables 
        WHERE schemaname = 'public'
    LOOP
        EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', tbl);
        EXECUTE format('DROP POLICY IF EXISTS "Public access on %I" ON public.%I', tbl, tbl);
        EXECUTE format('CREATE POLICY "Public access on %I" ON public.%I FOR ALL TO anon, authenticated, service_role USING (true) WITH CHECK (true)', tbl, tbl);
    END LOOP;
END $$;

GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated, service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated, service_role;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO anon, authenticated, service_role;

-- STEP 15: REALTIME PUBLICATION SETUP
DO $$
BEGIN
    ALTER PUBLICATION supabase_realtime ADD TABLE 
        public.community_posts, 
        public.community_comments, 
        public.community_likes, 
        public.machinery_messages, 
        public.machinery_bookings,
        public.khata_records,
        public.mandi_live_rates,
        public.truck_listings,
        public.truck_bookings,
        public.disease_scans;
EXCEPTION WHEN OTHERS THEN
    NULL;
END $$;

-- STEP 16: SEED PRODUCTION DATA
INSERT INTO public.profiles (
    email, full_name, phone, phone_number, village, district, state,
    land_acres, total_land_acres, soil_type, primary_crops, kcc_credit_limit, kcc_balance, agristack_id, farmer_id
) VALUES (
    'beyondtheearth75@gmail.com', 'B. Jaswanth Reddy', '+91 98492 11048', '+91 98492 11048',
    'Warangal Rural', 'Warangal', 'Telangana', 4.50, 4.50, 'Black Cotton Soil',
    ARRAY['cotton', 'chilli', 'paddy', 'tomato'], 150000.00, 42500.00, 'IN-TS-WRG-2026-88914', 'NK-87621'
);

INSERT INTO public.user_profiles (
    email, full_name, phone_number, state, district, mandal, village,
    primary_crop, farm_size_acres, dharani_passbook, kcc_active, kcc_sanctioned_limit, farmer_id
) VALUES (
    'beyondtheearth75@gmail.com', 'B. Jaswanth Reddy', '+91 98492 11048', 
    'Telangana', 'Warangal Rural', 'Kazipet', 'Kadipikonda',
    'Cotton & Chilli', 4.50, 'T09280041289', true, 150000.00, 'NK-87621'
) ON CONFLICT (email) DO NOTHING;

INSERT INTO public.mandi_live_rates (
    commodity, commodity_te, commodity_hi, variety, market, district, state,
    arrival_date, min_price, max_price, modal_price, msp_price, arrivals_qtl,
    trend, trend_pct, price_date
) VALUES
('Cotton', 'పత్తి', 'कपास', 'MCU-5 Medium Staple', 'Warangal APMC Yard', 'Warangal', 'Telangana', CURRENT_DATE, 7150.00, 7780.00, 7480.00, 7121.00, 1850.00, 'up', 2.80, CURRENT_DATE),
('Chilli', 'మిరప', 'मिर्च', 'Teja / Guntur Best', 'Enumamula APMC Yard', 'Warangal', 'Telangana', CURRENT_DATE, 18200.00, 22400.00, 20500.00, 13000.00, 3200.00, 'up', 4.50, CURRENT_DATE),
('Paddy', 'వరి / ధాన్యం', 'धान', 'BPT 5204 (Sona Masoori)', 'Kesamudram APMC', 'Mahabubabad', 'Telangana', CURRENT_DATE, 2280.00, 2450.00, 2380.00, 2183.00, 4100.00, 'up', 1.20, CURRENT_DATE),
('Tomato', 'టమాటా', 'टमाटर', 'Hybrid Red Round', 'Bowenpally APMC', 'Hyderabad', 'Telangana', CURRENT_DATE, 1600.00, 2200.00, 1950.00, 1400.00, 890.00, 'up', 5.00, CURRENT_DATE),
('Maize', 'మొక్కజొన్న', 'मक्का', 'Yellow Feed Grade', 'Warangal APMC Yard', 'Warangal', 'Telangana', CURRENT_DATE, 2150.00, 2320.00, 2240.00, 2090.00, 1100.00, 'down', 1.10, CURRENT_DATE),
('Wheat', 'గోధుమ', 'गेहूं', 'Lokwan Sharbati', 'Nizamabad APMC', 'Nizamabad', 'Telangana', CURRENT_DATE, 2400.00, 2650.00, 2520.00, 2275.00, 620.00, 'up', 0.80, CURRENT_DATE),
('Potato', 'బంగాళాదుంప', 'आलू', 'Kufri Jyoti', 'Agra APMC Yard', 'Agra', 'Uttar Pradesh', CURRENT_DATE, 1250.00, 1580.00, 1420.00, 1200.00, 2100.00, 'up', 1.50, CURRENT_DATE),
('Onion', 'ఉల్లిపాయ', 'प्याज', 'Nashik Red Pol', 'Lasalgaon APMC', 'Nashik', 'Maharashtra', CURRENT_DATE, 12800.00, 16200.00, 14500.00, 9500.00, 4500.00, 'up', 3.20, CURRENT_DATE);

INSERT INTO public.truck_listings (
    driver_name, driver_phone, truck_type, vehicle_plate, capacity_tonnes, available_capacity_tonnes, current_mandi, rate_per_km, status
) VALUES
('Ramesh Yadav', '+91 98490 22338', 'Tata Ace (1.5 Ton)', 'TS-03-UB-4491', 1.50, 1.50, 'Warangal APMC Yard', 24.00, 'ACTIVE'),
('Srinivas Rao', '+91 94401 55667', 'Eicher Pro 2049 (4 Ton)', 'TS-09-EA-8821', 4.00, 3.20, 'Enumamula APMC Yard', 38.00, 'ACTIVE'),
('Balwinder Singh', '+91 98665 11223', 'Ashok Leyland 1616 (12 Ton)', 'TS-08-TR-1029', 12.00, 8.50, 'Kesamudram APMC', 65.00, 'ACTIVE');

INSERT INTO public.equipment_rentals (
    name, category, rate, owner_name, phone_number, location, distance_str, specs, image_url, is_available
) VALUES
('Mahindra 575 DI Tractor (45 HP)', 'tractor', 750, 'Balaji Agri Rentals', '+91 98480 22338', 'Kazipet Bypass, Warangal', '2.5 km away', 'Heavy-duty 45HP tractor with rotavator and 3-bottom reversible disc plough. Certified driver included.', 'https://images.unsplash.com/photo-1592982537447-7440770cbfc9?w=400&auto=format&fit=crop&q=80', true),
('Garuda / AgriBot 16L Drone Sprayer', 'drone', 450, 'Telangana Drone Seva Kendra', '+91 94401 55667', 'Hunter Road, Hanamkonda', '4.1 km away', 'DGCA Certified agri-drone with centimeter-accurate RTK GPS and 16L active spray tank. Covers 1 acre in 6 minutes.', 'https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=400&auto=format&fit=crop&q=80', true),
('John Deere 4-Wheel Harvester', 'harvester', 1800, 'Kisan Krishi Sahayak', '+91 98665 11223', 'Enumamula Market Yard', '5.8 km away', 'Multi-crop combine harvester for Paddy and Maize. Clean grain separation with zero grain breakage.', 'https://images.unsplash.com/photo-1592982537447-7440770cbfc9?w=400&auto=format&fit=crop&q=80', true);

INSERT INTO public.subsidies (scheme_name, authority, benefit_amount, eligibility, official_portal_url, status)
VALUES
('PM-KISAN Samman Nidhi', 'Central Govt (Ministry of Agriculture)', '₹6,000 / year (3 equal installments)', 'All landholding farmer families across India', 'https://pmkisan.gov.in', 'Active / 17th Installment Open'),
('Pradhan Mantri Fasal Bima Yojana (PMFBY)', 'Central Govt & Agriculture Dept', 'Up to 90% crop loss claim coverage', 'All farmers growing notified crops', 'https://pmfby.gov.in', 'Kharif 2026 Enrollment Live'),
('Rythu Bandhu Investment Support', 'Govt of Telangana', '₹10,000 / acre per year', 'Pattedar farmers with Digital RoR in Telangana', 'https://rythubandhu.telangana.gov.in', 'Season Disbursement Active'),
('Kisan Credit Card (KCC) Subvention', 'NABARD & Commercial Banks', 'Credit limit up to ₹3.0 Lakh @ 4% p.a.', 'All farmers, sharecroppers, self-help groups', 'https://pmkisan.gov.in/KCC.aspx', 'Instant Bank Approvals');

INSERT INTO public.community_posts (
    id, author_name, author_village, avatar_url, crop_id, crop_tag,
    title, content, body, media_url, media_type, media_label,
    likes_count, comments_count, upvotes, is_verified, is_resolved
) VALUES
('post-cotton-1', 'Raju Naidu', 'Geesugonda (4.5 Acres)', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80', 'cotton', 'cotton', 'Pink bollworm in 45-day Cotton crop. Is Profenofos 50% EC working well?', 'Found 3 rosette flowers per 20 plants. Also noticed small pink larvae inside bolls. Weather is humid (88%). What dosage should I spray with power sprayer? Should I mix Neem Oil?', 'Found 3 rosette flowers per 20 plants. Also noticed small pink larvae inside bolls. Weather is humid (88%). What dosage should I spray with power sprayer? Should I mix Neem Oil?', 'https://images.unsplash.com/photo-1605000797499-95a51c5269ae?w=600&auto=format&fit=crop&q=80', 'image', '1 Field Photo', 28, 2, 28, true, false),
('post-chilli-2', 'Anil Kumar', 'Wardhannapet (3.2 Acres)', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80', 'chilli', 'chilli', 'Black Thrips control with Dashaparni Kashayam - 100% Organic results!', 'Sprayed homemade Dashaparni Kashayam (cow urine, neem, custard apple leaf, calotropis). Within 4 days, terminal leaf curl stopped and new tender leaves emerged completely healthy.', 'Sprayed homemade Dashaparni Kashayam (cow urine, neem, custard apple leaf, calotropis). Within 4 days, terminal leaf curl stopped and new tender leaves emerged completely healthy.', 'https://images.unsplash.com/photo-1592417817098-8f3d6910985c?w=600&auto=format&fit=crop&q=80', 'image', '1 Field Photo', 45, 1, 45, true, true);

INSERT INTO public.community_comments (id, post_id, author_name, author_role, avatar_url, content, comment_body, is_icar_expert)
VALUES
('comm-1', 'post-cotton-1', 'Dr. Srinivas (Agronomist, KVK)', 'Verified ICAR Scientist', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80', 'Spray Profenofos 50% EC @ 2ml/L water immediately. Also install 4 Pheromone traps per acre to monitor moth catches.', 'Spray Profenofos 50% EC @ 2ml/L water immediately. Also install 4 Pheromone traps per acre to monitor moth catches.', true),
('comm-2', 'post-cotton-1', 'B. Jaswanth Reddy', 'Progressive Farmer', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80', 'I had the same issue last week in Geesugonda. Neemazal 10,000 ppm mixed with Profenofos worked wonders. Spray before 9 AM.', 'I had the same issue last week in Geesugonda. Neemazal 10,000 ppm mixed with Profenofos worked wonders. Spray before 9 AM.', false);
