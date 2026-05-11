export interface AnomalyEvent {
  id: string;
  type: "NDVI_DROP" | "MOISTURE_STRESS" | "TEMP_SPIKE" | "OUTBREAK_CLUSTER";
  severity: "critical" | "warning" | "info";
  score: number; // Deviation score
  timestamp: string;
  description: string;
}

export function detectAnomalies(currentValue: number, historicalMean: number, stdDev: number): number {
  if (stdDev === 0) return 0;
  return Math.abs(currentValue - historicalMean) / stdDev; // Z-score
}

export async function processAnomalyPipeline(sensorData: { type: string, value: number }[]): Promise<AnomalyEvent[]> {
  const anomalies: AnomalyEvent[] = [];
  
  sensorData.forEach(data => {
    // Appropriate historical baselines for different sensors
    const baselines: Record<string, { mean: number, std: number }> = {
      ndvi: { mean: 75, std: 10 },
      moisture: { mean: 60, std: 15 },
      temp: { mean: 32, std: 4 },
    };

    const base = baselines[data.type] || { mean: 50, std: 10 };
    const zScore = detectAnomalies(data.value, base.mean, base.std);
    
    if (zScore > 2.5) { // Lower threshold to 2.5 for better sensitivity
      anomalies.push({
        id: `anom_${Date.now()}_${data.type}`,
        type: data.type === "ndvi" ? "NDVI_DROP" : "MOISTURE_STRESS",
        severity: zScore > 4 ? "critical" : "warning",
        score: zScore,
        timestamp: new Date().toISOString(),
        description: `Significant ${data.type} deviation (Z-Score: ${zScore.toFixed(2)}). Possible crop stress detected.`
      });
    }
  });
  
  return anomalies;
}

export function getSeverityColor(severity: AnomalyEvent["severity"]): string {
  switch (severity) {
    case "critical": return "#EF4444";
    case "warning": return "#F59E0B";
    default: return "#3B82F6";
  }
}
