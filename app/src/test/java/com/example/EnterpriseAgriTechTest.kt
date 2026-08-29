package com.example

import com.example.agristack.AgriStackPassportEngine
import com.example.biorx.BioRxEngine
import com.example.biorx.OrganicFormulationType
import com.example.bioshield.BioShieldRadarEngine
import com.example.bioshield.GeoLocationPoint
import com.example.gramhaul.GramHaulEngine
import com.example.gramhaul.HaulVehicleType
import com.example.mandipilot.MandiPilotEngine
import com.example.voice.FarmVoiceContext
import com.example.voice.IndicLanguage
import com.example.voice.VoiceOsEngine
import com.example.yantra.EscrowStatus
import com.example.yantra.YantraShareEngine
import kotlinx.coroutines.runBlocking
import org.junit.Assert.*
import org.junit.Test

class EnterpriseAgriTechTest {

    @Test
    fun testVoiceOsSub800msResponseAndMultilingualIntent() = runBlocking {
        val result = VoiceOsEngine.processSpeechQuery(
            rawTranscript = "What is the price of paddy in Guntur Mandi today?",
            language = IndicLanguage.ENGLISH,
            farmContext = FarmVoiceContext()
        )
        assertNotNull(result)
        assertEquals("MANDI_ARBITRAGE", result.intentCategory)
        assertTrue("Latency should be sub-800ms", result.latencyMs < 800)
        assertTrue("Answer should contain price details", result.actionableAnswer.contains("2,850"))

        // Test Telugu voice intent
        val teluguResult = VoiceOsEngine.processSpeechQuery(
            rawTranscript = "వరి తెగులు మందు ఏమిటి?",
            language = IndicLanguage.TELUGU,
            farmContext = FarmVoiceContext()
        )
        assertEquals("DIAGNOSTIC_PRESCRIPTION", teluguResult.intentCategory)
        assertTrue(teluguResult.latencyMs < 800)
    }

    @Test
    fun testBioShieldOutbreakClusterThreshold() {
        val epicenter = GeoLocationPoint(16.3067, 80.4365, "Guntur", "Andhra Pradesh")

        // 1. Less than 3 scans within 10km -> No cluster triggered
        val belowThresholdScans = listOf(
            Pair(16.3067, 80.4365),
            Pair(16.3120, 80.4410)
        )
        val noCluster = BioShieldRadarEngine.evaluateOutbreakCluster(
            belowThresholdScans, "Paddy Blast", "Rice", epicenter
        )
        assertNull("Cluster should NOT trigger for < 3 scans", noCluster)

        // 2. Exactly 4 scans within 10km -> Cluster triggered
        val validClusterScans = listOf(
            Pair(16.3067, 80.4365),
            Pair(16.3120, 80.4410),
            Pair(16.2990, 80.4300),
            Pair(16.3200, 80.4500)
        )
        val cluster = BioShieldRadarEngine.evaluateOutbreakCluster(
            validClusterScans, "Paddy Blast Fungal Blight", "Paddy / Rice", epicenter, humidityPct = 88.0
        )
        assertNotNull("Cluster MUST trigger for >= 3 scans", cluster)
        assertEquals(4, cluster!!.totalScansDetected)
        assertTrue("NDVI stress index should be computed", cluster.ndviStressIndex in 0.0..1.0)
        assertTrue("Bio defense plan should be provided", cluster.bioDefenseActionPlan.isNotBlank())
    }

    @Test
    fun testMandiPilotArbitrageAcrossAtLeast5Mandis() {
        val options = MandiPilotEngine.calculateMandiArbitrage(batchSizeQuintals = 50.0, isPerishable = false)

        assertTrue("Should evaluate at least 5 mandis within 100km", options.size >= 5)
        val best = options.firstOrNull { it.isRecommendedBestOption }
        assertNotNull("Should have an optimal recommended option", best)

        // Verify fee deductions (freight, APMC cess, spoilage)
        options.forEach { opt ->
            assertTrue("Freight should be deducted", opt.estimatedFreightPerQtl > 0.0)
            assertTrue("APMC cess should be deducted", opt.apmcCessPerQtl > 0.0)
            assertTrue("Net price must equal gross minus deductions",
                opt.netRealizedPricePerQtl <= opt.grossModalPricePerQtl
            )
            assertTrue("Distance must be within 100km", opt.distanceKm <= 100.0)
        }
    }

