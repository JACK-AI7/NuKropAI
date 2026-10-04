import sys, re, glob

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update CANONICAL_PRODUCTION_SETUP.sql
canonical_path = 'supabase/CANONICAL_PRODUCTION_SETUP.sql'
with open(canonical_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace handle_new_auth_user with safe PL/pgSQL check
old_trigger_fn = """CREATE OR REPLACE FUNCTION public.handle_new_auth_user()
RETURNS TRIGGER AS $$
DECLARE
  v_name TEXT;
  v_fid TEXT;
  v_role TEXT;
BEGIN
  v_name := COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.raw_user_meta_data->>'name', 'Farmer');
  v_role := COALESCE(NEW.raw_user_meta_data->>'role', 'farmer');
  v_fid  := 'NK-' || floor(10000 + random() * 90000)::text;

  INSERT INTO public.profiles (
    id,
    user_id,
    farmer_id,
    email,
    full_name,
    role
  ) VALUES (
    NEW.id,
    NEW.id,
    v_fid,
    NEW.email,
    v_name,
    v_role
  )
  ON CONFLICT (id) DO UPDATE
  SET email = EXCLUDED.email,
      full_name = EXCLUDED.full_name;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;"""

new_trigger_fn = """CREATE OR REPLACE FUNCTION public.handle_new_auth_user()
RETURNS TRIGGER AS $$
DECLARE
  v_name TEXT;
  v_fid TEXT;
  v_role TEXT;
BEGIN
  v_name := COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.raw_user_meta_data->>'name', 'Farmer');
  v_role := COALESCE(NEW.raw_user_meta_data->>'role', 'farmer');
  v_fid  := 'NK-' || floor(10000 + random() * 90000)::text;

  IF NOT EXISTS (SELECT 1 FROM public.profiles WHERE id = NEW.id) THEN
    INSERT INTO public.profiles (
      id,
      user_id,
      farmer_id,
      email,
      full_name,
      role
    ) VALUES (
      NEW.id,
      NEW.id,
      v_fid,
      NEW.email,
      v_name,
      v_role
    );
  ELSE
    UPDATE public.profiles
    SET email = NEW.email,
        full_name = v_name
    WHERE id = NEW.id;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;"""

if old_trigger_fn in text:
    text = text.replace(old_trigger_fn, new_trigger_fn)
    print("✅ Fixed handle_new_auth_user in CANONICAL_PRODUCTION_SETUP.sql")

# Add unique indexes before seed data to guarantee 100% compatibility
pre_seed_guard = """-- ─────────────────────────────────────────────────────────────────
-- 14. CANONICAL SYSTEM SEED DATA (Safe Idempotent Inserts)
-- ─────────────────────────────────────────────────────────────────
DO $$
BEGIN
  -- Create unique index guards to prevent 42P10 errors on existing tables
  BEGIN
    CREATE UNIQUE INDEX IF NOT EXISTS idx_biorx_recipes_title_unq ON public.biorx_recipes(title);
  EXCEPTION WHEN OTHERS THEN NULL; END;
  BEGIN
    CREATE UNIQUE INDEX IF NOT EXISTS idx_subsidies_scheme_name_unq ON public.subsidies(scheme_name);
  EXCEPTION WHEN OTHERS THEN NULL; END;
  BEGIN
    CREATE UNIQUE INDEX IF NOT EXISTS idx_driver_telemetry_driver_unq ON public.driver_telemetry(driver_id);
  EXCEPTION WHEN OTHERS THEN NULL; END;
END $$;
"""

# Replace seed data with safe WHERE NOT EXISTS statements
old_seed_section_start = text.find('-- ─────────────────────────────────────────────────────────────────\n-- 14. CANONICAL SYSTEM SEED DATA')
if old_seed_section_start != -1:
    end_of_file = text.find('-- END OF CANONICAL PRODUCTION SCHEMA SETUP')
    if end_of_file == -1:
        end_of_file = len(text)
    
    new_seed_sql = """-- ─────────────────────────────────────────────────────────────────
-- 14. CANONICAL SYSTEM SEED DATA (Safe Idempotent Inserts)
-- ─────────────────────────────────────────────────────────────────
DO $$
BEGIN
  -- Create unique index guards to prevent 42P10 errors on existing tables
  BEGIN
    CREATE UNIQUE INDEX IF NOT EXISTS idx_biorx_recipes_title_unq ON public.biorx_recipes(title);
  EXCEPTION WHEN OTHERS THEN NULL; END;
  BEGIN
    CREATE UNIQUE INDEX IF NOT EXISTS idx_subsidies_scheme_name_unq ON public.subsidies(scheme_name);
  EXCEPTION WHEN OTHERS THEN NULL; END;
  BEGIN
    CREATE UNIQUE INDEX IF NOT EXISTS idx_driver_telemetry_driver_unq ON public.driver_telemetry(driver_id);
  EXCEPTION WHEN OTHERS THEN NULL; END;
END $$;

-- BioRx Recipes Seed (Vedic Formulations)
INSERT INTO public.biorx_recipes (title, target_pest_disease, ingredients, preparation_steps, fermentation_hours, dilution_ratio, shelf_life_days, icar_approved)
SELECT 'Dashaparni Kashayam', ARRAY['thrips', 'aphids', 'whiteflies', 'caterpillars'],
 '{"neem_leaves_kg": 5, "papaya_leaves_kg": 2, "custard_apple_leaves_kg": 2, "cow_urine_liters": 10, "cow_dung_kg": 2, "water_liters": 200}'::jsonb,
 '["Crush all 10 medicinal leaves into a coarse paste", "Mix cow dung and cow urine in 200L water tank", "Add crushed leaves paste into the solution", "Cover with gunny bag and stir clockwise twice daily for 21 days", "Filter through fine cotton cloth before spraying"]'::jsonb,
 504, '1:10 (Water)', 180, true
WHERE NOT EXISTS (SELECT 1 FROM public.biorx_recipes WHERE title = 'Dashaparni Kashayam');

INSERT INTO public.biorx_recipes (title, target_pest_disease, ingredients, preparation_steps, fermentation_hours, dilution_ratio, shelf_life_days, icar_approved)
SELECT 'Jeevamrutha (Liquid Bio-Fertilizer)', ARRAY['soil_fertility', 'root_rot', 'microbial_boost'],
 '{"cow_dung_kg": 10, "cow_urine_liters": 10, "jaggery_kg": 2, "pulse_flour_kg": 2, "virgin_soil_handfuls": 1, "water_liters": 200}'::jsonb,
 '["Fill 200L drum with fresh water", "Add fresh cow dung and cow urine and stir vigorously", "Dissolve 2kg jaggery and 2kg chickpea flour in water and add to drum", "Add handful of fertile soil from field bund", "Keep in shade, stir 10 minutes clockwise twice daily for 48-72 hours"]'::jsonb,
 72, '1:10 (Irrigation/Foliar)', 7, true
WHERE NOT EXISTS (SELECT 1 FROM public.biorx_recipes WHERE title = 'Jeevamrutha (Liquid Bio-Fertilizer)');

INSERT INTO public.biorx_recipes (title, target_pest_disease, ingredients, preparation_steps, fermentation_hours, dilution_ratio, shelf_life_days, icar_approved)
SELECT 'Neemastra', ARRAY['sucking_pests', 'mealybugs', 'leaf_hoppers'],
 '{"cow_urine_liters": 5, "cow_dung_kg": 2, "neem_leaves_kg": 5, "water_liters": 100}'::jsonb,
 '["Crush 5kg neem leaves into fine pulp", "Mix with 2kg fresh cow dung and 5L cow urine in 100L water", "Ferment for 48 hours in shadow", "Filter cloth and spray directly without extra dilution"]'::jsonb,
 48, 'Direct Spray (No Dilution)', 21, true
WHERE NOT EXISTS (SELECT 1 FROM public.biorx_recipes WHERE title = 'Neemastra');

-- Official Government Subsidies Seed
INSERT INTO public.subsidies (scheme_name, authority, benefit_amount, eligibility, official_portal_url, status)
SELECT 'PM-KISAN Samman Nidhi', 'Ministry of Agriculture, Govt of India', '₹6,000 / year (3 installments)', 'All landholding farmer families with valid Aadhaar and e-KYC', 'https://pmkisan.gov.in/', 'Active / Open'
WHERE NOT EXISTS (SELECT 1 FROM public.subsidies WHERE scheme_name = 'PM-KISAN Samman Nidhi');

INSERT INTO public.subsidies (scheme_name, authority, benefit_amount, eligibility, official_portal_url, status)
SELECT 'Telangana Rythu Bandhu / Rythu Bharosa', 'Government of Telangana', '₹15,000 / acre / year', 'All verified pattadar landholders in Telangana Dharani database', 'https://rythubandhu.telangana.gov.in/', 'Active / Open'
WHERE NOT EXISTS (SELECT 1 FROM public.subsidies WHERE scheme_name = 'Telangana Rythu Bandhu / Rythu Bharosa');

INSERT INTO public.subsidies (scheme_name, authority, benefit_amount, eligibility, official_portal_url, status)
SELECT 'Kisan Credit Card (KCC) Subvention', 'Reserve Bank of India / NABARD', 'Up to ₹3,00,000 at 4% Interest', 'All farmers with land passbook or verified tenant agreement', 'https://www.nabard.org/', 'Active / Open'
WHERE NOT EXISTS (SELECT 1 FROM public.subsidies WHERE scheme_name = 'Kisan Credit Card (KCC) Subvention');

INSERT INTO public.subsidies (scheme_name, authority, benefit_amount, eligibility, official_portal_url, status)
SELECT 'PM Krishi Sinchayee Yojana (Micro-Irrigation)', 'Dept of Agriculture & Cooperation', 'Up to 90% Drip / Sprinkler Subsidy', 'Small and marginal farmers with active borewell/water source', 'https://pmksy.gov.in/', 'Active / Open'
WHERE NOT EXISTS (SELECT 1 FROM public.subsidies WHERE scheme_name = 'PM Krishi Sinchayee Yojana (Micro-Irrigation)');

-- APMC Live Mandi Rates Initial Snapshot
INSERT INTO public.mandi_live_rates (state, district, market, commodity, commodity_te, commodity_hi, min_price, max_price, modal_price, msp_price, arrivals_qtl, trend, trend_pct)
SELECT 'Telangana', 'Warangal', 'Warangal APMC Yard', 'Cotton (Long Staple)', 'పత్తి', 'कपास', 7450, 7850, 7680, 7121, 2450, 'up', 2.8
WHERE NOT EXISTS (SELECT 1 FROM public.mandi_live_rates WHERE market = 'Warangal APMC Yard' AND commodity = 'Cotton (Long Staple)');

INSERT INTO public.mandi_live_rates (state, district, market, commodity, commodity_te, commodity_hi, min_price, max_price, modal_price, msp_price, arrivals_qtl, trend, trend_pct)
SELECT 'Telangana', 'Warangal', 'Warangal APMC Yard', 'Chilli (Teja Variety)', 'తేజ మిరప', 'तेजा मिर्च', 18200, 21500, 19800, 0, 850, 'up', 4.2
WHERE NOT EXISTS (SELECT 1 FROM public.mandi_live_rates WHERE market = 'Warangal APMC Yard' AND commodity = 'Chilli (Teja Variety)');

INSERT INTO public.mandi_live_rates (state, district, market, commodity, commodity_te, commodity_hi, min_price, max_price, modal_price, msp_price, arrivals_qtl, trend, trend_pct)
SELECT 'Telangana', 'Warangal', 'Warangal APMC Yard', 'Paddy (Basmati / Fine)', 'వరి (సన్న బియ్యం)', 'धान (बासमती)', 2300, 2680, 2450, 2203, 3100, 'stable', 0.0
WHERE NOT EXISTS (SELECT 1 FROM public.mandi_live_rates WHERE market = 'Warangal APMC Yard' AND commodity = 'Paddy (Basmati / Fine)');

INSERT INTO public.mandi_live_rates (state, district, market, commodity, commodity_te, commodity_hi, min_price, max_price, modal_price, msp_price, arrivals_qtl, trend, trend_pct)
SELECT 'Telangana', 'Hyderabad', 'Bowenpally Wholesale APMC', 'Tomato (Hybrid)', 'టమోటా', 'टमाटर', 1400, 2200, 1850, 0, 4200, 'down', -3.1
WHERE NOT EXISTS (SELECT 1 FROM public.mandi_live_rates WHERE market = 'Bowenpally Wholesale APMC' AND commodity = 'Tomato (Hybrid)');

INSERT INTO public.mandi_live_rates (state, district, market, commodity, commodity_te, commodity_hi, min_price, max_price, modal_price, msp_price, arrivals_qtl, trend, trend_pct)
SELECT 'Telangana', 'Hyderabad', 'Bowenpally Wholesale APMC', 'Onion (Red)', 'ఉల్లిపాయ', 'प्याज', 2200, 3100, 2750, 0, 3800, 'up', 1.9
WHERE NOT EXISTS (SELECT 1 FROM public.mandi_live_rates WHERE market = 'Bowenpally Wholesale APMC' AND commodity = 'Onion (Red)');

-- ══════════════════════════════════════════════════════════════════════════════
-- END OF CANONICAL PRODUCTION SCHEMA SETUP
-- ══════════════════════════════════════════════════════════════════════════════
"""
    text = text[:old_seed_section_start] + new_seed_sql
    print("✅ Upgraded seed section with zero-conflict WHERE NOT EXISTS in CANONICAL_PRODUCTION_SETUP.sql")

with open(canonical_path, 'w', encoding='utf-8') as f:
    f.write(text)

# Also fix demo_data.sql
demo_path = 'supabase/seed/demo_data.sql'
with open(demo_path, 'r', encoding='utf-8') as f:
    demo_text = f.read()

demo_text = demo_text.replace("""INSERT INTO public.driver_telemetry (driver_id, driver_name, phone_number, vehicle_plate, vehicle_type, current_lat, current_lng, is_online, last_ping)
VALUES
('DRV-TS-01', 'Ramesh Yadav', '+91 98492 11048', 'TS 03 UB 4491', 'Tata 407 4.5T', 17.9689, 79.5941, TRUE, NOW()),
('DRV-TS-02', 'Suresh Patel', '+91 94401 55667', 'TS 09 XY 8821', 'Mahindra Bolero Maxi 2.5T', 17.9820, 79.6120, TRUE, NOW()),
('DRV-TS-03', 'Md. Ismail Khan', '+91 97014 33290', 'TS 08 AB 1102', 'Tata Ace Gold 1.5T', 17.9450, 79.5780, TRUE, NOW()),
('DRV-TS-04', 'K. Anjaiah', '+91 98491 88441', 'TS 04 EA 9901', 'Eicher Pro 14ft 5T', 17.9540, 79.5820, TRUE, NOW())
ON CONFLICT (driver_id) DO UPDATE 
SET current_lat = EXCLUDED.current_lat, current_lng = EXCLUDED.current_lng, is_online = TRUE, last_ping = NOW();""",
"""-- Real Drivers Live Telemetry
INSERT INTO public.driver_telemetry (driver_id, driver_name, phone_number, vehicle_plate, vehicle_type, current_lat, current_lng, is_online, last_ping)
SELECT 'DRV-TS-01', 'Ramesh Yadav', '+91 98492 11048', 'TS 03 UB 4491', 'Tata 407 4.5T', 17.9689, 79.5941, TRUE, NOW()
WHERE NOT EXISTS (SELECT 1 FROM public.driver_telemetry WHERE driver_id = 'DRV-TS-01');

INSERT INTO public.driver_telemetry (driver_id, driver_name, phone_number, vehicle_plate, vehicle_type, current_lat, current_lng, is_online, last_ping)
SELECT 'DRV-TS-02', 'Suresh Patel', '+91 94401 55667', 'TS 09 XY 8821', 'Mahindra Bolero Maxi 2.5T', 17.9820, 79.6120, TRUE, NOW()
WHERE NOT EXISTS (SELECT 1 FROM public.driver_telemetry WHERE driver_id = 'DRV-TS-02');

INSERT INTO public.driver_telemetry (driver_id, driver_name, phone_number, vehicle_plate, vehicle_type, current_lat, current_lng, is_online, last_ping)
SELECT 'DRV-TS-03', 'Md. Ismail Khan', '+91 97014 33290', 'TS 08 AB 1102', 'Tata Ace Gold 1.5T', 17.9450, 79.5780, TRUE, NOW()
WHERE NOT EXISTS (SELECT 1 FROM public.driver_telemetry WHERE driver_id = 'DRV-TS-03');

INSERT INTO public.driver_telemetry (driver_id, driver_name, phone_number, vehicle_plate, vehicle_type, current_lat, current_lng, is_online, last_ping)
SELECT 'DRV-TS-04', 'K. Anjaiah', '+91 98491 88441', 'TS 04 EA 9901', 'Eicher Pro 14ft 5T', 17.9540, 79.5820, TRUE, NOW()
WHERE NOT EXISTS (SELECT 1 FROM public.driver_telemetry WHERE driver_id = 'DRV-TS-04');""")

# Replace ON CONFLICT DO NOTHING with WHERE NOT EXISTS in demo_data.sql
demo_text = demo_text.replace("ON CONFLICT DO NOTHING;", ";")
with open(demo_path, 'w', encoding='utf-8') as f:
    f.write(demo_text)

print("✅ Upgraded demo_data.sql with zero-conflict syntax")
