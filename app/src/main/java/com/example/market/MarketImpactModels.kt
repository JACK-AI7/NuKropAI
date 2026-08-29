package com.example.market

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

/**
 * Outbreak severity levels representing the biological and geographical intensity of a crop disease outbreak.
 */
@Serializable
enum class OutbreakSeverity {
    @SerialName("LOW")
    LOW,

    @SerialName("MODERATE")
    MODERATE,

    @SerialName("HIGH")
    HIGH,

    @SerialName("CRITICAL")
    CRITICAL;

    companion object {
        fun fromString(value: String): OutbreakSeverity {
            return entries.firstOrNull { it.name.equals(value.trim(), ignoreCase = true) } ?: MODERATE
        }
    }
}

/**
 * Outbreak lifecycle stages influencing market supply and demand price dynamics.
 */
@Serializable
enum class OutbreakStage {
    @SerialName("EARLY_PANIC")
    EARLY_PANIC,

    @SerialName("SUPPLY_CONTRACTION")
    SUPPLY_CONTRACTION,

    @SerialName("RECOVERY")
    RECOVERY;

    companion object {
        fun fromString(value: String): OutbreakStage {
            return entries.firstOrNull { it.name.equals(value.trim(), ignoreCase = true) } ?: SUPPLY_CONTRACTION
        }
    }
}

/**
 * Direction of expected mandi price movement resulting from disease shocks.
 */
@Serializable
enum class ImpactDirection {
    @SerialName("SURGE")
    SURGE,

    @SerialName("DROP")
    DROP,

    @SerialName("VOLATILE")
    VOLATILE,

    @SerialName("STABLE")
    STABLE
}

/**
 * Risk classification for farmers and traders operating in affected agricultural markets.
 */
@Serializable
enum class MarketRiskLevel {
    @SerialName("LOW")
    LOW,

    @SerialName("MODERATE")
    MODERATE,

    @SerialName("HIGH")
    HIGH,

    @SerialName("CRITICAL")
    CRITICAL;

    companion object {
        fun fromDeltaPercentage(deltaPct: Double): MarketRiskLevel {
            val absDelta = kotlin.math.abs(deltaPct)
            return when {
                absDelta >= 25.0 -> CRITICAL
                absDelta >= 15.0 -> HIGH
                absDelta >= 7.0 -> MODERATE
                else -> LOW
            }
        }
    }
}

/**
 * Econometric mechanism causing market price fluctuations during disease outbreaks.
 */
@Serializable
enum class ImpactMechanism {
    @SerialName("SUPPLY_CONTRACTION")
    SUPPLY_CONTRACTION,

    @SerialName("DISTRESS_SELLING")
    DISTRESS_SELLING,

    @SerialName("QUALITY_DISCOUNT")
    QUALITY_DISCOUNT,

    @SerialName("REGIONAL_ARBITRAGE")
    REGIONAL_ARBITRAGE,

    @SerialName("PANIC_HOARDING")
    PANIC_HOARDING
}

/**
 * Granular mandi-level market price projection in the affected region or neighboring territory.
 */
@Serializable
data class AffectedMarketDetail(
    val marketName: String,
    val district: String,
    val state: String,
    val currentModalPrice: Double,
    val predictedModalPrice: Double,
    val deltaPercentage: Double,
    val direction: ImpactDirection,
    val isEpicenter: Boolean
)

/**
 * Comprehensive econometric market price impact assessment resulting from a regional outbreak alert.
 */
@Serializable
data class MarketPriceImpact(
    val alertId: String,
    val cropName: String,
    val diseaseName: String,
    val targetState: String,
    val targetMandi: String,
    val currentModalPrice: Double,
    val predictedModalPrice: Double,
    val priceDelta: Double,
    val deltaPercentage: Double,
    val direction: ImpactDirection,
    val riskLevel: MarketRiskLevel,
    val confidenceScore: Int,
    val mechanism: ImpactMechanism,
    val estimatedPeakDays: Int,
    val recommendedFarmerAction: String,
    val affectedMarkets: List<AffectedMarketDetail> = emptyList()
)
