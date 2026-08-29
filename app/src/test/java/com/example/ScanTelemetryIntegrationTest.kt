package com.example

import com.example.market.AffectedMarketDetail
import com.example.market.ImpactDirection
import com.example.market.ImpactMechanism
import com.example.market.MarketImpactCalculator
import com.example.market.MarketImpactRepository
import com.example.market.MarketPriceImpact
import com.example.market.MarketRiskLevel
import com.example.market.OutbreakSeverity
import com.example.market.OutbreakStage
import com.example.model.AlertType
import com.example.model.DiseaseScanPayload
import com.example.model.DiseaseScanRecord
import com.example.model.OutbreakAlert
import com.example.model.ScanSeverity
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.util.concurrent.TimeUnit

/**
 * Comprehensive Integration and Contract Test Suite for Scan Telemetry Serialization,
 * PostgREST Data Models, and End-to-End Pipeline from On-Device Scan Ingestion
 * to Density Aggregation and Econometric Mandi Market Impact Forecasting.
 */
class ScanTelemetryIntegrationTest {

    private val json = Json {
        ignoreUnknownKeys = true
        isLenient = true
        coerceInputValues = true
        encodeDefaults = true
        prettyPrint = false
    }

    // =========================================================================
    // TIER 1: DATA CONTRACT SERIALIZATION & DESERIALIZATION ROUNDTRIPS
    // =========================================================================

    @Test
    fun testDiseaseScanPayloadSerializationRoundtrip() {
        val payload = DiseaseScanPayload(
            diseaseName = "Fall Armyworm",
            cropName = "Maize",
            state = "Maharashtra",
            district = "Nashik",
            severity = "Critical",
            confidence = 96,
            latitude = 19.9975,
            longitude = 73.7898,
            scannedAt = 1724900000000L
        )

        val jsonStr = json.encodeToString(payload)

        // Verify snake_case serialization keys
        assertTrue(jsonStr.contains("\"disease_name\":\"Fall Armyworm\""))
        assertTrue(jsonStr.contains("\"crop_name\":\"Maize\""))
        assertTrue(jsonStr.contains("\"state\":\"Maharashtra\""))
        assertTrue(jsonStr.contains("\"district\":\"Nashik\""))
        assertTrue(jsonStr.contains("\"severity\":\"Critical\""))
        assertTrue(jsonStr.contains("\"confidence\":96"))
        assertTrue(jsonStr.contains("\"latitude\":19.9975"))
        assertTrue(jsonStr.contains("\"longitude\":73.7898"))
        assertTrue(jsonStr.contains("\"scanned_at\":1724900000000"))

        val decoded = json.decodeFromString<DiseaseScanPayload>(jsonStr)
        assertEquals(payload, decoded)
    }

    @Test
    fun testDiseaseScanRecordSerializationRoundtrip() {
        val record = DiseaseScanRecord(
            id = "rec-uuid-101",
            diseaseName = "Yellow Rust",
            cropName = "Wheat",
            state = "Punjab",
            district = "Ludhiana",
            latitude = 30.9010,
            longitude = 75.8573,
            severity = "High",
            confidence = 94,
            scannedAt = 1724901000000L
        )

        val jsonStr = json.encodeToString(record)
        assertTrue(jsonStr.contains("\"id\":\"rec-uuid-101\""))
        assertTrue(jsonStr.contains("\"disease_name\":\"Yellow Rust\""))

        val decoded = json.decodeFromString<DiseaseScanRecord>(jsonStr)
        assertEquals(record, decoded)
    }

    @Test
    fun testOutbreakAlertSerializationRoundtrip() {
        val alert = OutbreakAlert(
            id = "alert-epicenter-maharashtra-fall-armyworm",
            diseaseName = "Fall Armyworm",
            sourceState = "Maharashtra",
            targetState = "Maharashtra",
            alertType = "EPICENTER",
            severity = "CRITICAL",
            scanCount = 320,
            thresholdDensity = 100,
            timeWindowHours = 168,
            message = "CRITICAL OUTBREAK DETECTED in Maharashtra",
            recommendedAction = "Deploy immediate containment",
            predictedMarketImpactPct = 35.0,
            isActive = true,
            createdAt = "2026-08-29T10:00:00Z",
            updatedAt = "2026-08-29T10:00:00Z"
        )

        val jsonStr = json.encodeToString(alert)
        assertTrue(jsonStr.contains("\"alert_type\":\"EPICENTER\""))
        assertTrue(jsonStr.contains("\"severity\":\"CRITICAL\""))
        assertTrue(jsonStr.contains("\"scan_count\":320"))
        assertTrue(jsonStr.contains("\"threshold_density\":100"))
        assertTrue(jsonStr.contains("\"predicted_market_impact_pct\":35.0"))
        assertTrue(jsonStr.contains("\"is_active\":true"))

        val decoded = json.decodeFromString<OutbreakAlert>(jsonStr)
        assertEquals(alert, decoded)
    }

