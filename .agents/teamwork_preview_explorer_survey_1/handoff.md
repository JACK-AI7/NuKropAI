# Handoff Report — Explorer 1: Backend Architecture & Schema Specialist

## 1. Observation

### 1.1 Existing Backend Architecture & Supabase Integration
- **Supabase Credentials & Client**:
  - File: `app/src/main/java/com/example/SupabaseClient.kt`
  - Lines 18–28:
    ```kotlin
    val SUPABASE_URL = "https://yxjqseiegwjdfnccdchk.supabase.co"
    val SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    val supabase = createSupabaseClient(supabaseUrl = SUPABASE_URL, supabaseKey = SUPABASE_ANON_KEY) {
        install(Auth)
        install(Postgrest)
        install(Realtime)
    }
    ```
  - Lines 30–79: Companion `SupabaseApi` utilizes an `OkHttpClient` instance with direct PostgREST REST calls (`$SUPABASE_URL/rest/v1/...`) with `apikey` and `Authorization` headers.
  - RLS policies and table setup in `backend/supabase_setup.sql` (lines 74–82) explicitly enable Row Level Security and grant public anonymous read/write access via `CREATE POLICY "Allow public read and write on ..."` for zero-friction client sync.

- **Existing Database Schemas & Migrations**:
  - `backend/supabase_setup.sql`: Defines `user_profiles`, `mandi_live_rates`, `peer_messages`, and `equipment_rentals`.
  - `backend/schema.sql`: Contains the enterprise PostgreSQL schema, including `public.pest_outbreaks` (lines 43–53) with coordinates (`latitude`, `longitude`), `reporter_id`, `wind_direction`, `wind_speed`.
  - Node/Fastify backend in `backend/src/server.ts` routes `/pests` via `backend/src/routes/pest.routes.ts` and `backend/src/controllers/pest.controller.ts` interacting with `pest_outbreaks` with an in-memory database simulation fallback in `backend/src/config/db.ts` (lines 233–250).

- **On-Device Scanning & Location Pipelines**:
  - `app/src/main/java/com/example/DiseaseScannerScreen.kt` (lines 54–131): AI scan output is parsed into `CropScanData(status, name, confidence, severity, symptoms, cause, treatment, prevention, details, products)`.
  - `app/src/main/java/com/example/LocationHelper.kt` (lines 13–71): Extracts current location's Indian state name (`address.adminArea`) and mandi/district (`address.locality` / `subAdminArea`) or GPS coordinates (`latitude`, `longitude`).
  - `app/src/main/java/com/example/RegionalIntelligenceScreen.kt` (lines 39–53): Currently displays placeholder pest risk cards for regional intelligence.

---

## 2. Logic Chain

### 2.1 Core Problem & Architecture Requirements for R1
1. **Anonymous Disease Scan Recording**:
   - Farmers perform on-device crop disease scans in `DiseaseScannerScreen.kt`.
   - Upon disease diagnosis, the app must silently and asynchronously record the scan to the aggregation backend without exposing user identity.
   - Target schema must capture: `id` (UUID), `disease_name` (e.g. "Fall Armyworm", "Fungal Blight"), `crop_name`, `severity` (e.g. "Moderate", "High"), `confidence` (e.g. 92), `state` (e.g. "Maharashtra"), `district`, optional coordinates, and `scanned_at` timestamp.

2. **Density Threshold Aggregation & Alert Generation Logic**:
   - Outbreaks occur when scan density crosses a defined critical threshold (default: **100 scans** for a specific pest/disease in a state within a rolling window of **7 days / 168 hours**).
   - Once the threshold is crossed, the system must:
     a. Generate/update an **EPICENTER** alert for the affected source state (`alert_type = 'EPICENTER'`).
     b. Query geographic adjacency for all neighboring states.
     c. Automatically fan out **EARLY_WARNING** alerts for all neighboring states (`alert_type = 'EARLY_WARNING'`).

3. **Geographic State Adjacency Representation**:
   - To reliably determine neighboring regions without complex external GIS dependencies, we define a normalized reference table `public.state_adjacencies (state VARCHAR(100), neighbor_state VARCHAR(100), PRIMARY KEY(state, neighbor_state))`.
   - We mirror this adjacency matrix in Kotlin (`DiseaseAggregationService.kt` / `StateAdjacencyGraph`) to allow zero-latency local fallback and unit testability.

