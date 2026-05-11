import { 
  collection, 
  query, 
  where, 
  getDocs, 
  orderBy, 
  limit, 
  Timestamp 
} from "firebase/firestore";
import { db } from "./firebase";

export interface PlatformMetrics {
  totalScans: number;
  activeUsers: number;
  topDiseases: { name: string; count: number }[];
  scansByDay: { date: string; count: number }[];
}

export async function fetchPlatformMetrics(): Promise<PlatformMetrics> {
  try {
    const analyticsRef = collection(db, "analytics");
    
    // Total Scans
    const scanQuery = query(analyticsRef, where("type", "==", "scan"));
    const scanSnap = await getDocs(scanQuery);
    const totalScans = scanSnap.size;

    // Active Users (Last 24h)
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const userQuery = query(
      analyticsRef, 
      where("timestamp", ">=", Timestamp.fromDate(yesterday))
    );
    const userSnap = await getDocs(userQuery);
    const activeUsers = new Set(userSnap.docs.map(doc => doc.data().userId)).size;

    // Top Diseases
    const diseaseMap: Record<string, number> = {};
    scanSnap.forEach(doc => {
      const disease = doc.data().metadata?.disease;
      if (disease) {
        diseaseMap[disease] = (diseaseMap[disease] || 0) + 1;
      }
    });
    const topDiseases = Object.entries(diseaseMap)
      .map(([name, count]) => ({ name, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5);

    return {
      totalScans,
      activeUsers,
      topDiseases,
      scansByDay: [], // Simplified for now
    };
  } catch (error) {
    console.error("Fetch metrics error:", error);
    return { totalScans: 0, activeUsers: 0, topDiseases: [], scansByDay: [] };
  }
}
