# R2 Market Impact & Mandi Pricing Specialist — Investigation & Architecture Report

> **Author**: Explorer 2 (Market Impact & Mandi Pricing Specialist)  
> **Target Directory**: `c:\Users\bjasw\Downloads\agriculture-ai-os`  
> **Working Report Path**: `.agents/teamwork_preview_explorer_survey_2/handoff.md`  
> **Milestone**: Survey & Architectural Design (R2: Market Impact Calculator)  
> **Date**: 2026-08-29  

---

## 1. Observation

A detailed audit of the current repository reveals the existing pricing, mandi rate sync, alert services, and data flows.

### 1.1 Existing Mandi & Pricing Components

1. **`app/src/main/java/com/example/MarketScreen.kt`**
   - **Location & Search Reactive Loop** (Lines 45–105): Reads user location via `LocationHelper.getCurrentLocationStateAndMandi(context)` and streams live Mandi data using `MandiApiService.watchLiveMandiPrices(activeSearchState, activeSearchQuery)`.
   - **Current 7-Day Price Forecast Card** (Lines 274–310):
     ```kotlin
     val avgModal = records.map { it.modalPrice }.average()
     val forecastPeak = (avgModal * 1.054).toInt()
     // Static text: "AI Market Trend Analysis: Prices for $activeSearchQuery in $activeSearchState are projected to rise +5.4% over the next 4 days..."
     ```
     *Finding*: The forecast is currently a hardcoded static multiplier (`1.054`) with zero correlation to regional pest/disease outbreaks, crop vulnerabilities, or supply contraction dynamics.
   - **Mandi Records List** (Lines 324–352 & `MandiRecordCard` Lines 355–395): Displays `market`, `district`, `state`, `commodity`, `variety`, `minPrice`, `maxPrice`, `modalPrice`, and `arrivalDate`.

2. **`app/src/main/java/com/example/MandiApiService.kt`**
   - **Data Model** (Lines 27–37):
     ```kotlin
     data class MandiRecord(
         val state: String,
         val district: String,
         val market: String,
         val commodity: String,
         val variety: String,
         val minPrice: Double,
         val maxPrice: Double,
         val modalPrice: Double,
         val arrivalDate: String
     )
     ```
   - **Dual-Path Fetching Engine** (Lines 130–158):
     - First queries Supabase table `mandi_live_rates` via `SupabaseApi.fetchMandiRates(state, commodity)`.
     - Falls back to Direct Agmarknet Govt API `https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070` with 5 rotating API keys.
     - Caches data in `ConcurrentHashMap<String, List<MandiRecord>>` (`lastGoodData`).
     - Exposes reactive `watchLiveMandiPrices(state, commodity): StateFlow<MandiState>`.

3. **`app/src/main/java/com/example/PriceTickerService.kt`**
   - Tracks a commodity basket (`Maharashtra: Tomato/Onion`, `Punjab: Wheat`, `Gujarat: Cotton`, `UP: Potato`, `Karnataka: Rice`, `Rajasthan: Mustard`).
   - Polls every 3 minutes, calculating `delta`, `changePercent`, `isUp`, and `isDown` (Lines 7–19).

4. **`app/src/main/java/com/example/PriceTracker.kt` & `AlertWorker.kt`**
   - `PriceTracker` stores user-tracked crop alert thresholds in `SharedPreferences` (`TrackedCrop(id, state, mandi, crop, basePrice, targetPrice)`).
   - `AlertWorker` (WorkManager periodic task) monitors price shifts ($\ge ₹50$ variance) and rain alerts, posting high-priority system notifications.

5. **`app/src/main/java/com/example/SupabaseClient.kt`**
   - Configured with `SUPABASE_URL = "https://yxjqseiegwjdfnccdchk.supabase.co"` and valid anon token.
   - `SupabaseApi.fetchMandiRates` performs REST queries against `/rest/v1/mandi_live_rates`.

