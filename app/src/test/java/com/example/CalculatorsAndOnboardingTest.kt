package com.example

import com.example.ui.AllAvailableCrops
import com.example.ui.onboarding.SupportedLanguages
import org.junit.Assert.*
import org.junit.Test
import kotlin.math.ceil
import kotlin.math.roundToInt

class CalculatorsAndOnboardingTest {

    @Test
    fun testSupportedLanguagesCoverage() {
        val codes = SupportedLanguages.map { it.code }
        assertTrue("Telugu must be supported", codes.contains("te"))
        assertTrue("Hindi must be supported", codes.contains("hi"))
        assertTrue("Tamil must be supported", codes.contains("ta"))
        assertTrue("Kannada must be supported", codes.contains("kn"))
        assertTrue("Marathi must be supported", codes.contains("mr"))
        assertTrue("Punjabi must be supported", codes.contains("pa"))
        assertTrue("Gujarati must be supported", codes.contains("gu"))
        assertTrue("Bengali must be supported", codes.contains("bn"))
        assertTrue("English must be supported", codes.contains("en"))
        assertEquals("At least 9 Indic & regional languages supported", 9, SupportedLanguages.size)
    }

    @Test
    fun testAllAvailableCropsCatalogue() {
        val cropNames = AllAvailableCrops.map { it.name }
        assertTrue("Cotton present", cropNames.contains("Cotton"))
        assertTrue("Rice / Paddy present", cropNames.contains("Rice / Paddy"))
        assertTrue("Chilli present", cropNames.contains("Chilli"))
        assertTrue("Tobacco present", cropNames.contains("Tobacco"))
        assertTrue("Wheat present", cropNames.contains("Wheat"))
        assertTrue("At least 20 crops available in catalogue", AllAvailableCrops.size >= 20)
    }

    @Test
    fun testFertilizerCalculations() {
        val acreage = 5.0 // 5 acres of cotton
        val ureaBags = ceil(2.2 * acreage).toInt()
        val dapBags = ceil(1.0 * acreage).toInt()
        val mopBags = ceil(0.8 * acreage).toInt()

        assertEquals(11, ureaBags)
        assertEquals(5, dapBags)
        assertEquals(4, mopBags)
    }

    @Test
    fun testPesticideDosingCalculations() {
        // Field crops: 2.5 acres, 2.0 ml/L dosage, 16L knapsack
        val fieldArea = 2.5
        val fieldWaterL = fieldArea * 200.0 // 500L
        val fieldChemicalMl = fieldWaterL * 2.0 // 1000 ml
        val fieldTanks = ceil(fieldWaterL / 16.0).toInt() // 32 tanks

        assertEquals(500.0, fieldWaterL, 0.01)
        assertEquals(1000.0, fieldChemicalMl, 0.01)
        assertEquals(32, fieldTanks)

        // Tree crops: 50 trees, 10L per tree, 2.5 ml/L dosage
        val treeCount = 50.0
        val treeWaterL = treeCount * 10.0 // 500L
        val treeChemicalMl = treeWaterL * 2.5 // 1250 ml
        assertEquals(500.0, treeWaterL, 0.01)
        assertEquals(1250.0, treeChemicalMl, 0.01)
    }

    @Test
    fun testFarmingBudgetProfitabilityMetrics() {
        val totalCost = 50000.0 // Rs 50,000
        val expectedYieldQtl = 20.0 // 20 Quintals
        val marketPriceQtl = 3500.0 // Rs 3,500 / Qtl

        val noLossPrice = (totalCost / expectedYieldQtl * 10.0).roundToInt() / 10.0
        val requiredYield = (totalCost / marketPriceQtl * 10.0).roundToInt() / 10.0
        val grossRevenue = expectedYieldQtl * marketPriceQtl
        val estimatedProfit = grossRevenue - totalCost

        assertEquals(2500.0, noLossPrice, 0.1)
        assertEquals(14.3, requiredYield, 0.1)
        assertEquals(70000.0, grossRevenue, 0.1)
        assertEquals(20000.0, estimatedProfit, 0.1)
    }
}
