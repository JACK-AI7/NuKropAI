export interface SatelliteImagery {
  id: string;
  timestamp: string;
  ndviMapUrl: string;
  moistureIndex: number;
  vegetationCover: number; // 0-1
}

export async function fetchSentinelData(lat: number, lon: number, radius: number = 500): Promise<SatelliteImagery> {
  // Preparation for Sentinel Hub API
  // Real implementation would use: https://services.sentinel-hub.com/ogc/wms/
  
  const mockImageUrl = `https://api.sentinel-hub.com/mock/ndvi/${lat}/${lon}.png`;
  
  return {
    id: `sat_${Date.now()}`,
    timestamp: new Date().toISOString(),
    ndviMapUrl: mockImageUrl,
    moistureIndex: 0.65 + Math.random() * 0.2,
    vegetationCover: 0.78
  };
}

export async function getHistoricalPrecipitation(lat: number, lon: number, days: number = 30) {
  // Preparation for NASA POWER API
  // Real implementation would use: https://power.larc.nasa.gov/api/temporal/daily/point
  
  return {
    totalPrecipitation: 124.5, // mm
    anomaliesDetected: false,
    trend: "normal"
  };
}

export const SatelliteLayers = {
  NDVI: "NDVI_COLOR_MAP",
  MOISTURE: "MOISTURE_STRESS_MAP",
  VITALITY: "CROP_VITALITY_MAP"
};
