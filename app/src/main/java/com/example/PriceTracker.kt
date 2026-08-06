package com.example

import android.content.Context
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.Serializable

@Serializable
data class TrackedCrop(
    val id: String,
    val state: String,
    val mandi: String,
    val crop: String,
    val basePrice: Double,
    val targetPrice: Double = 0.0
)

object PriceTracker {
    private const val PREFS_NAME = "price_tracker_prefs"
    private const val KEY_TRACKED = "tracked_crops_list"

    fun getTrackedCrops(context: Context): List<TrackedCrop> {
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        val json = prefs.getString(KEY_TRACKED, "[]") ?: "[]"
        return try {
            Json.decodeFromString(json)
        } catch (e: Exception) {
            emptyList()
        }
    }

    fun addOrUpdateTrackedCrop(context: Context, state: String, mandi: String, crop: String, currentPrice: Double, targetPrice: Double = 0.0) {
        val current = getTrackedCrops(context).toMutableList()
        val id = "${state}_${mandi}_${crop}".lowercase().replace(" ", "_")
        
        // If updating an existing one without providing targetPrice, preserve the old one.
        val existingTarget = current.find { it.id == id }?.targetPrice ?: 0.0
        val finalTarget = if (targetPrice > 0.0) targetPrice else existingTarget

        current.removeAll { it.id == id }
        current.add(TrackedCrop(id, state, mandi, crop, currentPrice, finalTarget))
        
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        prefs.edit().putString(KEY_TRACKED, Json.encodeToString(current)).apply()
    }
    
    fun isTracked(context: Context, state: String, mandi: String, crop: String): Boolean {
        val current = getTrackedCrops(context)
        val id = "${state}_${mandi}_${crop}".lowercase().replace(" ", "_")
        return current.any { it.id == id }
    }
}
