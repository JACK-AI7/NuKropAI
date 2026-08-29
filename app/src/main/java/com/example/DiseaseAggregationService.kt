package com.example

import com.example.model.DiseaseScanPayload
import com.example.model.DiseaseScanRecord
import com.example.model.OutbreakAlert
import com.example.model.OutbreakAlertRecord
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.net.URLEncoder
import java.util.concurrent.TimeUnit

/**
 * Service responsible for:
 * 1. Pushing anonymous disease scans to Supabase PostgREST
 * 2. Fetching active outbreak alerts (Epicenters and Neighbor Early Warnings)
 * 3. In-memory symmetric Indian State Adjacency Graph for zero-latency lookups
 * 4. Pure evaluation engine for rolling density threshold calculation and alert fan-out
 */
object DiseaseAggregationService {

    private val httpClient = OkHttpClient.Builder()
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .build()

    private val json = Json {
        ignoreUnknownKeys = true
        isLenient = true
        coerceInputValues = true
    }

    /**
     * In-Memory Symmetric State Adjacency Graph for Indian States and Union Territories.
     */
    object StateAdjacencyGraph {
        private val graph: Map<String, List<String>> = mapOf(
            "Andhra Pradesh" to listOf("Telangana", "Odisha", "Chhattisgarh", "Karnataka", "Tamil Nadu", "Puducherry"),
            "Arunachal Pradesh" to listOf("Assam", "Nagaland"),
            "Assam" to listOf("Arunachal Pradesh", "Nagaland", "Manipur", "Mizoram", "Tripura", "Meghalaya", "West Bengal"),
            "Bihar" to listOf("Uttar Pradesh", "Jharkhand", "West Bengal"),
            "Chhattisgarh" to listOf("Madhya Pradesh", "Maharashtra", "Telangana", "Andhra Pradesh", "Odisha", "Jharkhand", "Uttar Pradesh"),
            "Goa" to listOf("Maharashtra", "Karnataka"),
            "Gujarat" to listOf("Rajasthan", "Madhya Pradesh", "Maharashtra", "Dadra and Nagar Haveli and Daman and Diu"),
            "Haryana" to listOf("Punjab", "Himachal Pradesh", "Rajasthan", "Uttar Pradesh", "Delhi", "Chandigarh"),
            "Himachal Pradesh" to listOf("Jammu and Kashmir", "Ladakh", "Punjab", "Haryana", "Uttarakhand", "Uttar Pradesh"),
            "Jharkhand" to listOf("Bihar", "Uttar Pradesh", "Chhattisgarh", "Odisha", "West Bengal"),
            "Karnataka" to listOf("Goa", "Maharashtra", "Telangana", "Andhra Pradesh", "Tamil Nadu", "Kerala"),
            "Kerala" to listOf("Karnataka", "Tamil Nadu", "Puducherry"),
            "Madhya Pradesh" to listOf("Rajasthan", "Uttar Pradesh", "Chhattisgarh", "Maharashtra", "Gujarat"),
            "Maharashtra" to listOf("Gujarat", "Madhya Pradesh", "Chhattisgarh", "Telangana", "Karnataka", "Goa", "Dadra and Nagar Haveli and Daman and Diu"),
            "Manipur" to listOf("Nagaland", "Assam", "Mizoram"),
            "Meghalaya" to listOf("Assam"),
            "Mizoram" to listOf("Assam", "Manipur", "Tripura"),
            "Nagaland" to listOf("Arunachal Pradesh", "Assam", "Manipur"),
            "Odisha" to listOf("West Bengal", "Jharkhand", "Chhattisgarh", "Andhra Pradesh"),
            "Punjab" to listOf("Jammu and Kashmir", "Himachal Pradesh", "Haryana", "Rajasthan", "Chandigarh"),
            "Rajasthan" to listOf("Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh", "Gujarat"),
            "Sikkim" to listOf("West Bengal"),
            "Tamil Nadu" to listOf("Kerala", "Karnataka", "Andhra Pradesh", "Puducherry"),
            "Telangana" to listOf("Maharashtra", "Chhattisgarh", "Karnataka", "Andhra Pradesh"),
            "Tripura" to listOf("Assam", "Mizoram"),
            "Uttar Pradesh" to listOf("Himachal Pradesh", "Haryana", "Delhi", "Rajasthan", "Madhya Pradesh", "Chhattisgarh", "Jharkhand", "Bihar", "Uttarakhand"),
            "Uttarakhand" to listOf("Himachal Pradesh", "Uttar Pradesh"),
            "West Bengal" to listOf("Sikkim", "Assam", "Bihar", "Jharkhand", "Odisha"),
            "Delhi" to listOf("Haryana", "Uttar Pradesh"),
            "Jammu and Kashmir" to listOf("Ladakh", "Himachal Pradesh", "Punjab"),
            "Ladakh" to listOf("Jammu and Kashmir", "Himachal Pradesh"),
            "Chandigarh" to listOf("Punjab", "Haryana"),
            "Puducherry" to listOf("Tamil Nadu", "Andhra Pradesh", "Kerala"),
            "Dadra and Nagar Haveli and Daman and Diu" to listOf("Gujarat", "Maharashtra")
        )