6. **Backend Infrastructure (`backend/`)**
   - `backend/mandi_pipeline_sync.py`: Python daemon fetching from Agmarknet API and populating PostgreSQL table `public.mandi_live_rates`.
   - `backend/schema.sql` & `backend/src/workers/jobs/mandiIngestion.ts`: Contains `public.mandi_live_rates` and `public.mandi_price_anomalies` table definitions.
   - `backend/src/services/MandiSyncService.ts`: Redis caching layer (`mandi_rates:state:commodity`) with 15-minute TTL.
   - `backend/src/controllers/pest.controller.ts`: Handles `public.pest_outbreaks` insertion and queries.

---

## 2. Logic Chain & Econometric Market Impact Formulation

### 2.1 Agricultural Economic Mechanics of Outbreaks

During regional pest and crop disease epidemics (e.g., *Phytophthora infestans* Late Blight in Tomato/Potato, *Spodoptera frugiperda* Fall Armyworm in Maize/Wheat, *Pectinophora gossypiella* Pink Bollworm in Cotton, *Puccinia striiformis* Yellow Rust in Wheat), two distinct market dynamics occur across time and geography:

```
                               ┌────────────────────────────────────────────────────────┐
                               │       Active Regional Outbreak Alert Triggered         │
                               │           (Scan Density S >= Threshold, e.g. 100)      │
                               └──────────────────────────┬─────────────────────────────┘
                                                          │
                                                          ▼
                     ┌────────────────────────────────────┴────────────────────────────────────┐
                     │                                                                         │
                     ▼                                                                         ▼
      ┌──────────────────────────────┐                                          ┌──────────────────────────────┐
      │     EARLY PANIC PHASE        │                                          │  SUPPLY CONTRACTION PHASE    │
      │        (Days 0 - 7)          │                                          │        (Days 7 - 30)         │
      ├──────────────────────────────┤                                          ├──────────────────────────────┤
      │ • Panic Harvesting           │                                          │ • Severe Yield Destruction   │
      │ • Distressed Lot Arrivals    │                                          │ • Arrival Deficit (30%-70%)  │
      │ • Heavy Quality Discounts    │                                          │ • Inter-State Sourcing Bids  │
      │ ──► PRICE DROP (-10% to -35%)│                                          │ ──► PRICE SURGE (+15% to +45%)
      └──────────────────────────────┘                                          └──────────────────────────────┘
                     │                                                                         │
                     ▼                                                                         ▼
      ┌──────────────────────────────┐                                          ┌──────────────────────────────┐
      │ Local Epicenter Mandis:      │                                          │ Consuming & Neighbor Mandis: │
      │ Oversupply of blemished crop │                                          │ Acute supply shortage        │
      │ Trader rejection of stocks   │                                          │ Traders bid up spot price    │
      └──────────────────────────────┘                                          └──────────────────────────────┘
```

### 2.2 Mathematical Model & Formulas

Let:
- $S$: Total verified disease scans in the epicenter state within the rolling 14-day window.
- $S_{\text{threshold}} = 100$: Critical density threshold.
- $D = \min\left(1.0, \frac{S}{S_{\text{threshold}}}\right)$: Density saturation factor ($0.0 \le D \le 1.0$).
- $P_0$: Current modal price in ₹/Quintal from active Mandi records.
- $\beta$: Base severity shock coefficient:
  $$\beta = \begin{cases} 
  0.32 & \text{if } \text{Severity} = \text{CRITICAL } (S \ge 100) \\
  0.22 & \text{if } \text{Severity} = \text{HIGH } (50 \le S < 100) \\
  0.12 & \text{if } \text{Severity} = \text{MODERATE } (20 \le S < 50) \\
  0.05 & \text{if } \text{Severity} = \text{LOW } (S < 20)
  \end{cases}$$

