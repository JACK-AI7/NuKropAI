-- ============================================================================
-- Migration: 001_disease_scans_and_outbreak_alerts.sql
-- Description: Schema, Adjacency Graph, Alerting Engine & Triggers for NuKropAI
-- National Crop Disease Aggregation and Early Warning System
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ----------------------------------------------------------------------------
-- 1. Disease Scans Table (Anonymous on-device telemetry logs)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.disease_scans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    disease_name VARCHAR(100) NOT NULL,
    crop_name VARCHAR(100) NOT NULL DEFAULT 'General',
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL DEFAULT '',
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    severity VARCHAR(50) NOT NULL DEFAULT 'Moderate',
    confidence INTEGER NOT NULL DEFAULT 90 CHECK (confidence BETWEEN 0 AND 100),
    scanned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_disease_scans_state_disease_time 
    ON public.disease_scans(state, disease_name, scanned_at DESC);
CREATE INDEX IF NOT EXISTS idx_disease_scans_time 
    ON public.disease_scans(scanned_at DESC);
CREATE INDEX IF NOT EXISTS idx_disease_scans_crop 
    ON public.disease_scans(crop_name);

-- ----------------------------------------------------------------------------
-- 2. State Adjacencies Table (Symmetric Indian State Boundary Graph)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.state_adjacencies (
    id SERIAL PRIMARY KEY,
    state VARCHAR(100) NOT NULL,
    neighbor_state VARCHAR(100) NOT NULL,
    border_risk_weight NUMERIC(4, 2) NOT NULL DEFAULT 1.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_state_neighbor UNIQUE (state, neighbor_state)
);

CREATE INDEX IF NOT EXISTS idx_state_adjacencies_state ON public.state_adjacencies(state);
CREATE INDEX IF NOT EXISTS idx_state_adjacencies_neighbor ON public.state_adjacencies(neighbor_state);

-- ----------------------------------------------------------------------------
-- 3. Outbreak Alerts Table (Epicenters & Early Warnings)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.outbreak_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    disease_name VARCHAR(100) NOT NULL,
    source_state VARCHAR(100) NOT NULL,
    target_state VARCHAR(100) NOT NULL,
    alert_type VARCHAR(50) NOT NULL CHECK (alert_type IN ('EPICENTER', 'EARLY_WARNING')),
    severity VARCHAR(50) NOT NULL DEFAULT 'MODERATE' CHECK (severity IN ('LOW', 'MODERATE', 'HIGH', 'CRITICAL')),
    scan_count INTEGER NOT NULL DEFAULT 0,
    threshold_density INTEGER NOT NULL DEFAULT 100,
    time_window_hours INTEGER NOT NULL DEFAULT 168,
    message TEXT NOT NULL,
    recommended_action TEXT NOT NULL,
    predicted_market_impact_pct NUMERIC(6, 2) NOT NULL DEFAULT 0.00,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_outbreak_alert_state UNIQUE (disease_name, source_state, target_state, alert_type)
);

CREATE INDEX IF NOT EXISTS idx_outbreak_alerts_target_active 
    ON public.outbreak_alerts(target_state, is_active);
CREATE INDEX IF NOT EXISTS idx_outbreak_alerts_source_disease 
    ON public.outbreak_alerts(source_state, disease_name);
CREATE INDEX IF NOT EXISTS idx_outbreak_alerts_disease_active 
    ON public.outbreak_alerts(disease_name, is_active);

-- ----------------------------------------------------------------------------
-- 4. Trigger Function: fn_evaluate_disease_outbreak()
-- Rolling 7-day (168 hours) density aggregation with threshold evaluation (>=100)
-- Generates/Updates EPICENTER alert in source state and fanning out EARLY_WARNINGs
-- to all adjacent neighboring states from public.state_adjacencies
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.fn_evaluate_disease_outbreak()
RETURNS TRIGGER AS $$
DECLARE
    v_scan_count INTEGER;
    v_window_hours INTEGER := 168; -- 7 days rolling window
    v_threshold INTEGER := 100;
    v_severity VARCHAR(50);
    v_epicenter_msg TEXT;
    v_epicenter_action TEXT;
    v_epicenter_impact NUMERIC(6,2);
    v_neighbor_record RECORD;
    v_neighbor_msg TEXT;
    v_neighbor_action TEXT;
    v_neighbor_impact NUMERIC(6,2);
