import * as BackgroundFetch from "expo-background-fetch";
import * as TaskManager from "expo-task-manager";
import * as Notifications from "expo-notifications";
import { doc, getDoc } from "firebase/firestore";
import { db } from "./firebase";
import AsyncStorage from "@react-native-async-storage/async-storage";

const BACKGROUND_FETCH_TASK = "background-fetch-alerts";

TaskManager.defineTask(BACKGROUND_FETCH_TASK, async () => {
  try {
    const saved = await AsyncStorage.getItem("nukropai_state_v3");
    if (!saved) return BackgroundFetch.BackgroundFetchResult.NoData;
    
    const state = JSON.parse(saved);
    // In our AppContext sync, we'll ensure the last known userId is saved
    const userId = state.lastUserId; 
    
    if (!userId) return BackgroundFetch.BackgroundFetchResult.NoData;
    console.log(`[BACKGROUND] Checking alerts for user: ${userId}`);

    // Simulate checking Firestore for new targeted alerts
    const userDoc = await getDoc(doc(db, "users", userId));
    const data = userDoc.data();
    
    if (data?.pendingAlerts?.length > 0) {
      const alert = data.pendingAlerts[0];
      await Notifications.scheduleNotificationAsync({
        content: {
          title: alert.title,
          body: alert.body,
          data: alert.data,
        },
        trigger: null,
      });
      return BackgroundFetch.BackgroundFetchResult.NewData;
    }

    return BackgroundFetch.BackgroundFetchResult.NoData;
  } catch (error) {
    return BackgroundFetch.BackgroundFetchResult.Failed;
  }
});

export async function registerBackgroundFetchAsync() {
  return BackgroundFetch.registerTaskAsync(BACKGROUND_FETCH_TASK, {
    minimumInterval: 60 * 15, // 15 minutes
    stopOnTerminate: false,
    startOnBoot: true,
  });
}
