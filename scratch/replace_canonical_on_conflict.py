import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('supabase/CANONICAL_PRODUCTION_SETUP.sql', 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize line endings
text = text.replace('\r\n', '\n')

# 1. Replace handle_new_auth_user
text = text.replace("""  INSERT INTO public.profiles (
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
      full_name = EXCLUDED.full_name;""",
"""  IF NOT EXISTS (SELECT 1 FROM public.profiles WHERE id = NEW.id) THEN
    INSERT INTO public.profiles (id, user_id, farmer_id, email, full_name, role)
    VALUES (NEW.id, NEW.id, v_fid, NEW.email, v_name, v_role);
  ELSE
    UPDATE public.profiles
    SET email = NEW.email, full_name = v_name
    WHERE id = NEW.id;
  END IF;""")

# 2. Replace BioRx Recipes Seed
old_biorx_seed = """-- BioRx Recipes Seed
INSERT INTO public.biorx_recipes (title, target_pest_disease, ingredients, preparation_steps, fermentation_hours, dilution_ratio, shelf_life_days, icar_approved)
VALUES
('Dashaparni Kashayam', ARRAY['thrips', 'aphids', 'whiteflies', 'caterpillars'],
 '{"neem_leaves_kg": 5, "papaya_leaves_kg": 2, "custard_apple_leaves_kg": 2, "cow_urine_liters": 10, "cow_dung_kg": 2, "water_liters": 200}'::jsonb,
 '["Crush all 10 medicinal leaves into a coarse paste", "Mix cow dung and cow urine in 200L water tank", "Add crushed leaves paste into the solution", "Cover with gunny bag and stir clockwise twice daily for 21 days", "Filter through fine cotton cloth before spraying"]'::jsonb,
 504, '1:10 (Water)', 180, true),
('Jeevamrutha (Liquid Bio-Fertilizer)', ARRAY['soil_fertility', 'root_rot', 'microbial_boost'],
 '{"cow_dung_kg": 10, "cow_urine_liters": 10, "jaggery_kg": 2, "pulse_flour_kg": 2, "virgin_soil_handfuls": 1, "water_liters": 200}'::jsonb,
 '["Fill 200L drum with fresh water", "Add fresh cow dung and cow urine and stir vigorously", "Dissolve 2kg jaggery and 2kg chickpea flour in water and add to drum", "Add handful of fertile soil from field bund", "Keep in shade, stir 10 minutes clockwise twice daily for 48-72 hours"]'::jsonb,
 72, '1:10 (Irrigation/Foliar)', 7, true),
('Neemastra', ARRAY['sucking_pests', 'mealybugs', 'leaf_hoppers'],
 '{"cow_urine_liters": 5, "cow_dung_kg": 2, "neem_leaves_kg": 5, "water_liters": 100}'::jsonb,
 '["Crush 5kg neem leaves into fine pulp", "Mix with 2kg fresh cow dung and 5L cow urine in 100L water", "Ferment for 48 hours in shadow", "Filter cloth and spray directly without extra dilution"]'::jsonb,
 48, 'Direct Spray (No Dilution)', 21, true)
ON CONFLICT (title) DO NOTHING;"""

new_biorx_seed = """-- BioRx Recipes Seed (Safe Zero-Conflict)
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
WHERE NOT EXISTS (SELECT 1 FROM public.biorx_recipes WHERE title = 'Neemastra');"""

text = text.replace(old_biorx_seed, new_biorx_seed)

# 3. Replace Subsidies Seed
old_subsidies_seed = """-- Official Government Subsidies Seed
INSERT INTO public.subsidies (scheme_name, authority, benefit_amount, eligibility, official_portal_url, status)
VALUES
('PM-KISAN Samman Nidhi', 'Ministry of Agriculture, Govt of India', '₹6,000 / year (3 installments)', 'All landholding farmer families with valid Aadhaar and e-KYC', 'https://pmkisan.gov.in/', 'Active / Open'),
('Telangana Rythu Bandhu / Rythu Bharosa', 'Government of Telangana', '₹15,000 / acre / year', 'All verified pattadar landholders in Telangana Dharani database', 'https://rythubandhu.telangana.gov.in/', 'Active / Open'),
('Kisan Credit Card (KCC) Subvention', 'Reserve Bank of India / NABARD', 'Up to ₹3,00,000 at 4% Interest', 'All farmers with land passbook or verified tenant agreement', 'https://www.nabard.org/', 'Active / Open'),
('PM Krishi Sinchayee Yojana (Micro-Irrigation)', 'Dept of Agriculture & Cooperation', 'Up to 90% Drip / Sprinkler Subsidy', 'Small and marginal farmers with active borewell/water source', 'https://pmksy.gov.in/', 'Active / Open')
ON CONFLICT (scheme_name) DO NOTHING;"""

new_subsidies_seed = """-- Official Government Subsidies Seed (Safe Zero-Conflict)
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
WHERE NOT EXISTS (SELECT 1 FROM public.subsidies WHERE scheme_name = 'PM Krishi Sinchayee Yojana (Micro-Irrigation)');"""

text = text.replace(old_subsidies_seed, new_subsidies_seed)

# 4. Replace Mandi Live Rates Seed
old_mandi_seed = """-- APMC Live Mandi Rates Initial Snapshot
INSERT INTO public.mandi_live_rates (state, district, market, commodity, commodity_te, commodity_hi, min_price, max_price, modal_price, msp_price, arrivals_qtl, trend, trend_pct)
VALUES
('Telangana', 'Warangal', 'Warangal APMC Yard', 'Cotton (Long Staple)', 'పత్తి', 'कपास', 7450, 7850, 7680, 7121, 2450, 'up', 2.8),
('Telangana', 'Warangal', 'Warangal APMC Yard', 'Chilli (Teja Variety)', 'తేజ మిరప', 'तेजा मिर्च', 18200, 21500, 19800, 0, 850, 'up', 4.2),
('Telangana', 'Warangal', 'Warangal APMC Yard', 'Paddy (Basmati / Fine)', 'వరి (సన్న బియ్యం)', 'धान (बासमती)', 2300, 2680, 2450, 2203, 3100, 'stable', 0.0),
('Telangana', 'Hyderabad', 'Bowenpally Wholesale APMC', 'Tomato (Hybrid)', 'టమోటా', 'टमाटर', 1400, 2200, 1850, 0, 4200, 'down', -3.1),
('Telangana', 'Hyderabad', 'Bowenpally Wholesale APMC', 'Onion (Red)', 'ఉల్లిపాయ', 'प्याज', 2200, 3100, 2750, 0, 3800, 'up', 1.9)
ON CONFLICT DO NOTHING;"""

new_mandi_seed = """-- APMC Live Mandi Rates Initial Snapshot (Safe Zero-Conflict)
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
WHERE NOT EXISTS (SELECT 1 FROM public.mandi_live_rates WHERE market = 'Bowenpally Wholesale APMC' AND commodity = 'Onion (Red)');"""

text = text.replace(old_mandi_seed, new_mandi_seed)

with open('supabase/CANONICAL_PRODUCTION_SETUP.sql', 'w', encoding='utf-8') as f:
    f.write(text)

print("✅ Successfully updated CANONICAL_PRODUCTION_SETUP.sql with 100% zero-conflict syntax!")
