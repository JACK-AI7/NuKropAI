-- ============================================================================
-- 🌾 NuKropAI Agrarian Intelligence OS — Development & Demo Seed Dataset
-- ⚠️ FOR LOCAL DEVELOPMENT / TEST ENVIRONMENT ONLY — DO NOT RUN IN PRODUCTION
-- ============================================================================
-- This file contains non-production seed data for UI testing, offline demos,
-- and local emulator validation. Production systems must ingest verified data
-- from authenticated drivers and official government APMC APIs.
-- ============================================================================

-- 1. Demo Moving Driver Fleet (Development Sandbox)
INSERT INTO public.driver_telemetry (driver_id, driver_name, vehicle_plate, vehicle_type, current_lat, current_lng, is_online, last_ping)
VALUES 
  ('GH-DEMO-4192', 'Suresh Yadav (Demo)', 'TS 03 UB 4491', 'Tata Ace Gold 1.5T', 17.9689, 79.5941, TRUE, NOW()),
  ('GH-DEMO-5521', 'M. Venkatesh (Demo)', 'TS 04 EC 8812', 'Mahindra Bolero Maxi 2.5T', 17.9812, 79.6105, TRUE, NOW()),
  ('GH-DEMO-3104', 'K. Anjaiah (Demo)', 'TS 08 RA 9940', 'Eicher Pro 14ft 5T', 17.9540, 79.5820, TRUE, NOW())
ON CONFLICT (driver_id) DO UPDATE 
SET current_lat = EXCLUDED.current_lat, current_lng = EXCLUDED.current_lng, is_online = TRUE, last_ping = NOW();

-- 2. Demo APMC Mandi Rates (Sample Benchmarks for Local Testing)
INSERT INTO public.mandi_live_rates (
  state, district, market_name, commodity, variety, min_price, max_price, modal_price, trend,
  source_name, source_url, source_dataset, trade_date, freshness_status, market_center_lat, market_center_lng
)
VALUES
  ('Telangana', 'Warangal', 'Warangal Enamamula APMC', 'Cotton', 'Hybrid / Local', 7400, 7850, 7650, 'UP',
   'Demo Dataset (For Dev Testing)', 'https://agmarknet.gov.in', 'Daily APMC Mandi Market Prices', CURRENT_DATE - INTERVAL '1 day', 'DAILY', 17.9945, 79.5892),
  ('Telangana', 'Warangal', 'Warangal Enamamula APMC', 'Chilli', 'Teja / Hybrid', 19800, 22500, 21200, 'UP',
   'Demo Dataset (For Dev Testing)', 'https://agmarknet.gov.in', 'Daily APMC Mandi Market Prices', CURRENT_DATE - INTERVAL '1 day', 'DAILY', 17.9945, 79.5892),
  ('Telangana', 'Warangal', 'Warangal Enamamula APMC', 'Maize', 'Yellow Hybrid', 2050, 2220, 2150, 'STABLE',
   'Demo Dataset (For Dev Testing)', 'https://agmarknet.gov.in', 'Daily APMC Mandi Market Prices', CURRENT_DATE - INTERVAL '1 day', 'DAILY', 17.9945, 79.5892),
  ('Telangana', 'Warangal', 'Warangal Enamamula APMC', 'Paddy', 'RNR 15048 / BPT', 2300, 2450, 2380, 'UP',
   'Demo Dataset (For Dev Testing)', 'https://agmarknet.gov.in', 'Daily APMC Mandi Market Prices', CURRENT_DATE - INTERVAL '1 day', 'DAILY', 17.9945, 79.5892),
  ('Telangana', 'Khammam', 'Khammam APMC', 'Cotton', 'DCH-32', 7350, 7780, 7600, 'UP',
   'Demo Dataset (For Dev Testing)', 'https://agmarknet.gov.in', 'Daily APMC Mandi Market Prices', CURRENT_DATE - INTERVAL '1 day', 'DAILY', 17.2472, 80.1514)
ON CONFLICT DO NOTHING;

-- 3. Demo BioShield Outbreak Alerts (Sample Agronomic Advisory)
INSERT INTO public.outbreak_alerts (crop_name, pest_name, state, district, severity, scan_count, market_price_impact, broadcast_message, is_active)
VALUES
  ('Cotton', 'Pink Bollworm (గులాబీ రంగు కాయ తొలిచే పురుగు)', 'Telangana', 'Warangal', 'HIGH_ALERT', 14, 4.50, 'వరంగల్ జిల్లాలో లింగాకర్షక బుట్టల్లో గులాబీ పురుగు ఆశించిన దాఖలాలున్నాయి. తగిన వేప నూనె లేదా ప్రొఫెనోఫాస్ పిచికారీ సిఫారసు చేయబడింది.', TRUE),
  ('Chilli', 'Black Thrips & Leaf Curl (నల్ల తామర & ఆకుముడత)', 'Telangana', 'Warangal', 'HIGH_ALERT', 28, 6.00, 'పొడి వాతావరణం వల్ల మిరపలో నల్ల తామర పురుగు గమనించబడింది. పొలంలో నీలం మరియు పసుపు జిగురు అట్టలు అమర్చండి.', TRUE)
ON CONFLICT DO NOTHING;

-- 4. Demo Kisan Community Posts (Sample Threads)
INSERT INTO public.community_posts (author_name, farmer_id, crop_id, crop_tag, title, content, likes_count, is_verified_agronomist)
VALUES
  ('రైతు మిత్రుడు (Demo)', 'NK-DEMO-01', 'cotton', 'cotton', 'పత్తి పంటలో గులాబీ పురుగు నివారణ పద్ధతులు', 'నా పొలంలో గులాబీ పురుగు నివారణ కోసం ఫెరమోన్ ట్రాప్స్ ఏర్పాటు చేశాను. మంచి ఫలితం కనిపిస్తోంది.', 12, FALSE),
  ('వ్యవసాయ విస్తరణ విభాగం (Demo)', 'NK-DEMO-AGRO', 'chilli', 'chilli', 'మిరపలో తామర పురుగుల సమగ్ర యాజమాన్యం', 'రైతు సోదరులారా, వాతావరణ మార్పులను గమనిస్తూ సిఫారసు చేసిన మోతాదులలో మాత్రమే జీవ నియంత్రణ మందులు వాడండి.', 45, TRUE)
ON CONFLICT DO NOTHING;
