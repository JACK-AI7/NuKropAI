export interface MLMetrics {
  accuracy: number;
  falsePositives: number;
  falseNegatives: number;
  avgInferenceLatency: number;
  confidenceDrift: number;
  region: string;
}

export interface SystemHealth {
  cloudWorkers: "healthy" | "degraded" | "offline";
  satelliteApi: "connected" | "latency" | "disconnected";
  ingestionPipeline: "active" | "stalled";
  lastSync: string;
}

export async function getMLPerformanceReport(region: string): Promise<MLMetrics> {
  // Simulated telemetry data
  return {
    accuracy: 0.942,
    falsePositives: 12,
    falseNegatives: 4,
    avgInferenceLatency: 128, // ms
    confidenceDrift: -0.012,
    region
  };
}

export async function getSystemHealth(): Promise<SystemHealth> {
  return {
    cloudWorkers: "healthy",
    satelliteApi: "connected",
    ingestionPipeline: "active",
    lastSync: new Date().toISOString()
  };
}

export function logLatency(component: string, ms: number) {
  if (ms > 500) {
    console.warn(`[PERFORMANCE] ${component} latency high: ${ms}ms`);
  }
}