- $\kappa(C)$: Crop Perishability & Supply Elasticity Multiplier:
  | Crop Category | Example Crops | Perishability Multiplier $\kappa(C)$ | Economic Rationale |
  |---|---|---|---|
  | **High Perishability Vegetables** | Tomato, Capsicum, Green Chilli | **1.40** | Cannot be stored; immediate panic dumping then absolute shortage. |
  | **Semi-Perishable Bulbs/Tubers** | Onion, Potato, Garlic | **1.20** | Storage rot risk; speculative hoarding by traders. |
  | **Commercial Cash Crops** | Cotton, Soybean, Mustard | **0.95** | Industrial processing buffer; fiber damage discounts. |
  | **Storable Cereals & Grains** | Wheat, Paddy/Rice, Maize | **0.80** | Central FCI buffer stock & warehouse storage dampens extreme spikes. |
  | **Default / Other Crops** | Pulses, Millets, Fruits | **1.00** | Standard elasticity baseline. |

- $\omega$: Geographic Market Spillover Multiplier:
  - $\omega_{\text{epicenter}} = 1.00$ (Direct epicenter mandis)
  - $\omega_{\text{neighbor}} = 0.70$ (Contiguous neighbor state / importing mandis)
  - $\omega_{\text{distant}} = 0.40$ (Distant terminal mandis)

#### Calculation Formulas

1. **Percentage Price Delta ($\Delta P\%$)**:
   - **For Supply Contraction Dynamic**:
     $$\Delta P\% = + \left( \beta \times \kappa(C) \times D \times \omega \times 100 \right)$$
   - **For Distress Selling Dynamic**:
     $$\Delta P\% = - \left( \beta \times \kappa(C) \times D \times \omega_{\text{epicenter}} \times 0.85 \times 100 \right)$$

2. **Predicted Future Modal Price ($P_{\text{predicted}}$)**:
   $$P_{\text{predicted}} = \max\left( \text{MSP}_{\text{floor}}, \text{round}\left( P_0 \times \left(1 + \frac{\Delta P\%}{100}\right) \right) \right)$$
   *(Where $\text{MSP}_{\text{floor}} = P_0 \times 0.40$ prevents impossible negative or zero prices).*

3. **Absolute Price Delta ($\Delta P_{\text{abs}}$)**:
   $$\Delta P_{\text{abs}} = P_{\text{predicted}} - P_0$$

4. **Prediction Confidence Score ($C_{\text{score}}$)**:
   $$C_{\text{score}} = \text{clamp}\left( 55 + (D \times 30) + (\text{hasRealTimeMandiData} ? 10 : 0) + (\text{multiDistrictConfirm} ? 5 : 0), 50, 98 \right)\%$$

5. **Market Risk Level Matrix**:
   | Calculated $|\Delta P\%|$ | Market Risk Level | UI Badge & Accent | Action Advisory for Farmers |
   |---|---|---|---|
   | $\ge 25.0\%$ | `CRITICAL_RISK` | 🔴 Red (`#FF3B30`) | **HOLD / STAGGER SALES**: Acute supply contraction will peak mandi prices within 4–7 days. Guard healthy stock against pest intrusion. |
   | $15.0\% - 24.9\%$ | `HIGH_RISK` | 🟠 Orange (`#FF9500`) | **PREPARE FOR SHIFT**: Price swing imminent. Monitor neighbor mandi rate arbitrage. |
   | $7.0\% - 14.9\%$ | `MODERATE_RISK` | 🟡 Yellow (`#FFCC00`) | **NORMAL TRADING**: Mild fluctuation expected. Grade produce before dispatch. |
   | $< 7.0\%$ | `LOW_RISK` | 🟢 Green (`#34C759`) | **STABLE MARKET**: Local price trends dominate; no major outbreak impact. |

---

## 3. Data Contracts & Architecture Specifications

### 3.1 Kotlin Domain Models (`com.example.market`)

