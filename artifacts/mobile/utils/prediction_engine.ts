export interface YieldEstimate {
  expectedYield: number;
  potentialYield: number;
  diseaseImpact: number;
  productivityScore: number;
  harvestConfidence: number;
  stresses: { type: string; intensity: number }[]; // 0-1
}

export interface ProfitForecast {
  expectedProfit: number;
  roi: number;
  bestSellingPrice: number;
  riskFactor: number;
}

export function calculateYield(
  crop: string,
  healthScore: number,
  diseaseSeverity: "low" | "medium" | "high",
  weather: { temp: number; humidity: number; rain: number },
  nearbyOutbreaks: number
): YieldEstimate {
  const baseYields: Record<string, number> = {
    "Rice": 15, "Cotton": 8, "Maize": 12, "Wheat": 14, "Chilli": 10,
  };

  const potential = baseYields[crop] || 10;
  const impactMap = { low: 0.05, medium: 0.20, high: 0.45 };
  const diseaseImpact = impactMap[diseaseSeverity] || 0;

  // Stress Modeling
  const stresses: { type: string; intensity: number }[] = [];
  
  // Heat Stress
  if (weather.temp > 35) {
    stresses.push({ type: "Heat Stress", intensity: (weather.temp - 35) / 10 });
  }
  // Drought Stress (Low rain + high temp)
  if (weather.rain < 2 && weather.temp > 30) {
    stresses.push({ type: "Drought Stress", intensity: 0.4 });
  }
  // Fungal Stress (High humidity)
  if (weather.humidity > 85) {
    stresses.push({ type: "Fungal Pressure", intensity: 0.3 });
  }

  const totalStress = stresses.reduce((acc, s) => acc + s.intensity, 0);
  const healthAdj = healthScore / 100;
  const stressAdj = 1 - (totalStress * 0.1);

  const expected = potential * healthAdj * (1 - diseaseImpact) * stressAdj;
  
  return {
    expectedYield: parseFloat(expected.toFixed(1)),
    potentialYield: potential,
    diseaseImpact: Math.round(diseaseImpact * 100),
    productivityScore: Math.round(healthScore * stressAdj),
    harvestConfidence: Math.round(healthScore * (1 - (totalStress / 2))),
    stresses
  };
}

export function forecastProfit(
  yieldEst: YieldEstimate,
  mandiPrice: number, // per quintal
  costPerAcre: number = 15000 // default estimate in INR
): ProfitForecast {
  const revenue = yieldEst.expectedYield * mandiPrice;
  const profit = revenue - costPerAcre;
  const roi = (profit / costPerAcre) * 100;

  return {
    expectedProfit: Math.round(profit),
    roi: parseFloat(roi.toFixed(1)),
    bestSellingPrice: mandiPrice,
    riskFactor: (100 - yieldEst.harvestConfidence) / 100
  };
}
