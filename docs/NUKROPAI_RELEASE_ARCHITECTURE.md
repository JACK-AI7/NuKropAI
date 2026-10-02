# NuKropAI — Release Architecture & Distribution Pipeline

**Release Target:** NuKropAI v2.4 Production Engine (Android Release APK)  
**Distribution Channel:** Sovereign Sideload via Official Vercel Web Showcase Hub  
**SHA-256 Integrity Verification:** Mandatory Cryptographic Verification  

---

## 1. Automated Release Pipeline

```mermaid
flowchart LR
    SourceCode[1. Source Code Verification] --> GradleBuild[2. Gradle Release Assembly]
    GradleBuild --> VerifyBinary[3. Binary & Manifest Verification]
    VerifyBinary --> HashGen[4. SHA-256 Checksum Generation]
    HashGen --> SyncApk[5. Automated Website Sync (sync-apk.js)]
    SyncApk --> WebBuild[6. Vite React Production Build]
    WebBuild --> VercelDeploy[7. Vercel Edge Global Deployment]
```

---

## 2. Release Binary Specifications

| Release Specification | Official Production Values |
| :--- | :--- |
| **Application Name** | **NuKropAI OS** |
| **Package Identifier** | `ai.nukrop.nukrop_app` |
| **Release Version** | **v2.4 (Production Engine)** |
| **Target Android API** | Android 14 (API Level 34) |
| **Minimum Android API** | Android 8.0 Oreo (API Level 26) |
| **Binary Filename** | `NuKropAI.apk` |
| **Exact Binary Size** | **51,797,812 bytes** (49.4 MB) |
| **SHA-256 Checksum** | `D825747717C02FB801B3D90D4CF21E697EBFFBE01C2908A31AA6B90E596B4805` |
| **Signing Certificate** | Android Production Keystore (`v1` + `v2` APK Signature Scheme) |

---

## 3. Web Showcase & Download Endpoints

The Vercel-hosted showcase portal (`web/`) serves the compiled release binary through synchronized endpoints:

1. **Primary Download URL:** `/NuKropAI.apk`
2. **Versioned Release URL:** `/NuKropAI_v2.0.apk`
3. **Latest Auto-Pointer URL:** `/NuKropAI_latest.apk`

### Automation Script (`web/sync-apk.js`)
When `./gradlew assembleRelease` finishes, running `npm run build` inside `web/` executes `node sync-apk.js`, which:
- Scans candidate APK paths (`../NuKropAI.apk`, `../app/build/outputs/apk/release/`).
- Validates binary file size (> 40 MB).
- Mirrors the active release to `web/public/` and `web/dist/`.
- Computes SHA-256 checksums ensuring web download cards match the real binary.

---

## 4. Sideload Installation Instructions (User-Facing)

1. **Download:** Tap "Download NuKropAI APK" on the showcase portal.
2. **Authorize:** If prompted by Android with *"File might be harmful"*, tap **Download anyway**.
3. **Install:** Open the downloaded APK from the notification bar. If prompted with *"Install unknown apps"*, toggle **Allow from this source**.
4. **Launch:** Open NuKropAI, select your preferred language (e.g. Telugu, Hindi, English), and begin farming with 100% data sovereignty.
