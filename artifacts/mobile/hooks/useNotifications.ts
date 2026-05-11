import * as Notifications from "expo-notifications";
import { useEffect, useRef, useState } from "react";
import { Platform } from "react-native";
import * as Device from "expo-device";
import { doc, updateDoc } from "firebase/firestore";
import { db } from "@/utils/firebase";
import { useAuth } from "@/contexts/AuthContext";

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: false,
  }),
});

export function useNotifications() {
  const { user } = useAuth();
  const [expoPushToken, setExpoPushToken] = useState("");
  const notificationListener = useRef<Notifications.Subscription>();
  const responseListener = useRef<Notifications.Subscription>();

  useEffect(() => {
    registerForPushNotificationsAsync().then((token) => {
      if (token) {
        setExpoPushToken(token);
        if (user) {
          updateDoc(doc(db, "users", user.uid), {
            pushToken: token,
            updatedAt: Date.now(),
          }).catch(console.error);
        }
      }
    });

    notificationListener.current = Notifications.addNotificationReceivedListener((notification) => {
      console.log("Notification Received:", notification);
    });

    responseListener.current = Notifications.addNotificationResponseReceivedListener((response) => {
      console.log("Notification Response:", response);
    });

    return () => {
      if (notificationListener.current) {
        Notifications.removeNotificationSubscription(notificationListener.current);
      }
      if (responseListener.current) {
        Notifications.removeNotificationSubscription(responseListener.current);
      }
    };
  }, [user]);

  return { expoPushToken };
}

import * as Constants from "expo-constants";

// ... (other imports)

async function registerForPushNotificationsAsync() {
  let token;

  if (Platform.OS === "android") {
    await Notifications.setNotificationChannelAsync("default", {
      name: "Default Notification Channel",
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
      lightColor: "#22C55E",
    });
  }

  if (Device.isDevice) {
    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;
    if (existingStatus !== "granted") {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }
    if (finalStatus !== "granted") {
      console.warn("Permission for push notifications not granted");
      return;
    }
    
    const projectId = Constants.default.expoConfig?.extra?.eas?.projectId || Constants.default.easConfig?.projectId;
    
    if (!projectId) {
      console.error("EAS Project ID not found in app config. Push notifications will not work.");
      return;
    }

    try {
      token = (await Notifications.getExpoPushTokenAsync({ projectId })).data;
    } catch (e) {
      console.error("Failed to get push token:", e);
    }
  } else {
    console.log("Must use physical device for Push Notifications");
  }

  return token;
}
