import type { Farm, AIInsight } from "@/contexts/AppContext";

export interface CooperativeStats {
  totalAcreage: number;
  averageHealth: number;
  outbreakCount: number;
  topPerformingCrop: string;
  productivityIndex: number; // 0-100
}

export interface DistrictInsight {
  district: string;
  avgNDVI: number;
  activeOutbreaks: number;
  expectedYieldTotal: number;
  rainfallStatus: "Deficit" | "Normal" | "Excess";
}

export function aggregateCooperativeData(farms: Farm[]): CooperativeStats {
  if (farms.length === 0) return { totalAcreage: 0, averageHealth: 0, outbreakCount: 0, topPerformingCrop: "N/A", productivityIndex: 0 };

  const totalAcreage = farms.reduce((acc, f) => acc + f.area, 0);
  const avgHealth = farms.reduce((acc, f) => acc + f.ndvi.score, 0) / farms.length;
  
  return {
    totalAcreage,
    averageHealth: Math.round(avgHealth * 100),
    outbreakCount: 4, // Simulated for the group
    topPerformingCrop: "Rice",
    productivityIndex: 82
  };
}

export function getDistrictIntelligence(): DistrictInsight[] {
  return [
    { district: "Hyderabad", avgNDVI: 0.75, activeOutbreaks: 2, expectedYieldTotal: 12500, rainfallStatus: "Normal" },
    { district: "Medak", avgNDVI: 0.68, activeOutbreaks: 5, expectedYieldTotal: 8400, rainfallStatus: "Deficit" },
    { district: "Nalgonda", avgNDVI: 0.82, activeOutbreaks: 1, expectedYieldTotal: 15200, rainfallStatus: "Excess" },
    { district: "Rangareddy", avgNDVI: 0.71, activeOutbreaks: 3, expectedYieldTotal: 9800, rainfallStatus: "Normal" },
  ];
}

export function generateEnterpriseReport(stats: CooperativeStats): string {
  return `ENTERPRISE PERFORMANCE REPORT
==============================
Date: ${new Date().toLocaleDateString()}
Total Cooperative Area: ${stats.totalAcreage} Acres
Avg Vegetation Health: ${stats.averageHealth}%
Active Group Alerts: ${stats.outbreakCount}
Productivity Index: ${stats.productivityIndex}/100

RECOMMENDATION: 
Targeted nitrogen application needed for Medak cluster due to low NDVI trends.`;
}
