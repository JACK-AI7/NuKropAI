package com.example.market

import com.example.DiseaseAggregationService
import com.example.MandiRecord
import com.example.model.OutbreakAlert
import java.util.Locale
import kotlin.math.abs
import kotlin.math.roundToInt

/**
 * Pure, deterministic econometric calculation engine modeling the impact of regional
 * crop disease outbreaks and epidemics on APMC Mandi prices across India.
 *
 * Models supply contraction surges, panic distress selling drops, perishability dynamics,
 * density saturation curves, and geographic inter-state spillover.
 */
object MarketImpactCalculator {

    /**
     * Perishability index ($\phi$) for Indian agricultural commodities.
     * Perishable horticulture crops experience rapid price swings, while durable cereals/fibers exhibit gradual shock curves.
     */
    private val PERISHABILITY_MAP: Map<String, Double> = mapOf(
        "tomato" to 1.40,
        "tamatar" to 1.40,
        "capsicum" to 1.35,
        "chilli" to 1.35,
        "chili" to 1.35,
        "chilly" to 1.35,
        "pepper" to 1.35,
        "shimla mirch" to 1.35,
        "green chilli" to 1.35,
        "red chilli" to 1.35,
        "onion" to 1.25,
        "pyaz" to 1.25,
        "potato" to 1.15,
        "aloo" to 1.15,
        "cotton" to 0.95,
        "kapas" to 0.95,
        "wheat" to 0.80,
        "gehun" to 0.80,
        "rice" to 0.80,
        "paddy" to 0.80,
        "chawal" to 0.80,
        "dhan" to 0.80,
        "mustard" to 0.90,
        "sarson" to 0.90,
        "soybean" to 0.90,
        "soyabean" to 0.90,
        "maize" to 0.85,
        "corn" to 0.85,
        "makka" to 0.85
    )

    /**
     * Baseline econometric severity shocks ($\beta$).
     */
    private const val BETA_CRITICAL = 0.32
    private const val BETA_HIGH = 0.22
    private const val BETA_MODERATE = 0.12
    private const val BETA_LOW = 0.05

    /**
     * Resolves the perishability multiplier ($\phi$) for a given crop name.
     */
    fun getPerishability(cropName: String): Double {
        if (cropName.isBlank()) return 1.00
        val normalized = cropName.trim().lowercase(Locale.ROOT)
        
        // Exact match
        PERISHABILITY_MAP[normalized]?.let { return it }

        // Substring / keyword match
        for ((key, value) in PERISHABILITY_MAP) {
            if (normalized.contains(key)) {
                return value
            }
        }

        return 1.00
    }

    /**
     * Resolves the baseline severity shock factor ($\beta$) for an outbreak severity level.
     */
    fun getSeverityShock(severity: String): Double {
        return when (severity.trim().uppercase(Locale.ROOT)) {
            "CRITICAL" -> BETA_CRITICAL
            "HIGH" -> BETA_HIGH
            "MODERATE" -> BETA_MODERATE
            "LOW" -> BETA_LOW
            else -> BETA_MODERATE
        }
    }

    /**
     * Computes the scan density saturation ($D$) bounded in $[0.1, 1.0]$.
     */
    fun calculateDensitySaturation(scanCount: Int): Double {
        return (scanCount / 100.0).coerceIn(0.1, 1.0)
    }

    /**
     * Computes the geographic spillover multiplier:
     * - Epicenter state: 1.00
     * - Direct neighboring state: 0.70
     * - Distant state: 0.40
     */
    fun getGeographicMultiplier(sourceState: String, targetState: String): Double {
        val sState = sourceState.trim()
        val tState = targetState.trim()

        if (sState.equals(tState, ignoreCase = true)) {
            return 1.00
        }

        val areNeighbors = DiseaseAggregationService.StateAdjacencyGraph.areNeighbors(sState, tState)
        return if (areNeighbors) 0.70 else 0.40
    }

