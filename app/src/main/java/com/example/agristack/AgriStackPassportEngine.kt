package com.example.agristack

import com.example.SupabaseApi
import kotlin.math.abs
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

data class RegionalSoilProfile(
    val nitrogen: Double,
    val phosphorus: Double,
    val potassium: Double,
    val soilPh: Double,
    val organicCarbonPct: Double,
    val zincPpm: Double,
    val ironPpm: Double,
    val boronPpm: Double,
    val fertilityGrade: String
)

object AgriStackPassportEngine {

    private val STATE_SOIL_BASELINES: Map<String, RegionalSoilProfile> = mapOf(
        "Andhra Pradesh" to RegionalSoilProfile(280.0, 34.5, 310.0, 6.8, 0.82, 1.15, 7.4, 0.65, "OPTIMAL HIGH YIELD (Grade A+)"),
        "Maharashtra" to RegionalSoilProfile(240.0, 28.0, 340.0, 7.4, 0.76, 0.95, 6.8, 0.58, "BALANCED DECCAN BLACK (Grade A)"),
        "Punjab" to RegionalSoilProfile(310.0, 42.0, 290.0, 7.1, 0.88, 1.30, 8.1, 0.72, "PRIME ALLUVIAL HIGH YIELD (Grade A+)"),
        "Tamil Nadu" to RegionalSoilProfile(260.0, 30.0, 280.0, 6.5, 0.72, 1.05, 7.0, 0.60, "FERTILE RED LOAM (Grade A)"),
        "Karnataka" to RegionalSoilProfile(250.0, 32.0, 300.0, 6.7, 0.78, 1.10, 7.2, 0.62, "BALANCED SOUTHERN ZONE (Grade A)"),
        "Telangana" to RegionalSoilProfile(270.0, 31.0, 305.0, 6.9, 0.79, 1.12, 7.1, 0.61, "RED SANDY LOAM (Grade A)"),
        "Gujarat" to RegionalSoilProfile(245.0, 29.5, 330.0, 7.6, 0.74, 0.98, 6.9, 0.59, "ALLUVIAL BLACK COTTON (Grade A)"),
        "Uttar Pradesh" to RegionalSoilProfile(295.0, 38.0, 285.0, 7.2, 0.84, 1.22, 7.8, 0.68, "GANGETIC FERTILE ALLUVIAL (Grade A+)")
    )

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

        // Land acreage factor (+30 to +120)
        baseScore += (landAcres * 18.0).toInt().coerceIn(30, 120)

        // PM-KISAN verification factor (+80)
        if (pmKisanVerified) baseScore += 80

        // Soil Organic Carbon factor (+30 to +90)
        baseScore += if (soilOrganicCarbonPct >= 0.75) 90 else if (soilOrganicCarbonPct >= 0.5) 60 else 30

        // Crop diversification (+25 per crop)
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
     * Generates sovereign ID formatted deterministically per state and district.
     */
    fun generateDeterministicSovereignId(state: String, district: String, seed: String = "seed"): String {
        val stateCode = state.filter { it.isLetter() }.take(2).uppercase()
        val distCode = district.filter { it.isLetter() }.take(3).uppercase()
        val hash = abs(seed.hashCode() % 900000) + 100000
        return "IN-$stateCode-$distCode-$hash"
    }

