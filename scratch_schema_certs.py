schema_addition = """
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
"""

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\backend\schema.sql", "a", encoding="utf-8") as f:
    f.write(schema_addition)