    /**
     * Calculates the comprehensive market price impact of an outbreak alert on a target mandi.
     *
     * @param alert The active outbreak alert (Epicenter or Early Warning).
     * @param currentModalPrice Baseline current modal price in INR/quintal.
     * @param targetState State of the target mandi.
     * @param targetMandi Name of the target mandi.
     * @param availableMandiRecords Live mandi price records for regional comparison.
     * @param stage Outbreak lifecycle stage (defaults to SUPPLY_CONTRACTION).
     * @return MarketPriceImpact with predicted prices, delta percentage, risk classification, and farmer advice.
     */
    fun calculateImpact(
        alert: OutbreakAlert,
        currentModalPrice: Double,
        targetState: String,
        targetMandi: String,
        availableMandiRecords: List<MandiRecord> = emptyList(),
        stage: OutbreakStage = OutbreakStage.SUPPLY_CONTRACTION
    ): MarketPriceImpact {
        val cropName = inferCropName(alert, availableMandiRecords)
        val diseaseName = alert.diseaseName.ifBlank { "Crop Disease" }
        val sourceState = alert.sourceState.ifBlank { targetState }
        val effectiveTargetState = targetState.ifBlank { alert.targetState }
        val effectiveTargetMandi = targetMandi.ifBlank { "Primary APMC Market" }

        val isEpicenter = sourceState.equals(effectiveTargetState, ignoreCase = true) ||
                alert.alertType.equals("EPICENTER", ignoreCase = true) && effectiveTargetState.equals(alert.targetState, ignoreCase = true)
        val isNeighbor = !isEpicenter && DiseaseAggregationService.StateAdjacencyGraph.areNeighbors(sourceState, effectiveTargetState)

        val perishability = getPerishability(cropName)
        val beta = getSeverityShock(alert.severity)
        val density = calculateDensitySaturation(alert.scanCount)
        val geoMultiplier = getGeographicMultiplier(sourceState, effectiveTargetState)

        // Stage dynamics econometric calculation
        val (rawDeltaPct, mechanism) = when (stage) {
            OutbreakStage.SUPPLY_CONTRACTION -> {
                val delta = +(beta * perishability * density * geoMultiplier * 100.0)
                val mech = if (isEpicenter) ImpactMechanism.SUPPLY_CONTRACTION else ImpactMechanism.REGIONAL_ARBITRAGE
                Pair(delta, mech)
            }
            OutbreakStage.EARLY_PANIC -> {
                if (isEpicenter) {
                    val delta = -(beta * perishability * density * 0.85 * 100.0)
                    Pair(delta, ImpactMechanism.DISTRESS_SELLING)
                } else if (isNeighbor) {
                    val delta = +(beta * perishability * density * geoMultiplier * 0.50 * 100.0)
                    Pair(delta, ImpactMechanism.REGIONAL_ARBITRAGE)
                } else {
                    Pair(0.0, ImpactMechanism.QUALITY_DISCOUNT)
                }
            }
            OutbreakStage.RECOVERY -> {
                val delta = -(beta * 0.30 * perishability * density * 100.0)
                Pair(delta, ImpactMechanism.QUALITY_DISCOUNT)
            }
        }

        // Apply price calculation with floor of 40% of baseline price
        val basePrice = if (currentModalPrice > 0.0) currentModalPrice else 2500.0 // Default reasonable agricultural modal price
        val nominalPriceDelta = basePrice * (rawDeltaPct / 100.0)
        val rawPredictedPrice = basePrice + nominalPriceDelta
        val floorPrice = basePrice * 0.40
        val predictedModalPrice = rawPredictedPrice.coerceAtLeast(floorPrice)

        val effectivePriceDelta = predictedModalPrice - basePrice
        val deltaPercentage = (effectivePriceDelta / basePrice) * 100.0

        val direction = when {
            deltaPercentage > 0.5 -> ImpactDirection.SURGE
            deltaPercentage < -0.5 -> ImpactDirection.DROP
            else -> ImpactDirection.STABLE
        }

        val riskLevel = MarketRiskLevel.fromDeltaPercentage(deltaPercentage)

        // Confidence score computation bounded in [50, 98]
        val dataBonus = if (availableMandiRecords.isNotEmpty()) 13 else 5
        val rawConfidence = (50.0 + (density * 35.0) + dataBonus).roundToInt()
        val confidenceScore = rawConfidence.coerceIn(50, 98)

        // Estimated peak days
        val estimatedPeakDays = calculatePeakDays(perishability, isEpicenter)

        // Recommended farmer action
        val recommendedAction = generateFarmerRecommendation(
            cropName = cropName,
            sourceState = sourceState,
            targetState = effectiveTargetState,
            isEpicenter = isEpicenter,
            isNeighbor = isNeighbor,
            direction = direction,
            riskLevel = riskLevel,
            deltaPercentage = deltaPercentage,
            peakDays = estimatedPeakDays,
            mechanism = mechanism
        )

        // Affected markets breakdown
        val affectedMarkets = generateAffectedMarkets(
            alert = alert,
            cropName = cropName,
            basePrice = basePrice,
            effectiveTargetState = effectiveTargetState,
            effectiveTargetMandi = effectiveTargetMandi,
            stage = stage,
            availableMandiRecords = availableMandiRecords
        )

        return MarketPriceImpact(
            alertId = alert.id,
            cropName = cropName,
            diseaseName = diseaseName,
            targetState = effectiveTargetState,
            targetMandi = effectiveTargetMandi,
            currentModalPrice = basePrice,
            predictedModalPrice = predictedModalPrice,
            priceDelta = effectivePriceDelta,
            deltaPercentage = deltaPercentage,
            direction = direction,
            riskLevel = riskLevel,
            confidenceScore = confidenceScore,
            mechanism = mechanism,
            estimatedPeakDays = estimatedPeakDays,
            recommendedFarmerAction = recommendedAction,
            affectedMarkets = affectedMarkets
        )
    }