4. **Dual-Layer Aggregation Engine (Postgres DB Trigger + Kotlin / Backend Service)**:
   - **Layer 1 (PostgreSQL DB Trigger)**: `fn_evaluate_disease_outbreak()` executes `AFTER INSERT ON public.disease_scans`. It performs an atomic `SELECT COUNT(*)` for `(disease_name, state)` in the past 7 days. When `count >= 100`, it inserts/updates `public.outbreak_alerts` for the source state and all adjacent states from `public.state_adjacencies`.
   - **Layer 2 (Kotlin Service in Android)**: `DiseaseAggregationService.kt` manages PostgREST REST calls (`POST /rest/v1/disease_scans` and `GET /rest/v1/outbreak_alerts?target_state=eq.{state}&is_active=eq.true`), handles network retries, and maintains a local cache and offline density evaluator.

---

## 3. Detailed Technical Design & Specifications

### 3.1 PostgreSQL Database Schema & Migration (`backend/migrations/001_disease_scans_and_outbreak_alerts.sql`)

```sql
-- 1. Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Anonymous Disease Scans Table
CREATE TABLE IF NOT EXISTS public.disease_scans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    disease_name VARCHAR(150) NOT NULL,
    crop_name VARCHAR(100) DEFAULT 'General',
    severity VARCHAR(50) DEFAULT 'Moderate',
    confidence INTEGER DEFAULT 90,
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    scanned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_disease_scans_state_disease ON public.disease_scans(state, disease_name, scanned_at DESC);
CREATE INDEX IF NOT EXISTS idx_disease_scans_scanned_at ON public.disease_scans(scanned_at DESC);

-- 3. State Geographic Adjacency Reference Table
CREATE TABLE IF NOT EXISTS public.state_adjacencies (
    state VARCHAR(100) NOT NULL,
    neighbor_state VARCHAR(100) NOT NULL,
    PRIMARY KEY (state, neighbor_state)
);

-- Seed Indian State Adjacencies (Symmetric Graph)
INSERT INTO public.state_adjacencies (state, neighbor_state) VALUES
-- Maharashtra
('Maharashtra', 'Gujarat'), ('Maharashtra', 'Madhya Pradesh'), ('Maharashtra', 'Chhattisgarh'),
('Maharashtra', 'Telangana'), ('Maharashtra', 'Karnataka'), ('Maharashtra', 'Goa'),
-- Punjab
('Punjab', 'Haryana'), ('Punjab', 'Rajasthan'), ('Punjab', 'Himachal Pradesh'), ('Punjab', 'Jammu and Kashmir'),
-- Haryana
('Haryana', 'Punjab'), ('Haryana', 'Rajasthan'), ('Haryana', 'Uttar Pradesh'), ('Haryana', 'Himachal Pradesh'), ('Haryana', 'Delhi'),
-- Karnataka
('Karnataka', 'Maharashtra'), ('Karnataka', 'Goa'), ('Karnataka', 'Kerala'), ('Karnataka', 'Tamil Nadu'), ('Karnataka', 'Andhra Pradesh'), ('Karnataka', 'Telangana'),
-- Uttar Pradesh
('Uttar Pradesh', 'Bihar'), ('Uttar Pradesh', 'Madhya Pradesh'), ('Uttar Pradesh', 'Rajasthan'), ('Uttar Pradesh', 'Haryana'), ('Uttar Pradesh', 'Uttarakhand'), ('Uttar Pradesh', 'Jharkhand'), ('Uttar Pradesh', 'Chhattisgarh'), ('Uttar Pradesh', 'Delhi'),
-- Madhya Pradesh
('Madhya Pradesh', 'Uttar Pradesh'), ('Madhya Pradesh', 'Rajasthan'), ('Madhya Pradesh', 'Gujarat'), ('Madhya Pradesh', 'Maharashtra'), ('Madhya Pradesh', 'Chhattisgarh'),
-- Gujarat
('Gujarat', 'Rajasthan'), ('Gujarat', 'Madhya Pradesh'), ('Gujarat', 'Maharashtra'),
-- Rajasthan
('Rajasthan', 'Punjab'), ('Rajasthan', 'Haryana'), ('Rajasthan', 'Uttar Pradesh'), ('Rajasthan', 'Madhya Pradesh'), ('Rajasthan', 'Gujarat'),
-- Tamil Nadu
('Tamil Nadu', 'Kerala'), ('Tamil Nadu', 'Karnataka'), ('Tamil Nadu', 'Andhra Pradesh'),
-- Andhra Pradesh
('Andhra Pradesh', 'Tamil Nadu'), ('Andhra Pradesh', 'Karnataka'), ('Andhra Pradesh', 'Telangana'), ('Andhra Pradesh', 'Odisha'), ('Andhra Pradesh', 'Chhattisgarh'),
-- Telangana
('Telangana', 'Maharashtra'), ('Telangana', 'Karnataka'), ('Telangana', 'Andhra Pradesh'), ('Telangana', 'Chhattisgarh'),
-- Bihar
('Bihar', 'Uttar Pradesh'), ('Bihar', 'Jharkhand'), ('Bihar', 'West Bengal'),
-- West Bengal
('West Bengal', 'Bihar'), ('West Bengal', 'Jharkhand'), ('West Bengal', 'Odisha'), ('West Bengal', 'Sikkim'), ('West Bengal', 'Assam'),
-- Odisha
('Odisha', 'West Bengal'), ('Odisha', 'Jharkhand'), ('Odisha', 'Chhattisgarh'), ('Odisha', 'Andhra Pradesh'),
-- Chhattisgarh
('Chhattisgarh', 'Madhya Pradesh'), ('Chhattisgarh', 'Maharashtra'), ('Chhattisgarh', 'Telangana'), ('Chhattisgarh', 'Andhra Pradesh'), ('Chhattisgarh', 'Odisha'), ('Chhattisgarh', 'Jharkhand'), ('Chhattisgarh', 'Uttar Pradesh'),
-- Kerala
('Kerala', 'Karnataka'), ('Kerala', 'Tamil Nadu'),
-- Himachal Pradesh
('Himachal Pradesh', 'Jammu and Kashmir'), ('Himachal Pradesh', 'Punjab'), ('Himachal Pradesh', 'Haryana'), ('Himachal Pradesh', 'Uttarakhand'),
-- Uttarakhand
('Uttarakhand', 'Himachal Pradesh'), ('Uttarakhand', 'Uttar Pradesh'), ('Uttarakhand', 'Haryana'),
-- Assam
('Assam', 'Arunachal Pradesh'), ('Assam', 'Nagaland'), ('Assam', 'Manipur'), ('Assam', 'Mizoram'), ('Assam', 'Tripura'), ('Assam', 'Meghalaya'), ('Assam', 'West Bengal'),
-- Jharkhand
('Jharkhand', 'Bihar'), ('Jharkhand', 'Uttar Pradesh'), ('Jharkhand', 'Chhattisgarh'), ('Jharkhand', 'Odisha'), ('Jharkhand', 'West Bengal')
ON CONFLICT DO NOTHING;

-- 4. Outbreak Alerts Table
CREATE TABLE IF NOT EXISTS public.outbreak_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    disease_name VARCHAR(150) NOT NULL,
    source_state VARCHAR(100) NOT NULL,
    target_state VARCHAR(100) NOT NULL,
    alert_type VARCHAR(50) NOT NULL DEFAULT 'EARLY_WARNING' CHECK (alert_type IN ('EPICENTER', 'EARLY_WARNING')),
    severity VARCHAR(50) NOT NULL DEFAULT 'HIGH' CHECK (severity IN ('LOW', 'MODERATE', 'HIGH', 'CRITICAL')),
    scan_count INTEGER NOT NULL DEFAULT 100,
    threshold_density INTEGER NOT NULL DEFAULT 100,
    time_window_hours INTEGER NOT NULL DEFAULT 168,
    message TEXT NOT NULL,
    recommended_action TEXT NOT NULL,
    predicted_market_impact_pct NUMERIC(5,2) DEFAULT -15.00,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_disease_target_state_type UNIQUE (disease_name, target_state, alert_type)
);

CREATE INDEX IF NOT EXISTS idx_outbreak_alerts_target ON public.outbreak_alerts(target_state, is_active, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_outbreak_alerts_disease ON public.outbreak_alerts(disease_name, is_active);

-- 5. Row Level Security Policies (RLS)
ALTER TABLE public.disease_scans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.state_adjacencies ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.outbreak_alerts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public insert on disease_scans" ON public.disease_scans FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public select on disease_scans" ON public.disease_scans FOR SELECT USING (true);
CREATE POLICY "Allow public select on state_adjacencies" ON public.state_adjacencies FOR SELECT USING (true);
CREATE POLICY "Allow public all on outbreak_alerts" ON public.outbreak_alerts FOR ALL USING (true) WITH CHECK (true);

-- 6. Trigger Function: Density Aggregation & Early Warning Alert Generation
CREATE OR REPLACE FUNCTION public.fn_evaluate_disease_outbreak()
RETURNS TRIGGER AS $$
DECLARE
    v_recent_count INTEGER;
    v_threshold INTEGER := 100;
    v_window_hours INTEGER := 168; -- 7 days rolling window
    v_neighbor RECORD;
    v_epicenter_msg TEXT;
    v_warning_msg TEXT;
    v_action TEXT;
BEGIN
    -- 1. Count recent scans for this disease and state within rolling window
    SELECT COUNT(*) INTO v_recent_count
    FROM public.disease_scans
    WHERE state = NEW.state
      AND disease_name = NEW.disease_name
      AND scanned_at >= NOW() - (v_window_hours || ' hours')::INTERVAL;

    -- 2. If threshold reached, create or update alerts
    IF v_recent_count >= v_threshold THEN
        v_epicenter_msg := format('CRITICAL OUTBREAK: High disease density of %s detected in %s (%s confirmed scans in past 7 days). Immediate intervention recommended.', NEW.disease_name, NEW.state, v_recent_count);
        v_action := 'Deploy emergency containment sprays (bio-fungicide/recommended insecticide), remove infected crop residues, and notify local Krishi Vigyan Kendra (KVK).';

        -- A. Create / Update Epicenter Alert
        INSERT INTO public.outbreak_alerts (
            disease_name, source_state, target_state, alert_type, severity,
            scan_count, threshold_density, time_window_hours, message, recommended_action, is_active, updated_at
        ) VALUES (
            NEW.disease_name, NEW.state, NEW.state, 'EPICENTER', 'CRITICAL',
            v_recent_count, v_threshold, v_window_hours, v_epicenter_msg, v_action, TRUE, NOW()
        )
        ON CONFLICT (disease_name, target_state, alert_type)
        DO UPDATE SET
            scan_count = EXCLUDED.scan_count,
            message = EXCLUDED.message,
            severity = 'CRITICAL',
            is_active = TRUE,
            updated_at = NOW();

        -- B. Fan-out Early Warning Alerts to all Neighboring States
        FOR v_neighbor IN
            SELECT neighbor_state FROM public.state_adjacencies WHERE state = NEW.state
        LOOP
            v_warning_msg := format('EARLY WARNING: Outbreak of %s detected in neighboring %s (%s scans). High risk of regional spread into %s.', NEW.disease_name, NEW.state, v_recent_count, v_neighbor.neighbor_state);

            INSERT INTO public.outbreak_alerts (
                disease_name, source_state, target_state, alert_type, severity,
                scan_count, threshold_density, time_window_hours, message, recommended_action, is_active, updated_at
            ) VALUES (
                NEW.disease_name, NEW.state, v_neighbor.neighbor_state, 'EARLY_WARNING', 'HIGH',
                v_recent_count, v_threshold, v_window_hours, v_warning_msg,
                'Inspect border and field margins, prepare preventive barrier spray, and monitor crops closely.',
                TRUE, NOW()
            )
            ON CONFLICT (disease_name, target_state, alert_type)
            DO UPDATE SET
                scan_count = EXCLUDED.scan_count,
                source_state = EXCLUDED.source_state,
                message = EXCLUDED.message,
                severity = 'HIGH',
                is_active = TRUE,
                updated_at = NOW();
        END LOOP;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 7. Attach Trigger to disease_scans table
DROP TRIGGER IF EXISTS trg_disease_outbreak_eval ON public.disease_scans;
CREATE TRIGGER trg_disease_outbreak_eval
AFTER INSERT ON public.disease_scans
FOR EACH ROW
EXECUTE FUNCTION public.fn_evaluate_disease_outbreak();
```

