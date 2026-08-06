-- NuKropAI OS Enterprise Schema
-- Requires PostgreSQL + PostGIS + TimescaleDB

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Geospatial Farm Foundation
CREATE TABLE IF NOT EXISTS farms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL, -- References global users table
    name VARCHAR(255) NOT NULL,
    boundary geometry(Polygon, 4326) NOT NULL,
    total_acreage DECIMAL(10, 4) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS farms_boundary_idx ON farms USING GIST (boundary);

-- 2. Farm Zones (Sub-polygons)
CREATE TABLE IF NOT EXISTS zones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    boundary geometry(Polygon, 4326) NOT NULL,
    crop_type VARCHAR(100),
    planting_date DATE,
    expected_harvest_date DATE,
    area_acreage DECIMAL(10, 4) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS zones_boundary_idx ON zones USING GIST (boundary);
CREATE INDEX IF NOT EXISTS zones_farm_id_idx ON zones(farm_id);

-- 3. IoT Edge Devices Topology
CREATE TABLE IF NOT EXISTS devices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    zone_id UUID REFERENCES zones(id) ON DELETE SET NULL,
    farm_id UUID NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- 'PUMP', 'VALVE', 'SOIL_SENSOR', 'WEATHER_STATION'
    name VARCHAR(255) NOT NULL,
    mac_address VARCHAR(50) UNIQUE,
    provider VARCHAR(100) DEFAULT 'edge_mqtt',
    parent_device_id UUID REFERENCES devices(id), -- Graph adjacency list for topology (e.g. valve -> pump)
    status VARCHAR(50) DEFAULT 'OFFLINE',
    last_seen TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS devices_zone_id_idx ON devices(zone_id);
CREATE INDEX IF NOT EXISTS devices_parent_id_idx ON devices(parent_device_id);

-- 4. High-Throughput IoT Telemetry (TimescaleDB Hypertable)
CREATE TABLE IF NOT EXISTS telemetry (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    device_id UUID NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
    metric_name VARCHAR(50) NOT NULL, -- e.g., 'moisture', 'nitrogen', 'flow_rate', 'power_kw'
    value DOUBLE PRECISION NOT NULL
);

-- Convert telemetry into a hypertable, chunking by time (every 1 day for high frequency)
SELECT create_hypertable('telemetry', 'time', if_not_exists => TRUE, chunk_time_interval => INTERVAL '1 day');

CREATE INDEX IF NOT EXISTS telemetry_device_idx ON telemetry(device_id, time DESC);

-- 5. Autonomous Irrigation Events Ledger
CREATE TABLE IF NOT EXISTS irrigation_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    zone_id UUID NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
    device_id UUID NOT NULL REFERENCES devices(id),
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    water_volume_liters DECIMAL(12, 2) DEFAULT 0.0,
    triggered_by VARCHAR(100) NOT NULL, -- 'AI_ORCHESTRATOR', 'MANUAL', 'EDGE_FALLBACK'
    status VARCHAR(50) DEFAULT 'IN_PROGRESS', -- 'IN_PROGRESS', 'COMPLETED', 'FAILED'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Soil Health & AI Processing Cache
CREATE TABLE IF NOT EXISTS soil_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    zone_id UUID NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
    report_date DATE NOT NULL,
    ph DECIMAL(4,2),
    nitrogen DECIMAL(8,2),
    phosphorus DECIMAL(8,2),
    potassium DECIMAL(8,2),
    organic_matter DECIMAL(5,2),
    raw_ocr_text TEXT,
    ai_recommendation TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
