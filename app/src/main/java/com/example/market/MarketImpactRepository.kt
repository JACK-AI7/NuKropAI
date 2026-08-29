package com.example.market

import com.example.DiseaseAggregationService
import com.example.MandiRecord
import com.example.model.OutbreakAlert
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.util.Locale
import java.util.concurrent.ConcurrentHashMap

/**
 * Interface defining operations for querying regional disease outbreaks and
 * forecasting APMC Mandi market price shocks.
 */
interface IMarketImpactRepository {

    /**
     * Fetches active outbreak alerts targeted at a specific state (both Epicenter & Early Warning).
     */
    suspend fun getActiveAlerts(state: String): Result<List<OutbreakAlert>>

    /**
     * Fetches all active outbreak alerts across the country.
     */
    suspend fun getAllActiveAlerts(): Result<List<OutbreakAlert>>

    /**
     * Computes market price impact forecasts for all active alerts affecting a given state.
     * Correlates with provided live Mandi records or uses default commodity baselines.
     */
    suspend fun getMarketImpacts(
        state: String,
        mandiRecords: List<MandiRecord> = emptyList()
    ): Result<List<MarketPriceImpact>>

    /**
     * Finds the primary market price impact for a specific commodity in a given state.
     */
    suspend fun getImpactForCrop(
        cropName: String,
        state: String,
        mandiRecords: List<MandiRecord> = emptyList()
    ): Result<MarketPriceImpact?>

    /**
     * Pure synchronous calculation helper for computing market impact given an alert and mandi parameters.
     */
    fun calculateImpact(
        alert: OutbreakAlert,
        currentModalPrice: Double,
        targetState: String,
        targetMandi: String,
        mandiRecords: List<MandiRecord> = emptyList(),
        stage: OutbreakStage = OutbreakStage.SUPPLY_CONTRACTION
    ): MarketPriceImpact
}

/**
 * Singleton repository coordinating outbreak alert telemetry, live mandi price data,
 * and econometric price shock calculations.
 */
object MarketImpactRepository : IMarketImpactRepository {

    private val impactCache = ConcurrentHashMap<String, MarketPriceImpact>()
    private val alertCache = ConcurrentHashMap<String, List<OutbreakAlert>>()

    override suspend fun getActiveAlerts(state: String): Result<List<OutbreakAlert>> = withContext(Dispatchers.IO) {
        val cached = alertCache[state.trim().lowercase(Locale.ROOT)]
        if (cached != null) {
            return@withContext Result.success(cached)
        }

        val result = DiseaseAggregationService.fetchActiveAlerts(state)
        result.onSuccess { alerts ->
            alertCache[state.trim().lowercase(Locale.ROOT)] = alerts
        }
        result
    }

    override suspend fun getAllActiveAlerts(): Result<List<OutbreakAlert>> = withContext(Dispatchers.IO) {
        DiseaseAggregationService.fetchAllActiveAlerts()
    }

