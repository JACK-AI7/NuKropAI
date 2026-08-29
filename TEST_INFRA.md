# E2E Test Infra: NuKropAI National Crop Disease Aggregation & Early Warning System

## Test Philosophy
- Opaque-box, requirement-driven, deterministic testing of the aggregation engine, density threshold rules, neighbor geographic alert fan-out, econometric market impact calculations, and telemetry data models.
- Systematic 4-tier test case design methodology (Category-Partition, Boundary Value Analysis, Pairwise Combinatorial, and Real-World Agricultural Epidemic Scenarios).

## Feature Inventory & Test Mapping
| # | Feature | Requirement | Tier 1 (Feature) | Tier 2 (BVA/Corner) | Tier 3 (Cross-Feature) | Tier 4 (Real-World) |
|---|---------|-------------|:----------------:|:-------------------:|:----------------------:|:-------------------:|
| 1 | Scan Density Aggregation (100 scans threshold) | R1 | 5 | 5 | ✓ | ✓ |
| 2 | Geographic Neighbor Alert Fan-out | R1 | 5 | 5 | ✓ | ✓ |
| 3 | Time-Window Rolling Filter (168h) | R1 | 5 | 5 | ✓ | ✓ |
| 4 | Market Impact Supply Contraction (+% surge) | R2 | 5 | 5 | ✓ | ✓ |
| 5 | Market Impact Distress Selling (-% drop) | R2 | 5 | 5 | ✓ | ✓ |
| 6 | Crop Perishability & Geographic Multipliers | R2 | 5 | 5 | ✓ | ✓ |
| 7 | Price Floor & Confidence Safeguards | R2 | 5 | 5 | ✓ | ✓ |
| 8 | Telemetry Data Contracts & Serialization | R3 | 5 | 5 | ✓ | ✓ |

## Test Runner
- Command: `./gradlew testDebugUnitTest`
- Expected: All unit and integration tests pass with exit code 0.

## Test File Layout
- `app/src/test/java/com/example/DiseaseAggregationTest.kt` (Scan aggregation, 100 threshold, neighbor fanout, temporal filtering)
- `app/src/test/java/com/example/MarketImpactCalculatorTest.kt` (Econometric shock calculation, perishability weighting, stages, price floors, risk matrix)
- `app/src/test/java/com/example/ScanTelemetryIntegrationTest.kt` (End-to-end integration and data contract validation)