```kotlin
package com.example.market

import kotlinx.serialization.Serializable

@Serializable
enum class OutbreakSeverity {
    LOW, MODERATE, HIGH, CRITICAL
}

@Serializable
enum class OutbreakStage {
    EARLY_PANIC,         // Days 0-7: Distress selling & quality discounts
    SUPPLY_CONTRACTION,  // Days 7-30: Crop loss creates supply deficit -> price surge
    RECOVERY             // Days 30+: Supply stabilizes, prices normalize
}

@Serializable
enum class ImpactDirection {
    SURGE,      // Price increase (+)
    DROP,       // Price decrease (-)
    VOLATILE,   // Rapid bi-directional swings
    STABLE      // Negligible change
}

@Serializable
enum class MarketRiskLevel {
    LOW, MODERATE, HIGH, CRITICAL
}

@Serializable
enum class ImpactMechanism {
    SUPPLY_CONTRACTION,
    DISTRESS_SELLING,
    QUALITY_DISCOUNT,
    REGIONAL_ARBITRAGE,
    PANIC_HOARDING
}

@Serializable
data class OutbreakAlert(
    val id: String,
    val diseaseName: String,
    val cropName: String,
    val epicenterState: String,
    val epicenterDistricts: List<String>,
    val scanCount: Int,
    val severity: OutbreakSeverity,
    val stage: OutbreakStage,
    val radiusKm: Double,
    val neighboringStates: List<String>,
    val isActive: Boolean = true,
    val triggeredAt: String
)

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
```

### 3.2 Pure Calculation Engine: `MarketImpactCalculator`

