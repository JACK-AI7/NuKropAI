-- Database Initialization Schema for NuKropAI Enterprise
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users Table
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'buyer' CHECK (role IN ('farmer', 'buyer', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);

-- 2. Refresh Tokens Table for JWT rotation
CREATE TABLE IF NOT EXISTS public.refresh_tokens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    revoked BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_refresh_tokens_hash ON public.refresh_tokens(token_hash);
CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user ON public.refresh_tokens(user_id);

-- 3. Mandi Live Rates Table
CREATE TABLE IF NOT EXISTS public.mandi_live_rates (
    id SERIAL PRIMARY KEY,
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    market VARCHAR(100) NOT NULL,
    commodity VARCHAR(100) NOT NULL,
    variety VARCHAR(100) NOT NULL,
    arrival_date VARCHAR(50) NOT NULL,
    min_price NUMERIC(12, 2) NOT NULL,
    max_price NUMERIC(12, 2) NOT NULL,
    modal_price NUMERIC(12, 2) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_mandi_commodity ON public.mandi_live_rates(commodity);
CREATE INDEX IF NOT EXISTS idx_mandi_state_district ON public.mandi_live_rates(state, district);

-- 4. Pest Outbreaks Table (Radar Network)
CREATE TABLE IF NOT EXISTS public.pest_outbreaks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pest_name VARCHAR(100) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    reporter_id UUID REFERENCES public.users(id) ON DELETE SET NULL,
    reported_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    wind_direction VARCHAR(50) NOT NULL DEFAULT 'East',
    wind_speed NUMERIC(5, 2) NOT NULL DEFAULT 12.0
);
CREATE INDEX IF NOT EXISTS idx_pest_outbreaks_coords ON public.pest_outbreaks(latitude, longitude);

-- 5. Soil Telemetry Table (Subsoil Probe)
CREATE TABLE IF NOT EXISTS public.soil_telemetry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    nitrogen INTEGER NOT NULL CHECK (nitrogen >= 0),
    phosphorus INTEGER NOT NULL CHECK (phosphorus >= 0),
    potassium INTEGER NOT NULL CHECK (potassium >= 0),
    ph NUMERIC(3,1) NOT NULL CHECK (ph BETWEEN 0.0 AND 14.0),
    organic_carbon NUMERIC(4,2) NOT NULL CHECK (organic_carbon >= 0.0),
    moisture INTEGER NOT NULL CHECK (moisture BETWEEN 0 AND 100),
    logged_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_soil_telemetry_user_logged ON public.soil_telemetry(user_id, logged_at DESC);

-- 6. Valve Operations (Smart Micro-Irrigation)
CREATE TABLE IF NOT EXISTS public.valve_operations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    valve_name VARCHAR(100) NOT NULL,
    state VARCHAR(20) NOT NULL CHECK (state IN ('OPEN', 'CLOSED')),
    flow_rate NUMERIC(4,1) NOT NULL DEFAULT 0.0,
    triggered_by VARCHAR(50) NOT NULL DEFAULT 'manual',
    logged_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_valve_ops_name_logged ON public.valve_operations(valve_name, logged_at DESC);

-- 7. Escrow Contracts (Blockchain Smart Contracts)
CREATE TABLE IF NOT EXISTS public.escrow_contracts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contract_address VARCHAR(100) UNIQUE NOT NULL,
    buyer_name VARCHAR(255) NOT NULL,
    commodity VARCHAR(100) NOT NULL,
    amount NUMERIC(15, 2) NOT NULL CHECK (amount > 0.0),
    funds_status VARCHAR(20) NOT NULL DEFAULT 'LOCKED' CHECK (funds_status IN ('LOCKED', 'RELEASED', 'REFUNDED')),
    qr_verification_code VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    verified_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS idx_escrow_contracts_address ON public.escrow_contracts(contract_address);
CREATE INDEX IF NOT EXISTS idx_escrow_contracts_status ON public.escrow_contracts(funds_status);

-- 8. Crop Simulations (What-If Crop Simulation Sandbox)
CREATE TABLE IF NOT EXISTS public.crop_simulations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    crop_name VARCHAR(100) NOT NULL,
    field_size NUMERIC(5,2) NOT NULL CHECK (field_size > 0.0),
    yield_loss_risk INTEGER NOT NULL CHECK (yield_loss_risk BETWEEN 0 AND 100),
    recommendation TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_crop_simulations_user ON public.crop_simulations(user_id);

-- 9. IoT Devices Registry (Tuya, Shelly, MQTT, GSM)
CREATE TABLE IF NOT EXISTS public.iot_devices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    device_name VARCHAR(100) NOT NULL,
    provider VARCHAR(50) NOT NULL CHECK (provider IN ('tuya', 'shelly', 'mqtt', 'gsm', 'custom')),
    provider_device_id VARCHAR(255) NOT NULL,
    provider_config JSONB DEFAULT '{}'::jsonb, -- Store SSID, Broker URL, API Keys
    status VARCHAR(20) NOT NULL DEFAULT 'offline' CHECK (status IN ('online', 'offline', 'fault')),
    last_heartbeat TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_iot_devices_farmer ON public.iot_devices(farmer_id);
CREATE INDEX IF NOT EXISTS idx_iot_devices_provider_id ON public.iot_devices(provider_device_id);

-- 10. IoT Telemetry Logs
CREATE TABLE IF NOT EXISTS public.iot_telemetry_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID NOT NULL REFERENCES public.iot_devices(id) ON DELETE CASCADE,
    voltage NUMERIC(5,2),
    amperage NUMERIC(5,2),
    moisture NUMERIC(5,2),
    raw_payload JSONB NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_iot_telemetry_device_time ON public.iot_telemetry_logs(device_id, timestamp DESC);

-- 11. IoT Command Queue (State Verification Engine)
CREATE TABLE IF NOT EXISTS public.iot_commands_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID NOT NULL REFERENCES public.iot_devices(id) ON DELETE CASCADE,
    command VARCHAR(100) NOT NULL,
    payload JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'verification', 'running', 'failed', 'completed')),
    queued_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS idx_iot_commands_status ON public.iot_commands_queue(status);

