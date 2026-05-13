# NuKropAI v1.0 — Build Reproducibility Guide

This document ensures the v1.0 production build can be reproduced exactly.

## Source Commit

```
Tag:    v1.0-production
Branch: main
Commit: see git log
```

## Dependencies (Pinned)

| Package | Version |
|---------|---------|
| expo | ~52.0.0 |
| react-native | 0.76.0 |
| expo-router | ~4.0.0 |
| @react-native-firebase/app | ^21.6.0 |
| @react-native-firebase/auth | ^21.6.0 |
| @react-native-firebase/firestore | ^21.6.0 |
| @react-native-firebase/storage | ^21.6.0 |
| @react-native-firebase/crashlytics | ^21.6.0 |
| @react-native-firebase/analytics | ^21.6.0 |
| react-native-maps | 1.18.0 |
| expo-notifications | ~0.29.11 |
| expo-location | ~18.0.4 |
| expo-image-picker | ~16.0.3 |

## EAS Build Environment

```json
{
  "preview": {
    "distribution": "internal",
    "android": { "buildType": "apk" },
    "env": { "EXPO_PUBLIC_DOMAIN": "api.nukrop.ai" }
  },
  "production": {
    "autoIncrement": true,
    "android": { "buildType": "app-bundle" },
    "env": { "EXPO_PUBLIC_DOMAIN": "api.nukrop.ai" }
  }
}
```

## Required Secrets (EAS Secrets / CI)

| Secret | Description |
|--------|-------------|
| `EXPO_PUBLIC_FIREBASE_API_KEY` | Firebase Web API Key |
| `EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN` | Firebase Auth Domain |
| `EXPO_PUBLIC_FIREBASE_PROJECT_ID` | Firebase Project ID |
| `EXPO_PUBLIC_FIREBASE_STORAGE_BUCKET` | Firebase Storage Bucket |
| `EXPO_PUBLIC_FIREBASE_MESSAGING_SENDER_ID` | Firebase Sender ID |
| `EXPO_PUBLIC_FIREBASE_APP_ID` | Firebase App ID |
| `google-services.json` | Android native Firebase config (provisioned via EAS credentials) |

## Build Commands

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Navigate to mobile project
cd artifacts/mobile

# Build APK (QA/Preview)
eas build --platform android --profile preview

# Build AAB (Play Store)
eas build --platform android --profile production
```

## Node / pnpm Requirements

| Tool | Version |
|------|---------|
| Node.js | 20+ |
| pnpm | 9+ |
| eas-cli | >= 12.0.0 |

## Installation from Fresh Clone

```bash
git clone https://github.com/JACK-AI7/NuKropAI.git
cd NuKropAI
pnpm install
cd artifacts/mobile
# Provision google-services.json from Firebase Console
# Set EAS secrets via: eas secret:push --scope project
eas build --platform android --profile production
```
