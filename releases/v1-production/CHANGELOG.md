# NuKropAI v1.0 — Changelog

All notable changes to NuKropAI are documented in this file.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] — 2026-05-14 🚀 Production Release

### Added
- Full onboarding flow with language selection (English, Hindi, Telugu)
- Firebase Phone / Google Authentication
- AI Crop Disease Scanner with adaptive image compression
- Multilingual AI Chat Advisor (streaming responses)
- Voice-first input support with waveform animation
- Hyper-local weather intelligence with predictive crop alerts
- Mandi Intel: real-time agricultural market prices
- Farm boundary GPS mapping (react-native-maps)
- Multi-farm management dashboard
- Offline-first data persistence (AsyncStorage + Firestore sync)
- Cloud conflict resolution — timestamp-based (latest-write-wins)
- Firebase Crashlytics crash reporting
- Firebase Analytics event tracking
- Push notifications (disease outbreaks, weather alerts, market dips)
- AI Insight cards on dashboard (warning, tip, danger, success)
- Admin panel for enterprise/advisor role management
- Audit logging for sensitive role-change actions
- Error boundary with graceful fallback UI
- Adaptive UI for dark mode (Forest Green palette)
- Background sync with 60-minute intelligent scheduling

### Fixed
- Grey screen on startup (splash screen safety timeout added)
- Sync loop from Firestore `onSnapshot` fighting with local state
- Cloud sync triggering while app is in background
- Image picker crashes on low-RAM devices (adaptive compression)
- Notification permission crash on first-launch denied flow

### Security
- No hardcoded secrets in source code
- All Firebase credentials via environment variables
- google-services.json excluded from version control
- Audit trail for RBAC role changes

### Infrastructure
- EAS build profiles: `development`, `preview` (APK), `production` (AAB)
- Production backend: `api.nukrop.ai`
- Firebase project: `com.nukropai.app`

---

*For full release notes see: `RELEASE_NOTES.md`*