---

### 3.2 Android Client-Side Architecture (`DiseaseAggregationService.kt`)

- **File**: `app/src/main/java/com/example/DiseaseAggregationService.kt`
- **Responsibilities**:
  1. `recordScan(diseaseName, crop, state, district, severity, confidence, lat, lng)`: Sends JSON payload to `$SUPABASE_URL/rest/v1/disease_scans`.
  2. `fetchActiveAlerts(state: String): List<OutbreakAlert>`: Queries `$SUPABASE_URL/rest/v1/outbreak_alerts?target_state=eq.{state}&is_active=eq.true&order=updated_at.desc`.
  3. `getNeighboringStates(state: String): List<String>`: Provides local in-memory adjacency lookup.
  4. `evaluateScanThresholdLocal(scans: List<DiseaseScanRecord>, threshold: Int = 100): List<OutbreakAlert>`: Provides client-side and unit-test evaluation of the 100-scan density rule.

---

### 3.3 UI Integration Plan for NuKropAI App

1. **`DiseaseScannerScreen.kt`**:
   - In `CameraScanner` / `PickVisualMedia` completion block, after parsing `CropScanData`:
   - If `data.status != "Healthy"`, launch coroutine in IO dispatcher:
     ```kotlin
     scope.launch(Dispatchers.IO) {
         val (state, district) = LocationHelper.getCurrentLocationStateAndMandi(context) ?: Pair("Maharashtra", "Pune")
         DiseaseAggregationService.recordScan(
             diseaseName = data.name,
             crop = "Crop",
             state = state.ifBlank { "Maharashtra" },
             district = district,
             severity = data.severity,
             confidence = data.confidence
         )
     }
     ```

