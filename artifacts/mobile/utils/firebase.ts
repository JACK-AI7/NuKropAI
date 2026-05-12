import { Platform } from "react-native";
import { initializeApp, getApps, getApp } from "firebase/app";
import { getAuth, initializeAuth, browserLocalPersistence } from "firebase/auth";
import { getFirestore, enableIndexedDbPersistence } from "firebase/firestore";
import { getStorage } from "firebase/storage";
import ReactNativeAsyncStorage from "@react-native-async-storage/async-storage";

// Native SDKs
import authNative from "@react-native-firebase/auth";
import firestoreNative from "@react-native-firebase/firestore";
import storageNative from "@react-native-firebase/storage";

const firebaseConfig = {
  apiKey: process.env["EXPO_PUBLIC_FIREBASE_API_KEY"],
  authDomain: process.env["EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN"],
  projectId: process.env["EXPO_PUBLIC_FIREBASE_PROJECT_ID"],
  storageBucket: process.env["EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET"],
  messagingSenderId: process.env["EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID"],
  appId: process.env["EXPO_PUBLIC_FIREBASE_APP_ID"],
};

const isPlaceholder = Object.values(firebaseConfig).some(v => !v || (typeof v === "string" && v.includes("YOUR_")));
if (isPlaceholder && !__DEV__) {
  console.error("CRITICAL: Firebase configuration is missing in production build.");
}

// Universal Auth
let auth: any;
let db: any;
let storage: any;

if (Platform.OS === "web") {
  const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();
  auth = initializeAuth(app, {
    persistence: browserLocalPersistence,
  });
  db = getFirestore(app);
  storage = getStorage(app);
  
  // Enable web persistence
  enableIndexedDbPersistence(db).catch((err) => {
    if (err.code === "failed-precondition") {
      console.warn("Firestore persistence failed (multiple tabs open)");
    } else if (err.code === "unimplemented") {
      console.warn("Firestore persistence not supported by browser");
    }
  });
} else {
  // Use Native SDKs (pre-configured via google-services.json / GoogleService-Info.plist)
  auth = authNative();
  db = firestoreNative();
  storage = storageNative();
  
  // Native Firestore Hardening
  db.settings({
    persistence: true,
    cacheSizeBytes: firestoreNative.CACHE_SIZE_UNLIMITED,
  });
}

export { auth, db, storage };