    @Test
    fun testMarketPriceImpactSerializationRoundtrip() {
        val affectedMarkets = listOf(
            AffectedMarketDetail(
                marketName = "Nashik APMC",
                district = "Nashik",
                state = "Maharashtra",
                currentModalPrice = 2000.0,
                predictedModalPrice = 2896.0,
                deltaPercentage = 44.8,
                direction = ImpactDirection.SURGE,
                isEpicenter = true
            ),
            AffectedMarketDetail(
                marketName = "Indore APMC",
                district = "Indore",
                state = "Madhya Pradesh",
                currentModalPrice = 2100.0,
                predictedModalPrice = 2758.56,
                deltaPercentage = 31.36,
                direction = ImpactDirection.SURGE,
                isEpicenter = false
            )
        )

        val impact = MarketPriceImpact(
            alertId = "alert-101",
            cropName = "Tomato",
            diseaseName = "Tomato Early Blight",
            targetState = "Maharashtra",
            targetMandi = "Nashik APMC",
            currentModalPrice = 2000.0,
            predictedModalPrice = 2896.0,
            priceDelta = 896.0,
            deltaPercentage = 44.8,
            direction = ImpactDirection.SURGE,
            riskLevel = MarketRiskLevel.CRITICAL,
            confidenceScore = 95,
            mechanism = ImpactMechanism.SUPPLY_CONTRACTION,
            estimatedPeakDays = 3,
            recommendedFarmerAction = "Stagger mandi arrivals",
            affectedMarkets = affectedMarkets
        )

        val jsonStr = json.encodeToString(impact)
        val decoded = json.decodeFromString<MarketPriceImpact>(jsonStr)

        assertEquals(impact.alertId, decoded.alertId)
        assertEquals(impact.cropName, decoded.cropName)
        assertEquals(impact.predictedModalPrice, decoded.predictedModalPrice, 0.01)
        assertEquals(impact.direction, decoded.direction)
        assertEquals(impact.riskLevel, decoded.riskLevel)
        assertEquals(impact.mechanism, decoded.mechanism)
        assertEquals(2, decoded.affectedMarkets.size)
        assertEquals("Nashik APMC", decoded.affectedMarkets[0].marketName)
        assertTrue(decoded.affectedMarkets[0].isEpicenter)
        assertFalse(decoded.affectedMarkets[1].isEpicenter)
    }

    @Test
    fun testDomainEnumsSerialNames() {
        assertEquals("\"EPICENTER\"", json.encodeToString(AlertType.EPICENTER))
        assertEquals("\"EARLY_WARNING\"", json.encodeToString(AlertType.EARLY_WARNING))
        assertEquals("\"CRITICAL\"", json.encodeToString(ScanSeverity.CRITICAL))
        assertEquals("\"HIGH\"", json.encodeToString(ScanSeverity.HIGH))
        assertEquals("\"MODERATE\"", json.encodeToString(ScanSeverity.MODERATE))
        assertEquals("\"LOW\"", json.encodeToString(ScanSeverity.LOW))

        assertEquals("\"EARLY_PANIC\"", json.encodeToString(OutbreakStage.EARLY_PANIC))
        assertEquals("\"SUPPLY_CONTRACTION\"", json.encodeToString(OutbreakStage.SUPPLY_CONTRACTION))
        assertEquals("\"RECOVERY\"", json.encodeToString(OutbreakStage.RECOVERY))

        assertEquals("\"SURGE\"", json.encodeToString(ImpactDirection.SURGE))
        assertEquals("\"DROP\"", json.encodeToString(ImpactDirection.DROP))
        assertEquals("\"VOLATILE\"", json.encodeToString(ImpactDirection.VOLATILE))
        assertEquals("\"STABLE\"", json.encodeToString(ImpactDirection.STABLE))

        assertEquals("\"SUPPLY_CONTRACTION\"", json.encodeToString(ImpactMechanism.SUPPLY_CONTRACTION))
        assertEquals("\"DISTRESS_SELLING\"", json.encodeToString(ImpactMechanism.DISTRESS_SELLING))
        assertEquals("\"QUALITY_DISCOUNT\"", json.encodeToString(ImpactMechanism.QUALITY_DISCOUNT))
        assertEquals("\"REGIONAL_ARBITRAGE\"", json.encodeToString(ImpactMechanism.REGIONAL_ARBITRAGE))
        assertEquals("\"PANIC_HOARDING\"", json.encodeToString(ImpactMechanism.PANIC_HOARDING))
    }