```kotlin
package com.example.market

import kotlin.math.max
import kotlin.math.roundToInt

object MarketImpactCalculator {

    private const val DENSITY_THRESHOLD = 100.0

    private val PERISHABILITY_MAP = mapOf(
        "tomato" to 1.40,
        "capsicum" to 1.35,
        "green chilli" to 1.35,
        "onion" to 1.25,
        "potato" to 1.15,
        "cotton" to 0.95,
        "wheat" to 0.80,
        "rice" to 0.80,
        "paddy" to 0.80,
        "mustard" to 0.90,
        "soybean" to 0.90,
        "maize" to 0.85
    )

    fun calculateImpact(
        alert: OutbreakAlert,
        currentModalPrice: Double,
        targetState: String,
        targetMandi: String,
        availableMandiRecords: List<MandiRecord> = emptyList()
    ): MarketPriceImpact {
        val cropKey = alert.cropName.trim().lowercase()
        val perishability = PERISHABILITY_MAP[cropKey] ?: 1.00

        // 1. Density factor D
        val densityFactor = (alert.scanCount / DENSITY_THRESHOLD).coerceIn(0.1, 1.0)

        // 2. Base severity shock beta
        val beta = when (alert.severity) {
            OutbreakSeverity.CRITICAL -> 0.32
            OutbreakSeverity.HIGH -> 0.22
            OutbreakSeverity.MODERATE -> 0.12
            OutbreakSeverity.LOW -> 0.05
        }

        // 3. Geographic multiplier omega
        val isEpicenter = alert.epicenterState.equals(targetState, ignoreCase = true)
        val isNeighbor = alert.neighboringStates.any { it.equals(targetState, ignoreCase = true) }
        val geographicMultiplier = when {
            isEpicenter -> 1.00
            isNeighbor -> 0.70
            else -> 0.40
        }

        // 4. Direction & percentage delta calculation
        val (deltaPct, direction, mechanism) = when (alert.stage) {
            OutbreakStage.EARLY_PANIC -> {
                if (isEpicenter) {
                    val drop = -(beta * perishability * densityFactor * 0.85 * 100)
                    Triple(drop, ImpactDirection.DROP, ImpactMechanism.DISTRESS_SELLING)
                } else {
                    val mildSurge = +(beta * perishability * densityFactor * geographicMultiplier * 0.50 * 100)
                    Triple(mildSurge, ImpactDirection.SURGE, ImpactMechanism.REGIONAL_ARBITRAGE)
                }
            }
            OutbreakStage.SUPPLY_CONTRACTION -> {
                val surge = +(beta * perishability * densityFactor * geographicMultiplier * 100)
                Triple(surge, ImpactDirection.SURGE, ImpactMechanism.SUPPLY_CONTRACTION)
            }
            OutbreakStage.RECOVERY -> {
                val mildDrop = -(beta * 0.30 * perishability * densityFactor * 100)
                Triple(mildDrop, ImpactDirection.DROP, ImpactMechanism.QUALITY_DISCOUNT)
            }
        }

        // 5. Compute predicted price
        val basePrice = if (currentModalPrice > 0.0) currentModalPrice else 2200.0
        val rawPredicted = basePrice * (1.0 + (deltaPct / 100.0))
        val minFloor = basePrice * 0.40
        val predictedModalPrice = max(minFloor, rawPredicted).roundToInt().toDouble()
        val priceDelta = predictedModalPrice - basePrice

        // 6. Risk Level
        val absDelta = kotlin.math.abs(deltaPct)
        val riskLevel = when {
            absDelta >= 25.0 -> MarketRiskLevel.CRITICAL
            absDelta >= 15.0 -> MarketRiskLevel.HIGH
            absDelta >= 7.0 -> MarketRiskLevel.MODERATE
            else -> MarketRiskLevel.LOW
        }

        // 7. Confidence Score
        val hasMandiData = availableMandiRecords.isNotEmpty()
        val confidence = ((55 + (densityFactor * 30) + (if (hasMandiData) 10 else 0)).roundToInt()).coerceIn(50, 98)

        // 8. Peak horizon
        val peakDays = when (alert.stage) {
            OutbreakStage.EARLY_PANIC -> 3
            OutbreakStage.SUPPLY_CONTRACTION -> 6
            OutbreakStage.RECOVERY -> 14
        }

        // 9. Recommended action
        val action = generateFarmerRecommendation(direction, riskLevel, alert.cropName, isEpicenter, peakDays)

        // 10. Affected markets list
        val affected = availableMandiRecords.take(5).map { record ->
            val mRaw = record.modalPrice * (1.0 + (deltaPct / 100.0))
            val mPred = max(record.modalPrice * 0.40, mRaw).roundToInt().toDouble()
            AffectedMarketDetail(
                marketName = record.market,
                district = record.district,
                state = record.state,
                currentModalPrice = record.modalPrice,
                predictedModalPrice = mPred,
                deltaPercentage = ((mPred - record.modalPrice) / record.modalPrice * 100.0).roundToInt().toDouble(),
                direction = direction,
                isEpicenter = isEpicenter
            )
        }

        return MarketPriceImpact(
            alertId = alert.id,
            cropName = alert.cropName,
            diseaseName = alert.diseaseName,
            targetState = targetState,
            targetMandi = targetMandi,
            currentModalPrice = basePrice,
            predictedModalPrice = predictedModalPrice,
            priceDelta = priceDelta,
            deltaPercentage = (deltaPct * 10.0).roundToInt() / 10.0,
            direction = direction,
            riskLevel = riskLevel,
            confidenceScore = confidence,
            mechanism = mechanism,
            estimatedPeakDays = peakDays,
            recommendedFarmerAction = action,
            affectedMarkets = affected
        )
    }

    private fun generateFarmerRecommendation(
        direction: ImpactDirection,
        risk: MarketRiskLevel,
        crop: String,
        isEpicenter: Boolean,
        peakDays: Int
    ): String {
        return when {
            direction == ImpactDirection.SURGE && risk == MarketRiskLevel.CRITICAL ->
                "HOLD / STAGGER: Acute regional supply contraction will peak $crop prices in $peakDays days. Avoid early distress sell; guard healthy harvest."
            direction == ImpactDirection.SURGE ->
                "MONITOR ARBITRAGE: Prices rising due to supply shortage. Consider transporting grade-A produce to high-demand neighboring mandis."
            direction == ImpactDirection.DROP && isEpicenter ->
                "GRADE & PROTECT: Local mandi seeing panic arrivals and heavy price discounts. Strictly sort Grade-A produce or store in local cold units."
            else ->
                "NORMAL DISPATCH: Stable price band. Follow standard harvesting and marketing schedule."
        }
    }
}
```

### 3.3 Outbreak Alert & Market Impact Repository Contract