    private fun inferCropName(alert: OutbreakAlert, records: List<MandiRecord>): String {
        // Try from live records
        records.firstOrNull { it.commodity.isNotBlank() }?.commodity?.let { return it }

        // Try from alert message or disease name
        val text = "${alert.diseaseName} ${alert.message}".lowercase(Locale.ROOT)
        for (crop in listOf("Tomato", "Capsicum", "Chilli", "Onion", "Potato", "Cotton", "Wheat", "Rice", "Mustard", "Soybean", "Maize")) {
            if (text.contains(crop.lowercase(Locale.ROOT))) {
                return crop
            }
        }
        return "General"
    }

    private fun calculatePeakDays(perishability: Double, isEpicenter: Boolean): Int {
        return when {
            perishability >= 1.35 -> if (isEpicenter) 3 else 5
            perishability >= 1.15 -> if (isEpicenter) 6 else 9
            perishability >= 0.90 -> if (isEpicenter) 14 else 18
            else -> if (isEpicenter) 21 else 28
        }
    }

    private fun generateFarmerRecommendation(
        cropName: String,
        sourceState: String,
        targetState: String,
        isEpicenter: Boolean,
        isNeighbor: Boolean,
        direction: ImpactDirection,
        riskLevel: MarketRiskLevel,
        deltaPercentage: Double,
        peakDays: Int,
        mechanism: ImpactMechanism
    ): String {
        val formattedPct = String.format(Locale.US, "%.1f", abs(deltaPercentage))

        return when {
            isEpicenter && direction == ImpactDirection.SURGE -> {
                "Severe regional crop damage has contracted local supply. For healthy/unaffected harvest lots, stagger mandi arrivals over the next $peakDays days to capitalize on peak spot premiums (+$formattedPct%). Maintain strict grading."
            }
            isEpicenter && direction == ImpactDirection.DROP -> {
                "Outbreak distress selling is temporarily depressing local mandi rates (-$formattedPct%). Avoid panic dumping; utilize ventilated on-farm storage or divert clean harvest to adjacent district mandis."
            }
            isNeighbor && direction == ImpactDirection.SURGE -> {
                "Neighboring outbreak in $sourceState is driving regional procurement demand into $targetState mandis (+$formattedPct% premium). Transport surplus graded lots to major border APMC yards to capture regional price arbitrage."
            }
            mechanism == ImpactMechanism.QUALITY_DISCOUNT -> {
                "Market is discounting disease-spotted produce. Execute thorough field sorting and post-harvest washing to secure Grade-A benchmark prices."
            }
            riskLevel == MarketRiskLevel.LOW || direction == ImpactDirection.STABLE -> {
                "Normal market conditions prevail. Proceed with standard harvesting cycles and monitor local APMC price updates."
            }
            else -> {
                "Moderate price volatility expected ($formattedPct%). Coordinate with local FPO (Farmer Producer Organization) for collective bargaining and bulk transportation."
            }
        }
    }