BEGIN
    -- Count recent scans for this disease in this state within the 168-hour rolling window
    SELECT COUNT(*)
    INTO v_scan_count
    FROM public.disease_scans
    WHERE disease_name = NEW.disease_name
      AND state = NEW.state
      AND scanned_at >= NOW() - (v_window_hours || ' hours')::INTERVAL;

    -- If the count meets or exceeds the outbreak threshold (100 scans)
    IF v_scan_count >= v_threshold THEN
        -- Dynamic severity & market shock escalation
        IF v_scan_count >= 300 THEN
            v_severity := 'CRITICAL';
            v_epicenter_impact := 35.00;
            v_neighbor_impact := 20.00;
        ELSIF v_scan_count >= 200 THEN
            v_severity := 'HIGH';
            v_epicenter_impact := 25.00;
            v_neighbor_impact := 15.00;
        ELSE
            v_severity := 'MODERATE';
            v_epicenter_impact := 15.00;
            v_neighbor_impact := 8.00;
        END IF;

        v_epicenter_msg := 'CRITICAL OUTBREAK DETECTED: ' || NEW.disease_name || ' outbreak confirmed in ' || NEW.state || ' with ' || v_scan_count || ' recent scan detections crossing density threshold (' || v_threshold || ').';
        v_epicenter_action := 'Deploy immediate containment, quarantine affected fields, apply targeted chemical/biological fungicides or insecticides, and alert local Krishi Vigyan Kendra (KVK).';

        -- 1. Upsert EPICENTER alert for source state
        INSERT INTO public.outbreak_alerts (
            disease_name,
            source_state,
            target_state,
            alert_type,
            severity,
            scan_count,
            threshold_density,
            time_window_hours,
            message,
            recommended_action,
            predicted_market_impact_pct,
            is_active,
            updated_at
        ) VALUES (
            NEW.disease_name,
            NEW.state,
            NEW.state,
            'EPICENTER',
            v_severity,
            v_scan_count,
            v_threshold,
            v_window_hours,
            v_epicenter_msg,
            v_epicenter_action,
            v_epicenter_impact,
            TRUE,
            NOW()
        )
        ON CONFLICT (disease_name, source_state, target_state, alert_type)
        DO UPDATE SET
            severity = EXCLUDED.severity,
            scan_count = EXCLUDED.scan_count,
            message = EXCLUDED.message,
            recommended_action = EXCLUDED.recommended_action,
            predicted_market_impact_pct = EXCLUDED.predicted_market_impact_pct,
            is_active = TRUE,
            updated_at = NOW();

        -- 2. Fan out EARLY_WARNING alerts for all adjacent neighboring states
        FOR v_neighbor_record IN
            SELECT neighbor_state, border_risk_weight
            FROM public.state_adjacencies
            WHERE state = NEW.state
        LOOP
            v_neighbor_msg := 'EARLY WARNING: Outbreak of ' || NEW.disease_name || ' detected in neighboring ' || NEW.state || ' (' || v_scan_count || ' active scans). High risk of trans-boundary spore/pest vector transmission to ' || v_neighbor_record.neighbor_state || '.';
            v_neighbor_action := 'Inspect border district fields daily, prepare preventative spraying protocols, and monitor Mandi arrivals from ' || NEW.state || '.';

            INSERT INTO public.outbreak_alerts (
                disease_name,
                source_state,
                target_state,
                alert_type,
                severity,
                scan_count,
                threshold_density,
                time_window_hours,
                message,
                recommended_action,
                predicted_market_impact_pct,
                is_active,
                updated_at
            ) VALUES (
                NEW.disease_name,
                NEW.state,
                v_neighbor_record.neighbor_state,
                'EARLY_WARNING',
                CASE WHEN v_severity = 'CRITICAL' THEN 'HIGH' ELSE 'MODERATE' END,
                v_scan_count,
                v_threshold,
                v_window_hours,
                v_neighbor_msg,
                v_neighbor_action,
                ROUND(v_neighbor_impact * v_neighbor_record.border_risk_weight, 2),
                TRUE,
                NOW()
            )
            ON CONFLICT (disease_name, source_state, target_state, alert_type)
            DO UPDATE SET
                severity = EXCLUDED.severity,
                scan_count = EXCLUDED.scan_count,
                message = EXCLUDED.message,
                recommended_action = EXCLUDED.recommended_action,
                predicted_market_impact_pct = EXCLUDED.predicted_market_impact_pct,
                is_active = TRUE,
                updated_at = NOW();
        END LOOP;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_disease_scan_outbreak_eval ON public.disease_scans;
CREATE TRIGGER trg_disease_scan_outbreak_eval
AFTER INSERT ON public.disease_scans
FOR EACH ROW
EXECUTE FUNCTION public.fn_evaluate_disease_outbreak();

-- ----------------------------------------------------------------------------
-- 5. Seed Data: Full Symmetric Indian State Adjacency Graph (28 States & UTs)
-- ----------------------------------------------------------------------------
INSERT INTO public.state_adjacencies (state, neighbor_state, border_risk_weight) VALUES
-- Andhra Pradesh
('Andhra Pradesh', 'Telangana', 1.00),
('Andhra Pradesh', 'Odisha', 0.90),
('Andhra Pradesh', 'Chhattisgarh', 0.85),
('Andhra Pradesh', 'Karnataka', 0.95),
('Andhra Pradesh', 'Tamil Nadu', 1.00),
('Andhra Pradesh', 'Puducherry', 0.80),

