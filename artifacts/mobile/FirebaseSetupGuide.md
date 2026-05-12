# NuKropAI: Firebase Production Setup Guide

To ensure NuKropAI functions correctly in production (Crashlytics, Analytics, Push Notifications, and Auth), please follow these steps in the Firebase Console.

## 1. Project Initialization
* Create a new project at [console.firebase.google.com](https://console.firebase.google.com).
* Enable **Google Analytics** for the project.

## 2. Android App Configuration
* Register the Android app with package name: `com.nukrop.ai`.
* **IMPORTANT:** Generate and add your **SHA-1 and SHA-256 fingerprints** from your release keystore. This is required for Google Sign-In and Phone Auth.
    * Run: `keytool -list -v -keystore your-release-key.keystore`
* Download `google-services.json` and place it in `artifacts/mobile/`.

## 3. Authentication
* Enable **Google Sign-In** in the Auth tab.
* Add your `EXPO_PUBLIC_FIREBASE_API_KEY` and other keys to your EAS secrets or `.env.production`.

## 4. Firestore & Storage
* Initialize Firestore in **Production Mode**.
* Set up security rules (already provided in the repository).
* Enable Firebase Storage for crop scan uploads.

## 5. Crashlytics & Performance
* Enable **Crashlytics** in the Firebase Console.
* Ensure you have run a build with the `google-services.json` included to "trigger" the first heartbeat.

## 6. Cloud Messaging (FCM)
* NuKropAI uses FCM for disease outbreak alerts.
* Upload your **FCM Server Key** or **Service Account JSON** to the backend environment if using a custom push server.

---

**Release Checklist:**
- [ ] `google-services.json` included in build.
- [ ] SHA-1 fingerprints added to Firebase.
- [ ] Proguard/R8 enabled in `android/app/build.gradle` (Expo handles this by default in production).
- [ ] Asset density buckets verified (Splash/Icon).
