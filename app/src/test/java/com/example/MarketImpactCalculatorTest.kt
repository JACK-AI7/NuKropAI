package com.example

import com.example.market.AffectedMarketDetail
import com.example.market.ImpactDirection
import com.example.market.ImpactMechanism
import com.example.market.MarketImpactCalculator
import com.example.market.MarketImpactRepository
import com.example.market.MarketRiskLevel
import com.example.market.OutbreakSeverity
import com.example.market.OutbreakStage
import com.example.model.OutbreakAlert
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Comprehensive 4-Tier Test Suite for Market Impact Econometric Engine, Perishability Modeling,
 * Stage Dynamics, Price Floors, Confidence Scoring, and APMC Mandi Forecasts.
 */
class MarketImpactCalculatorTest {

    // =========================================================================
    // TIER 1: CORE FEATURE TESTS (Primary Happy Path & Mathematical Foundations)
    // =========================================================================

    @Test
    fun testPerishabilityMappingAllCropsAndAliases() {
        // High Perishability Horticulture (1.35 - 1.40)
        assertEquals(1.40, MarketImpactCalculator.getPerishability("Tomato"), 0.001)
        assertEquals(1.40, MarketImpactCalculator.getPerishability("Tamatar"), 0.001)
        assertEquals(1.40, MarketImpactCalculator.getPerishability("Organic Red Tomato"), 0.001)
        assertEquals(1.35, MarketImpactCalculator.getPerishability("Capsicum"), 0.001)
        assertEquals(1.35, MarketImpactCalculator.getPerishability("Chilli"), 0.001)
        assertEquals(1.35, MarketImpactCalculator.getPerishability("Chili"), 0.001)
        assertEquals(1.35, MarketImpactCalculator.getPerishability("Chilly"), 0.001)
        assertEquals(1.35, MarketImpactCalculator.getPerishability("Pepper"), 0.001)
        assertEquals(1.35, MarketImpactCalculator.getPerishability("Shimla Mirch"), 0.001)
        assertEquals(1.35, MarketImpactCalculator.getPerishability("Green Chilli"), 0.001)
        assertEquals(1.35, MarketImpactCalculator.getPerishability("Red Chilli"), 0.001)

        // Semi-Perishable Alliums & Tubers (1.15 - 1.25)
        assertEquals(1.25, MarketImpactCalculator.getPerishability("Onion"), 0.001)
        assertEquals(1.25, MarketImpactCalculator.getPerishability("Pyaz"), 0.001)
        assertEquals(1.25, MarketImpactCalculator.getPerishability("Nashik Red Onion"), 0.001)
        assertEquals(1.15, MarketImpactCalculator.getPerishability("Potato"), 0.001)
        assertEquals(1.15, MarketImpactCalculator.getPerishability("Aloo"), 0.001)
        assertEquals(1.15, MarketImpactCalculator.getPerishability("Agra Table Potato"), 0.001)

        // Fibers & Cash Crops (0.95)
        assertEquals(0.95, MarketImpactCalculator.getPerishability("Cotton"), 0.001)
        assertEquals(0.95, MarketImpactCalculator.getPerishability("Kapas"), 0.001)
        assertEquals(0.95, MarketImpactCalculator.getPerishability("Shankar-6 Cotton"), 0.001)

        // Oilseeds & Coarse Grains (0.85 - 0.90)
        assertEquals(0.90, MarketImpactCalculator.getPerishability("Mustard"), 0.001)
        assertEquals(0.90, MarketImpactCalculator.getPerishability("Sarson"), 0.001)
        assertEquals(0.90, MarketImpactCalculator.getPerishability("Soybean"), 0.001)
        assertEquals(0.90, MarketImpactCalculator.getPerishability("Soyabean"), 0.001)
        assertEquals(0.85, MarketImpactCalculator.getPerishability("Maize"), 0.001)
        assertEquals(0.85, MarketImpactCalculator.getPerishability("Corn"), 0.001)
        assertEquals(0.85, MarketImpactCalculator.getPerishability("Makka"), 0.001)

        // Durable Cereals (0.80)
        assertEquals(0.80, MarketImpactCalculator.getPerishability("Wheat"), 0.001)
        assertEquals(0.80, MarketImpactCalculator.getPerishability("Gehun"), 0.001)
        assertEquals(0.80, MarketImpactCalculator.getPerishability("Sharbati Wheat"), 0.001)
        assertEquals(0.80, MarketImpactCalculator.getPerishability("Rice"), 0.001)
        assertEquals(0.80, MarketImpactCalculator.getPerishability("Paddy"), 0.001)
        assertEquals(0.80, MarketImpactCalculator.getPerishability("Chawal"), 0.001)
        assertEquals(0.80, MarketImpactCalculator.getPerishability("Dhan"), 0.001)
        assertEquals(0.80, MarketImpactCalculator.getPerishability("Basmati Rice"), 0.001)

        // Unknown Crop Default (1.00)
        assertEquals(1.00, MarketImpactCalculator.getPerishability("UnknownCrop"), 0.001)
        assertEquals(1.00, MarketImpactCalculator.getPerishability(""), 0.001)
    }

