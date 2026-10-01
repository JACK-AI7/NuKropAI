-- ============================================================================
-- 003_gramhaul_truck_listings.sql
-- NuKropAI Enterprise AgriTech: GramHaul Shared Logistics & Fleet Tracking
-- ============================================================================

CREATE TABLE IF NOT EXISTS public.truck_listings (
    id TEXT PRIMARY KEY DEFAULT gen_random_uuid()::text,
    user_id TEXT,                                            -- Driver Auth ID or Farmer Profile ID
    driver_name TEXT NOT NULL,
    driver_phone TEXT NOT NULL,
    vehicle_type TEXT NOT NULL DEFAULT 'Tata 407 (Heavy Duty)',
    vehicle_plate TEXT NOT NULL,
    capacity_tons NUMERIC(5,2) DEFAULT 3.0,
    total_bags_capacity INTEGER NOT NULL DEFAULT 30,
    filled_bags INTEGER NOT NULL DEFAULT 0,
    rate_per_bag NUMERIC(8,2) NOT NULL DEFAULT 45.00,
    rate_per_km NUMERIC(8,2) DEFAULT 20.00,
    solo_rate NUMERIC(10,2) DEFAULT 1800.00,
    origin_village TEXT NOT NULL,
    destination_mandi TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    pickup_eta TEXT DEFAULT '30 mins',
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    is_cold_chain BOOLEAN DEFAULT FALSE,
    status TEXT DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'FULL', 'DEPARTED', 'CANCELLED')),
    rating NUMERIC(2,1) DEFAULT 4.9,
    trips_count INTEGER DEFAULT 25,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Performance indexes for spatial queries, active status filtering, and chronological sorting
CREATE INDEX IF NOT EXISTS idx_truck_listings_status ON public.truck_listings(status);
CREATE INDEX IF NOT EXISTS idx_truck_listings_coords ON public.truck_listings(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_truck_listings_created_at ON public.truck_listings(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE public.truck_listings ENABLE ROW LEVEL SECURITY;

-- Transparent RLS Policies for Mobile/Web Client Access
CREATE POLICY "Allow public read on truck_listings"
ON public.truck_listings FOR SELECT
USING (true);

CREATE POLICY "Allow public insert on truck_listings"
ON public.truck_listings FOR INSERT
WITH CHECK (true);

CREATE POLICY "Allow public update on truck_listings"
ON public.truck_listings FOR UPDATE
USING (true)
WITH CHECK (true);

CREATE POLICY "Allow public delete on truck_listings"
ON public.truck_listings FOR DELETE
USING (true);

-- Seed Authentic Regional Pooled Truck Fleet Records
INSERT INTO public.truck_listings (
    id, driver_name, driver_phone, vehicle_type, vehicle_plate, 
    capacity_tons, total_bags_capacity, filled_bags, rate_per_bag, 
    rate_per_km, solo_rate, origin_village, destination_mandi, departure_time, 
    pickup_eta, latitude, longitude, is_cold_chain, status, rating, trips_count
) VALUES
(
    'TRK-8419', 'Ramesh Yadav', '+91 98492 11048', 'Tata 407 (Heavy Duty)', 'TS-03-UB-8419',
    3.5, 30, 22, 45.00,
    22.00, 1800.00, 'Narsampet Rural', 'Warangal Enumamula APMC Yard', 'Today, 4:30 PM',
    '25 mins', 17.9750, 79.5990, FALSE, 'ACTIVE', 4.9, 142
),
(
    'TRK-4920', 'K. Venkatesham', '+91 94401 77391', 'Eicher Pro 2049 (Express)', 'AP-36-TA-4920',
    5.0, 45, 31, 65.00,
    28.00, 2800.00, 'Station Road, Warangal', 'Bowenpally APMC, Hyderabad', 'Today, 6:00 PM',
    '45 mins', 17.9880, 79.6150, FALSE, 'ACTIVE', 4.8, 98
),
(
    'TRK-1102', 'Md. Ismail Khan', '+91 99890 32184', 'Mahindra Bolero Maxi Truck', 'TS-04-EA-1102',
    2.0, 20, 14, 45.00,
    18.00, 1400.00, 'Mulugu Hub', 'Warangal Enumamula APMC Yard', 'Today, 5:15 PM',
    '35 mins', 17.9620, 79.6050, FALSE, 'ACTIVE', 4.9, 210
),
(
    'TRK-3391', 'Gurpreet Singh', '+91 98765 43210', 'Tata Ace (Chhota Hathi)', 'PB-10-CZ-3391',
    1.5, 15, 5, 40.00,
    16.00, 1200.00, 'Kazipet Mandi Gate', 'Warangal APMC Yard', 'Today, 5:45 PM',
    '20 mins', 17.9820, 79.5820, FALSE, 'ACTIVE', 5.0, 36
)
ON CONFLICT (id) DO NOTHING;