-- Arunachal Pradesh
('Arunachal Pradesh', 'Assam', 1.00),
('Arunachal Pradesh', 'Nagaland', 0.90),

-- Assam
('Assam', 'Arunachal Pradesh', 1.00),
('Assam', 'Nagaland', 0.95),
('Assam', 'Manipur', 0.90),
('Assam', 'Mizoram', 0.90),
('Assam', 'Tripura', 0.90),
('Assam', 'Meghalaya', 1.00),
('Assam', 'West Bengal', 1.00),

-- Bihar
('Bihar', 'Uttar Pradesh', 1.00),
('Bihar', 'Jharkhand', 1.00),
('Bihar', 'West Bengal', 0.95),

-- Chhattisgarh
('Chhattisgarh', 'Madhya Pradesh', 1.00),
('Chhattisgarh', 'Maharashtra', 0.95),
('Chhattisgarh', 'Telangana', 0.90),
('Chhattisgarh', 'Andhra Pradesh', 0.85),
('Chhattisgarh', 'Odisha', 1.00),
('Chhattisgarh', 'Jharkhand', 0.95),
('Chhattisgarh', 'Uttar Pradesh', 0.90),

-- Goa
('Goa', 'Maharashtra', 1.00),
('Goa', 'Karnataka', 1.00),

-- Gujarat
('Gujarat', 'Rajasthan', 1.00),
('Gujarat', 'Madhya Pradesh', 0.95),
('Gujarat', 'Maharashtra', 1.00),
('Gujarat', 'Dadra and Nagar Haveli and Daman and Diu', 0.80),

-- Haryana
('Haryana', 'Punjab', 1.00),
('Haryana', 'Himachal Pradesh', 0.90),
('Haryana', 'Rajasthan', 1.00),
('Haryana', 'Uttar Pradesh', 1.00),
('Haryana', 'Delhi', 1.00),
('Haryana', 'Chandigarh', 0.90),

-- Himachal Pradesh
('Himachal Pradesh', 'Jammu and Kashmir', 0.95),
('Himachal Pradesh', 'Ladakh', 0.85),
('Himachal Pradesh', 'Punjab', 1.00),
('Himachal Pradesh', 'Haryana', 0.90),
('Himachal Pradesh', 'Uttarakhand', 0.95),
('Himachal Pradesh', 'Uttar Pradesh', 0.80),

-- Jharkhand
('Jharkhand', 'Bihar', 1.00),
('Jharkhand', 'Uttar Pradesh', 0.90),
('Jharkhand', 'Chhattisgarh', 0.95),
('Jharkhand', 'Odisha', 1.00),
('Jharkhand', 'West Bengal', 1.00),

-- Karnataka
('Karnataka', 'Goa', 1.00),
('Karnataka', 'Maharashtra', 1.00),
('Karnataka', 'Telangana', 0.95),
('Karnataka', 'Andhra Pradesh', 0.95),
('Karnataka', 'Tamil Nadu', 1.00),
('Karnataka', 'Kerala', 1.00),

-- Kerala
('Kerala', 'Karnataka', 1.00),
('Kerala', 'Tamil Nadu', 1.00),
('Kerala', 'Puducherry', 0.80),

-- Madhya Pradesh
('Madhya Pradesh', 'Rajasthan', 1.00),
('Madhya Pradesh', 'Uttar Pradesh', 1.00),
('Madhya Pradesh', 'Chhattisgarh', 1.00),
('Madhya Pradesh', 'Maharashtra', 1.00),
('Madhya Pradesh', 'Gujarat', 0.95),

-- Maharashtra
('Maharashtra', 'Gujarat', 1.00),
('Maharashtra', 'Madhya Pradesh', 1.00),
('Maharashtra', 'Chhattisgarh', 0.95),
('Maharashtra', 'Telangana', 1.00),
('Maharashtra', 'Karnataka', 1.00),
('Maharashtra', 'Goa', 1.00),
('Maharashtra', 'Dadra and Nagar Haveli and Daman and Diu', 0.80),

-- Manipur
('Manipur', 'Nagaland', 0.95),
('Manipur', 'Assam', 0.90),
('Manipur', 'Mizoram', 0.95),

-- Meghalaya
('Meghalaya', 'Assam', 1.00),

-- Mizoram
('Mizoram', 'Assam', 0.90),
('Mizoram', 'Manipur', 0.95),
('Mizoram', 'Tripura', 0.95),