    @Test
    fun testSeverityShockFactors() {
        assertEquals(0.32, MarketImpactCalculator.getSeverityShock("CRITICAL"), 0.001)
        assertEquals(0.22, MarketImpactCalculator.getSeverityShock("HIGH"), 0.001)
        assertEquals(0.12, MarketImpactCalculator.getSeverityShock("MODERATE"), 0.001)
        assertEquals(0.05, MarketImpactCalculator.getSeverityShock("LOW"), 0.001)
        // Case-insensitivity & fallback
        assertEquals(0.32, MarketImpactCalculator.getSeverityShock("critical"), 0.001)
        assertEquals(0.22, MarketImpactCalculator.getSeverityShock("High"), 0.001)
        assertEquals(0.12, MarketImpactCalculator.getSeverityShock("UNKNOWN_SEVERITY"), 0.001)
    }

    @Test
    fun testSupplyContractionPriceSurge() {
        // Critical Tomato outbreak at Epicenter (Maharashtra -> Maharashtra)
        // beta = 0.32, perishability = 1.40, D = 1.0 (100 scans), geo = 1.0
        // deltaPct = 0.32 * 1.40 * 1.0 * 1.0 * 100 = +44.8%
        val alert = OutbreakAlert(
            id = "test-alert-1",
            diseaseName = "Tomato Early Blight",
            sourceState = "Maharashtra",
            targetState = "Maharashtra",
            alertType = "EPICENTER",
            severity = "CRITICAL",
            scanCount = 100
        )

        val impact = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = 2000.0,
            targetState = "Maharashtra",
            targetMandi = "Nashik APMC",
            stage = OutbreakStage.SUPPLY_CONTRACTION
        )