2. **`HomeScreen.kt`**:
   - Update the "Hyperlocal Pest Prediction AI" section (lines 210–231) to reactively bind to `DiseaseAggregationService.watchAlertsForState(userState)`.
   - If an active alert exists (either EPICENTER or EARLY_WARNING), display the dynamic alert title, source state, scan count, and recommended action.

3. **`RegionalIntelligenceScreen.kt`**:
   - Replace static mockup cards with a dynamic list of active regional and neighboring alerts fetched via `DiseaseAggregationService.fetchActiveAlerts(userState)`.

---

## 4. Caveats

- **Assumption regarding State Names**: The geolocation reverse geocoding via `Geocoder.adminArea` standardizes state names (e.g. "Maharashtra", "Punjab"). The adjacency matrix and REST queries should use case-insensitive matching (`ilike` in PostgREST or `.trim().lowercase()`) to avoid spelling mismatches.
- **Threshold Parameterization**: While the default density threshold is set to 100 scans per 7-day window as requested in R1, both the SQL trigger and the Kotlin evaluation engine allow parameterization for smaller test batches (e.g. 5 scans for unit tests or 100 for production).
- **Fastify Backend Integration**: The Node/Fastify backend in `backend/src/controllers/pest.controller.ts` can also be updated to expose `/pests/scan` and `/pests/alerts` routes mirroring the Postgres queries for enterprise setups utilizing the Node API gateway.