-- Nagaland
('Nagaland', 'Arunachal Pradesh', 0.90),
('Nagaland', 'Assam', 0.95),
('Nagaland', 'Manipur', 0.95),

-- Odisha
('Odisha', 'West Bengal', 1.00),
('Odisha', 'Jharkhand', 1.00),
('Odisha', 'Chhattisgarh', 1.00),
('Odisha', 'Andhra Pradesh', 0.90),

-- Punjab
('Punjab', 'Jammu and Kashmir', 0.95),
('Punjab', 'Himachal Pradesh', 1.00),
('Punjab', 'Haryana', 1.00),
('Punjab', 'Rajasthan', 1.00),
('Punjab', 'Chandigarh', 0.90),

-- Rajasthan
('Rajasthan', 'Punjab', 1.00),
('Rajasthan', 'Haryana', 1.00),
('Rajasthan', 'Uttar Pradesh', 1.00),
('Rajasthan', 'Madhya Pradesh', 1.00),
('Rajasthan', 'Gujarat', 1.00),

-- Sikkim
('Sikkim', 'West Bengal', 1.00),

-- Tamil Nadu
('Tamil Nadu', 'Kerala', 1.00),
('Tamil Nadu', 'Karnataka', 1.00),
('Tamil Nadu', 'Andhra Pradesh', 1.00),
('Tamil Nadu', 'Puducherry', 0.90),

-- Telangana
('Telangana', 'Maharashtra', 1.00),
('Telangana', 'Chhattisgarh', 0.90),
('Telangana', 'Karnataka', 0.95),
('Telangana', 'Andhra Pradesh', 1.00),

-- Tripura
('Tripura', 'Assam', 0.90),
('Tripura', 'Mizoram', 0.95),

-- Uttar Pradesh
('Uttar Pradesh', 'Himachal Pradesh', 0.80),
('Uttar Pradesh', 'Haryana', 1.00),
('Uttar Pradesh', 'Delhi', 1.00),
('Uttar Pradesh', 'Rajasthan', 1.00),
('Uttar Pradesh', 'Madhya Pradesh', 1.00),
('Uttar Pradesh', 'Chhattisgarh', 0.90),
('Uttar Pradesh', 'Jharkhand', 0.90),
('Uttar Pradesh', 'Bihar', 1.00),
('Uttar Pradesh', 'Uttarakhand', 1.00),

-- Uttarakhand
('Uttarakhand', 'Himachal Pradesh', 0.95),
('Uttarakhand', 'Uttar Pradesh', 1.00),

-- West Bengal
('West Bengal', 'Sikkim', 1.00),
('West Bengal', 'Assam', 1.00),
('West Bengal', 'Bihar', 0.95),
('West Bengal', 'Jharkhand', 1.00),
('West Bengal', 'Odisha', 1.00),

-- Delhi
('Delhi', 'Haryana', 1.00),
('Delhi', 'Uttar Pradesh', 1.00),

-- Jammu and Kashmir
('Jammu and Kashmir', 'Ladakh', 0.90),
('Jammu and Kashmir', 'Himachal Pradesh', 0.95),
('Jammu and Kashmir', 'Punjab', 0.95),

-- Ladakh
('Ladakh', 'Jammu and Kashmir', 0.90),
('Ladakh', 'Himachal Pradesh', 0.85),

-- Chandigarh
('Chandigarh', 'Punjab', 0.90),
('Chandigarh', 'Haryana', 0.90),

-- Puducherry
('Puducherry', 'Tamil Nadu', 0.90),
('Puducherry', 'Andhra Pradesh', 0.80),
('Puducherry', 'Kerala', 0.80),

-- Dadra and Nagar Haveli and Daman and Diu
('Dadra and Nagar Haveli and Daman and Diu', 'Gujarat', 0.80),
('Dadra and Nagar Haveli and Daman and Diu', 'Maharashtra', 0.80)

ON CONFLICT (state, neighbor_state) DO NOTHING;

-- ----------------------------------------------------------------------------
-- 6. Row Level Security (RLS) Policies
-- ----------------------------------------------------------------------------
ALTER TABLE public.disease_scans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.state_adjacencies ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.outbreak_alerts ENABLE ROW LEVEL SECURITY;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public read and write on disease_scans') THEN
        CREATE POLICY "Allow public read and write on disease_scans" ON public.disease_scans FOR ALL USING (true) WITH CHECK (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public read and write on state_adjacencies') THEN
        CREATE POLICY "Allow public read and write on state_adjacencies" ON public.state_adjacencies FOR ALL USING (true) WITH CHECK (true);
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'Allow public read and write on outbreak_alerts') THEN
        CREATE POLICY "Allow public read and write on outbreak_alerts" ON public.outbreak_alerts FOR ALL USING (true) WITH CHECK (true);
    END IF;
END $$;