-- 12. IoT Automation Rules (Rule Engine)
CREATE TABLE IF NOT EXISTS public.iot_automation_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID NOT NULL REFERENCES public.iot_devices(id) ON DELETE CASCADE,
    rule_name VARCHAR(100) NOT NULL,
    condition_config JSONB NOT NULL, -- e.g., {"metric": "moisture", "op": "<", "value": 35}
    action_config JSONB NOT NULL,    -- e.g., {"command": "MOTOR_ON", "duration_mins": 15}
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 13. Event Sourcing Table for strict IoT audit trailing
CREATE TABLE IF NOT EXISTS public.device_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID NOT NULL REFERENCES public.iot_devices(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL CHECK (event_type IN ('COMMAND_ISSUED', 'TELEMETRY_RECEIVED', 'FAULT_DETECTED', 'STATE_CONFIRMED', 'PROTECTION_TRIGGERED')),
    payload JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_device_events_device_time ON public.device_events(device_id, created_at DESC);

-- 14. Multi-Tenant Organizations (Cooperatives/Agri-Businesses)
CREATE TABLE IF NOT EXISTS public.organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('cooperative', 'enterprise', 'individual')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 15. Organization Members (RBAC)
CREATE TABLE IF NOT EXISTS public.org_members (
    org_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL CHECK (role IN ('owner', 'admin', 'operator', 'viewer')),
    PRIMARY KEY (org_id, user_id)
);

-- 16. Farm Zones (Physical Graph Topology)
CREATE TABLE IF NOT EXISTS public.farm_zones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    org_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    crop_type VARCHAR(100),
    area_hectares NUMERIC(6,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_farm_zones_org ON public.farm_zones(org_id);

-- 17. Irrigation Topology (Pump -> Valve -> Zone Graph)
CREATE TABLE IF NOT EXISTS public.irrigation_topology (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_device_id UUID NOT NULL REFERENCES public.iot_devices(id) ON DELETE CASCADE, -- e.g., The Pump
    target_device_id UUID REFERENCES public.iot_devices(id) ON DELETE CASCADE, -- e.g., The Valve (Optional)
    farm_zone_id UUID NOT NULL REFERENCES public.farm_zones(id) ON DELETE CASCADE,
    flow_capacity_lph NUMERIC(8,2) NOT NULL DEFAULT 0.0, -- Liters per hour
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 18. Dead Letter Queue (DLQ) for failed/corrupted IoT Telemetry
CREATE TABLE IF NOT EXISTS public.device_dlq (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID REFERENCES public.iot_devices(id) ON DELETE SET NULL,
    error_reason TEXT NOT NULL,
    raw_payload JSONB NOT NULL,
    logged_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE INDEX IF NOT EXISTS idx_device_dlq_unresolved ON public.device_dlq(resolved) WHERE resolved = FALSE;

-- 19. Edge Node Identity & Trust (mTLS Certificates)
CREATE TABLE IF NOT EXISTS public.edge_identities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    mac_address VARCHAR(100) UNIQUE NOT NULL,
    org_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    cert_fingerprint VARCHAR(255) NOT NULL,

-- 9. IoT Devices Registry (Tuya, Shelly, MQTT, GSM)
CREATE TABLE IF NOT EXISTS public.iot_devices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    farm_zone_id UUID REFERENCES public.farm_zones(id) ON DELETE SET NULL, -- Enforcing topology
    device_name VARCHAR(100) NOT NULL,
    provider VARCHAR(50) NOT NULL CHECK (provider IN ('tuya', 'shelly', 'mqtt', 'gsm', 'custom')),
    provider_device_id VARCHAR(255) NOT NULL,
    provider_config JSONB DEFAULT '{}'::jsonb, -- Store SSID, Broker URL, API Keys
    status VARCHAR(20) NOT NULL DEFAULT 'offline' CHECK (status IN ('online', 'offline', 'fault')),
    last_heartbeat TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_iot_devices_farmer ON public.iot_devices(farmer_id);
CREATE INDEX IF NOT EXISTS idx_iot_devices_zone ON public.iot_devices(farm_zone_id);
CREATE INDEX IF NOT EXISTS idx_iot_devices_provider_id ON public.iot_devices(provider_device_id);

-- 10. IoT Telemetry Logs
CREATE TABLE IF NOT EXISTS public.iot_telemetry_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID NOT NULL REFERENCES public.iot_devices(id) ON DELETE CASCADE,
    voltage NUMERIC(5,2),
    amperage NUMERIC(5,2),
    moisture NUMERIC(5,2),
    raw_payload JSONB NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_iot_telemetry_device_time ON public.iot_telemetry_logs(device_id, timestamp DESC);

-- 11. IoT Command Queue (State Verification Engine)
CREATE TABLE IF NOT EXISTS public.iot_commands_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID NOT NULL REFERENCES public.iot_devices(id) ON DELETE CASCADE,
    command VARCHAR(100) NOT NULL,
    payload JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'verification', 'running', 'failed', 'completed')),
    queued_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS idx_iot_commands_status ON public.iot_commands_queue(status);

-- 12. IoT Automation Rules (Rule Engine)
CREATE TABLE IF NOT EXISTS public.iot_automation_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID NOT NULL REFERENCES public.iot_devices(id) ON DELETE CASCADE,
    rule_name VARCHAR(100) NOT NULL,
    condition_config JSONB NOT NULL, -- e.g., {"metric": "moisture", "op": "<", "value": 35}
    action_config JSONB NOT NULL,    -- e.g., {"command": "MOTOR_ON", "duration_mins": 15}
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 13. Event Sourcing Table for strict IoT audit trailing
CREATE TABLE IF NOT EXISTS public.device_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID NOT NULL REFERENCES public.iot_devices(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL CHECK (event_type IN ('COMMAND_ISSUED', 'TELEMETRY_RECEIVED', 'FAULT_DETECTED', 'STATE_CONFIRMED', 'PROTECTION_TRIGGERED')),
    payload JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_device_events_device_time ON public.device_events(device_id, created_at DESC);

-- 14. Multi-Tenant Organizations (Cooperatives/Agri-Businesses)
CREATE TABLE IF NOT EXISTS public.organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('cooperative', 'enterprise', 'individual')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 15. Organization Members (RBAC)
CREATE TABLE IF NOT EXISTS public.org_members (
    org_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL CHECK (role IN ('owner', 'admin', 'operator', 'viewer')),
    PRIMARY KEY (org_id, user_id)
);

-- 15.5 Farms (Core Domain)
CREATE TABLE IF NOT EXISTS public.farms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    org_id UUID REFERENCES public.organizations(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    location_state VARCHAR(100),
    location_district VARCHAR(100),
    total_area_hectares NUMERIC(8,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_farms_farmer ON public.farms(farmer_id);

-- 16. Farm Zones (Physical Graph Topology)
CREATE TABLE IF NOT EXISTS public.farm_zones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID NOT NULL REFERENCES public.farms(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    area_hectares NUMERIC(6,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_farm_zones_farm ON public.farm_zones(farm_id);

-- 16.5 Crops (Planted instances)
CREATE TABLE IF NOT EXISTS public.crops (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_zone_id UUID NOT NULL REFERENCES public.farm_zones(id) ON DELETE CASCADE,
    crop_type VARCHAR(100) NOT NULL,
    variety VARCHAR(100),
    planted_at TIMESTAMP WITH TIME ZONE NOT NULL,
    expected_harvest_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'growing' CHECK (status IN ('growing', 'harvested', 'failed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_crops_zone ON public.crops(farm_zone_id);

-- 17. Irrigation Topology (Pump -> Valve -> Zone Graph)
CREATE TABLE IF NOT EXISTS public.irrigation_topology (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_device_id UUID NOT NULL REFERENCES public.iot_devices(id) ON DELETE CASCADE, -- e.g., The Pump
    target_device_id UUID REFERENCES public.iot_devices(id) ON DELETE CASCADE, -- e.g., The Valve (Optional)
    farm_zone_id UUID NOT NULL REFERENCES public.farm_zones(id) ON DELETE CASCADE,
    flow_capacity_lph NUMERIC(8,2) NOT NULL DEFAULT 0.0, -- Liters per hour
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 18. Telemetry Quarantine Pipeline (Advanced DLQ)
CREATE TABLE IF NOT EXISTS public.telemetry_quarantine (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID REFERENCES public.iot_devices(id) ON DELETE SET NULL,
    error_reason TEXT NOT NULL,
    raw_payload JSONB NOT NULL,
    schema_version VARCHAR(50) DEFAULT 'v1',
    logged_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE INDEX IF NOT EXISTS idx_telemetry_quarantine_unresolved ON public.telemetry_quarantine(resolved) WHERE resolved = FALSE;

-- 19. Edge Node Identity & Trust (mTLS Certificates)
CREATE TABLE IF NOT EXISTS public.edge_identities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    mac_address VARCHAR(100) UNIQUE NOT NULL,
    org_id UUID NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    cert_fingerprint VARCHAR(255) NOT NULL,
    is_revoked BOOLEAN NOT NULL DEFAULT FALSE,
    last_connected_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS idx_edge_identities_mac ON public.edge_identities(mac_address);

-- 20. Edge Configuration Versioning
CREATE TABLE IF NOT EXISTS public.edge_deployments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    edge_id UUID NOT NULL REFERENCES public.edge_identities(id) ON DELETE CASCADE,
    firmware_version VARCHAR(50) NOT NULL,
    rule_version INTEGER NOT NULL DEFAULT 1,
    topology_version INTEGER NOT NULL DEFAULT 1,
    orchestration_version INTEGER NOT NULL DEFAULT 1,
    deployed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 21. Subsidies (Structured Database)
CREATE TABLE IF NOT EXISTS public.subsidies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    agency VARCHAR(255) NOT NULL,
    amount NUMERIC(15, 2),
    amount_type VARCHAR(50) DEFAULT 'fixed',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.subsidy_eligibility_rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subsidy_id UUID NOT NULL REFERENCES public.subsidies(id) ON DELETE CASCADE,
    state VARCHAR(100),
    crop VARCHAR(100),
    max_land_size_hectares NUMERIC(8,2),
    min_land_size_hectares NUMERIC(8,2),
    social_category VARCHAR(100)
);

-- 22. AI Farm Calendar Engine
CREATE TABLE IF NOT EXISTS public.farm_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_zone_id UUID NOT NULL REFERENCES public.farm_zones(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    assigned_to UUID REFERENCES public.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.farm_timeline_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_zone_id UUID NOT NULL REFERENCES public.farm_zones(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    description TEXT,
    event_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 23. Intelligent Field Navigation
CREATE TABLE IF NOT EXISTS public.field_navigation_paths (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_zone_id UUID NOT NULL REFERENCES public.farm_zones(id) ON DELETE CASCADE,
    path_data JSONB NOT NULL,
    distance_meters NUMERIC(10,2),
    estimated_time_mins INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.spray_coverage_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    path_id UUID NOT NULL REFERENCES public.field_navigation_paths(id) ON DELETE CASCADE,
    coverage_polygon JSONB NOT NULL,
    chemical_used VARCHAR(100),
    amount_liters NUMERIC(8,2),
    logged_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 24. Market Anomalies
CREATE TABLE IF NOT EXISTS public.mandi_price_anomalies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    market VARCHAR(100) NOT NULL,
    commodity VARCHAR(100) NOT NULL,
    expected_price NUMERIC(12, 2) NOT NULL,
    actual_price NUMERIC(12, 2) NOT NULL,
    anomaly_reason TEXT,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 25. OTA Releases
CREATE TABLE IF NOT EXISTS public.ota_releases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    version_code INTEGER NOT NULL,
    version_name VARCHAR(50) NOT NULL,
    download_url TEXT NOT NULL,
    sha256_hash VARCHAR(64) NOT NULL,
    release_notes TEXT,
    is_mandatory BOOLEAN DEFAULT FALSE,
    signature_status VARCHAR(50) DEFAULT 'verified',
    released_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 26. AI Farm Memory Engine
CREATE TABLE IF NOT EXISTS public.ai_farm_memory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_zone_id UUID NOT NULL REFERENCES public.farm_zones(id) ON DELETE CASCADE,
    season VARCHAR(50) NOT NULL, -- e.g. "Kharif 2025"
    crop_id UUID REFERENCES public.crops(id),
    yield_kg NUMERIC(10,2),
    diseases_detected JSONB DEFAULT '[]'::jsonb,
    total_water_used_liters NUMERIC(12,2),
    historical_notes TEXT,
    logged_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 27. Workflow Orchestrations
CREATE TABLE IF NOT EXISTS public.workflow_orchestrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_type VARCHAR(100) NOT NULL, -- e.g. "irrigation", "subsidy_eval"
    target_id UUID, -- Can be farm_zone_id, crop_id, etc.
    job_id VARCHAR(255), -- BullMQ job ID
    status VARCHAR(50) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed')),
    state_data JSONB DEFAULT '{}'::jsonb,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 28. Domain Events Ledger (Event Sourcing)
CREATE TABLE IF NOT EXISTS public.domain_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL, -- CROP_PLANTED, IRRIGATION_STARTED, etc.
    aggregate_id UUID NOT NULL, -- ID of the Crop, Farm, Workflow, etc.
    aggregate_type VARCHAR(50) NOT NULL, -- 'crop', 'workflow', 'device'
    payload JSONB NOT NULL,
    schema_version VARCHAR(50) DEFAULT 'v1',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_domain_events_aggregate ON public.domain_events(aggregate_id);
CREATE INDEX IF NOT EXISTS idx_domain_events_type_time ON public.domain_events(event_type, created_at DESC);
