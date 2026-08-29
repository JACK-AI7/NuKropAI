-- ============================================================================
-- NuKropAI Enterprise AgriTech Expansion (7 Consolidated Modules)
-- ============================================================================

-- 1. BioShield Spatial-Temporal Outbreak Clusters & Geo-Fences
CREATE TABLE IF NOT EXISTS spatial_outbreak_clusters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    disease_name TEXT NOT NULL,
    crop_name TEXT NOT NULL,
    center_latitude DOUBLE PRECISION NOT NULL,
    center_longitude DOUBLE PRECISION NOT NULL,
    radius_km DOUBLE PRECISION DEFAULT 10.0,
    scan_count INT DEFAULT 1,
    severity_level TEXT CHECK (severity_level IN ('LOW', 'MODERATE', 'HIGH', 'CRITICAL')) DEFAULT 'MODERATE',
    microclimate_risk_score DOUBLE PRECISION DEFAULT 0.75,
    bio_defense_protocol TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_spatial_clusters_active ON spatial_outbreak_clusters (is_active, disease_name);

-- 2. MandiPilot Arbitrage Quotes & Price Discovery
CREATE TABLE IF NOT EXISTS mandi_arbitrage_quotes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    commodity TEXT NOT NULL,
    variety TEXT DEFAULT 'Standard',
    origin_district TEXT NOT NULL,
    origin_state TEXT NOT NULL,
    mandi_name TEXT NOT NULL,
    distance_km DOUBLE PRECISION NOT NULL,
    modal_price DOUBLE PRECISION NOT NULL,
    estimated_freight DOUBLE PRECISION NOT NULL,
    apmc_cess DOUBLE PRECISION NOT NULL,
    transit_spoilage_cost DOUBLE PRECISION NOT NULL,
    net_realized_price DOUBLE PRECISION NOT NULL,
    arbitrage_spread DOUBLE PRECISION DEFAULT 0.0,
    forecast_7d_trend TEXT DEFAULT 'BULLISH',
    forecast_15d_price DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. GramHaul Shared Rural Logistics
CREATE TABLE IF NOT EXISTS gramhaul_trips (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    driver_name TEXT NOT NULL,
    driver_phone TEXT NOT NULL,
    vehicle_type TEXT CHECK (vehicle_type IN ('PICKUP_TRUCK', 'TRACTOR_TROLLEY', 'MINI_TRUCK', 'COLD_CHAIN_VAN')) NOT NULL,
    total_capacity_quintals DOUBLE PRECISION NOT NULL,
    booked_capacity_quintals DOUBLE PRECISION DEFAULT 0.0,
    origin_hub TEXT NOT NULL,
    destination_mandi TEXT NOT NULL,
    total_distance_km DOUBLE PRECISION NOT NULL,
    base_fare DOUBLE PRECISION NOT NULL,
    is_cold_chain BOOLEAN DEFAULT FALSE,
    status TEXT CHECK (status IN ('OPEN', 'FULL', 'DISPATCHED', 'COMPLETED', 'CANCELLED')) DEFAULT 'OPEN',
    departure_time TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS gramhaul_load_bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trip_id UUID REFERENCES gramhaul_trips(id) ON DELETE CASCADE,
    farmer_id TEXT NOT NULL,
    commodity TEXT NOT NULL,
    weight_quintals DOUBLE PRECISION NOT NULL,
    allocated_fare DOUBLE PRECISION NOT NULL,
    pickup_point TEXT NOT NULL,
    booking_status TEXT DEFAULT 'CONFIRMED',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. AgriStack Sovereign Soil & Farm Health Passports
CREATE TABLE IF NOT EXISTS agristack_passports (
    farmer_id TEXT PRIMARY KEY,
    farmer_name TEXT NOT NULL,
    aadhaar_hash TEXT,
    survey_number TEXT NOT NULL,
    village TEXT NOT NULL,
    district TEXT NOT NULL,
    state TEXT NOT NULL,
    total_land_acres DOUBLE PRECISION NOT NULL,
    primary_crops TEXT[] DEFAULT '{}',
    agri_credit_score INT CHECK (agri_credit_score BETWEEN 300 AND 900) DEFAULT 720,
    pm_kisan_verified BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS soil_health_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id TEXT REFERENCES agristack_passports(farmer_id) ON DELETE CASCADE,
    nitrogen_kg_per_ha DOUBLE PRECISION NOT NULL,
    phosphorus_kg_per_ha DOUBLE PRECISION NOT NULL,
    potassium_kg_per_ha DOUBLE PRECISION NOT NULL,
    soil_ph DOUBLE PRECISION NOT NULL,
    organic_carbon_pct DOUBLE PRECISION NOT NULL,
    zinc_ppm DOUBLE PRECISION NOT NULL,
    iron_ppm DOUBLE PRECISION NOT NULL,
    boron_ppm DOUBLE PRECISION NOT NULL,
    overall_fertility_index TEXT CHECK (overall_fertility_index IN ('OPTIMAL', 'MODERATE', 'DEPLETED')) DEFAULT 'OPTIMAL',
    tested_date DATE NOT NULL DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. YantraShare Machinery Telematics & Escrow
CREATE TABLE IF NOT EXISTS yantrashare_telematics (
    equipment_id TEXT PRIMARY KEY,
    equipment_name TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    category TEXT NOT NULL,
    current_lat DOUBLE PRECISION,
    current_lon DOUBLE PRECISION,
    engine_hours_total DOUBLE PRECISION DEFAULT 0.0,
    fuel_level_pct INT DEFAULT 100,
    battery_health_pct INT DEFAULT 100,
    is_geofenced BOOLEAN DEFAULT TRUE,
    last_service_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS yantrashare_escrow (
    booking_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    equipment_id TEXT REFERENCES yantrashare_telematics(equipment_id),
    renter_id TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    total_amount DOUBLE PRECISION NOT NULL,
    escrow_status TEXT CHECK (escrow_status IN ('LOCKED', 'OPERATING', 'RELEASED_TO_OWNER', 'REFUNDED_TO_RENTER')) DEFAULT 'LOCKED',
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    rating_by_renter INT CHECK (rating_by_renter BETWEEN 1 AND 5),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. BioRx Regenerative Prescriptions
CREATE TABLE IF NOT EXISTS biorx_prescriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    farmer_id TEXT NOT NULL,
    crop_name TEXT NOT NULL,
    growth_stage TEXT NOT NULL,
    farm_acreage DOUBLE PRECISION NOT NULL,
    formulation_name TEXT NOT NULL,
    raw_ingredients JSONB NOT NULL,
    dilution_ratio TEXT NOT NULL,
    application_method TEXT NOT NULL,
    target_pest_or_soil TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
