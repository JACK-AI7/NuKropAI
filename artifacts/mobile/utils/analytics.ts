import analytics from "@react-native-firebase/analytics";
import crashlytics from "@react-native-firebase/crashlytics";
import { collection, addDoc, serverTimestamp } from "firebase/firestore";
import { db } from "./firebase";

export type EventType = "scan" | "chat" | "alert_click" | "weather_view" | "market_view" | "app_open" | "scan_success" | "scan_error" | "upload_failure";

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

export async function logError(error: Error, message?: string, metadata: Record<string, any> = {}) {
  try {
    // 1. Record to Crashlytics
    if (message) {
      crashlytics().log(`[Context]: ${message}`);
    }
    Object.entries(metadata).forEach(([key, value]) => {
      crashlytics().setAttribute(key, String(value));
    });
    crashlytics().recordError(error);

    // 2. Also log as a specific analytics event
    await analytics().logEvent("app_error", {
      errorMessage: error.message,
      context: message || "general",
      ...metadata,
    });
  } catch (err) {
    console.error("Error logging failed:", err);
  }
}