        fun getNeighbors(state: String): List<String> {
            val normalizedState = state.trim()
            return graph[normalizedState] ?: graph.entries.firstOrNull {
                it.key.equals(normalizedState, ignoreCase = true)
            }?.value ?: emptyList()
        }

        fun areNeighbors(state1: String, state2: String): Boolean {
            val neighbors = getNeighbors(state1)
            return neighbors.any { it.equals(state2.trim(), ignoreCase = true) }
        }

        fun getAllStates(): List<String> {
            return graph.keys.toList()
        }
    }

    /**
     * Records an anonymous disease scan telemetry record to Supabase PostgREST endpoint.
     */
    suspend fun recordScan(payload: DiseaseScanPayload): Result<Boolean> = withContext(Dispatchers.IO) {
        try {
            val url = "$SUPABASE_URL/rest/v1/disease_scans"
            val payloadJson = JSONObject().apply {
                put("disease_name", payload.diseaseName)
                put("crop_name", payload.cropName)
                put("state", payload.state)
                put("district", payload.district)
                put("severity", payload.severity)
                put("confidence", payload.confidence)
                if (payload.latitude != null) put("latitude", payload.latitude)
                if (payload.longitude != null) put("longitude", payload.longitude)
            }.toString()

            val mediaType = "application/json".toMediaTypeOrNull()
            val body = payloadJson.toRequestBody(mediaType)
            val request = Request.Builder()
                .url(url)
                .addHeader("apikey", SUPABASE_ANON_KEY)
                .addHeader("Authorization", "Bearer $SUPABASE_ANON_KEY")
                .addHeader("Content-Type", "application/json")
                .addHeader("Prefer", "return=minimal")
                .post(body)
                .build()

            val response = httpClient.newCall(request).execute()
            val isSuccess = response.isSuccessful || response.code in 200..299
            response.close()
            Result.success(isSuccess)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Fetches active outbreak alerts targeted at a specific state (both Epicenter & Early Warning).
     */
    suspend fun fetchActiveAlerts(state: String): Result<List<OutbreakAlertRecord>> = withContext(Dispatchers.IO) {
        try {
            val stateEnc = URLEncoder.encode(state.trim(), "UTF-8")
            val url = "$SUPABASE_URL/rest/v1/outbreak_alerts?select=*&target_state=eq.$stateEnc&is_active=eq.true&order=scan_count.desc"
            val request = Request.Builder()
                .url(url)
                .addHeader("apikey", SUPABASE_ANON_KEY)
                .addHeader("Authorization", "Bearer $SUPABASE_ANON_KEY")
                .addHeader("Accept", "application/json")
                .get()
                .build()

            val response = httpClient.newCall(request).execute()
            val bodyStr = response.body?.string() ?: ""
            val isSuccess = response.isSuccessful
            response.close()

            if (!isSuccess || bodyStr.isBlank()) {
                return@withContext Result.success(emptyList())
            }

            val alerts = try {
                json.decodeFromString<List<OutbreakAlertRecord>>(bodyStr)
            } catch (_: Exception) {
                parseAlertsFromJsonArray(bodyStr)
            }

            Result.success(alerts)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Fetches all active outbreak alerts across the country.
     */
    suspend fun fetchAllActiveAlerts(): Result<List<OutbreakAlertRecord>> = withContext(Dispatchers.IO) {
        try {
            val url = "$SUPABASE_URL/rest/v1/outbreak_alerts?select=*&is_active=eq.true&order=scan_count.desc"
            val request = Request.Builder()
                .url(url)
                .addHeader("apikey", SUPABASE_ANON_KEY)
                .addHeader("Authorization", "Bearer $SUPABASE_ANON_KEY")
                .addHeader("Accept", "application/json")
                .get()
                .build()

            val response = httpClient.newCall(request).execute()
            val bodyStr = response.body?.string() ?: ""
            val isSuccess = response.isSuccessful
            response.close()

            if (!isSuccess || bodyStr.isBlank()) {
                return@withContext Result.success(emptyList())
            }

            val alerts = try {
                json.decodeFromString<List<OutbreakAlertRecord>>(bodyStr)
            } catch (_: Exception) {
                parseAlertsFromJsonArray(bodyStr)
            }

            Result.success(alerts)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    private fun parseAlertsFromJsonArray(bodyStr: String): List<OutbreakAlertRecord> {
        val list = mutableListOf<OutbreakAlertRecord>()
        try {
            val jsonArray = JSONArray(bodyStr)
            for (i in 0 until jsonArray.length()) {
                val obj = jsonArray.getJSONObject(i)
                list.add(
                    OutbreakAlert(
                        id = obj.optString("id", ""),
                        diseaseName = obj.optString("disease_name", ""),
                        sourceState = obj.optString("source_state", ""),
                        targetState = obj.optString("target_state", ""),
                        alertType = obj.optString("alert_type", "EPICENTER"),
                        severity = obj.optString("severity", "MODERATE"),
                        scanCount = obj.optInt("scan_count", 0),
                        thresholdDensity = obj.optInt("threshold_density", 100),
                        timeWindowHours = obj.optInt("time_window_hours", 168),
                        message = obj.optString("message", ""),
                        recommendedAction = obj.optString("recommended_action", ""),
                        predictedMarketImpactPct = obj.optDouble("predicted_market_impact_pct", 0.0),
                        isActive = obj.optBoolean("is_active", true),
                        createdAt = obj.optString("created_at", ""),
                        updatedAt = obj.optString("updated_at", "")
                    )
                )
            }
        } catch (_: Exception) {}
        return list
    }

    /**
     * Pure density evaluation function.
     * Evaluates a collection of scans against an outbreak density threshold within a rolling time window.
     * Generates EPICENTER alerts for source states and fans out EARLY_WARNING alerts to all adjacent states.
     *
     * @param scans List of historical or incoming disease scans.
     * @param threshold Scan count threshold required to trigger an outbreak (default: 100).
     * @param windowHours Rolling time window in hours (default: 168 hours = 7 days).
     * @return Generated list of OutbreakAlertRecord items.
     */
    fun evaluateDensityThreshold(
        scans: List<DiseaseScanRecord>,
        threshold: Int = 100,
        windowHours: Long = 168
    ): List<OutbreakAlertRecord> {
        if (scans.isEmpty()) return emptyList()

        val now = System.currentTimeMillis()
        val windowMillis = windowHours * 3600 * 1000L

        // Reference timestamp: latest scan timestamp or current system time
        val maxScanTimestamp = scans.maxOfOrNull { it.scannedAt } ?: now
        val referenceTime = if (maxScanTimestamp > now) maxScanTimestamp else now
        val windowStart = referenceTime - windowMillis

        // 1. Filter scans within the rolling window
        val recentScans = scans.filter { it.scannedAt in windowStart..referenceTime || it.scannedAt == 0L }

        // 2. Group by disease name and state
        val groupedScans = recentScans.groupBy { Pair(it.diseaseName.trim(), it.state.trim()) }

        val generatedAlerts = mutableListOf<OutbreakAlertRecord>()

        for ((key, scanList) in groupedScans) {
            val (diseaseName, state) = key
            val scanCount = scanList.size

            if (scanCount >= threshold && diseaseName.isNotBlank() && state.isNotBlank()) {
                // Determine severity and impact percentages
                val (severityStr, epicenterImpact, neighborBaseImpact) = when {
                    scanCount >= 300 -> Triple("CRITICAL", 35.0, 20.0)
                    scanCount >= 200 -> Triple("HIGH", 25.0, 15.0)
                    else -> Triple("MODERATE", 15.0, 8.0)
                }

                val neighborSeverity = if (severityStr == "CRITICAL") "HIGH" else "MODERATE"

                val epicenterMessage = "CRITICAL OUTBREAK DETECTED: $diseaseName outbreak confirmed in $state with $scanCount recent scan detections crossing density threshold ($threshold)."
                val epicenterAction = "Deploy immediate containment, quarantine affected fields, apply targeted chemical/biological fungicides or insecticides, and alert local Krishi Vigyan Kendra (KVK)."

                // 1. Create Epicenter Alert
                val epicenterAlert = OutbreakAlert(
                    id = "alert-epicenter-${state.lowercase().replace(" ", "-")}-${diseaseName.lowercase().replace(" ", "-")}",
                    diseaseName = diseaseName,
                    sourceState = state,
                    targetState = state,
                    alertType = "EPICENTER",
                    severity = severityStr,
                    scanCount = scanCount,
                    thresholdDensity = threshold,
                    timeWindowHours = windowHours.toInt(),
                    message = epicenterMessage,
                    recommendedAction = epicenterAction,
                    predictedMarketImpactPct = epicenterImpact,
                    isActive = true
                )
                generatedAlerts.add(epicenterAlert)

                // 2. Fan out Early Warning alerts for all adjacent neighboring states
                val neighbors = StateAdjacencyGraph.getNeighbors(state)
                for (neighbor in neighbors) {
                    val neighborMessage = "EARLY WARNING: Outbreak of $diseaseName detected in neighboring $state ($scanCount active scans). High risk of trans-boundary spore/pest vector transmission to $neighbor."
                    val neighborAction = "Inspect border district fields daily, prepare preventative spraying protocols, and monitor Mandi arrivals from $state."

                    val earlyWarningAlert = OutbreakAlert(
                        id = "alert-early-${neighbor.lowercase().replace(" ", "-")}-${diseaseName.lowercase().replace(" ", "-")}",
                        diseaseName = diseaseName,
                        sourceState = state,
                        targetState = neighbor,
                        alertType = "EARLY_WARNING",
                        severity = neighborSeverity,
                        scanCount = scanCount,
                        thresholdDensity = threshold,
                        timeWindowHours = windowHours.toInt(),
                        message = neighborMessage,
                        recommendedAction = neighborAction,
                        predictedMarketImpactPct = neighborBaseImpact,
                        isActive = true
                    )
                    generatedAlerts.add(earlyWarningAlert)
                }
            }
        }

        return generatedAlerts
    }
}