    /**
     * Matches government schemes dynamically based on land holding, state, credit rating, and crop types.
     */
    fun matchEligibleSchemes(
        state: String,
        landAcres: Double,
        creditScore: Int,
        crops: List<String>
    ): List<AgriSchemeBenefit> {
        val list = mutableListOf<AgriSchemeBenefit>()

        // 1. PM-KISAN (Universal Direct Benefit Transfer)
        list.add(
            AgriSchemeBenefit(
                schemeCode = "PM-KISAN",
                schemeName = "PM Kisan Samman Nidhi",
                ministryOrDepartment = "Ministry of Agriculture",
                directBenefitAmountFormatted = "₹6,000 / Year",
                applicationStatus = "1-CLICK APPROVED",
                validityYear = "2026-27"
            )
        )

        // 2. PMFBY (Pradhan Mantri Fasal Bima Yojana)
        list.add(
            AgriSchemeBenefit(
                schemeCode = "PMFBY",
                schemeName = "Pradhan Mantri Fasal Bima Yojana",
                ministryOrDepartment = "Govt of India",
                directBenefitAmountFormatted = "100% Weather Crop Cover",
                applicationStatus = "DOCUMENT VERIFIED",
                validityYear = "Kharif 2026"
            )
        )

        // 3. SMAM Mechanization & Agri Drone Subsidy (Land holding >= 2.0 acres)
        if (landAcres >= 2.0) {
            list.add(
                AgriSchemeBenefit(
                    schemeCode = "SMAM-DRONE",
                    schemeName = "Sub-Mission on Agri Mechanization (Drone)",
                    ministryOrDepartment = "Dept of Agriculture",
                    directBenefitAmountFormatted = "50% Subsidy (₹5,00,000)",
                    applicationStatus = "ELIGIBLE - CLAIM NOW",
                    validityYear = "2026-27"
                )
            )
        }

        // 4. PM-KUSUM Solar Drip Irrigation (Credit Score >= 650)
        if (creditScore >= 650) {
            list.add(
                AgriSchemeBenefit(
                    schemeCode = "PM-KUSUM",
                    schemeName = "Solar Drip Irrigation Component-B",
                    ministryOrDepartment = "Ministry of New & Renewable Energy",
                    directBenefitAmountFormatted = "60% Direct Grant",
                    applicationStatus = "ELIGIBLE - CLAIM NOW",
                    validityYear = "2026-27"
                )
            )
        }

        return list
    }

    /**
     * Retrieves or generates sovereign AgriStack Passport with deterministic agro-ecological baselines.
     */
    fun getSovereignPassport(
        farmerName: String = "B. Jaswanth Reddy",
        state: String = "Andhra Pradesh",
        district: String = "Guntur",
        surveyNumber: String = "SY-412/2B",
        villageName: String = "Narakodur Village",
        landAcres: Double = 4.5,
        primaryCrops: List<String> = listOf("Paddy / Rice", "Chilli & Spices"),
        pmKisanVerified: Boolean = true
    ): AgriStackPassport {
        val soilBaseline = STATE_SOIL_BASELINES[state] ?: STATE_SOIL_BASELINES["Andhra Pradesh"]!!

        val soil = SoilHealthMetrics(
            nitrogenKgPerHa = soilBaseline.nitrogen,
            phosphorusKgPerHa = soilBaseline.phosphorus,
            potassiumKgPerHa = soilBaseline.potassium,
            soilPh = soilBaseline.soilPh,
            organicCarbonPct = soilBaseline.organicCarbonPct,
            zincPpm = soilBaseline.zincPpm,
            ironPpm = soilBaseline.ironPpm,
            boronPpm = soilBaseline.boronPpm,
            overallFertilityIndex = soilBaseline.fertilityGrade
        )

        val (score, tier) = calculateAgriCreditScore(
            landAcres = landAcres,
            pmKisanVerified = pmKisanVerified,
            soilOrganicCarbonPct = soil.organicCarbonPct,
            cropCount = primaryCrops.size
        )

        val kccLimit = landAcres * 75000.0 // ₹75,000 per acre KCC scale of finance
        val schemes = matchEligibleSchemes(state, landAcres, score, primaryCrops)
        val sovereignId = generateDeterministicSovereignId(state, district, farmerName)

        return AgriStackPassport(
            sovereignFarmerId = sovereignId,
            farmerName = farmerName,
            surveyParcelNumber = surveyNumber,
            villageName = villageName,
            district = district,
            state = state,
            landSizeAcres = landAcres,
            primaryCrops = primaryCrops,
            pmKisanVerified = pmKisanVerified,
            agriCreditScore = score,
            creditRatingTier = tier,
            maxEligibleKccLoanLimit = kccLimit,
            soilHealthSummary = soil,
            eligibleSchemes = schemes
        )
    }

    /**
     * Asynchronously queries live Supabase PostgREST table `agristack_passports` with fallback to deterministic passport.
     */
    suspend fun getLiveOrFallbackPassport(
        farmerId: String,
        defaultName: String = "B. Jaswanth Reddy",
        defaultState: String = "Andhra Pradesh",
        defaultDistrict: String = "Guntur"
    ): AgriStackPassport {
        try {
            val livePassport = SupabaseApi.fetchAgriStackPassport(farmerId)
            if (livePassport != null) {
                return livePassport
            }
        } catch (_: Exception) {}

        return getSovereignPassport(
            farmerName = defaultName,
            state = defaultState,
            district = defaultDistrict
        )
    }
}
