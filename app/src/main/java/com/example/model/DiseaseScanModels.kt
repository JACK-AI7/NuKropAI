package com.example.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
enum class AlertType {
    @SerialName("EPICENTER")
    EPICENTER,
    @SerialName("EARLY_WARNING")
    EARLY_WARNING
}

@Serializable
enum class ScanSeverity {
    @SerialName("LOW")
    LOW,
    @SerialName("MODERATE")
    MODERATE,
    @SerialName("HIGH")
    HIGH,
    @SerialName("CRITICAL")
    CRITICAL
}

/**
 * Payload sent from Android client to backend when an on-device scan is performed.
 */
@Serializable
data class DiseaseScanPayload(
    @SerialName("disease_name")
    val diseaseName: String,
    @SerialName("crop_name")
    val cropName: String = "General",
    @SerialName("state")
    val state: String,
    @SerialName("district")
    val district: String = "",
    @SerialName("severity")
    val severity: String = "Moderate",
    @SerialName("confidence")
    val confidence: Int = 90,
    @SerialName("latitude")
    val latitude: Double? = null,
    @SerialName("longitude")
    val longitude: Double? = null,
    @SerialName("scanned_at")
    val scannedAt: Long = System.currentTimeMillis()
)

/**
 * Record representing a scan logged in the database or evaluated locally.
 */
@Serializable
data class DiseaseScanRecord(
    @SerialName("id")
    val id: String = "",
    @SerialName("disease_name")
    val diseaseName: String,
    @SerialName("crop_name")
    val cropName: String = "General",
    @SerialName("state")
    val state: String,
    @SerialName("district")
    val district: String = "",
    @SerialName("latitude")
    val latitude: Double? = null,
    @SerialName("longitude")
    val longitude: Double? = null,
    @SerialName("severity")
    val severity: String = "Moderate",
    @SerialName("confidence")
    val confidence: Int = 90,
    @SerialName("scanned_at")
    val scannedAt: Long = System.currentTimeMillis()
)

/**
 * Active Outbreak Alert (Epicenter or Neighbor Early Warning)
 */
@Serializable
data class OutbreakAlert(
    @SerialName("id")
    val id: String = "",
    @SerialName("disease_name")
    val diseaseName: String,
    @SerialName("source_state")
    val sourceState: String,
    @SerialName("target_state")
    val targetState: String,
    @SerialName("alert_type")
    val alertType: String = "EPICENTER", // "EPICENTER" or "EARLY_WARNING"
    @SerialName("severity")
    val severity: String = "MODERATE",  // "LOW", "MODERATE", "HIGH", "CRITICAL"
    @SerialName("scan_count")
    val scanCount: Int = 0,
    @SerialName("threshold_density")
    val thresholdDensity: Int = 100,
    @SerialName("time_window_hours")
    val timeWindowHours: Int = 168,
    @SerialName("message")
    val message: String = "",
    @SerialName("recommended_action")
    val recommendedAction: String = "",
    @SerialName("predicted_market_impact_pct")
    val predictedMarketImpactPct: Double = 0.0,
    @SerialName("is_active")
    val isActive: Boolean = true,
    @SerialName("created_at")
    val createdAt: String = "",
    @SerialName("updated_at")
    val updatedAt: String = ""
)

typealias OutbreakAlertRecord = OutbreakAlert
