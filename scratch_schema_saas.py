schema_addition = """
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
"""

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\backend\schema.sql", "a", encoding="utf-8") as f:
    f.write(schema_addition)
