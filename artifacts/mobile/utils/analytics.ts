import analytics from "@react-native-firebase/analytics";
import { collection, addDoc, serverTimestamp } from "firebase/firestore";
import { db } from "./firebase";

export type EventType = "scan" | "chat" | "alert_click" | "weather_view" | "market_view" | "app_open";

export async function logEvent(userId: string | undefined, type: EventType, metadata: Record<string, any> = {}) {
  try {
    // 1. Log to dedicated Firebase Analytics dashboard
    await analytics().logEvent(type, {
      userId: userId || "anonymous",
      ...metadata,
    });

    // 2. Log to Firestore for custom in-app query needs
    await addDoc(collection(db, "analytics"), {
      userId: userId || "anonymous",
      type,
      metadata,
      timestamp: serverTimestamp(),
    });
  } catch (error) {
    console.error("Analytics logging error:", error);
  }
}