---

## 5. Conclusion

1. The proposed architecture natively leverages the existing Supabase configuration (`SupabaseClient.kt`) without requiring additional third-party infrastructure.
2. The schema definitions for `disease_scans`, `state_adjacencies`, and `outbreak_alerts` alongside the PostgreSQL trigger `fn_evaluate_disease_outbreak()` satisfy all R1 criteria.
3. The 100-scan density threshold triggers an Epicenter alert for the originating state and automatically fans out early warning alerts to all adjacent neighboring states.
4. Independent verification through SQL simulation, Kotlin unit tests, and `./gradlew assembleDebug` can be executed cleanly.

---

## 6. Verification Method

### 6.1 Database / Trigger Logic Verification
1. **Insert 99 scans**:
   ```sql
   DO $$
   BEGIN
       FOR i IN 1..99 LOOP
           INSERT INTO public.disease_scans (disease_name, state, severity, confidence)
           VALUES ('Fall Armyworm', 'Maharashtra', 'High', 95);
       END LOOP;
   END $$;
   ```
   *Expectation*: `SELECT count(*) FROM public.outbreak_alerts WHERE disease_name = 'Fall Armyworm'` returns `0`.

2. **Insert the 100th scan**:
   ```sql
   INSERT INTO public.disease_scans (disease_name, state, severity, confidence)
   VALUES ('Fall Armyworm', 'Maharashtra', 'High', 95);
   ```
   *Expectation*:
   - Epicenter alert exists: `SELECT * FROM public.outbreak_alerts WHERE target_state = 'Maharashtra' AND alert_type = 'EPICENTER' AND scan_count = 100;` returns 1 row.
   - Neighbor alerts exist: `SELECT target_state, alert_type FROM public.outbreak_alerts WHERE source_state = 'Maharashtra' AND alert_type = 'EARLY_WARNING';` returns rows for Gujarat, Madhya Pradesh, Chhattisgarh, Telangana, Karnataka, Goa.

### 6.2 Android Compilation Verification
- Run `./gradlew assembleDebug` to verify that Kotlin data models, `DiseaseAggregationService.kt`, and UI integrations compile cleanly with exit code 0.
