schema_addition = """
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
"""

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\backend\schema.sql", "a", encoding="utf-8") as f:
    f.write(schema_addition)