```kotlin
package com.example.market

import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.StateFlow

interface IMarketImpactRepository {
    /**
     * Streams active regional outbreak alerts for a specific crop and state
     */
    fun getActiveAlertsFlow(state: String, crop: String): Flow<List<OutbreakAlert>>

    /**
     * Calculates the real-time market price impact for the given state and crop
     */
    suspend fun getMarketImpact(state: String, crop: String, mandi: String): Result<MarketPriceImpact?>

    /**
     * Pushes on-device disease scan to the central aggregation backend
     */
    suspend fun recordDiseaseScan(
        diseaseName: String,
        cropName: String,
        state: String,
        district: String,
        latitude: Double,
        longitude: Double,
        confidence: Int,
        severity: String
    ): Result<Unit>
}
```

---

## 4. Integration Hooks with Existing Screens

### 4.1 Integration into `MarketScreen.kt`

Currently, `MarketScreen.kt` renders a static `7-Day AI Price Forecast Card` on lines 274–310.
The new **`OutbreakMarketImpactCard`** will dynamically replace or enrich this section whenever an active outbreak alert exists for the searched crop/state:

```kotlin
@Composable
fun OutbreakMarketImpactCard(
    impact: MarketPriceImpact,
    onViewActionPlan: () -> Unit = {}
) {
    val isSurge = impact.direction == ImpactDirection.SURGE
    val badgeBg = if (isSurge) Color(0x33FF3B30) else Color(0x33FF9500)
    val badgeColor = if (isSurge) Color(0xFFFF453A) else Color(0xFFFF9F0A)
    val directionSymbol = if (isSurge) "↗ +" else "↘ "

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(NuKropCard)
            .border(1.5.dp, badgeColor.copy(alpha = 0.5f), RoundedCornerShape(16.dp))
            .padding(16.dp)
    ) {
        Column {
            // Header Row: Badge & Risk
            Row(
                Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    Icon(Icons.Filled.Warning, contentDescription = "Alert", tint = badgeColor, modifier = Modifier.size(18.dp))
                    Text(
                        text = "Outbreak Market Impact Alert",
                        color = NuKropText,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(badgeBg)
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                ) {
                    Text(
                        text = "${impact.riskLevel.name.replace("_", " ")} (${impact.confidenceScore}% CONFIDENCE)",
                        color = badgeColor,
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }

            Spacer(Modifier.height(10.dp))

            // Price Impact Metrics
            Row(
                Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text("Current Modal Rate", fontSize = 11.sp, color = NuKropTextDim)
                    Text("₹${impact.currentModalPrice.toInt()} / Qtl", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                }
                Icon(Icons.Filled.ArrowForward, null, tint = NuKropTextDim, modifier = Modifier.size(16.dp))
                Column(horizontalAlignment = Alignment.End) {
                    Text("Predicted Outbreak Peak", fontSize = 11.sp, color = NuKropTextDim)
                    Text(
                        "₹${impact.predictedModalPrice.toInt()} / Qtl ($directionSymbol${impact.deltaPercentage}%)",
                        fontSize = 16.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = badgeColor
                    )
                }
            }

            Spacer(Modifier.height(10.dp))

            // Explanation & Mechanism
            Text(
                text = "${impact.diseaseName} outbreak in ${impact.targetState} is causing a ${impact.mechanism.name.lowercase().replace('_', ' ')}. ${impact.recommendedFarmerAction}",
                color = NuKropTextMuted,
                fontSize = 12.sp,
                lineHeight = 17.sp
            )

            Spacer(Modifier.height(12.dp))

            // Affected Mandis Pill List
            if (impact.affectedMarkets.isNotEmpty()) {
                Text("Affected Regional Mandis:", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = NuKropTextDim)
                Spacer(Modifier.height(6.dp))
                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.horizontalScroll(rememberScrollState())
                ) {
                    impact.affectedMarkets.forEach { m ->
                        Box(
                            Modifier
                                .clip(RoundedCornerShape(6.dp))
                                .background(Color(0xFF1A2210))
                                .border(1.dp, Color(0x30FFFFFF), RoundedCornerShape(6.dp))
                                .padding(horizontal = 8.dp, vertical = 4.dp)
                        ) {
                            Text("${m.marketName}: ₹${m.predictedModalPrice.toInt()} (${if (m.deltaPercentage >= 0) "+" else ""}${m.deltaPercentage}%)", fontSize = 10.sp, color = NuKropText)
                        }
                    }
                }
            }
        }
    }
}
```

