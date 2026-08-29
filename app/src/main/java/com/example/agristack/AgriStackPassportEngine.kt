package com.example.agristack

import kotlin.math.roundToInt

data class AgriStackPassport(
    val sovereignFarmerId: String,
    val farmerName: String,
    val surveyParcelNumber: String,
    val villageName: String,
    val district: String,
    val state: String,
    val landSizeAcres: Double,
    val primaryCrops: List<String>,
    val pmKisanVerified: Boolean,
    val agriCreditScore: Int, // 300 to 900
    val creditRatingTier: String, // "AAA Sovereign Prime", "A+ Strong", "BBB Moderate"
    val maxEligibleKccLoanLimit: Double, // Kisan Credit Card limit in INR
    val soilHealthSummary: SoilHealthMetrics,
    val eligibleSchemes: List<AgriSchemeBenefit>
)

data class SoilHealthMetrics(
    val nitrogenKgPerHa: Double,
    val phosphorusKgPerHa: Double,
    val potassiumKgPerHa: Double,
    val soilPh: Double,
    val organicCarbonPct: Double,
    val zincPpm: Double,
    val ironPpm: Double,
    val boronPpm: Double,
    val overallFertilityIndex: String // "OPTIMAL HIGH YIELD", "BALANCED", "DEPLETED"
)

data class AgriSchemeBenefit(
    val schemeCode: String,
    val schemeName: String,
    val ministryOrDepartment: String,
    val directBenefitAmountFormatted: String,
    val applicationStatus: String, // "1-CLICK APPROVED", "ELIGIBLE - CLAIM NOW", "DOCUMENT VERIFIED"
    val validityYear: String
)

object AgriStackPassportEngine {

    /**
     * Generates algorithmic agri-credit score (300 - 900) based on:
     * - Land Holding & Soil Fertility Index (35%)
     * - PM-KISAN verification status (25%)
     * - Crop diversity & historical yield resilience (40%)
     */
    fun calculateAgriCreditScore(
        landAcres: Double,
        pmKisanVerified: Boolean,
        soilOrganicCarbonPct: Double,
        cropCount: Int
    ): Pair<Int, String> {
        var baseScore = 550

        // Land acreage factor (+50 to +120)
        baseScore += (landAcres * 18.0).toInt().coerceIn(30, 120)

        // PM-KISAN verification factor (+80)
        if (pmKisanVerified) baseScore += 80

        // Soil Organic Carbon factor (+40 to +90)
        baseScore += if (soilOrganicCarbonPct >= 0.75) 90 else if (soilOrganicCarbonPct >= 0.5) 60 else 30

        // Crop diversification (+20 per crop)
        baseScore += (cropCount * 25).coerceIn(25, 75)

        val finalScore = baseScore.coerceIn(300, 900)
        val tier = when {
            finalScore >= 800 -> "AAA Sovereign Prime (Interest Subvention @ 4%)"
            finalScore >= 720 -> "A+ High Trust Institutional Grade"
            finalScore >= 620 -> "BBB Cooperative Standard Grade"
            else -> "C Provisional Underwriting"
        }

        return Pair(finalScore, tier)
    }

    /**
     * Retrieves or generates sovereign AgriStack Passport
     */
    fun getSovereignPassport(farmerName: String = "B. Jaswanth Reddy", state: String = "Andhra Pradesh"): AgriStackPassport {
        val soil = SoilHealthMetrics(
            nitrogenKgPerHa = 280.0,
            phosphorusKgPerHa = 34.5,
            potassiumKgPerHa = 310.0,
            soilPh = 6.8,
            organicCarbonPct = 0.82,
            zincPpm = 1.15,
            ironPpm = 7.4,
            boronPpm = 0.65,
            overallFertilityIndex = "OPTIMAL HIGH YIELD (Grade A+)"
        )

        val (score, tier) = calculateAgriCreditScore(4.5, true, soil.organicCarbonPct, 2)
        val kccLimit = (4.5 * 75000.0) // ₹75,000 per acre KCC scale of finance

        val schemes = listOf(
            AgriSchemeBenefit("PM-KISAN", "PM Kisan Samman Nidhi", "Ministry of Agriculture", "₹6,000 / Year", "1-CLICK APPROVED", "2026-27"),
            AgriSchemeBenefit("PMFBY", "Pradhan Mantri Fasal Bima Yojana", "Govt of India", "100% Weather Crop Cover", "DOCUMENT VERIFIED", "Kharif 2026"),
            AgriSchemeBenefit("SMAM-DRONE", "Sub-Mission on Agri Mechanization (Drone)", "Dept of Agriculture", "50% Subsidy (₹5,00,000)", "ELIGIBLE - CLAIM NOW", "2026-27"),
            AgriSchemeBenefit("PM-KUSUM", "Solar Drip Irrigation Component-B", "Ministry of New & Renewable Energy", "60% Direct Grant", "ELIGIBLE - CLAIM NOW", "2026-27")
        )

        return AgriStackPassport(
            sovereignFarmerId = "IN-AP-GNT-${System.currentTimeMillis() % 1000000}",
            farmerName = farmerName,
            surveyParcelNumber = "SY-412/2B",
            villageName = "Narakodur Village",
            district = "Guntur",
            state = state,
            landSizeAcres = 4.5,
            primaryCrops = listOf("Paddy / Rice", "Chilli & Spices"),
            pmKisanVerified = true,
            agriCreditScore = score,
            creditRatingTier = tier,
            maxEligibleKccLoanLimit = kccLimit,
            soilHealthSummary = soil,
            eligibleSchemes = schemes
        )
    }
}
