package com.example

import com.example.model.DiseaseScanRecord
import com.example.model.OutbreakAlert
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import java.util.concurrent.TimeUnit

/**
 * Comprehensive 4-Tier Test Suite for Disease Aggregation, Outbreak Density Threshold Evaluation,
 * and Trans-boundary Neighbor Early Warning Alert Generation.
 */
class DiseaseAggregationTest {

    // =========================================================================
    // TIER 1: CORE FEATURE TESTS (Happy Path & Fundamental Contracts)
    // =========================================================================

    @Test
    fun testEpicenterAlertGenerationAtThreshold() {
        // 100 scans for Fall Armyworm in Maharashtra crossing 100-density threshold
        val scans = (1..100).map { i ->
            DiseaseScanRecord(
                id = "scan-mh-$i",
                diseaseName = "Fall Armyworm",
                cropName = "Maize",
                state = "Maharashtra",
                district = if (i % 2 == 0) "Nashik" else "Pune",
                scannedAt = System.currentTimeMillis() - TimeUnit.HOURS.toMillis(i.toLong() % 24)
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(scans, threshold = 100)

        // Find Epicenter Alert
        val epicenter = alerts.find { it.alertType == "EPICENTER" && it.targetState == "Maharashtra" }
        assertNotNull("Epicenter alert must be generated for Maharashtra", epicenter)
        epicenter?.let {
            assertEquals("Fall Armyworm", it.diseaseName)
            assertEquals("Maharashtra", it.sourceState)
            assertEquals("Maharashtra", it.targetState)
            assertEquals("MODERATE", it.severity)
            assertEquals(100, it.scanCount)
            assertEquals(100, it.thresholdDensity)
            assertEquals(15.0, it.predictedMarketImpactPct, 0.01)
            assertTrue(it.isActive)
            assertTrue(it.message.contains("CRITICAL OUTBREAK DETECTED"))
            assertTrue(it.recommendedAction.contains("quarantine affected fields"))
        }
    }

    @Test
    fun testNeighborEarlyWarningFanOut() {
        // 100 scans in Maharashtra should fan out early warnings to all adjacent states
        val scans = (1..100).map { i ->
            DiseaseScanRecord(
                id = "scan-mh-$i",
                diseaseName = "Fall Armyworm",
                cropName = "Maize",
                state = "Maharashtra",
                district = "Aurangabad",
                scannedAt = System.currentTimeMillis() - TimeUnit.HOURS.toMillis(i.toLong() % 12)
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(scans, threshold = 100)
        val earlyWarnings = alerts.filter { it.alertType == "EARLY_WARNING" }

        val expectedNeighbors = listOf(
            "Gujarat",
            "Madhya Pradesh",
            "Chhattisgarh",
            "Telangana",
            "Karnataka",
            "Goa",
            "Dadra and Nagar Haveli and Daman and Diu"
        )

        assertEquals("Should generate early warnings for all 7 neighboring states", 7, earlyWarnings.size)
        val targetStates = earlyWarnings.map { it.targetState }.toSet()

        for (neighbor in expectedNeighbors) {
            assertTrue("Target states must contain $neighbor", targetStates.contains(neighbor))
            val alert = earlyWarnings.find { it.targetState == neighbor }
            assertNotNull(alert)
            assertEquals("Maharashtra", alert?.sourceState)
            assertEquals("Fall Armyworm", alert?.diseaseName)
            assertEquals("MODERATE", alert?.severity)
            assertEquals(8.0, alert?.predictedMarketImpactPct ?: 0.0, 0.01)
            assertTrue(alert?.isActive == true)
            assertTrue(alert?.message?.contains("EARLY WARNING: Outbreak of Fall Armyworm detected in neighboring Maharashtra") == true)
        }
    }

    @Test
    fun testHighSeverityScalingAt200Scans() {
        // 200 scans should upgrade severity to HIGH (Epicenter impact 25%, Neighbor impact 15%)
        val scans = (1..200).map { i ->
            DiseaseScanRecord(
                id = "scan-pb-$i",
                diseaseName = "Yellow Rust",
                cropName = "Wheat",
                state = "Punjab",
                district = "Ludhiana",
                scannedAt = System.currentTimeMillis() - TimeUnit.MINUTES.toMillis(i.toLong())
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(scans, threshold = 100)
        val epicenter = alerts.find { it.alertType == "EPICENTER" && it.targetState == "Punjab" }
        val neighborAlert = alerts.find { it.alertType == "EARLY_WARNING" && it.targetState == "Haryana" }

        assertNotNull(epicenter)
        assertEquals("HIGH", epicenter?.severity)
        assertEquals(25.0, epicenter?.predictedMarketImpactPct ?: 0.0, 0.01)

        assertNotNull(neighborAlert)
        assertEquals("MODERATE", neighborAlert?.severity)
        assertEquals(15.0, neighborAlert?.predictedMarketImpactPct ?: 0.0, 0.01)
    }

    @Test
    fun testCriticalSeverityScalingAt300PlusScans() {
        // 350 scans should upgrade severity to CRITICAL (Epicenter impact 35%, Neighbor impact 20%, neighbor severity HIGH)
        val scans = (1..350).map { i ->
            DiseaseScanRecord(
                id = "scan-ka-$i",
                diseaseName = "Tomato Late Blight",
                cropName = "Tomato",
                state = "Karnataka",
                district = "Kolar",
                scannedAt = System.currentTimeMillis() - TimeUnit.MINUTES.toMillis(i.toLong())
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(scans, threshold = 100)
        val epicenter = alerts.find { it.alertType == "EPICENTER" && it.targetState == "Karnataka" }
        val neighborAlert = alerts.find { it.alertType == "EARLY_WARNING" && it.targetState == "Tamil Nadu" }

        assertNotNull(epicenter)
        assertEquals("CRITICAL", epicenter?.severity)
        assertEquals(35.0, epicenter?.predictedMarketImpactPct ?: 0.0, 0.01)
        assertEquals(350, epicenter?.scanCount)

        assertNotNull(neighborAlert)
        assertEquals("HIGH", neighborAlert?.severity)
        assertEquals(20.0, neighborAlert?.predictedMarketImpactPct ?: 0.0, 0.01)
        assertEquals(350, neighborAlert?.scanCount)
    }

    @Test
    fun testStateAdjacencyLookupBasics() {
        val punjabNeighbors = DiseaseAggregationService.StateAdjacencyGraph.getNeighbors("Punjab")
        assertTrue(punjabNeighbors.contains("Haryana"))
        assertTrue(punjabNeighbors.contains("Himachal Pradesh"))
        assertTrue(punjabNeighbors.contains("Rajasthan"))
        assertTrue(punjabNeighbors.contains("Jammu and Kashmir"))
        assertTrue(punjabNeighbors.contains("Chandigarh"))
        assertEquals(5, punjabNeighbors.size)

        assertTrue(DiseaseAggregationService.StateAdjacencyGraph.areNeighbors("Punjab", "Haryana"))
        assertFalse(DiseaseAggregationService.StateAdjacencyGraph.areNeighbors("Punjab", "Kerala"))
        assertFalse(DiseaseAggregationService.StateAdjacencyGraph.areNeighbors("Punjab", "Assam"))
    }

    // =========================================================================
    // TIER 2: BOUNDARY VALUE ANALYSIS & CORNER CASE TESTS
    // =========================================================================

    @Test
    fun testEmptyScansListReturnsEmptyAlerts() {
        val alerts = DiseaseAggregationService.evaluateDensityThreshold(emptyList())
        assertTrue("Empty scans must return empty alerts list", alerts.isEmpty())
    }

    @Test
    fun testSubThreshold99ScansGeneratesNoAlert() {
        // Boundary test: Exactly 99 scans (< 100) must NOT trigger any alert
        val scans = (1..99).map { i ->
            DiseaseScanRecord(
                id = "scan-sub-$i",
                diseaseName = "Pink Bollworm",
                cropName = "Cotton",
                state = "Gujarat",
                district = "Rajkot",
                scannedAt = System.currentTimeMillis()
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(scans, threshold = 100)
        assertTrue("99 scans should not cross the 100 threshold", alerts.isEmpty())
    }

    @Test
    fun testExactThreshold100ScansTriggersAlert() {
        // Boundary test: Exactly 100 scans (== 100) must trigger alerts
        val scans = (1..100).map { i ->
            DiseaseScanRecord(
                id = "scan-exact-$i",
                diseaseName = "Pink Bollworm",
                cropName = "Cotton",
                state = "Gujarat",
                district = "Rajkot",
                scannedAt = System.currentTimeMillis()
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(scans, threshold = 100)
        assertFalse("100 scans must trigger alerts", alerts.isEmpty())
        val epicenter = alerts.find { it.alertType == "EPICENTER" }
        assertNotNull(epicenter)
        assertEquals(100, epicenter?.scanCount)
    }

    @Test
    fun testAboveThreshold101ScansPreservesAccurateCount() {
        val scans = (1..101).map { i ->
            DiseaseScanRecord(
                id = "scan-above-$i",
                diseaseName = "Pink Bollworm",
                cropName = "Cotton",
                state = "Gujarat",
                district = "Rajkot",
                scannedAt = System.currentTimeMillis()
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(scans, threshold = 100)
        val epicenter = alerts.find { it.alertType == "EPICENTER" }
        assertNotNull(epicenter)
        assertEquals(101, epicenter?.scanCount)
    }

    @Test
    fun testTimestampExpiryBeyond168HoursExcluded() {
        val now = System.currentTimeMillis()
        val expiredTime = now - TimeUnit.HOURS.toMillis(200) // 200 hours ago (> 168 hours)
        val freshTime = now - TimeUnit.HOURS.toMillis(10)     // 10 hours ago

        // 60 expired scans + 50 fresh scans = 110 total scans, but only 50 in 168h window
        val expiredScans = (1..60).map { i ->
            DiseaseScanRecord(
                id = "scan-old-$i",
                diseaseName = "Stem Rot",
                cropName = "Soybean",
                state = "Madhya Pradesh",
                district = "Indore",
                scannedAt = expiredTime
            )
        }

        val freshScans = (1..50).map { i ->
            DiseaseScanRecord(
                id = "scan-fresh-$i",
                diseaseName = "Stem Rot",
                cropName = "Soybean",
                state = "Madhya Pradesh",
                district = "Indore",
                scannedAt = freshTime
            )
        }

        val combinedScans = expiredScans + freshScans
        val alerts = DiseaseAggregationService.evaluateDensityThreshold(combinedScans, threshold = 100, windowHours = 168)

        // Only 50 scans inside the 168h rolling window -> No alert
        assertTrue("Scans older than 168 hours must be excluded from density threshold", alerts.isEmpty())
    }

    @Test
    fun testTimestampFilterIncludesSufficientRecentScans() {
        val now = System.currentTimeMillis()
        val expiredTime = now - TimeUnit.HOURS.toMillis(300)
        val freshTime = now - TimeUnit.HOURS.toMillis(24)

        // 50 expired scans + 100 fresh scans = 150 total, 100 recent
        val expiredScans = (1..50).map { i ->
            DiseaseScanRecord(
                id = "scan-old-$i",
                diseaseName = "Stem Rot",
                cropName = "Soybean",
                state = "Madhya Pradesh",
                district = "Indore",
                scannedAt = expiredTime
            )
        }

        val freshScans = (1..100).map { i ->
            DiseaseScanRecord(
                id = "scan-fresh-$i",
                diseaseName = "Stem Rot",
                cropName = "Soybean",
                state = "Madhya Pradesh",
                district = "Indore",
                scannedAt = freshTime
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(expiredScans + freshScans, threshold = 100)
        val epicenter = alerts.find { it.alertType == "EPICENTER" }
        assertNotNull("Should trigger alert with exactly 100 recent scans", epicenter)
        assertEquals(100, epicenter?.scanCount)
    }

    @Test
    fun testZeroTimestampTreatedAsRecent() {
        // Scans with scannedAt == 0L represent fallback/legacy records that should not be dropped
        val scans = (1..100).map { i ->
            DiseaseScanRecord(
                id = "scan-zero-$i",
                diseaseName = "Leaf Blast",
                cropName = "Rice",
                state = "Andhra Pradesh",
                district = "Guntur",
                scannedAt = 0L
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(scans, threshold = 100)
        val epicenter = alerts.find { it.alertType == "EPICENTER" }
        assertNotNull(epicenter)
        assertEquals(100, epicenter?.scanCount)
    }

    @Test
    fun testMixedDiseaseSegregationInSameState() {
        // 100 scans of Fall Armyworm and 99 scans of Pink Bollworm in Maharashtra
        val faScans = (1..100).map { i ->
            DiseaseScanRecord(
                id = "fa-$i",
                diseaseName = "Fall Armyworm",
                cropName = "Maize",
                state = "Maharashtra",
                district = "Pune",
                scannedAt = System.currentTimeMillis()
            )
        }

        val pbScans = (1..99).map { i ->
            DiseaseScanRecord(
                id = "pb-$i",
                diseaseName = "Pink Bollworm",
                cropName = "Cotton",
                state = "Maharashtra",
                district = "Akola",
                scannedAt = System.currentTimeMillis()
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(faScans + pbScans, threshold = 100)

        // Only Fall Armyworm should have triggered alerts
        val faAlerts = alerts.filter { it.diseaseName == "Fall Armyworm" }
        val pbAlerts = alerts.filter { it.diseaseName == "Pink Bollworm" }

        assertTrue("Fall Armyworm should trigger alerts", faAlerts.isNotEmpty())
        assertTrue("Pink Bollworm with 99 scans must not trigger alerts", pbAlerts.isEmpty())
    }

    @Test
    fun testBlankOrWhitespaceDiseaseAndStateIgnored() {
        val blankScans = (1..120).map { i ->
            DiseaseScanRecord(
                id = "blank-$i",
                diseaseName = if (i % 2 == 0) "" else "   ",
                cropName = "General",
                state = "Maharashtra",
                scannedAt = System.currentTimeMillis()
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(blankScans, threshold = 100)
        assertTrue("Blank disease names must not generate alerts", alerts.isEmpty())
    }

    @Test
    fun testCaseInsensitiveStateAdjacencyMatching() {
        val neighborsLower = DiseaseAggregationService.StateAdjacencyGraph.getNeighbors("maharashtra")
        val neighborsUpper = DiseaseAggregationService.StateAdjacencyGraph.getNeighbors("MAHARASHTRA")
        val neighborsPadded = DiseaseAggregationService.StateAdjacencyGraph.getNeighbors("  Maharashtra  ")

        assertEquals(7, neighborsLower.size)
        assertEquals(neighborsLower, neighborsUpper)
        assertEquals(neighborsLower, neighborsPadded)
    }

    // =========================================================================
    // TIER 3: CROSS-FEATURE & TOPOLOGICAL TESTS
    // =========================================================================

    @Test
    fun testConcurrentMultiStateOutbreaks() {
        // Outbreak 1: 120 scans of Fall Armyworm in Maharashtra (1 Epicenter + 7 Neighbors = 8 alerts)
        val mhScans = (1..120).map { i ->
            DiseaseScanRecord(
                id = "mh-$i",
                diseaseName = "Fall Armyworm",
                cropName = "Maize",
                state = "Maharashtra",
                scannedAt = System.currentTimeMillis()
            )
        }

        // Outbreak 2: 150 scans of Yellow Rust in Punjab (1 Epicenter + 5 Neighbors = 6 alerts)
        val pbScans = (1..150).map { i ->
            DiseaseScanRecord(
                id = "pb-$i",
                diseaseName = "Yellow Rust",
                cropName = "Wheat",
                state = "Punjab",
                scannedAt = System.currentTimeMillis()
            )
        }

        // Outbreak 3: 250 scans of Late Blight in Uttar Pradesh (1 Epicenter + 9 Neighbors = 10 alerts)
        val upScans = (1..250).map { i ->
            DiseaseScanRecord(
                id = "up-$i",
                diseaseName = "Potato Late Blight",
                cropName = "Potato",
                state = "Uttar Pradesh",
                scannedAt = System.currentTimeMillis()
            )
        }

        val allScans = mhScans + pbScans + upScans
        val alerts = DiseaseAggregationService.evaluateDensityThreshold(allScans, threshold = 100)

        assertEquals("Total generated alerts should be 8 + 6 + 10 = 24", 24, alerts.size)

        val faAlerts = alerts.filter { it.diseaseName == "Fall Armyworm" }
        val yrAlerts = alerts.filter { it.diseaseName == "Yellow Rust" }
        val lbAlerts = alerts.filter { it.diseaseName == "Potato Late Blight" }

        assertEquals(8, faAlerts.size)
        assertEquals(6, yrAlerts.size)
        assertEquals(10, lbAlerts.size)
    }

    @Test
    fun testStateAdjacencyGraphSymmetry() {
        val allStates = DiseaseAggregationService.StateAdjacencyGraph.getAllStates()
        assertTrue("Adjacency graph must contain all major Indian states", allStates.size >= 30)

        for (state in allStates) {
            val neighbors = DiseaseAggregationService.StateAdjacencyGraph.getNeighbors(state)
            assertNotNull("Neighbor list should not be null for $state", neighbors)
            assertFalse("Neighbor list should not be empty for $state", neighbors.isEmpty())

            for (neighbor in neighbors) {
                val reverseNeighbors = DiseaseAggregationService.StateAdjacencyGraph.getNeighbors(neighbor)
                assertTrue(
                    "Adjacency graph must be symmetric: $state is neighbor of $neighbor, so $neighbor must have $state as neighbor",
                    reverseNeighbors.any { it.equals(state, ignoreCase = true) }
                )
                assertTrue(
                    "areNeighbors($state, $neighbor) must equal areNeighbors($neighbor, $state)",
                    DiseaseAggregationService.StateAdjacencyGraph.areNeighbors(state, neighbor) &&
                            DiseaseAggregationService.StateAdjacencyGraph.areNeighbors(neighbor, state)
                )
            }
        }
    }

    @Test
    fun testCustomThresholdAndWindowParameters() {
        val now = System.currentTimeMillis()
        // 50 scans within 48 hours
        val scans = (1..50).map { i ->
            DiseaseScanRecord(
                id = "scan-custom-$i",
                diseaseName = "Chilli Leaf Curl",
                cropName = "Chilli",
                state = "Andhra Pradesh",
                district = "Guntur",
                scannedAt = now - TimeUnit.HOURS.toMillis(i.toLong() % 48)
            )
        }

        // Custom threshold = 50, window = 72 hours
        val alerts = DiseaseAggregationService.evaluateDensityThreshold(scans, threshold = 50, windowHours = 72)
        val epicenter = alerts.find { it.alertType == "EPICENTER" }
        assertNotNull("Should trigger alert with custom threshold = 50", epicenter)
        assertEquals(50, epicenter?.scanCount)
        assertEquals(50, epicenter?.thresholdDensity)
        assertEquals(72, epicenter?.timeWindowHours)
    }

    // =========================================================================
    // TIER 4: REAL-WORLD AGRICULTURAL EPIDEMIC SCENARIOS
    // =========================================================================

    @Test
    fun testFallArmywormEpidemicInMaharashtra() {
        // Real-world scenario: 320 Fall Armyworm scans across Vidarbha/Marathwada in Maharashtra
        val districts = listOf("Nashik", "Pune", "Ahmednagar", "Solapur", "Kolhapur", "Satara", "Jalgaon", "Aurangabad", "Beed", "Nanded")
        val scans = (1..320).map { i ->
            DiseaseScanRecord(
                id = "fa-mh-$i",
                diseaseName = "Fall Armyworm (Spodoptera frugiperda)",
                cropName = "Maize / Corn",
                state = "Maharashtra",
                district = districts[i % districts.size],
                latitude = 18.5204 + (i * 0.01),
                longitude = 73.8567 + (i * 0.01),
                severity = if (i % 3 == 0) "Critical" else "High",
                confidence = 92 + (i % 8),
                scannedAt = System.currentTimeMillis() - TimeUnit.HOURS.toMillis(i.toLong() % 120)
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(scans, threshold = 100)

        // 1. Epicenter in Maharashtra
        val epicenter = alerts.find { it.alertType == "EPICENTER" && it.targetState == "Maharashtra" }
        assertNotNull("Epicenter alert must exist for Maharashtra", epicenter)
        assertEquals("CRITICAL", epicenter?.severity)
        assertEquals(320, epicenter?.scanCount)
        assertEquals(35.0, epicenter?.predictedMarketImpactPct ?: 0.0, 0.01)

        // 2. Early Warning Fan-out
        val neighbors = alerts.filter { it.alertType == "EARLY_WARNING" }
        assertEquals(7, neighbors.size)

        // Check Madhya Pradesh early warning specifically
        val mpAlert = neighbors.find { it.targetState == "Madhya Pradesh" }
        assertNotNull("Madhya Pradesh must receive early warning", mpAlert)
        assertEquals("HIGH", mpAlert?.severity)
        assertEquals(20.0, mpAlert?.predictedMarketImpactPct ?: 0.0, 0.01)
        assertTrue(mpAlert?.message?.contains("Trans-boundary", ignoreCase = true) == true ||
                mpAlert?.message?.contains("trans-boundary", ignoreCase = true) == true)
    }

    @Test
    fun testYellowRustEpidemicInPunjab() {
        // Real-world scenario: 215 Yellow Rust (Puccinia striiformis) scans in Punjab (Sub-Himalayan wheat belt)
        val districts = listOf("Gurdaspur", "Hoshiarpur", "Rupnagar", "Pathankot", "Nawanshahr", "Ludhiana")
        val scans = (1..215).map { i ->
            DiseaseScanRecord(
                id = "yr-pb-$i",
                diseaseName = "Yellow Rust (Puccinia striiformis)",
                cropName = "Wheat",
                state = "Punjab",
                district = districts[i % districts.size],
                latitude = 31.6340 + (i * 0.005),
                longitude = 74.8723 + (i * 0.005),
                severity = "High",
                confidence = 94,
                scannedAt = System.currentTimeMillis() - TimeUnit.HOURS.toMillis(i.toLong() % 72)
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(scans, threshold = 100)

        val epicenter = alerts.find { it.alertType == "EPICENTER" && it.targetState == "Punjab" }
        assertNotNull(epicenter)
        assertEquals("HIGH", epicenter?.severity)
        assertEquals(215, epicenter?.scanCount)
        assertEquals(25.0, epicenter?.predictedMarketImpactPct ?: 0.0, 0.01)

        // Haryana neighbor alert
        val haryanaAlert = alerts.find { it.alertType == "EARLY_WARNING" && it.targetState == "Haryana" }
        assertNotNull("Haryana must receive early warning from Punjab outbreak", haryanaAlert)
        assertEquals("MODERATE", haryanaAlert?.severity)
        assertEquals(15.0, haryanaAlert?.predictedMarketImpactPct ?: 0.0, 0.01)
        assertTrue(haryanaAlert?.recommendedAction?.contains("Inspect border district fields daily") == true)
    }

    @Test
    fun testTomatoLateBlightOutbreakInKolarKarnataka() {
        // Real-world scenario: 110 Tomato Late Blight scans in Karnataka (Kolar/Chikkaballapur belt)
        val scans = (1..110).map { i ->
            DiseaseScanRecord(
                id = "tlb-ka-$i",
                diseaseName = "Tomato Late Blight",
                cropName = "Tomato",
                state = "Karnataka",
                district = if (i % 2 == 0) "Kolar" else "Chikkaballapur",
                scannedAt = System.currentTimeMillis() - TimeUnit.HOURS.toMillis(i.toLong() % 48)
            )
        }

        val alerts = DiseaseAggregationService.evaluateDensityThreshold(scans, threshold = 100)

        val epicenter = alerts.find { it.alertType == "EPICENTER" && it.targetState == "Karnataka" }
        assertNotNull(epicenter)
        assertEquals("MODERATE", epicenter?.severity)
        assertEquals(110, epicenter?.scanCount)
        assertEquals(15.0, epicenter?.predictedMarketImpactPct ?: 0.0, 0.01)

        val earlyWarnings = alerts.filter { it.alertType == "EARLY_WARNING" }
        assertEquals(6, earlyWarnings.size) // Goa, Maharashtra, Telangana, AP, Tamil Nadu, Kerala
        val apWarning = earlyWarnings.find { it.targetState == "Andhra Pradesh" }
        assertNotNull(apWarning)
        assertEquals(8.0, apWarning?.predictedMarketImpactPct ?: 0.0, 0.01)
    }
}
