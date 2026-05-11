export interface MandiMarket {
  id: string;
  name: string;
  distance: number; // km
  location: { lat: number; lon: number };
  crops: { name: string; price: number; trend: "up" | "down" | "stable" }[];
}

const REGIONAL_MARKETS: Omit<MandiMarket, "distance">[] = [
  {
    id: "m1",
    name: "Bowenpally Mandi (Hyderabad)",
    location: { lat: 17.47, lon: 78.47 },
    crops: [
      { name: "Tomato", price: 18, trend: "up" },
      { name: "Onion", price: 24, trend: "down" },
      { name: "Maize", price: 2150, trend: "stable" },
    ]
  },
  {
    id: "m2",
    name: "Gudimalkapur Market",
    location: { lat: 17.38, lon: 78.43 },
    crops: [
      { name: "Chilli", price: 185, trend: "up" },
      { name: "Tomato", price: 16, trend: "down" },
    ]
  },
  {
    id: "m3",
    name: "Siddipet Mandi",
    location: { lat: 18.10, lon: 78.85 },
    crops: [
      { name: "Cotton", price: 7200, trend: "up" },
      { name: "Maize", price: 2100, trend: "stable" },
    ]
  },
  {
    id: "m4",
    name: "Warangal Enamamula Mandi",
    location: { lat: 17.96, lon: 79.59 },
    crops: [
      { name: "Chilli", price: 210, trend: "up" },
      { name: "Cotton", price: 7400, trend: "up" },
    ]
  }
];

function calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number) {
  const R = 6371; // Earth radius in km
  const dLat = (lat2 - lat1) * (Math.PI / 180);
  const dLon = (lon2 - lon1) * (Math.PI / 180);
  const a = 
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * (Math.PI / 180)) * Math.cos(lat2 * (Math.PI / 180)) * 
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return Math.round(R * c);
}

export function getNearbyMarkets(userLat: number, userLon: number): MandiMarket[] {
  return REGIONAL_MARKETS.map(m => ({
    ...m,
    distance: calculateDistance(userLat, userLon, m.location.lat, m.location.lon)
  })).sort((a, b) => a.distance - b.distance);
}

export function getBestMarketForCrop(crop: string, userLat: number, userLon: number): { market: MandiMarket; price: number } | null {
  const markets = getNearbyMarkets(userLat, userLon);
  let best = null;
  let maxPrice = -1;

  for (const m of markets) {
    const cropData = m.crops.find(c => c.name.toLowerCase() === crop.toLowerCase());
    if (cropData && cropData.price > maxPrice) {
      // Basic logic: Higher price is better, but maybe consider distance later
      maxPrice = cropData.price;
      best = m;
    }
  }

  return best ? { market: best, price: maxPrice } : null;
}