        assertEquals(44.8, impact.deltaPercentage, 0.1)
        assertEquals(2896.0, impact.predictedModalPrice, 1.0)
        assertEquals(896.0, impact.priceDelta, 1.0)
        assertEquals(ImpactDirection.SURGE, impact.direction)
        assertEquals(MarketRiskLevel.CRITICAL, impact.riskLevel)
        assertEquals(ImpactMechanism.SUPPLY_CONTRACTION, impact.mechanism)
        assertTrue(impact.confidenceScore in 50..98)
        assertEquals(3, impact.estimatedPeakDays) // Tomato epicenter peak = 3 days
    }

    @Test
    fun testEarlyPanicDistressSellingAtEpicenter() {
        // Early panic at Epicenter: farmers rush to dump harvest before total decay
        // deltaPct = -(beta * perishability * D * 0.85 * 100)
        // High severity Onion: beta = 0.22, perishability = 1.25, D = 1.0 -> -(0.22 * 1.25 * 1.0 * 0.85 * 100) = -23.375%
        val alert = OutbreakAlert(
            id = "test-alert-distress",
            diseaseName = "Onion Purple Blotch",
            sourceState = "Maharashtra",
            targetState = "Maharashtra",
            alertType = "EPICENTER",
            severity = "HIGH",
            scanCount = 100
        )

        val impact = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = 3000.0,
            targetState = "Maharashtra",
            targetMandi = "Lasalgaon Mandi",
            stage = OutbreakStage.EARLY_PANIC
        )

        assertEquals(-23.375, impact.deltaPercentage, 0.2)
        assertEquals(2298.75, impact.predictedModalPrice, 2.0)
        assertEquals(-701.25, impact.priceDelta, 2.0)
        assertEquals(ImpactDirection.DROP, impact.direction)
        assertEquals(ImpactMechanism.DISTRESS_SELLING, impact.mechanism)
        assertEquals(MarketRiskLevel.HIGH, impact.riskLevel)
        assertTrue(impact.recommendedFarmerAction.contains("Avoid panic dumping"))
    }

    @Test
    fun testRecoveryStageQualityDiscount() {
        // Recovery stage: market applies quality discount for blemished produce
        // deltaPct = -(beta * 0.30 * perishability * D * 100)
        // High severity Potato: beta = 0.22, perishability = 1.15, D = 1.0 -> -(0.22 * 0.30 * 1.15 * 1.0 * 100) = -7.59%
        val alert = OutbreakAlert(
            id = "test-alert-recovery",
            diseaseName = "Potato Late Blight",
            sourceState = "Uttar Pradesh",
            targetState = "Uttar Pradesh",
            alertType = "EPICENTER",
            severity = "HIGH",
            scanCount = 100
        )

        val impact = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = 1500.0,
            targetState = "Uttar Pradesh",
            targetMandi = "Agra Mandi",
            stage = OutbreakStage.RECOVERY
        )

        assertEquals(-7.59, impact.deltaPercentage, 0.2)
        assertEquals(ImpactDirection.DROP, impact.direction)
        assertEquals(ImpactMechanism.QUALITY_DISCOUNT, impact.mechanism)
        assertEquals(MarketRiskLevel.MODERATE, impact.riskLevel)
        assertTrue(impact.recommendedFarmerAction.contains("Avoid panic dumping") || impact.recommendedFarmerAction.contains("Execute thorough field sorting"))

        // Also test recovery recommendation on distant market where isEpicenter is false
        val distantImpact = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = 1500.0,
            targetState = "Kerala",
            targetMandi = "Kochi Mandi",
            stage = OutbreakStage.RECOVERY
        )
        assertTrue(distantImpact.recommendedFarmerAction.contains("Execute thorough field sorting"))
    }

    @Test
    fun testNeighborSpilloverArbitrage() {
        // Neighbor state experiences supply vacuum and price surge:
        // deltaPct = beta * perishability * D * geo (0.70) * 100
        // Critical Tomato in Maharashtra, evaluated for neighbor Madhya Pradesh
        // 0.32 * 1.40 * 1.0 * 0.70 * 100 = 31.36%
        val alert = OutbreakAlert(
            id = "test-alert-neighbor",
            diseaseName = "Tomato Early Blight",
            sourceState = "Maharashtra",
            targetState = "Madhya Pradesh",
            alertType = "EARLY_WARNING",
            severity = "CRITICAL",
            scanCount = 100
        )

        val impact = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = 2000.0,
            targetState = "Madhya Pradesh",
            targetMandi = "Indore Mandi",
            stage = OutbreakStage.SUPPLY_CONTRACTION
        )

        assertEquals(31.36, impact.deltaPercentage, 0.2)
        assertEquals(ImpactDirection.SURGE, impact.direction)
        assertEquals(ImpactMechanism.REGIONAL_ARBITRAGE, impact.mechanism)
        assertEquals(MarketRiskLevel.CRITICAL, impact.riskLevel)
        assertTrue(impact.recommendedFarmerAction.contains("Transport surplus graded lots"))
    }

    // =========================================================================
    // TIER 2: BOUNDARY VALUE ANALYSIS & SAFEGUARD TESTS
    // =========================================================================

    @Test
    fun testZeroOrNegativePriceFallback() {
        val alert = OutbreakAlert(
            id = "test-alert-zero-price",
            diseaseName = "Wheat Yellow Rust",
            sourceState = "Punjab",
            targetState = "Punjab",
            alertType = "EPICENTER",
            severity = "MODERATE",
            scanCount = 100
        )

        // Current modal price = 0.0 -> Should fall back to 2500.0 base price
        val impactZero = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = 0.0,
            targetState = "Punjab",
            targetMandi = "Khanna APMC"
        )
        assertEquals(2500.0, impactZero.currentModalPrice, 0.01)
        assertTrue(impactZero.predictedModalPrice > 2500.0)

        // Negative price -> Should fall back to 2500.0 base price
        val impactNegative = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = -500.0,
            targetState = "Punjab",
            targetMandi = "Khanna APMC"
        )
        assertEquals(2500.0, impactNegative.currentModalPrice, 0.01)
    }

    @Test
    fun testDensitySaturationBounds() {
        // Density formula: (scanCount / 100.0).coerceIn(0.1, 1.0)
        assertEquals(0.10, MarketImpactCalculator.calculateDensitySaturation(0), 0.001)
        assertEquals(0.10, MarketImpactCalculator.calculateDensitySaturation(-10), 0.001)
        assertEquals(0.10, MarketImpactCalculator.calculateDensitySaturation(5), 0.001)
        assertEquals(0.50, MarketImpactCalculator.calculateDensitySaturation(50), 0.001)
        assertEquals(0.85, MarketImpactCalculator.calculateDensitySaturation(85), 0.001)
        assertEquals(1.00, MarketImpactCalculator.calculateDensitySaturation(100), 0.001)
        assertEquals(1.00, MarketImpactCalculator.calculateDensitySaturation(350), 0.001)
        assertEquals(1.00, MarketImpactCalculator.calculateDensitySaturation(1000), 0.001)
    }

    @Test
    fun testPriceFloorEnforcementUnderExtremeDistressSelling() {
        // Theoretical extreme drop alert: price floor protects at minimum 40% of baseline price
        val alert = OutbreakAlert(
            id = "test-alert-extreme-crash",
            diseaseName = "Catastrophic Tomato Blight",
            sourceState = "Karnataka",
            targetState = "Karnataka",
            alertType = "EPICENTER",
            severity = "CRITICAL",
            scanCount = 500
        )

        val impact = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = 1000.0,
            targetState = "Karnataka",
            targetMandi = "Kolar APMC",
            stage = OutbreakStage.EARLY_PANIC
        )

        // Floor price = 1000.0 * 0.40 = 400.0
        assertTrue("Predicted price must not fall below 40% floor (400.0)", impact.predictedModalPrice >= 400.0)
        assertEquals(619.2, impact.predictedModalPrice, 0.1)
        assertEquals(-38.08, impact.deltaPercentage, 0.1)
    }

    @Test
    fun testConfidenceScoreBounding() {
        // Test lower bound: 0 scans, empty records
        // density = 0.10, raw = 50 + (0.10 * 35) + 5 = 58.5 -> 59
        val lowAlert = OutbreakAlert(
            id = "low-conf",
            diseaseName = "Unknown Disease",
            sourceState = "Goa",
            targetState = "Goa",
            scanCount = 0
        )
        val lowImpact = MarketImpactCalculator.calculateImpact(
            alert = lowAlert,
            currentModalPrice = 2000.0,
            targetState = "Goa",
            targetMandi = "Mapusa Mandi",
            availableMandiRecords = emptyList()
        )
        assertEquals(59, lowImpact.confidenceScore)
        assertTrue(lowImpact.confidenceScore in 50..98)

        // Test upper bound: 500 scans, live mandi records provided
        // density = 1.00, raw = 50 + (1.0 * 35) + 13 = 98
        val highAlert = OutbreakAlert(
            id = "high-conf",
            diseaseName = "Cotton Bollworm",
            sourceState = "Gujarat",
            targetState = "Gujarat",
            scanCount = 500
        )
        val mockRecords = listOf(
            com.example.MandiRecord(
                state = "Gujarat",
                district = "Rajkot",
                market = "Rajkot APMC",
                commodity = "Cotton",
                variety = "Shankar",
                minPrice = 6800.0,
                maxPrice = 7400.0,
                modalPrice = 7100.0,
                arrivalDate = "Today"
            )
        )
        val highImpact = MarketImpactCalculator.calculateImpact(
            alert = highAlert,
            currentModalPrice = 7100.0,
            targetState = "Gujarat",
            targetMandi = "Rajkot APMC",
            availableMandiRecords = mockRecords
        )
        assertEquals(98, highImpact.confidenceScore)
        assertTrue(highImpact.confidenceScore in 50..98)
    }

    @Test
    fun testStableMarketDirectionBoundaries() {
        // Very low shock producing delta < 0.5%
        // Low severity (0.05) Wheat (0.80) at Distant State (0.40) with 10 scans (D=0.10)
        // deltaPct = 0.05 * 0.80 * 0.10 * 0.40 * 100 = 0.16%
        val alert = OutbreakAlert(
            id = "test-stable",
            diseaseName = "Wheat Rust",
            sourceState = "Punjab",
            targetState = "Kerala",
            alertType = "EARLY_WARNING",
            severity = "LOW",
            scanCount = 10
        )

        val impact = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = 2200.0,
            targetState = "Kerala",
            targetMandi = "Kochi APMC",
            stage = OutbreakStage.SUPPLY_CONTRACTION
        )

        assertEquals(0.16, impact.deltaPercentage, 0.05)
        assertEquals(ImpactDirection.STABLE, impact.direction)
        assertEquals(MarketRiskLevel.LOW, impact.riskLevel)
        assertTrue(impact.recommendedFarmerAction.contains("Normal market conditions prevail"))
    }

    // =========================================================================
    // TIER 3: CROSS-FEATURE & COMBINATORIAL TESTS
    // =========================================================================

    @Test
    fun testGeographicMultiplierAcrossDistanceTiers() {
        // Epicenter (1.00)
        assertEquals(1.00, MarketImpactCalculator.getGeographicMultiplier("Maharashtra", "Maharashtra"), 0.001)
        assertEquals(1.00, MarketImpactCalculator.getGeographicMultiplier("Punjab", "Punjab"), 0.001)

        // Direct Neighbors (0.70)
        assertEquals(0.70, MarketImpactCalculator.getGeographicMultiplier("Maharashtra", "Madhya Pradesh"), 0.001)
        assertEquals(0.70, MarketImpactCalculator.getGeographicMultiplier("Maharashtra", "Gujarat"), 0.001)
        assertEquals(0.70, MarketImpactCalculator.getGeographicMultiplier("Maharashtra", "Karnataka"), 0.001)
        assertEquals(0.70, MarketImpactCalculator.getGeographicMultiplier("Punjab", "Haryana"), 0.001)
        assertEquals(0.70, MarketImpactCalculator.getGeographicMultiplier("Punjab", "Himachal Pradesh"), 0.001)
        assertEquals(0.70, MarketImpactCalculator.getGeographicMultiplier("Uttar Pradesh", "Bihar"), 0.001)
        assertEquals(0.70, MarketImpactCalculator.getGeographicMultiplier("Tamil Nadu", "Kerala"), 0.001)

        // Distant / Non-Adjacent States (0.40)
        assertEquals(0.40, MarketImpactCalculator.getGeographicMultiplier("Punjab", "Kerala"), 0.001)
        assertEquals(0.40, MarketImpactCalculator.getGeographicMultiplier("Maharashtra", "Assam"), 0.001)
        assertEquals(0.40, MarketImpactCalculator.getGeographicMultiplier("Gujarat", "Odisha"), 0.001)
        assertEquals(0.40, MarketImpactCalculator.getGeographicMultiplier("Tamil Nadu", "Himachal Pradesh"), 0.001)
    }

    @Test
    fun testRiskLevelClassificationThresholds() {
        // CRITICAL: >= 25.0%
        assertEquals(MarketRiskLevel.CRITICAL, MarketRiskLevel.fromDeltaPercentage(25.0))
        assertEquals(MarketRiskLevel.CRITICAL, MarketRiskLevel.fromDeltaPercentage(44.8))
        assertEquals(MarketRiskLevel.CRITICAL, MarketRiskLevel.fromDeltaPercentage(-25.0))
        assertEquals(MarketRiskLevel.CRITICAL, MarketRiskLevel.fromDeltaPercentage(-35.0))

        // HIGH: 15.0% to 24.9%
        assertEquals(MarketRiskLevel.HIGH, MarketRiskLevel.fromDeltaPercentage(15.0))
        assertEquals(MarketRiskLevel.HIGH, MarketRiskLevel.fromDeltaPercentage(24.9))
        assertEquals(MarketRiskLevel.HIGH, MarketRiskLevel.fromDeltaPercentage(-15.0))
        assertEquals(MarketRiskLevel.HIGH, MarketRiskLevel.fromDeltaPercentage(-23.4))

        // MODERATE: 7.0% to 14.9%
        assertEquals(MarketRiskLevel.MODERATE, MarketRiskLevel.fromDeltaPercentage(7.0))
        assertEquals(MarketRiskLevel.MODERATE, MarketRiskLevel.fromDeltaPercentage(14.9))
        assertEquals(MarketRiskLevel.MODERATE, MarketRiskLevel.fromDeltaPercentage(-7.0))
        assertEquals(MarketRiskLevel.MODERATE, MarketRiskLevel.fromDeltaPercentage(-12.0))

        // LOW: < 7.0%
        assertEquals(MarketRiskLevel.LOW, MarketRiskLevel.fromDeltaPercentage(6.9))
        assertEquals(MarketRiskLevel.LOW, MarketRiskLevel.fromDeltaPercentage(0.0))
        assertEquals(MarketRiskLevel.LOW, MarketRiskLevel.fromDeltaPercentage(-6.9))
    }

    @Test
    fun testPeakDaysCalculationAcrossPerishabilities() {
        // Horticulture (>= 1.35): Epicenter 3d, Neighbor 5d
        val tomatoAlert = OutbreakAlert(id = "1", diseaseName = "Tomato Blight", sourceState = "MH", targetState = "MH", severity = "CRITICAL", scanCount = 100)
        val tomatoEpi = MarketImpactCalculator.calculateImpact(tomatoAlert, 2000.0, "MH", "Mandi 1")
        assertEquals(3, tomatoEpi.estimatedPeakDays)

        val tomatoNeighbor = MarketImpactCalculator.calculateImpact(tomatoAlert, 2000.0, "Gujarat", "Mandi 2")
        assertEquals(5, tomatoNeighbor.estimatedPeakDays)

        // Semi-Perishable (>= 1.15): Epicenter 6d, Neighbor 9d
        val onionAlert = OutbreakAlert(id = "2", diseaseName = "Onion Blotch", sourceState = "MH", targetState = "MH", severity = "HIGH", scanCount = 100)
        val onionEpi = MarketImpactCalculator.calculateImpact(onionAlert, 2000.0, "MH", "Mandi 1")
        assertEquals(6, onionEpi.estimatedPeakDays)
        val onionNeighbor = MarketImpactCalculator.calculateImpact(onionAlert, 2000.0, "Gujarat", "Mandi 2")
        assertEquals(9, onionNeighbor.estimatedPeakDays)

        // Cash / Fiber (>= 0.90): Epicenter 14d, Neighbor 18d
        val cottonAlert = OutbreakAlert(id = "3", diseaseName = "Cotton Bollworm", sourceState = "GJ", targetState = "GJ", severity = "HIGH", scanCount = 100)
        val cottonEpi = MarketImpactCalculator.calculateImpact(cottonAlert, 6500.0, "GJ", "Mandi 1")
        assertEquals(14, cottonEpi.estimatedPeakDays)
        val cottonNeighbor = MarketImpactCalculator.calculateImpact(cottonAlert, 6500.0, "Maharashtra", "Mandi 2")
        assertEquals(18, cottonNeighbor.estimatedPeakDays)

        // Cereals (< 0.90): Epicenter 21d, Neighbor 28d
        val wheatAlert = OutbreakAlert(id = "4", diseaseName = "Wheat Rust", sourceState = "PB", targetState = "PB", severity = "HIGH", scanCount = 100)
        val wheatEpi = MarketImpactCalculator.calculateImpact(wheatAlert, 2275.0, "PB", "Mandi 1")
        assertEquals(21, wheatEpi.estimatedPeakDays)
        val wheatNeighbor = MarketImpactCalculator.calculateImpact(wheatAlert, 2275.0, "Haryana", "Mandi 2")
        assertEquals(28, wheatNeighbor.estimatedPeakDays)
    }

    @Test
    fun testStageAndSeverityCombinatorialMatrix() {
        val severities = listOf("CRITICAL", "HIGH", "MODERATE", "LOW")
        val stages = listOf(OutbreakStage.SUPPLY_CONTRACTION, OutbreakStage.EARLY_PANIC, OutbreakStage.RECOVERY)

        for (sev in severities) {
            for (stg in stages) {
                val alert = OutbreakAlert(
                    id = "matrix-$sev-$stg",
                    diseaseName = "Soybean Stem Rot",
                    sourceState = "Madhya Pradesh",
                    targetState = "Madhya Pradesh",
                    alertType = "EPICENTER",
                    severity = sev,
                    scanCount = 150
                )

                val impact = MarketImpactCalculator.calculateImpact(
                    alert = alert,
                    currentModalPrice = 4500.0,
                    targetState = "Madhya Pradesh",
                    targetMandi = "Indore APMC",
                    stage = stg
                )

                assertNotNull(impact)
                assertTrue(impact.predictedModalPrice >= 1800.0) // 40% floor of 4500
                assertTrue(impact.confidenceScore in 50..98)

                when (stg) {
                    OutbreakStage.SUPPLY_CONTRACTION -> {
                        assertEquals(ImpactDirection.SURGE, impact.direction)
                        assertEquals(ImpactMechanism.SUPPLY_CONTRACTION, impact.mechanism)
                    }
                    OutbreakStage.EARLY_PANIC -> {
                        assertEquals(ImpactDirection.DROP, impact.direction)
                        assertEquals(ImpactMechanism.DISTRESS_SELLING, impact.mechanism)
                    }
                    OutbreakStage.RECOVERY -> {
                        assertEquals(ImpactDirection.DROP, impact.direction)
                        assertEquals(ImpactMechanism.QUALITY_DISCOUNT, impact.mechanism)
                    }
                }
            }
        }
    }

    @Test
    fun testAffectedMarketsBreakdownGeneration() {
        val alert = OutbreakAlert(
            id = "alert-multi-market",
            diseaseName = "Tomato Early Blight",
            sourceState = "Maharashtra",
            targetState = "Maharashtra",
            alertType = "EPICENTER",
            severity = "HIGH",
            scanCount = 120
        )

        val mandiRecords = listOf(
            com.example.MandiRecord(state = "Maharashtra", district = "Nashik", market = "Pimpalgaon APMC", commodity = "Tomato", variety = "Hybrid", minPrice = 1800.0, maxPrice = 2400.0, modalPrice = 2100.0, arrivalDate = "Today"),
            com.example.MandiRecord(state = "Maharashtra", district = "Pune", market = "Narayangaon APMC", commodity = "Tomato", variety = "Desi", minPrice = 1900.0, maxPrice = 2500.0, modalPrice = 2200.0, arrivalDate = "Today"),
            com.example.MandiRecord(state = "Madhya Pradesh", district = "Indore", market = "Choithram APMC", commodity = "Tomato", variety = "Local", minPrice = 1700.0, maxPrice = 2300.0, modalPrice = 2000.0, arrivalDate = "Today")
        )

        val impact = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = 2100.0,
            targetState = "Maharashtra",
            targetMandi = "Pimpalgaon APMC",
            availableMandiRecords = mandiRecords
        )

        assertTrue(impact.affectedMarkets.isNotEmpty())
        val epicenterMarkets = impact.affectedMarkets.filter { it.isEpicenter }
        val neighborMarkets = impact.affectedMarkets.filter { !it.isEpicenter }

        assertTrue(epicenterMarkets.isNotEmpty())
        for (m in epicenterMarkets) {
            assertTrue(m.predictedModalPrice > m.currentModalPrice)
            assertEquals(ImpactDirection.SURGE, m.direction)
        }
    }

    // =========================================================================
    // TIER 4: REAL-WORLD COMMODITY MANDI SCENARIOS
    // =========================================================================

    @Test
    fun testTomatoPriceShockInNashikMandi() {
        // Real-world: Tomato Early Blight in Nashik, Maharashtra
        // Baseline price: Rs 2000/Qtl, 150 scans (D=1.0), CRITICAL severity (beta=0.32)
        // Supply contraction: delta = 0.32 * 1.40 * 1.0 * 1.0 * 100 = 44.8%
        // Predicted price: 2000 * 1.448 = 2896.0 INR/Qtl
        val alert = OutbreakAlert(
            id = "tlb-nashik",
            diseaseName = "Tomato Early Blight (Alternaria solani)",
            sourceState = "Maharashtra",
            targetState = "Maharashtra",
            alertType = "EPICENTER",
            severity = "CRITICAL",
            scanCount = 150
        )

        val impact = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = 2000.0,
            targetState = "Maharashtra",
            targetMandi = "Nashik APMC",
            stage = OutbreakStage.SUPPLY_CONTRACTION
        )

        assertEquals("Tomato", impact.cropName)
        assertEquals(44.8, impact.deltaPercentage, 0.1)
        assertEquals(2896.0, impact.predictedModalPrice, 1.0)
        assertEquals(896.0, impact.priceDelta, 1.0)
        assertEquals(ImpactDirection.SURGE, impact.direction)
        assertEquals(MarketRiskLevel.CRITICAL, impact.riskLevel)
        assertTrue(impact.recommendedFarmerAction.contains("stagger mandi arrivals over the next 3 days"))
    }

    @Test
    fun testWheatYellowRustShockInKhannaPunjab() {
        // Real-world: Yellow Rust in Khanna APMC, Punjab (Asia's largest grain market)
        // Baseline price: Rs 2275/Qtl (Govt MSP), 100 scans, HIGH severity (beta=0.22)
        // Perishability 0.80 -> delta = 0.22 * 0.80 * 1.0 * 1.0 * 100 = +17.6%
        // Predicted price: 2275 * 1.176 = 2675.4 INR/Qtl
        val alert = OutbreakAlert(
            id = "yr-khanna",
            diseaseName = "Wheat Yellow Rust (Puccinia striiformis)",
            sourceState = "Punjab",
            targetState = "Punjab",
            alertType = "EPICENTER",
            severity = "HIGH",
            scanCount = 100
        )

        val impact = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = 2275.0,
            targetState = "Punjab",
            targetMandi = "Khanna APMC",
            stage = OutbreakStage.SUPPLY_CONTRACTION
        )

        assertEquals("Wheat", impact.cropName)
        assertEquals(17.6, impact.deltaPercentage, 0.1)
        assertEquals(2675.4, impact.predictedModalPrice, 1.0)
        assertEquals(400.4, impact.priceDelta, 1.0)
        assertEquals(ImpactDirection.SURGE, impact.direction)
        assertEquals(MarketRiskLevel.HIGH, impact.riskLevel)
        assertEquals(21, impact.estimatedPeakDays)
    }

    @Test
    fun testOnionDistressSellingInLasalgaon() {
        // Real-world: Onion Purple Blotch in Lasalgaon APMC (Asia's largest onion market)
        // Baseline price: Rs 3200/Qtl, EARLY_PANIC stage, HIGH severity (beta=0.22)
        // Perishability 1.25 -> delta = -(0.22 * 1.25 * 1.0 * 0.85 * 100) = -23.375%
        // Predicted price: 3200 * (1 - 0.23375) = 2452.0 INR/Qtl
        val alert = OutbreakAlert(
            id = "opb-lasalgaon",
            diseaseName = "Onion Purple Blotch (Alternaria porri)",
            sourceState = "Maharashtra",
            targetState = "Maharashtra",
            alertType = "EPICENTER",
            severity = "HIGH",
            scanCount = 100
        )

        val impact = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = 3200.0,
            targetState = "Maharashtra",
            targetMandi = "Lasalgaon Mandi",
            stage = OutbreakStage.EARLY_PANIC
        )

        assertEquals("Onion", impact.cropName)
        assertEquals(-23.375, impact.deltaPercentage, 0.2)
        assertEquals(2452.0, impact.predictedModalPrice, 2.0)
        assertEquals(-748.0, impact.priceDelta, 2.0)
        assertEquals(ImpactDirection.DROP, impact.direction)
        assertEquals(ImpactMechanism.DISTRESS_SELLING, impact.mechanism)
        assertEquals(MarketRiskLevel.HIGH, impact.riskLevel)
    }

    @Test
    fun testCottonPinkBollwormInRajkotGujarat() {
        // Real-world: Pink Bollworm in Rajkot APMC, Gujarat
        // Baseline price: Rs 7000/Qtl, MODERATE severity (beta=0.12), 100 scans (D=1.0)
        // Perishability 0.95 -> delta = 0.12 * 0.95 * 1.0 * 1.0 * 100 = +11.4%
        // Predicted price: 7000 * 1.114 = 7798.0 INR/Qtl
        val alert = OutbreakAlert(
            id = "pb-rajkot",
            diseaseName = "Cotton Pink Bollworm (Pectinophora gossypiella)",
            sourceState = "Gujarat",
            targetState = "Gujarat",
            alertType = "EPICENTER",
            severity = "MODERATE",
            scanCount = 100
        )

        val impact = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = 7000.0,
            targetState = "Gujarat",
            targetMandi = "Rajkot APMC",
            stage = OutbreakStage.SUPPLY_CONTRACTION
        )

        assertEquals("Cotton", impact.cropName)
        assertEquals(11.4, impact.deltaPercentage, 0.1)
        assertEquals(7798.0, impact.predictedModalPrice, 1.0)
        assertEquals(798.0, impact.priceDelta, 1.0)
        assertEquals(ImpactDirection.SURGE, impact.direction)
        assertEquals(MarketRiskLevel.MODERATE, impact.riskLevel)
        assertEquals(14, impact.estimatedPeakDays)
    }

    @Test
    fun testChilliLeafCurlOutbreakInGunturAP() {
        // Real-world: Chilli Leaf Curl in Guntur Mandi (India's premier spice hub)
        // Baseline price: Rs 18000/Qtl, HIGH severity (beta=0.22), 100 scans
        // Perishability 1.35 -> delta = 0.22 * 1.35 * 1.0 * 1.0 * 100 = +29.7%
        // Predicted price: 18000 * 1.297 = 23346.0 INR/Qtl
        val alert = OutbreakAlert(
            id = "clc-guntur",
            diseaseName = "Chilli Leaf Curl Virus",
            sourceState = "Andhra Pradesh",
            targetState = "Andhra Pradesh",
            alertType = "EPICENTER",
            severity = "HIGH",
            scanCount = 100
        )

        val impact = MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = 18000.0,
            targetState = "Andhra Pradesh",
            targetMandi = "Guntur Mirchi Yard",
            stage = OutbreakStage.SUPPLY_CONTRACTION
        )

        assertEquals("Chilli", impact.cropName)
        assertEquals(29.7, impact.deltaPercentage, 0.1)
        assertEquals(23346.0, impact.predictedModalPrice, 2.0)
        assertEquals(5346.0, impact.priceDelta, 2.0)
        assertEquals(ImpactDirection.SURGE, impact.direction)
        assertEquals(MarketRiskLevel.CRITICAL, impact.riskLevel)
        assertEquals(3, impact.estimatedPeakDays)
    }

    @Test
    fun testMarketImpactRepositoryCalculationAndCache() {
        MarketImpactRepository.clearCache()

        val alert = OutbreakAlert(
            id = "repo-test-1",
            diseaseName = "Cotton Bollworm Outbreak",
            sourceState = "Gujarat",
            targetState = "Gujarat",
            alertType = "EPICENTER",
            severity = "HIGH",
            scanCount = 120
        )

        val impact = MarketImpactRepository.calculateImpact(
            alert = alert,
            currentModalPrice = 6500.0,
            targetState = "Gujarat",
            targetMandi = "Rajkot APMC"
        )

        assertNotNull(impact)
        assertEquals("Gujarat", impact.targetState)
        assertTrue(impact.predictedModalPrice > 6500.0)
        assertTrue(impact.affectedMarkets.isNotEmpty())
    }
}