    private fun generateAffectedMarkets(
        alert: OutbreakAlert,
        cropName: String,
        basePrice: Double,
        effectiveTargetState: String,
        effectiveTargetMandi: String,
        stage: OutbreakStage,
        availableMandiRecords: List<MandiRecord>
    ): List<AffectedMarketDetail> {
        val details = mutableListOf<AffectedMarketDetail>()

        // 1. If matching mandi records exist in the dataset, compute detail for each
        if (availableMandiRecords.isNotEmpty()) {
            val matchingRecords = availableMandiRecords.filter {
                it.commodity.contains(cropName, ignoreCase = true) || cropName.equals("General", ignoreCase = true)
            }.take(5)

            for (record in matchingRecords) {
                val isEpi = record.state.equals(alert.sourceState, ignoreCase = true)
                val mGeo = getGeographicMultiplier(alert.sourceState, record.state)
                val beta = getSeverityShock(alert.severity)
                val dens = calculateDensitySaturation(alert.scanCount)
                val perish = getPerishability(record.commodity)

                val delta = when (stage) {
                    OutbreakStage.SUPPLY_CONTRACTION -> +(beta * perish * dens * mGeo * 100.0)
                    OutbreakStage.EARLY_PANIC -> if (isEpi) -(beta * perish * dens * 0.85 * 100.0) else +(beta * perish * dens * mGeo * 0.50 * 100.0)
                    OutbreakStage.RECOVERY -> -(beta * 0.30 * perish * dens * 100.0)
                }

                val currentMPrice = if (record.modalPrice > 0) record.modalPrice else basePrice
                val predMPrice = (currentMPrice * (1.0 + delta / 100.0)).coerceAtLeast(currentMPrice * 0.40)
                val effDelta = ((predMPrice - currentMPrice) / currentMPrice) * 100.0
                val dir = if (effDelta > 0.5) ImpactDirection.SURGE else if (effDelta < -0.5) ImpactDirection.DROP else ImpactDirection.STABLE

                details.add(
                    AffectedMarketDetail(
                        marketName = record.market.ifBlank { "APMC Yard" },
                        district = record.district.ifBlank { "Central" },
                        state = record.state.ifBlank { effectiveTargetState },
                        currentModalPrice = currentMPrice,
                        predictedModalPrice = predMPrice,
                        deltaPercentage = effDelta,
                        direction = dir,
                        isEpicenter = isEpi
                    )
                )
            }
        }

        // 2. Ensure primary target market is included if not already present
        if (details.none { it.marketName.equals(effectiveTargetMandi, ignoreCase = true) }) {
            val isEpi = effectiveTargetState.equals(alert.sourceState, ignoreCase = true)
            val mGeo = getGeographicMultiplier(alert.sourceState, effectiveTargetState)
            val beta = getSeverityShock(alert.severity)
            val dens = calculateDensitySaturation(alert.scanCount)
            val perish = getPerishability(cropName)

            val delta = when (stage) {
                OutbreakStage.SUPPLY_CONTRACTION -> +(beta * perish * dens * mGeo * 100.0)
                OutbreakStage.EARLY_PANIC -> if (isEpi) -(beta * perish * dens * 0.85 * 100.0) else +(beta * perish * dens * mGeo * 0.50 * 100.0)
                OutbreakStage.RECOVERY -> -(beta * 0.30 * perish * dens * 100.0)
            }

            val predPrice = (basePrice * (1.0 + delta / 100.0)).coerceAtLeast(basePrice * 0.40)
            val effDelta = ((predPrice - basePrice) / basePrice) * 100.0
            val dir = if (effDelta > 0.5) ImpactDirection.SURGE else if (effDelta < -0.5) ImpactDirection.DROP else ImpactDirection.STABLE

            details.add(
                0,
                AffectedMarketDetail(
                    marketName = effectiveTargetMandi,
                    district = "District HQ",
                    state = effectiveTargetState,
                    currentModalPrice = basePrice,
                    predictedModalPrice = predPrice,
                    deltaPercentage = effDelta,
                    direction = dir,
                    isEpicenter = isEpi
                )
            )
        }

        return details
    }
}