    override suspend fun getMarketImpacts(
        state: String,
        mandiRecords: List<MandiRecord>
    ): Result<List<MarketPriceImpact>> = withContext(Dispatchers.IO) {
        try {
            val alertsResult = getActiveAlerts(state)
            val alerts = alertsResult.getOrNull() ?: emptyList()

            if (alerts.isEmpty()) {
                return@withContext Result.success(emptyList())
            }

            val impacts = alerts.map { alert ->
                // Look for relevant mandi records for this alert
                val relevantRecords = mandiRecords.filter { record ->
                    isRecordRelevantToAlert(record, alert)
                }

                val primaryRecord = relevantRecords.firstOrNull {
                    it.state.equals(state, ignoreCase = true)
                } ?: relevantRecords.firstOrNull()

                val basePrice = primaryRecord?.modalPrice ?: getDefaultModalPrice(alert)
                val targetMandi = primaryRecord?.market ?: "${state} Primary Mandi"

                MarketImpactCalculator.calculateImpact(
                    alert = alert,
                    currentModalPrice = basePrice,
                    targetState = state,
                    targetMandi = targetMandi,
                    availableMandiRecords = relevantRecords.ifEmpty { mandiRecords }
                )
            }

            Result.success(impacts)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun getImpactForCrop(
        cropName: String,
        state: String,
        mandiRecords: List<MandiRecord>
    ): Result<MarketPriceImpact?> = withContext(Dispatchers.IO) {
        try {
            val alertsResult = getActiveAlerts(state)
            val alerts = alertsResult.getOrNull() ?: emptyList()

            val normalizedCrop = cropName.trim().lowercase(Locale.ROOT)
            val matchingAlert = alerts.firstOrNull { alert ->
                alert.diseaseName.lowercase(Locale.ROOT).contains(normalizedCrop) ||
                        alert.message.lowercase(Locale.ROOT).contains(normalizedCrop)
            } ?: alerts.firstOrNull()

            if (matchingAlert == null) {
                return@withContext Result.success(null)
            }

            val relevantRecords = mandiRecords.filter {
                it.commodity.lowercase(Locale.ROOT).contains(normalizedCrop) ||
                        normalizedCrop.contains(it.commodity.lowercase(Locale.ROOT))
            }

            val primaryRecord = relevantRecords.firstOrNull {
                it.state.equals(state, ignoreCase = true)
            } ?: relevantRecords.firstOrNull()

            val basePrice = primaryRecord?.modalPrice ?: getDefaultModalPrice(matchingAlert)
            val targetMandi = primaryRecord?.market ?: "${state} APMC Mandi"

            val impact = MarketImpactCalculator.calculateImpact(
                alert = matchingAlert,
                currentModalPrice = basePrice,
                targetState = state,
                targetMandi = targetMandi,
                availableMandiRecords = relevantRecords.ifEmpty { mandiRecords }
            )

            Result.success(impact)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override fun calculateImpact(
        alert: OutbreakAlert,
        currentModalPrice: Double,
        targetState: String,
        targetMandi: String,
        mandiRecords: List<MandiRecord>,
        stage: OutbreakStage
    ): MarketPriceImpact {
        return MarketImpactCalculator.calculateImpact(
            alert = alert,
            currentModalPrice = currentModalPrice,
            targetState = targetState,
            targetMandi = targetMandi,
            availableMandiRecords = mandiRecords,
            stage = stage
        )
    }

    /**
     * Clears local in-memory caches.
     */
    fun clearCache() {
        impactCache.clear()
        alertCache.clear()
    }

    private fun isRecordRelevantToAlert(record: MandiRecord, alert: OutbreakAlert): Boolean {
        val commodity = record.commodity.lowercase(Locale.ROOT)
        val disease = alert.diseaseName.lowercase(Locale.ROOT)
        val message = alert.message.lowercase(Locale.ROOT)

        return disease.contains(commodity) || message.contains(commodity) ||
                commodity.contains("tomato") && disease.contains("blight") ||
                commodity.contains("potato") && disease.contains("blight") ||
                commodity.contains("cotton") && disease.contains("bollworm") ||
                commodity.contains("wheat") && disease.contains("rust") ||
                commodity.contains("chilli") && disease.contains("leaf curl") ||
                commodity.contains("onion") && disease.contains("thrips")
    }

    private fun getDefaultModalPrice(alert: OutbreakAlert): Double {
        val text = "${alert.diseaseName} ${alert.message}".lowercase(Locale.ROOT)
        return when {
            text.contains("tomato") -> 2200.0
            text.contains("onion") -> 1800.0
            text.contains("potato") -> 1500.0
            text.contains("chilli") || text.contains("capsicum") -> 4500.0
            text.contains("cotton") -> 6800.0
            text.contains("wheat") -> 2275.0
            text.contains("rice") || text.contains("paddy") -> 2183.0
            text.contains("mustard") -> 5450.0
            text.contains("soybean") -> 4600.0
            text.contains("maize") -> 2090.0
            else -> 2500.0
        }
    }
}