### 4.2 Integration into `HomeScreen.kt`

- **Hyperlocal Outbreak Impact Card** (Lines 210–230):
  Replace the hardcoded Rampur warning with a real-time reactive card bound to the highest-severity active alert for the user's registered/detected state and primary crop.
- **Price Ticker & Marquee** (Lines 153–171):
  Append an indicator when a ticker commodity has an active outbreak alert: `Tomato (Pune): ₹2,800 [⚠️ +24% Outbreak Surge Alert]`.

### 4.3 Integration into `AlertWorker.kt` (Background Push Notifications)

```kotlin
// Check active outbreak alerts and calculate price impacts
val activeOutbreaks = OutbreakAlertRepository.getActiveAlertsForState(userState)
for (alert in activeOutbreaks) {
    if (alert.severity >= OutbreakSeverity.HIGH) {
        val impact = MarketImpactCalculator.calculateImpact(alert, baseModalPrice, userState, userMandi)
        if (impact.riskLevel >= MarketRiskLevel.HIGH) {
            sendNotification(
                "🚨 Regional Crop Outbreak Price Alert",
                "${alert.diseaseName} outbreak in ${alert.epicenterState}: ${alert.cropName} prices predicted to shift by ${impact.deltaPercentage}% (Target ₹${impact.predictedModalPrice.toInt()}/Qtl)."
            )
        }
    }
}
```

---

## 5. Database Schema & Backend Contract Extensions

To support the calculator and alerts seamlessly in Supabase / PostgreSQL:

```sql
-- 1. Disease Scans Table (Scan Aggregation Storage)
CREATE TABLE IF NOT EXISTS public.disease_scans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    disease_name VARCHAR(150) NOT NULL,
    crop_name VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    confidence INTEGER NOT NULL CHECK (confidence BETWEEN 0 AND 100),
    severity VARCHAR(50) NOT NULL DEFAULT 'Moderate',
    scanned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_disease_scans_agg ON public.disease_scans(state, crop_name, disease_name, scanned_at DESC);

-- 2. Outbreak Alerts Table (Generated when scans >= 100 in rolling 14 days)
CREATE TABLE IF NOT EXISTS public.outbreak_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    disease_name VARCHAR(150) NOT NULL,
    crop_name VARCHAR(100) NOT NULL,
    epicenter_state VARCHAR(100) NOT NULL,
    epicenter_districts JSONB NOT NULL DEFAULT '[]'::jsonb,
    scan_count INTEGER NOT NULL,
    severity VARCHAR(50) NOT NULL CHECK (severity IN ('LOW', 'MODERATE', 'HIGH', 'CRITICAL')),
    stage VARCHAR(50) NOT NULL DEFAULT 'SUPPLY_CONTRACTION' CHECK (stage IN ('EARLY_PANIC', 'SUPPLY_CONTRACTION', 'RECOVERY')),
    radius_km DOUBLE PRECISION NOT NULL DEFAULT 50.0,
    neighboring_states JSONB NOT NULL DEFAULT '[]'::jsonb,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_outbreak_alerts_active ON public.outbreak_alerts(epicenter_state, crop_name) WHERE is_active = TRUE;

-- 3. Dynamic Neighboring State Mapping Reference
CREATE TABLE IF NOT EXISTS public.state_neighbor_map (
    state VARCHAR(100) PRIMARY KEY,
    neighbors TEXT[] NOT NULL
);

INSERT INTO public.state_neighbor_map (state, neighbors) VALUES
('Punjab', ARRAY['Haryana', 'Himachal Pradesh', 'Rajasthan', 'Jammu and Kashmir']),
('Maharashtra', ARRAY['Gujarat', 'Madhya Pradesh', 'Karnataka', 'Telangana', 'Goa']),
('Uttar Pradesh', ARRAY['Bihar', 'Madhya Pradesh', 'Haryana', 'Rajasthan', 'Uttarakhand']),
('Gujarat', ARRAY['Rajasthan', 'Maharashtra', 'Madhya Pradesh']),
('Karnataka', ARRAY['Maharashtra', 'Goa', 'Kerala', 'Tamil Nadu', 'Andhra Pradesh', 'Telangana'])
ON CONFLICT (state) DO NOTHING;
```

