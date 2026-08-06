schema_addition = """
-- 13. Event Sourcing Table for strict IoT audit trailing
CREATE TABLE IF NOT EXISTS public.device_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID NOT NULL REFERENCES public.iot_devices(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL CHECK (event_type IN ('COMMAND_ISSUED', 'TELEMETRY_RECEIVED', 'FAULT_DETECTED', 'STATE_CONFIRMED', 'PROTECTION_TRIGGERED')),
    payload JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_device_events_device_time ON public.device_events(device_id, created_at DESC);
"""

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\backend\schema.sql", "a", encoding="utf-8") as f:
    f.write(schema_addition)
