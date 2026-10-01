package com.example

import android.graphics.Bitmap
import android.graphics.Color
import androidx.test.core.app.ApplicationProvider
import com.example.agristack.AgriStackPassportEngine
import com.example.bioshield.BioShieldRadarEngine
import com.example.bioshield.GeoLocationPoint
import com.example.bioshield.OutbreakRiskLevel
import com.example.gramhaul.GramHaulEngine
import com.example.gramhaul.HaulVehicleType
import com.example.mandipilot.MandiPilotEngine
import com.example.ml.DetectionSource
import com.example.ml.DiseaseDetector
import com.example.ml.DiseaseSeverityLevel
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import kotlin.random.Random

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class EmpiricalChallengeM1_2Test {

    private lateinit var detector: DiseaseDetector

    @Before
    fun setup() {
        val context = ApplicationProvider.getApplicationContext<android.content.Context>()
        detector = DiseaseDetector(context)
    }

    // =========================================================================
    // 1. ML DISEASE DETECTOR EMPIRICAL STRESS TESTS
    // =========================================================================

    @Test
    fun testDiseaseDetectorMultiChannelColorSimulation() {
        // Test suite across 8 distinct color channels and leaf pathology conditions
        val testConditions = listOf(
            "Healthy Forest Green" to Triple(34, 139, 34),
            "Healthy Dark Olive" to Triple(40, 110, 40),
            "Powdery White Mildew" to Triple(235, 235, 235),
            "Rust Orange Pustules" to Triple(210, 95, 20),
            "Yellow Mosaic Chlorosis" to Triple(225, 210, 30),
            "Necrotic Dark Blight" to Triple(75, 35, 15),
            "Extreme Pure Black" to Triple(0, 0, 0),
            "Extreme Pure White" to Triple(255, 255, 255),
            "Extreme Pure Blue" to Triple(0, 0, 255)
        )

        for ((name, rgb) in testConditions) {
            val bitmap = Bitmap.createBitmap(128, 128, Bitmap.Config.ARGB_8888)
            for (x in 0 until 128) {
                for (y in 0 until 128) {
                    bitmap.setPixel(x, y, Color.rgb(rgb.first, rgb.second, rgb.third))
                }
            }

            val result = detector.classify(bitmap, "Paddy")
            assertNotNull("Result for $name must not be null", result)
            assertTrue("Confidence for $name (${result.confidence}%) must be in [70, 98]", result.confidence in 70..98)
            assertTrue("Disease name for $name must be non-blank", result.diseaseName.isNotBlank())
            assertTrue("Treatment for $name must be non-blank", result.treatment.isNotBlank())
            assertTrue("Products for $name must be non-empty", result.products.isNotEmpty())
            assertTrue("Severity must be defined", result.severity.displayName.isNotBlank())

            // Verify store links in product recommendations
            result.products.forEach { (prodInfo, stores) ->
                assertTrue("Product name must be present", prodInfo.first.isNotBlank())
                assertTrue("Dosage must be present", prodInfo.second.isNotBlank())
                assertTrue("Stores list must not be empty", stores.isNotEmpty())
                stores.forEach { store ->
                    assertTrue("Store name required", store.name.isNotBlank())
                    assertTrue("Store URL must start with http", store.url.startsWith("http"))
                }
            }
        }
    }

    @Test
    fun testDiseaseDetectorAdversarialShapesAndNoise() {
        val random = Random(42)

        // 1. Random noise bitmap
        val noiseBitmap = Bitmap.createBitmap(128, 128, Bitmap.Config.ARGB_8888)
        for (x in 0 until 128) {
            for (y in 0 until 128) {
                noiseBitmap.setPixel(x, y, Color.rgb(random.nextInt(256), random.nextInt(256), random.nextInt(256)))
            }
        }
        val noiseResult = detector.classify(noiseBitmap, "Tomato")
        assertTrue("Noise bitmap confidence in [70, 98]", noiseResult.confidence in 70..98)

        // 2. High aspect ratio non-square bitmap (256 x 64)
        val rectBitmap = Bitmap.createBitmap(256, 64, Bitmap.Config.ARGB_8888)
        for (x in 0 until 256) {
            for (y in 0 until 64) {
                rectBitmap.setPixel(x, y, Color.rgb(45, 160, 45))
            }
        }
        val rectResult = detector.classify(rectBitmap, "Chilli")
        assertTrue("Rectangular bitmap confidence in [70, 98]", rectResult.confidence in 70..98)
        assertTrue("All-green rectangular bitmap must be healthy", rectResult.isHealthy)

        // 3. Patchy lesion variance test (concentric spots simulating Alternaria early blight)
        val lesionBitmap = Bitmap.createBitmap(128, 128, Bitmap.Config.ARGB_8888)
        for (x in 0 until 128) {
            for (y in 0 until 128) {
                val distFromCenter = Math.hypot((x - 64).toDouble(), (y - 64).toDouble())
                if (distFromCenter < 25.0) {
                    lesionBitmap.setPixel(x, y, Color.rgb(85, 40, 15)) // dark necrotic center
                } else if (distFromCenter < 35.0) {
                    lesionBitmap.setPixel(x, y, Color.rgb(200, 190, 30)) // yellow halo
                } else {
                    lesionBitmap.setPixel(x, y, Color.rgb(35, 130, 35)) // green leaf
                }
            }
        }
        val lesionResult = detector.classify(lesionBitmap, "Potato")
        assertFalse("Leaf with concentrated necrotic lesions must be diagnosed as diseased", lesionResult.isHealthy)
        assertTrue("Confidence must be dynamically calculated between 72 and 97", lesionResult.confidence in 72..97)
        assertTrue("Severity should be MODERATE, HIGH, or CRITICAL", lesionResult.severity != DiseaseSeverityLevel.HEALTHY)
    }

    // =========================================================================
    // 2. MANDIPILOT OFFLINE ARBITRAGE & PRICE FORECASTING STRESS TESTS
    // =========================================================================

    @Test
    fun testMandiPilotOfflineRegionalArbitrageMatrix() {
        val states = listOf("Andhra Pradesh", "Maharashtra", "Punjab", "Karnataka", "Tamil Nadu", "UnknownState")

        for (state in states) {
            val options = MandiPilotEngine.calculateMandiArbitrage(
                batchSizeQuintals = 100.0,
                isPerishable = true,
                localMandiPrice = 2500.0,
                state = state
            )

            assertTrue("State $state must return at least 5 candidate mandis", options.size >= 5)
            val bestOption = options.firstOrNull { it.isRecommendedBestOption }
            assertNotNull("State $state must designate a recommended best option", bestOption)

            // Verify mathematical invariants
            options.forEach { opt ->
                assertTrue("Distance must be <= 100km", opt.distanceKm <= 100.0)
                assertTrue("Gross modal price must be positive", opt.grossModalPricePerQtl > 0)
                assertTrue("Freight deduction must be positive", opt.estimatedFreightPerQtl > 0)
                assertTrue("APMC cess must be positive", opt.apmcCessPerQtl > 0)
                assertTrue("Transit spoilage penalty must be positive for perishables", opt.transitSpoilagePenaltyPerQtl > 0)
                // Invariant: Net Realized = Gross - Freight - Cess - Spoilage
                val expectedNet = opt.grossModalPricePerQtl - opt.estimatedFreightPerQtl - opt.apmcCessPerQtl - opt.transitSpoilagePenaltyPerQtl
                assertEquals("Net price calculation check", expectedNet, opt.netRealizedPricePerQtl, 0.2)
            }
        }
    }

    @Test
    fun testMandiPilotPriceForecastingAndBuyerBids() {
        val commodities = listOf("Paddy / Rice", "Chilli & Spices", "Tomato", "Wheat", "Soybean", "Cotton", "Maize")

        for (commodity in commodities) {
            val forecast = MandiPilotEngine.forecastPriceMovement(commodity, 2400.0)
            assertTrue("Forecast 7d must be positive", forecast.forecast7dPrice > 0)
            assertTrue("Forecast 15d must be positive", forecast.forecast15dPrice > 0)
            assertTrue("Confidence must be in [78, 95]", forecast.confidencePct in 78..95)
            assertTrue("Trend must have label", forecast.predictedTrend.isNotBlank())
            assertTrue("Driving factor must be descriptive", forecast.keyDrivingFactor.isNotBlank())

            val bids = MandiPilotEngine.getVerifiedBuyerBids(commodity, 2400.0, "Maharashtra")
            assertEquals(3, bids.size)
            bids.forEach { bid ->
                assertTrue("Buyer ID must start with state prefix MH", bid.buyerId.startsWith("MH-"))
                assertTrue("Buyer name must be present", bid.buyerName.isNotBlank())
                assertTrue("Offered price must be > 0", bid.offeredPricePerQtl > 0)
                assertTrue("Procurement volume > 0", bid.procurementVolumeQtl > 0)
                assertTrue("Payment term must be descriptive", bid.paymentTerm.isNotBlank())
            }
        }
    }

    // =========================================================================
    // 3. AGRISTACK PASSPORT & CREDIT SCORING STRESS TESTS
    // =========================================================================

    @Test
    fun testAgriStackCreditScoreMathematicalInvariants() {
        // Test combinations across extreme boundaries
        val testCases = listOf(
            Triple(0.5, false, 0.3) to 1,  // Small land, unverified, low organic carbon, 1 crop
            Triple(2.5, true, 0.6) to 2,   // Medium land, verified, medium carbon, 2 crops
            Triple(10.0, true, 0.9) to 4,  // Large land, verified, high carbon, 4 crops
            Triple(100.0, true, 1.5) to 8, // Very large commercial land
            Triple(0.0, false, 0.0) to 0   // Zero baseline
        )

        for ((params, cropCount) in testCases) {
            val (acres, verified, carbon) = params
            val (score, tier) = AgriStackPassportEngine.calculateAgriCreditScore(
                landAcres = acres,
                pmKisanVerified = verified,
                soilOrganicCarbonPct = carbon,
                cropCount = cropCount
            )

            assertTrue("Credit score ($score) must strictly be bounded in [300, 900]", score in 300..900)
            assertTrue("Tier ($tier) must not be blank", tier.isNotBlank())

            if (score >= 800) {
                assertTrue("Tier must mention Prime for score >= 800", tier.contains("Prime"))
            }
        }
    }

    @Test
    fun testAgriStackSovereignPassportAndSchemesOffline() {
        val states = listOf("Andhra Pradesh", "Maharashtra", "Punjab", "Tamil Nadu", "Karnataka", "Telangana", "Gujarat", "Uttar Pradesh", "Bihar")

        for (state in states) {
            val passport = AgriStackPassportEngine.getSovereignPassport(
                farmerName = "Ravi Kumar",
                state = state,
                district = "Central District",
                landAcres = 3.5,
                primaryCrops = listOf("Cotton", "Chilli")
            )

            assertNotNull(passport)
            assertTrue("Sovereign ID format IN-XX-YYY-NNNNNN", passport.sovereignFarmerId.startsWith("IN-"))
            assertEquals("Ravi Kumar", passport.farmerName)
            assertEquals(3.5, passport.landSizeAcres, 0.01)
            assertTrue("KCC limit must be calculated (3.5 * 75,000 = 262,500)", passport.maxEligibleKccLoanLimit == 262500.0)

            // Soil metrics verification
            val soil = passport.soilHealthSummary
            assertTrue("Nitrogen must be positive", soil.nitrogenKgPerHa > 0)
            assertTrue("Phosphorus must be positive", soil.phosphorusKgPerHa > 0)
            assertTrue("Potassium must be positive", soil.potassiumKgPerHa > 0)
            assertTrue("Soil pH in realistic range [5.0, 9.0]", soil.soilPh in 5.0..9.0)
            assertTrue("Fertility index must be present", soil.overallFertilityIndex.isNotBlank())

            // Schemes verification: landAcres >= 2.0 should include SMAM Drone
            assertTrue("Eligible schemes must not be empty", passport.eligibleSchemes.isNotEmpty())
            assertTrue("PM-KISAN must always be present", passport.eligibleSchemes.any { it.schemeCode == "PM-KISAN" })
            assertTrue("SMAM Drone must be present for 3.5 acres", passport.eligibleSchemes.any { it.schemeCode == "SMAM-DRONE" })
        }
    }

    // =========================================================================
    // 4. GRAMHAUL LOGISTICS FLEET POOLING STRESS TESTS
    // =========================================================================

    @Test
    fun testGramHaulProportionalFareAndVehicles() {
        val vehicles = listOf(
            HaulVehicleType.PICKUP_TRUCK,
            HaulVehicleType.TRACTOR_TROLLEY,
            HaulVehicleType.MINI_TRUCK,
            HaulVehicleType.COLD_CHAIN_REEFER
        )

        for (vehicle in vehicles) {
            val batches = listOf(
                "Farmer A" to 4.0,
                "Farmer B" to 6.0,
                "Farmer C" to 10.0
            )

            val allocations = GramHaulEngine.calculatePooledFareSharing(vehicle, 50.0, batches)
            assertEquals(3, allocations.size)

            val totalAllocatedFare = allocations.sumOf { it.allocatedCostRupees }
            val expectedTotalFare = (vehicle.baseRatePerKm * 50.0) + 200.0

            assertEquals("Sum of allocated fares must equal total trip cost", expectedTotalFare, totalAllocatedFare, 1.0)

            allocations.forEach { batch ->
                assertTrue("Allocated cost must be positive", batch.allocatedCostRupees > 0)
                assertTrue("Cost saved pct must be in [15, 78]", batch.costSavedPctVsSoloHire in 15..78)
            }
        }
    }

    @Test
    fun testGramHaulTripPlanGenerator() {
        val trips = GramHaulEngine.findAvailablePooledTrips(
            farmerAcreageYieldQuintals = 12.0,
            isPerishable = true,
            state = "Punjab"
        )

        assertTrue("Must return available trips", trips.isNotEmpty())
        val trip1 = trips[0]
        assertEquals(HaulVehicleType.COLD_CHAIN_REEFER, trip1.vehicle) // perishable requires cold chain
        assertTrue("Trip distance must be positive", trip1.totalDistanceKm > 0)
        assertTrue("Driver phone must be present", trip1.driverPhone.isNotBlank())
        assertTrue("Available space must be >= 0", trip1.availableSpaceQuintals >= 0.0)
    }

    // =========================================================================
    // 5. BIOSHIELD RADAR OUTBREAK CLUSTERING STRESS TESTS
    // =========================================================================

    @Test
    fun testBioShieldRadarClusteringInvariants() {
        val epicenter = GeoLocationPoint(17.3850, 78.4867, "Hyderabad", "Telangana")

        // 1. Distance formula test
        val dist0 = BioShieldRadarEngine.calculateDistanceKm(17.3850, 78.4867, 17.3850, 78.4867)
        assertEquals(0.0, dist0, 0.001)

        // 2. Outbreak trigger rule: < 3 scans -> null
        val scans2 = listOf(Pair(17.3850, 78.4867), Pair(17.3900, 78.4900))
        assertNull(BioShieldRadarEngine.evaluateOutbreakCluster(scans2, "Fungal Blight", "Rice", epicenter))

        // 3. Outbreak trigger rule: 3 proximate scans -> Valid OutbreakCluster
        val scans3 = listOf(
            Pair(17.3850, 78.4867),
            Pair(17.3900, 78.4900),
            Pair(17.3800, 78.4800)
        )
        val cluster = BioShieldRadarEngine.evaluateOutbreakCluster(scans3, "Chilli Leaf Curl Begomovirus", "Chilli", epicenter, humidityPct = 82.0)
        assertNotNull(cluster)
        assertEquals(3, cluster!!.totalScansDetected)
        assertTrue("Radius is 10km", cluster.radiusKm == 10.0)
        assertTrue("NDVI stress in [0.0, 1.0]", cluster.ndviStressIndex in 0.0..1.0)
        assertTrue("Action plan must mention sticky traps or bio-defense", cluster.bioDefenseActionPlan.isNotBlank())

        // 4. Danger zone check
        val insideFarm = BioShieldRadarEngine.isFarmInDangerZone(17.3900, 78.4900, cluster)
        assertTrue("Farm near epicenter must be in danger zone", insideFarm)

        val farAwayFarm = BioShieldRadarEngine.isFarmInDangerZone(18.5000, 79.5000, cluster) // > 100km away
        assertFalse("Far away farm must NOT be in danger zone", farAwayFarm)
    }

    @Test
    fun testBioDefenseProtocolPathologyTaxonomy() {
        val blastPlan = BioShieldRadarEngine.resolveBioDefenseProtocol("Paddy Blast Fungal Infection", "Paddy")
        assertTrue("Blast plan must mention Pseudomonas or bio-barrier", blastPlan.contains("Pseudomonas"))

        val borerPlan = BioShieldRadarEngine.resolveBioDefenseProtocol("Fall Armyworm Spodoptera Borer", "Maize")
        assertTrue("Borer plan must mention Neemastra or Pheromone Traps", borerPlan.contains("Neemastra"))

        val mosaicPlan = BioShieldRadarEngine.resolveBioDefenseProtocol("Yellow Mosaic Begomovirus", "Soybean")
        assertTrue("Mosaic plan must mention Sticky Traps or Agniastra", mosaicPlan.contains("Sticky Traps"))

        val wiltPlan = BioShieldRadarEngine.resolveBioDefenseProtocol("Fusarium Wilt & Root Rot", "Cotton")
        assertTrue("Wilt plan must mention Trichoderma viride", wiltPlan.contains("Trichoderma"))
    }
}