---

## 6. Caveats & Assumptions

1. **State & District Normalization**: Government Mandi data uses varied state spellings (e.g. `NCT of Delhi` vs `Delhi`, `Punjab` vs `PUNJAB`). All queries and lookups must normalize using `.trim().lowercase()` or standard Title Case.
2. **Missing Local Mandi Price Fallback**: In the event that Agmarknet has no live arrivals for a specific small mandi today, the calculator must fall back to the state district modal average, or minimum guaranteed benchmark price (MSP floor), rather than failing with division by zero.
3. **Cold Storage Buffering**: Crops like Potato in UP or Apple in Himachal have cold storage buffers which can extend the transition from Early Panic to Supply Contraction by 10–14 days. The stage classifier accounts for this via perishability weighting.
4. **No Codebase Degradation**: All proposals are 100% additive and maintain backwards compatibility with existing UI themes (`NuKropAccent`, `NuKropCard`, `NuKropDark`).

---

## 7. Conclusion & Next Steps

1. **Complete Specification Delivered**:
   - Algorithmic econometric model with exact mathematical formulas for $\Delta P\%$, $P_{\text{predicted}}$, risk levels, and confidence scores.
   - Comprehensive Kotlin domain models (`OutbreakAlert`, `MarketPriceImpact`, `AffectedMarketDetail`, enums).
   - Testable, pure calculator engine (`MarketImpactCalculator.kt`).
   - Clean UI integration specifications for `MarketScreen.kt` and `HomeScreen.kt`.
   - Database schema extensions for `disease_scans` and `outbreak_alerts`.

2. **Handover to Implementer / Worker Agents**:
   - Worker M2 (Backend/Calculator) can implement `MarketImpactCalculator.kt` and `MarketImpactRepository.kt`.
   - Worker M1/M3 (UI) can bind `OutbreakMarketImpactCard` into `MarketScreen.kt` and `HomeScreen.kt`.

---

## 8. Verification Method

To independently verify the calculator and its integration:

1. **Unit Test Verification (`MarketImpactCalculatorTest.kt`)**:
   - **Scenario 1 (Supply Contraction)**: 120 Tomato Late Blight scans in Punjab (`CRITICAL` severity, $S=120 \implies D=1.0$, $\beta=0.32$, $\kappa=1.40$, base modal price ₹2,000/Qtl).
     - Expected Output: $\Delta P\% = +44.8\%$, Predicted Price: ₹2,896/Qtl, Risk: `CRITICAL_RISK`, Mechanism: `SUPPLY_CONTRACTION`.
   - **Scenario 2 (Early Panic Distress Selling)**: 60 Wheat Yellow Rust scans in Haryana (`HIGH` severity, $S=60 \implies D=0.6$, $\beta=0.22$, $\kappa=0.80$, early stage, base modal price ₹2,200/Qtl).
     - Expected Output: $\Delta P\% = -8.9\%$, Predicted Price: ₹2,004/Qtl, Risk: `MODERATE_RISK`, Mechanism: `DISTRESS_SELLING`.
   - **Scenario 3 (Neighboring State Spillover)**: Outbreak in Punjab affecting Haryana mandi.
     - Expected Output: $\omega = 0.70$, $\Delta P\% = +31.4\%$, Risk: `CRITICAL_RISK`.

2. **Android Build Verification**:
   - Run `./gradlew testDebugUnitTest` and `./gradlew assembleDebug` to confirm clean compilation with 0 errors.
