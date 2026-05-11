import { 
  collection, 
  query, 
  where, 
  getDocs, 
  Timestamp 
} from "firebase/firestore";
import { db } from "./firebase";

export interface OutbreakRegion {
  district: string;
  count: number;
  diseases: { name: string; count: number }[];
  severity: "low" | "medium" | "high";
}

export interface DiseaseRisk {
  disease: string;
  probability: number; // 0-1
  factors: string[];
  severity: "low" | "medium" | "high";
}

export async function fetchRegionalOutbreaks(state: string): Promise<OutbreakRegion[]> {
  try {
    const analyticsRef = collection(db, "analytics");
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

    const q = query(
      analyticsRef,
      where("type", "==", "scan"),
      where("timestamp", ">=", Timestamp.fromDate(oneWeekAgo))
      // In a real app, we'd also filter by state if we stored it in the analytic doc
    );

    const snap = await getDocs(q);
    const districtMap: Record<string, { count: number; diseases: Record<string, number> }> = {};

    snap.forEach(doc => {
      const data = doc.data();
      const district = data.metadata?.district || "Unknown District";
      const disease = data.metadata?.disease;

      if (!districtMap[district]) {
        districtMap[district] = { count: 0, diseases: {} };
      }
      districtMap[district].count++;
      if (disease) {
        districtMap[district].diseases[disease] = (districtMap[district].diseases[disease] || 0) + 1;
      }
    });

    return Object.entries(districtMap).map(([district, data]) => {
      const diseases = Object.entries(data.diseases)
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count);
      
      const severity = data.count > 10 ? "high" : data.count > 5 ? "medium" : "low";

      return { district, count: data.count, diseases, severity };
    });
  } catch (error) {
    console.error("Outbreak fetch error:", error);
    return [];
  }
}

export function calculateDiseaseRisk(
  humidity: number, 
  temp: number, 
  nearbyOutbreaks: OutbreakRegion[]
): DiseaseRisk[] {
  const risks: DiseaseRisk[] = [];

  // Fungal Risk (High Humidity > 80% and Temp 20-30°C)
  if (humidity > 80 && temp > 20 && temp < 30) {
    risks.push({
      disease: "Late Blight / Fungal Spread",
      probability: 0.85,
      factors: ["High Humidity (>80%)", "Optimal Temp for Spores"],
      severity: "high"
    });
  }

  // Check nearby outbreak density
  const totalNearby = nearbyOutbreaks.reduce((acc, curr) => acc + curr.count, 0);
  if (totalNearby > 20) {
    risks.push({
      disease: "Regional Epidemic Risk",
      probability: 0.7,
      factors: [`${totalNearby} scans reported in your district this week`],
      severity: "medium"
    });
  }

  return risks;
}