    // =========================================================================
    // TIER 2: ROBUSTNESS, NULL SAFETY & UNICODE FIDELITY
    // =========================================================================

    @Test
    fun testNullAndDefaultOptionalFieldsInPayload() {
        val payloadWithNulls = DiseaseScanPayload(
            diseaseName = "Powdery Mildew",
            state = "Rajasthan",
            latitude = null,
            longitude = null
        )

        val jsonStr = json.encodeToString(payloadWithNulls)
        val decoded = json.decodeFromString<DiseaseScanPayload>(jsonStr)

        assertEquals("General", decoded.cropName)
        assertEquals("", decoded.district)
        assertEquals("Moderate", decoded.severity)
        assertEquals(90, decoded.confidence)
        assertNull(decoded.latitude)
        assertNull(decoded.longitude)
    }

    @Test
    fun testUnicodeAndSpecialCharactersInScanData() {
        val hindiPayload = DiseaseScanPayload(
            diseaseName = "फॉल आर्मीवर्म (Spodoptera frugiperda)",
            cropName = "मक्का / Corn",
            state = "Maharashtra",
            district = "नांदेड / Nanded",
            severity = "Critical",
            confidence = 98,
            latitude = 19.1383,
            longitude = 77.3210
        )

        val jsonStr = json.encodeToString(hindiPayload)
        val decoded = json.decodeFromString<DiseaseScanPayload>(jsonStr)

        assertEquals("फॉल आर्मीवर्म (Spodoptera frugiperda)", decoded.diseaseName)
        assertEquals("मक्का / Corn", decoded.cropName)
        assertEquals("नांदेड / Nanded", decoded.district)

        // Convert to record and evaluate in aggregation engine
        val scans = (1..100).map { i ->
            DiseaseScanRecord(
                id = "scan-unicode-$i",
                diseaseName = decoded.diseaseName,
                cropName = decoded.cropName,
                state = decoded.state,
                district = decoded.district,
                scannedAt = System.currentTimeMillis()
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(scans, threshold = 100)
        assertEquals(8, alerts.size) // 1 epicenter + 7 neighbors
        val epicenter = alerts.find { it.alertType == "EPICENTER" }
        assertNotNull(epicenter)
        assertEquals("फॉल आर्मीवर्म (Spodoptera frugiperda)", epicenter?.diseaseName)
    }

    @Test
    fun testLenientDecodingOfUnknownKeys() {
        // Backend or Edge function might add extra telemetry metadata
        val rawJsonWithExtraKeys = """
            {
                "disease_name": "Tomato Leaf Curl",
                "crop_name": "Tomato",
                "state": "Andhra Pradesh",
                "district": "Chittoor",
                "severity": "High",
                "confidence": 92,
                "client_version": "2.4.0",
                "device_model": "Pixel 7a",
                "battery_level": 85,
                "network_type": "5G"
            }
        """.trimIndent()

        val decoded = json.decodeFromString<DiseaseScanPayload>(rawJsonWithExtraKeys)
        assertEquals("Tomato Leaf Curl", decoded.diseaseName)
        assertEquals("Andhra Pradesh", decoded.state)
        assertEquals(92, decoded.confidence)
    }

    // =========================================================================
    // TIER 3: MULTI-STEP TELEMETRY INGESTION TO AGGREGATION FLOW
    // =========================================================================

    @Test
    fun testFullTelemetryBatchIngestionAndAggregationPipeline() {
        // Step 1: Simulate 120 field scans arriving as JSON telemetry payloads
        val rawPayloads = (1..120).map { i ->
            """
            {
                "disease_name": "Fall Armyworm",
                "crop_name": "Maize",
                "state": "Maharashtra",
                "district": "${if (i % 2 == 0) "Nashik" else "Ahmednagar"}",
                "severity": "${if (i % 4 == 0) "Critical" else "High"}",
                "confidence": 95,
                "latitude": 19.9975,
                "longitude": 73.7898,
                "scanned_at": ${System.currentTimeMillis() - (i * 60000L)}
            }
            """.trimIndent()
        }

        // Step 2: Parse incoming JSON payloads
        val payloads = rawPayloads.map { json.decodeFromString<DiseaseScanPayload>(it) }
        assertEquals(120, payloads.size)

        // Step 3: Transform to stored records
        val records = payloads.mapIndexed { index, p ->
            DiseaseScanRecord(
                id = "db-scan-$index",
                diseaseName = p.diseaseName,
                cropName = p.cropName,
                state = p.state,
                district = p.district,
                latitude = p.latitude,
                longitude = p.longitude,
                severity = p.severity,
                confidence = p.confidence,
                scannedAt = p.scannedAt
            )
        }

        // Step 4: Run density evaluation
        val alerts = DiseaseAggregationService.evaluateDensityThreshold(records, threshold = 100)

        // Step 5: Verify alert outputs
        assertEquals(8, alerts.size) // 1 Epicenter + 7 Neighbors
        val epicenter = alerts.find { it.alertType == "EPICENTER" }
        assertNotNull(epicenter)
        assertEquals(120, epicenter?.scanCount)
        assertEquals("Maharashtra", epicenter?.sourceState)
        assertEquals("Maharashtra", epicenter?.targetState)

        val neighbors = alerts.filter { it.alertType == "EARLY_WARNING" }
        assertEquals(7, neighbors.size)
        assertTrue(neighbors.any { it.targetState == "Gujarat" })
        assertTrue(neighbors.any { it.targetState == "Madhya Pradesh" })
        assertTrue(neighbors.any { it.targetState == "Karnataka" })
    }

    @Test
    fun testSubThresholdTelemetryBatchDoesNotTriggerAlerts() {
        // Ingest 80 scans for Pink Bollworm in Gujarat (sub-threshold)
        val scans80 = (1..80).map { i ->
            DiseaseScanRecord(
                id = "sub-$i",
                diseaseName = "Pink Bollworm",
                cropName = "Cotton",
                state = "Gujarat",
                district = "Rajkot",
                scannedAt = System.currentTimeMillis()
            )
        }

        val alertsInitial = DiseaseAggregationService.evaluateDensityThreshold(scans80, threshold = 100)
        assertTrue("80 scans should not generate alerts", alertsInitial.isEmpty())

        // Ingest 20 additional scans -> Now crosses 100 threshold
        val additional20 = (81..100).map { i ->
            DiseaseScanRecord(
                id = "sub-$i",
                diseaseName = "Pink Bollworm",
                cropName = "Cotton",
                state = "Gujarat",
                district = "Surat",
                scannedAt = System.currentTimeMillis()
            )
        }

        val alertsFinal = DiseaseAggregationService.evaluateDensityThreshold(scans80 + additional20, threshold = 100)
        assertFalse("100 scans must trigger alerts", alertsFinal.isEmpty())
        val epicenter = alertsFinal.find { it.alertType == "EPICENTER" }
        assertNotNull(epicenter)
        assertEquals(100, epicenter?.scanCount)
    }

    // =========================================================================
    // TIER 4: END-TO-END TELEMETRY TO MARKET PRICE IMPACT INTEGRATION FLOW
    // =========================================================================

    @Test
    fun testEndToEndTelemetryToMarketForecastFlow() {
        // Scenario: 110 Tomato Late Blight scans diagnosed in Karnataka (Kolar belt)
        val incomingScans = (1..110).map { i ->
            DiseaseScanRecord(
                id = "telemetry-tlb-$i",
                diseaseName = "Tomato Late Blight",
                cropName = "Tomato",
                state = "Karnataka",
                district = if (i % 2 == 0) "Kolar" else "Chikkaballapur",
                latitude = 13.1367 + (i * 0.001),
                longitude = 78.1291 + (i * 0.001),
                severity = "High",
                confidence = 95,
                scannedAt = System.currentTimeMillis() - TimeUnit.HOURS.toMillis(i.toLong() % 48)
            )
        }

        // 1. Aggregation Engine Evaluates Outbreak
        val generatedAlerts = DiseaseAggregationService.evaluateDensityThreshold(incomingScans, threshold = 100)
        assertTrue(generatedAlerts.isNotEmpty())

        val epicenterAlert = generatedAlerts.find { it.alertType == "EPICENTER" && it.targetState == "Karnataka" }
        assertNotNull("Epicenter alert must be generated for Karnataka", epicenterAlert)

        val apNeighborAlert = generatedAlerts.find { it.alertType == "EARLY_WARNING" && it.targetState == "Andhra Pradesh" }
        assertNotNull("Andhra Pradesh must receive Early Warning alert", apNeighborAlert)

        // 2. Market Impact Calculation at Epicenter (Kolar Mandi, Karnataka)
        // Crop: Tomato (perishability 1.40), Severity: MODERATE (beta 0.12 for 110 scans), D: 1.0, Geo: 1.0
        // deltaPct = 0.12 * 1.40 * 1.0 * 1.0 * 100 = 16.8%
        val kolarImpact = MarketImpactCalculator.calculateImpact(
            alert = epicenterAlert!!,
            currentModalPrice = 1800.0,
            targetState = "Karnataka",
            targetMandi = "Kolar APMC",
            stage = OutbreakStage.SUPPLY_CONTRACTION
        )

        assertEquals("Tomato", kolarImpact.cropName)
        assertEquals(16.8, kolarImpact.deltaPercentage, 0.1)
        assertEquals(2102.4, kolarImpact.predictedModalPrice, 1.0)
        assertEquals(302.4, kolarImpact.priceDelta, 1.0)
        assertEquals(ImpactDirection.SURGE, kolarImpact.direction)
        assertEquals(MarketRiskLevel.HIGH, kolarImpact.riskLevel)
        assertEquals(ImpactMechanism.SUPPLY_CONTRACTION, kolarImpact.mechanism)
        assertEquals(3, kolarImpact.estimatedPeakDays)

        // 3. Market Impact Calculation at Neighbor State (Madanapalle Mandi, Andhra Pradesh)
        // Neighbor geoMultiplier = 0.70 -> deltaPct = 0.12 * 1.40 * 1.0 * 0.70 * 100 = 11.76%
        val apImpact = MarketImpactCalculator.calculateImpact(
            alert = apNeighborAlert!!,
            currentModalPrice = 1900.0,
            targetState = "Andhra Pradesh",
            targetMandi = "Madanapalle APMC",
            stage = OutbreakStage.SUPPLY_CONTRACTION
        )

        assertEquals("Tomato", apImpact.cropName)
        assertEquals(11.76, apImpact.deltaPercentage, 0.1)
        assertEquals(2123.44, apImpact.predictedModalPrice, 1.0)
        assertEquals(223.44, apImpact.priceDelta, 1.0)
        assertEquals(ImpactDirection.SURGE, apImpact.direction)
        assertEquals(MarketRiskLevel.MODERATE, apImpact.riskLevel)
        assertEquals(ImpactMechanism.REGIONAL_ARBITRAGE, apImpact.mechanism)

        // 4. Validate Repository Integration and Caching
        MarketImpactRepository.clearCache()
        val repoImpact = MarketImpactRepository.calculateImpact(
            alert = epicenterAlert,
            currentModalPrice = 1800.0,
            targetState = "Karnataka",
            targetMandi = "Kolar APMC",
            stage = OutbreakStage.SUPPLY_CONTRACTION
        )
        assertEquals(kolarImpact.predictedModalPrice, repoImpact.predictedModalPrice, 0.01)

        // 5. Final JSON Serialization Roundtrip for Client API Response
        val responseJson = json.encodeToString(kolarImpact)
        val decodedResponse = json.decodeFromString<MarketPriceImpact>(responseJson)
        assertEquals(kolarImpact.predictedModalPrice, decodedResponse.predictedModalPrice, 0.01)
        assertEquals(kolarImpact.mechanism, decodedResponse.mechanism)
        assertEquals(kolarImpact.riskLevel, decodedResponse.riskLevel)
    }
}
