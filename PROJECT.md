# Project: NuKropAI National Crop Disease Aggregation and Early Warning System

## Architecture

NuKropAI's National Crop Disease Aggregation and Early Warning System provides real-time detection, national geospatial aggregation, outbreak density threshold evaluation, neighboring state early warnings, and econometric market price impact forecasting for farmers across India.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           NuKropAI Android Application                          │
├──────────────────────────────────────┬──────────────────────────────────────────┤
│        On-Device Vision AI           │           Compose UI Layer               │
│  - CameraX / MediaPicker Ingestion   │  - HomeScreen (Regional Outbreak Banner) │
│  - Vision AI / TFLite Inference      │  - MarketScreen (Outbreak Price Impact)  │
│  - Anonymous Scan Telemetry Hook     │  - DiseaseScannerScreen (Result Privacy) │
└──────────────────┬───────────────────┴───────────────────▲──────────────────────┘
                   │                                       │
                   │ Push Anonymous Scan                   │ Fetch Active Alerts
                   │ (disease, crop, state, lat/lng)       │ & Market Price Impacts
                   ▼                                       │
┌──────────────────────────────────────────────────────────┴──────────────────────┐
│                    Supabase / PostgreSQL Aggregation Backend                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│  1. `public.disease_scans` (Anonymous scan logs)                                │
│  2. `public.state_adjacencies` (Symmetric Indian state neighbor graph)          │
│  3. `public.outbreak_alerts` (Epicenter & Early Warning alerts)                 │
│  4. PostgreSQL Trigger `fn_evaluate_disease_outbreak()`                         │
│     - Evaluates scan density in rolling 7-day window                            │
│     - Crossing 100-scan threshold triggers Epicenter alert                      │
│     - Automatically fans out Early Warning alerts to all neighboring states     │
└──────────────────────────────────┬──────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     Market Impact Calculation Engine (Kotlin)                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│  - Econometric calculation: Supply Contraction (Surge) vs Distress Selling      │
│  - Crop Perishability Weights (Tomato: 1.4, Onion: 1.25, Cotton: 0.95, etc.)   │
│  - Geographic Multipliers (Epicenter: 1.0, Neighbor: 0.7, Distant: 0.4)        │
│  - Market Risk Levels (Low, Moderate, High, Critical) & Farmer Action Advisories│
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Feature Inventory

| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | SQL Schema & Migrations | Create PostgreSQL migration for `disease_scans`, `state_adjacencies`, and `outbreak_alerts` with RLS policies and indices | M1 | R1 |
| 2 | Outbreak Density Trigger & Alerts | PostgreSQL trigger `fn_evaluate_disease_outbreak()` and Kotlin aggregation engine detecting $\ge 100$ scans/state and fanning out neighbor alerts | M1 | R1 |
| 3 | Backend API & Service Layer | Kotlin `DiseaseAggregationService.kt` and `SupabaseClient.kt` REST API for push and query | M1 | R1 |
| 4 | Market Impact Econometric Engine | Pure Kotlin `MarketImpactCalculator.kt` modeling price delta %, predicted price, risk level, confidence, and farmer action | M2 | R2 |
| 5 | Outbreak Alert & Market Repository | Repository layer `MarketImpactRepository.kt` integrating live Mandi rates with active alerts | M2 | R2 |
| 6 | On-Device Scan Hook | Hook in `DiseaseScannerScreen.kt` pushing anonymous scan telemetry asynchronously upon diagnosis | M3 | R3 |
| 7 | HomeScreen Outbreak Alert UI | Dynamic `RegionalOutbreakAlertSection` in `HomeScreen.kt` displaying active state/neighbor alerts | M3 | R3 |
| 8 | MarketScreen Price Impact UI | Dynamic `OutbreakMarketImpactCard` & price badges in `MarketScreen.kt` correlating search crop with outbreaks | M3 | R3 |
| 9 | Comprehensive E2E & Unit Test Suite | Tier 1-4 unit & integration test suite verifying 100-scan threshold, neighbor fanout, econometric math, and UI flow | M4 (E2E) | Acceptance Criteria |
| 10 | Final Build & Forensic Audit | Clean `./gradlew assembleDebug` verification and Forensic Auditor integrity verification | M5 | Acceptance Criteria |

---

## Milestones

| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Database Schema, Migrations & Aggregation Backend | SQL migration files (`backend/migrations/001_disease_scans_and_outbreak_alerts.sql`, `backend/schema.sql`, `backend/supabase_setup.sql`), `state_adjacencies` seed data, PostgreSQL trigger `fn_evaluate_disease_outbreak()`, and `DiseaseAggregationService.kt` | none | DONE |
| M2 | Market Impact Calculator & Domain Models | `MarketImpactModels.kt`, `MarketImpactCalculator.kt`, and `MarketImpactRepository.kt` with full econometric supply/demand formulas and neighbor spillover | M1 | DONE |
| M3 | Android App Scan Hook & Jetpack Compose UI | Telemetry push in `DiseaseScannerScreen.kt`, `HomeScreen.kt` active alert banners, `MarketScreen.kt` outbreak price impact cards, and `AppStrings.kt` localization | M1, M2 | DONE |
| M4 | E2E & Unit Testing Track | Comprehensive test suite (`DiseaseAggregationTest.kt`, `MarketImpactCalculatorTest.kt`, `ScanTelemetryTest.kt`) verifying 100-scan trigger, neighbor fan-out, and market calculations | M1, M2, M3 | IN_PROGRESS |
| M5 | Final Verification, Build & Forensic Audit | Clean `./gradlew assembleDebug` run, end-to-end integration validation, and Forensic Auditor verification | M4 | PLANNED |

