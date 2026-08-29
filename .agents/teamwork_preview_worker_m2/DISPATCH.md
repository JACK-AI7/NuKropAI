# DISPATCH

## 2026-08-29T04:23:21Z
You are Worker M2: Market Impact Calculator & Domain Models Implementer.

Authoritative Request: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\ORIGINAL_REQUEST.md
Scope Document: c:\Users\bjasw\Downloads\agriculture-ai-os\PROJECT.md
Working Directory: c:\Users\bjasw\Downloads\agriculture-ai-os
Your Agent Directory: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m2

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Exclusively Owned Files:
- `app/src/main/java/com/example/market/MarketImpactModels.kt`
- `app/src/main/java/com/example/market/MarketImpactCalculator.kt`
- `app/src/main/java/com/example/market/MarketImpactRepository.kt`

Your Instructions:
1. Implement `app/src/main/java/com/example/market/MarketImpactModels.kt`:
   - Enums: `OutbreakSeverity`, `OutbreakStage`, `ImpactDirection`, `MarketRiskLevel`, `ImpactMechanism`
   - Data models: `AffectedMarketDetail`, `MarketPriceImpact`
   - Ensure compatibility with `com.example.model.OutbreakAlert` and `com.example.MandiRecord`.
2. Implement `app/src/main/java/com/example/market/MarketImpactCalculator.kt`:
   - Pure, deterministic calculation engine modeling regional disease outbreaks on mandi prices.
   - Crop perishability map (Tomato: 1.40, Capsicum/Chilli: 1.35, Onion: 1.25, Potato: 1.15, Cotton: 0.95, Wheat/Rice/Paddy: 0.80, Mustard/Soybean: 0.90, Maize: 0.85, default: 1.0).
   - Severity shocks: CRITICAL = 0.32, HIGH = 0.22, MODERATE = 0.12, LOW = 0.05.
   - Density saturation: D = (scanCount / 100.0).coerceIn(0.1, 1.0).
   - Geographic multiplier: Epicenter = 1.00, Neighbor = 0.70, Distant = 0.40.
   - Stage dynamics:
     - `SUPPLY_CONTRACTION`: + (beta * perishability * D * geographicMultiplier * 100)%
     - `EARLY_PANIC`: Epicenter - (beta * perishability * D * 0.85 * 100)%, Neighbor + (beta * perishability * D * geographicMultiplier * 0.50 * 100)%
     - `RECOVERY`: - (beta * 0.30 * perishability * D * 100)%
   - Calculated predicted price with floor (min 40% of base), delta percentage, absolute delta, risk levels (Critical >= 25%, High >= 15%, Moderate >= 7%, Low < 7%), confidence score (50-98%), peak days, farmer recommendation, and affected markets details.
3. Implement `app/src/main/java/com/example/market/MarketImpactRepository.kt`:
   - Provide `IMarketImpactRepository` and `MarketImpactRepository` singleton with methods to query active alerts via `DiseaseAggregationService` and calculate market price impacts against live mandi records.
4. Verify by running `./gradlew assembleDebug` using `run_command`.
5. Write handoff report to `c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m2\handoff.md` and send message when complete.
