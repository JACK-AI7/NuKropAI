package com.example

import io.github.jan.supabase.createSupabaseClient
import io.github.jan.supabase.auth.Auth
import io.github.jan.supabase.postgrest.Postgrest
import io.github.jan.supabase.realtime.Realtime
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.net.URLEncoder
import java.util.concurrent.TimeUnit

val SUPABASE_URL = "https://yxjqseiegwjdfnccdchk.supabase.co"
val SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl4anFzZWllZ3dqZGZuY2NkY2hrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU5NDU2NTMsImV4cCI6MjEwMTUyMTY1M30.J4swglpV5qu3hRZFll3aqhG1Y2G9mUllvXMjKq6Ikmo"

val supabase = createSupabaseClient(
    supabaseUrl = SUPABASE_URL,
    supabaseKey = SUPABASE_ANON_KEY
) {
    install(Auth)
    install(Postgrest)
    install(Realtime)
}

object SupabaseApi {
    private val httpClient = OkHttpClient.Builder()
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .build()

    /**
     * Query real mandi live rates directly from Supabase DB table `mandi_live_rates`
     */
    suspend fun fetchMandiRates(state: String, commodity: String): List<MandiRecord> = withContext(Dispatchers.IO) {
        try {
            val stateEnc = URLEncoder.encode(state.trim(), "UTF-8")
            val commEnc = URLEncoder.encode(commodity.trim(), "UTF-8")
            val url = "$SUPABASE_URL/rest/v1/mandi_live_rates?select=*&state=ilike.*$stateEnc*&commodity=ilike.*$commEnc*&order=id.desc&limit=20"
            val request = Request.Builder()
                .url(url)
                .addHeader("apikey", SUPABASE_ANON_KEY)
                .addHeader("Authorization", "Bearer $SUPABASE_ANON_KEY")
                .addHeader("Accept", "application/json")
                .get()
                .build()

            val (isSuccessful, body) = httpClient.newCall(request).execute().use { response ->
                Pair(response.isSuccessful, response.body?.string() ?: "")
            }
            if (!isSuccessful || body.isBlank()) return@withContext emptyList()

            val jsonArray = JSONArray(body)
            val list = mutableListOf<MandiRecord>()
            for (i in 0 until jsonArray.length()) {
                val obj = jsonArray.getJSONObject(i)
                list.add(
                    MandiRecord(
                        state = obj.optString("state", state),
                        district = obj.optString("district", "Central"),
                        market = obj.optString("market", "Main Market"),
                        commodity = obj.optString("commodity", commodity),
                        variety = obj.optString("variety", "Standard"),
                        minPrice = obj.optDouble("min_price", 2000.0),
                        maxPrice = obj.optDouble("max_price", 2600.0),
                        modalPrice = obj.optDouble("modal_price", 2400.0),
                        arrivalDate = obj.optString("arrival_date", "Today")
                    )
                )
            }
            list
        } catch (e: Exception) {
            emptyList()
        }
    }

    /**
     * Sync user location / profile to Supabase `user_profiles` for nearby farmer discovery
     */
    suspend fun syncProfile(userEmail: String, name: String, state: String, district: String, crop: String, lat: Double, lng: Double) = withContext(Dispatchers.IO) {
        try {
            val jsonPayload = JSONObject().apply {
                put("email", userEmail)
                put("full_name", name)
                put("state", state)
                put("district", district)
                put("primary_crop", crop)
                put("latitude", lat)
                put("longitude", lng)
            }.toString()

            val url = "$SUPABASE_URL/rest/v1/user_profiles"
            val mediaType = "application/json".toMediaTypeOrNull()
            val body = jsonPayload.toRequestBody(mediaType)
            val request = Request.Builder()
                .url(url)
                .addHeader("apikey", SUPABASE_ANON_KEY)
                .addHeader("Authorization", "Bearer $SUPABASE_ANON_KEY")
                .addHeader("Prefer", "resolution=merge-duplicates")
                .post(body)
                .build()

            httpClient.newCall(request).execute().use { /* close response stream */ }
        } catch (_: Exception) {}
    }

    /**
     * Record an anonymous disease scan in Supabase `disease_scans`
     */
    suspend fun recordDiseaseScan(payload: com.example.model.DiseaseScanPayload): Boolean = withContext(Dispatchers.IO) {
        try {
            val result = DiseaseAggregationService.recordScan(payload)
            result.getOrDefault(false)
        } catch (_: Exception) {
            false
        }
    }

    /**
     * Fetch active outbreak alerts for a given target state
     */
    suspend fun fetchOutbreakAlerts(state: String): List<com.example.model.OutbreakAlertRecord> = withContext(Dispatchers.IO) {
        try {
            val result = DiseaseAggregationService.fetchActiveAlerts(state)
            result.getOrDefault(emptyList())
        } catch (_: Exception) {
            emptyList()
        }
    }
}