    @Test
    fun testGramHaulSharedLogisticsCostAllocation() {
        val batches = listOf(
            "Farmer Ramesh" to 10.0,
            "Farmer Suresh" to 15.0,
            "Farmer Anil" to 5.0
        )
        val vehicle = HaulVehicleType.TRACTOR_TROLLEY
        val allocations = GramHaulEngine.calculatePooledFareSharing(vehicle, 30.0, batches)

        assertEquals(3, allocations.size)
        // Suresh has 50% of the weight (15/30), should pay half the total fare
        val suresh = allocations.first { it.farmerName == "Farmer Suresh" }
        val ramesh = allocations.first { it.farmerName == "Farmer Ramesh" }
        val anil = allocations.first { it.farmerName == "Farmer Anil" }

        assertTrue(suresh.allocatedCostRupees > ramesh.allocatedCostRupees)
        assertTrue(ramesh.allocatedCostRupees > anil.allocatedCostRupees)
        assertTrue("Proportional savings should be positive", suresh.costSavedPctVsSoloHire > 0)
    }

    @Test
    fun testAgriStackPassportAndCreditScoreGeneration() {
        val (score, tier) = AgriStackPassportEngine.calculateAgriCreditScore(
            landAcres = 4.5,
            pmKisanVerified = true,
            soilOrganicCarbonPct = 0.82,
            cropCount = 2
        )
        assertTrue("Credit score must be between 300 and 900", score in 300..900)
        assertTrue("High land holding & PM-Kisan verification should achieve prime rating", score >= 720)
        assertTrue("Rating tier should be descriptive", tier.isNotBlank())

        val passport = AgriStackPassportEngine.getSovereignPassport("B. Jaswanth Reddy", "Andhra Pradesh")
        assertNotNull(passport)
        assertTrue(passport.eligibleSchemes.isNotEmpty())
        assertTrue(passport.soilHealthSummary.nitrogenKgPerHa > 0)
    }

    @Test
    fun testYantraShareEscrowContract() {
        val listings = YantraShareEngine.getSampleListings()
        assertTrue("Equipment network should provide machinery listings", listings.isNotEmpty())

        val tractor = listings.first { it.category == com.example.yantra.MachineryCategory.TRACTOR }
        val contract = YantraShareEngine.createEscrowContract(tractor, rentalAcreage = 5.0, includeOperator = true)

        assertNotNull(contract)
        assertEquals(EscrowStatus.FUNDS_LOCKED, contract.status)
        assertEquals((tractor.perAcreRateRupees * 5.0) + 300.0, contract.totalEscrowAmount, 0.1)
    }

    @Test
    fun testBioRxDosageScalingForAcreage() {
        val rx1Acre = BioRxEngine.calculatePrescription(OrganicFormulationType.JEEVAMRUTHA, acreage = 1.0)
        val rx5Acre = BioRxEngine.calculatePrescription(OrganicFormulationType.JEEVAMRUTHA, acreage = 5.0)

        // 5x acreage should require 5x raw ingredients
        val dung1 = rx1Acre.scaledIngredients.first { it.ingredientName.contains("Dung") }
        val dung5 = rx5Acre.scaledIngredients.first { it.ingredientName.contains("Dung") }

        assertEquals("10.0 kg", dung1.scaledQuantityFormatted)
        assertEquals("50.0 kg", dung5.scaledQuantityFormatted)
        assertTrue(rx5Acre.costSavedVsChemicalPesticidesRupees > rx1Acre.costSavedVsChemicalPesticidesRupees)
        assertTrue(rx5Acre.preparationSteps.isNotEmpty())
    }
}