---

## Interface Contracts

### 1. Telemetry & Aggregation Contract
```kotlin
package com.example.model

import kotlinx.serialization.Serializable

@Serializable
data class DiseaseScanPayload(
    val diseaseName: String,
    val cropName: String = "General",
    val state: String,
    val district: String = "",
    val severity: String = "Moderate",
    val confidence: Int = 90,
    val latitude: Double? = null,
    val longitude: Double? = null,
    val scannedAt: Long = System.currentTimeMillis()
)

@Serializable
data class OutbreakAlert(
    val id: String,
    val diseaseName: String,
    val sourceState: String,
    val targetState: String,
    val alertType: String, // "EPICENTER" or "EARLY_WARNING"
    val severity: String,  // "LOW", "MODERATE", "HIGH", "CRITICAL"
    val scanCount: Int,
    val thresholdDensity: Int = 100,
    val timeWindowHours: Int = 168,
    val message: String,
    val recommendedAction: String,
    val predictedMarketImpactPct: Double = 0.0,
    val isActive: Boolean = true,
    val createdAt: String = "",
    val updatedAt: String = ""
)
```

### 2. Market Impact Calculator Contract
```kotlin
package com.example.market

import com.example.model.OutbreakAlert
import kotlinx.serialization.Serializable

@Serializable
enum class OutbreakSeverity { LOW, MODERATE, HIGH, CRITICAL }

@Serializable
enum class OutbreakStage { EARLY_PANIC, SUPPLY_CONTRACTION, RECOVERY }

@Serializable
enum class ImpactDirection { SURGE, DROP, VOLATILE, STABLE }

@Serializable
enum class MarketRiskLevel { LOW, MODERATE, HIGH, CRITICAL }

@Serializable
enum class ImpactMechanism { SUPPLY_CONTRACTION, DISTRESS_SELLING, QUALITY_DISCOUNT, REGIONAL_ARBITRAGE, PANIC_HOARDING }

@Serializable
data class AffectedMarketDetail(
    val marketName: String,
    val district: String,
    val state: String,
    val currentModalPrice: Double,
    val predictedModalPrice: Double,
    val deltaPercentage: Double,
    val direction: ImpactDirection,
    val isEpicenter: Boolean
)

@Serializable
data class MarketPriceImpact(
    val alertId: String,
    val cropName: String,
    val diseaseName: String,
    val targetState: String,
    val targetMandi: String,
    val currentModalPrice: Double,
    val predictedModalPrice: Double,
    val priceDelta: Double,
    val deltaPercentage: Double,
    val direction: ImpactDirection,
    val riskLevel: MarketRiskLevel,
    val confidenceScore: Int,
    val mechanism: ImpactMechanism,
    val estimatedPeakDays: Int,
    val recommendedFarmerAction: String,
    val affectedMarkets: List<AffectedMarketDetail>
)

object MarketImpactCalculator {
    fun calculateImpact(
        alert: OutbreakAlert,
        currentModalPrice: Double,
        targetState: String,
        targetMandi: String,
        availableMandiRecords: List<com.example.MandiRecord> = emptyList()
    ): MarketPriceImpact
}
```

---

## Code Layout

- Database & Migrations:
  - `backend/migrations/001_disease_scans_and_outbreak_alerts.sql` (New Migration)
  - `backend/schema.sql` (Updated global Postgres schema)
  - `backend/supabase_setup.sql` (Updated Supabase setup script)
- Android Core & Domain Models:
  - `app/src/main/java/com/example/model/DiseaseScanModels.kt` (New Data Models)
  - `app/src/main/java/com/example/market/MarketImpactModels.kt` (New Market Models)
  - `app/src/main/java/com/example/market/MarketImpactCalculator.kt` (New Calculation Engine)
- Services & Repositories:
  - `app/src/main/java/com/example/DiseaseAggregationService.kt` (New Aggregation & Alert Service)
  - `app/src/main/java/com/example/market/MarketImpactRepository.kt` (New Market Impact Repository)
  - `app/src/main/java/com/example/SupabaseClient.kt` (Updated Supabase API methods)
- Android UI Components:
  - `app/src/main/java/com/example/DiseaseScannerScreen.kt` (Updated Scan Hook & Telemetry)
  - `app/src/main/java/com/example/HomeScreen.kt` (Updated Dynamic Outbreak Banner)
  - `app/src/main/java/com/example/MarketScreen.kt` (Updated Outbreak Price Impact Card)
  - `app/src/main/java/com/example/RegionalIntelligenceScreen.kt` (Updated Live Outbreak Alerts)
  - `app/src/main/java/com/example/AppStrings.kt` (Updated Localization Strings)
- Unit & E2E Tests:
  - `app/src/test/java/com/example/DiseaseAggregationTest.kt` (Threshold & Neighbor Alert Tests)
  - `app/src/test/java/com/example/MarketImpactCalculatorTest.kt` (Price Shock & Econometric Tests)
  - `app/src/test/java/com/example/ScanTelemetryIntegrationTest.kt` (Integration Tests)
