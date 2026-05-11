export interface NDVIData {
  timestamp: string;
  score: number; // 0-1 (NDVI scale)
  healthStatus: "Excellent" | "Good" | "Average" | "Poor";
  canopyDensity: number; // Percentage
  moistureIndex: number; // 0-1
}

export function calculateNDVIHealth(score: number): NDVIData["healthStatus"] {
  if (score > 0.8) return "Excellent";
  if (score > 0.6) return "Good";
  if (score > 0.4) return "Average";
  return "Poor";
}

export function simulateNDVIMap(bounds: { lat: number; lon: number }[]): number[][] {
  // Simulates a grid of NDVI values for a farm area
  const grid: number[][] = [];
  for (let i = 0; i < 5; i++) {
    const row: number[] = [];
    for (let j = 0; j < 5; j++) {
      row.push(0.5 + Math.random() * 0.4); // Random NDVI values between 0.5 and 0.9
    }
    grid.push(row);
  }
  return grid;
}

export function getVegetationAnomalies(ndviGrid: number[][]): { x: number, y: number, severity: number }[] {
  const anomalies: { x: number, y: number, severity: number }[] = [];
  ndviGrid.forEach((row, y) => {
    row.forEach((val, x) => {
      if (val < 0.4) {
        anomalies.push({ x, y, severity: 1 - val });
      }
    });
  });
  return anomalies;
}

export interface GeospatialOverlay {
  type: "outbreak" | "rainfall" | "vegetation" | "market";
  points: { lat: number, lon: number, value: number }[];
  color: string;
}

export function getRegionalOverlays(centerLat: number, centerLon: number): GeospatialOverlay[] {
  return [
    {
      type: "outbreak",
      color: "#FF453A",
      points: [
        { lat: centerLat + 0.01, lon: centerLon + 0.01, value: 0.8 },
        { lat: centerLat - 0.005, lon: centerLon + 0.02, value: 0.6 },
      ]
    },
    {
      type: "vegetation",
      color: "#22C55E",
      points: [
        { lat: centerLat, lon: centerLon, value: 0.9 },
        { lat: centerLat + 0.02, lon: centerLon - 0.01, value: 0.7 },
      ]
    }
  ];
}
