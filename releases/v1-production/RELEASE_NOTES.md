# NuKropAI v1.0 — Production Release Notes

**Release Date:** 2026-05-14  
**Build Profile:** production (AAB) + preview (APK)  
**Version Code:** 1  
**Package:** `com.nukropai.app`

---

## 🚀 Release Summary

NuKropAI v1.0 is the inaugural production release of the NuKropAI agricultural intelligence platform. This release is fully hardened for pilot rollout to farmers across Telangana and adjacent states, targeting low-end Android devices (2GB–3GB RAM) with intermittent connectivity.

---

## ✅ Validated Systems

| System | Status | Notes |
|--------|--------|-------|
| **Onboarding** | ✅ PASS | Language selection (EN/HI/TE), farm setup flow |
| **Authentication** | ✅ PASS | Firebase Auth + anonymous fallback |
| **AI Scanner** | ✅ PASS | Camera + gallery, adaptive compression |
| **Maps** | ✅ PASS | Farm GPS boundary, react-native-maps |
| **Push Notifications** | ✅ PASS | expo-notifications, disease + weather + market |
| **Cloud Sync** | ✅ PASS | Firestore conflict resolution (timestamp-based) |
| **Weather API** | ✅ PASS | Hyper-local weather with graceful fallback |
| **Market Prices** | ✅ PASS | Mandi Intel with offline cache |
| **Offline Mode** | ✅ PASS | AsyncStorage persistence, auto-retry on reconnect |
| **AI Chat** | ✅ PASS | Multilingual advisor (EN/HI/TE), streaming support |
| **Image Upload** | ✅ PASS | Firebase Storage, adaptive retry on failure |
| **Crashlytics** | ✅ PASS | Native Firebase Crashlytics enabled |
| **Analytics** | ✅ PASS | Firebase Analytics event tracking |

---

## 🔧 Production Hardening (Included in this Release)

- **Adaptive Image Compression**: 70% JPEG quality baseline; automatically reduces for devices with <3GB RAM
- **Battery Optimization**: Background sync limited to 60-minute windows; prevented from running during low-battery states
- **Sync Resilience**: 2.5-second debounce on state saves; cloud sync guarded behind `AppState === "active"` checks
- **Cloud Conflict Resolution**: Timestamp-based (`updatedAt`) conflict resolution — latest-write-wins with local-to-cloud promotion
- **Splash Screen Safety**: 5-second safety timeout prevents infinite loading on slow devices
- **Error Boundary**: Top-level `<ErrorBoundary>` wraps all navigation to prevent white screens from propagating
- **Exponential Backoff**: API request utility retries up to 3× with exponential backoff on 5xx errors and AbortError

---

## 📦 Build Instructions

### Prerequisites
- EAS CLI (`npm install -g eas-cli`)
- Expo account with project linked (`nukropai-mobile`)
- `google-services.json` provisioned in `artifacts/mobile/`

### Generate Production APK (Side-loading / QA)
```bash
cd artifacts/mobile
eas build --platform android --profile preview
```

### Generate Production AAB (Play Store)
```bash
cd artifacts/mobile
eas build --platform android --profile production
```

> **Note:** Both builds use `EXPO_PUBLIC_DOMAIN=api.nukrop.ai` as the backend endpoint.  
> Firebase config is injected at native build time via `google-services.json`.

---

## 🛡️ Security Checklist

- [x] No hardcoded API keys in source code
- [x] Firebase config via `EXPO_PUBLIC_*` env vars only
- [x] `google-services.json` excluded from git via `.gitignore`
- [x] `.env` excluded from git
- [x] Signing keys excluded (`*.jks`, `*.p12`, `*.key`)
- [x] `credentials.json` excluded from git
- [x] Audit logging for role changes (Firestore `audit_logs`)

---

## 📱 Device Compatibility

| Device Class | RAM | Android | Status |
|---|---|---|---|
| Low-end (Redmi, Realme) | 2GB | 10+ | ✅ Supported |
| Mid-range | 3GB | 10+ | ✅ Supported |
| Flagship | 6GB+ | 12+ | ✅ Supported |

---

## 🔗 Build Artifacts (EAS Remote)

After running EAS builds, download links will be available at:  
**https://expo.dev/accounts/[your-account]/projects/nukropai-mobile/builds**

---

*NuKropAI — Intelligence in the Fields.*
