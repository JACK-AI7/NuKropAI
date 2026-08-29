package com.example.bioshield

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlin.math.*

data class GeoLocationPoint(
    val latitude: Double,
    val longitude: Double,
    val districtName: String,
    val stateName: String
)

data class OutbreakCluster(
    val clusterId: String,
    val diseaseName: String,
    val cropName: String,
    val epicenter: GeoLocationPoint,
    val radiusKm: Double,
    val totalScansDetected: Int,
    val riskSeverity: OutbreakRiskLevel,
    val avgMicroclimateHumidity: Double,
    val ndviStressIndex: Double, // 0.0 to 1.0 (lower is higher stress)
    val bioDefenseActionPlan: String,
    val estimatedContainmentDays: Int
)

enum class OutbreakRiskLevel(val label: String, val badgeColorHex: Long) {
    WATCH("MODERATE RISK", 0xFFFFC107),
    WARNING("HIGH OUTBREAK RISK", 0xFFFF9800),
    CRITICAL("CRITICAL BIO-HAZARD", 0xFFF44336)
}

object BioShieldRadarEngine {

    /**
     * Computes Haversine distance in Kilometers between two coordinates
     */
    fun calculateDistanceKm(lat1: Double, lon1: Double, lat2: Double, lon2: Double): Double {
        val r = 6371.0 // Earth radius in km
        val dLat = Math.toRadians(lat2 - lat1)
        val dLon = Math.toRadians(lon2 - lon1)
        val a = sin(dLat / 2).pow(2) +
                cos(Math.toRadians(lat1)) * cos(Math.toRadians(lat2)) *
                sin(dLon / 2).pow(2)
        val c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return r * c
    }

    /**
     * Evaluates spatial-temporal cluster rule:
     * Triggers active cluster if >= 3 matching diagnostic scans occur in a 10km radius within 48 hours.
     */
    fun evaluateOutbreakCluster(
        scanCoordinates: List<Pair<Double, Double>>,
        diseaseName: String,
        cropName: String,
        epicenter: GeoLocationPoint,
        humidityPct: Double = 84.0,
        leafWetnessHours: Double = 8.5
    ): OutbreakCluster? {
        val maxRadiusKm = 10.0
        val proximateScans = scanCoordinates.count { (lat, lon) ->
            calculateDistanceKm(epicenter.latitude, epicenter.longitude, lat, lon) <= maxRadiusKm
        }

        if (proximateScans < 3) return null

        val riskLevel = when {
            proximateScans >= 15 || (humidityPct > 85.0 && leafWetnessHours > 10.0) -> OutbreakRiskLevel.CRITICAL
            proximateScans >= 6 || humidityPct > 75.0 -> OutbreakRiskLevel.WARNING
            else -> OutbreakRiskLevel.WATCH
        }

        val ndviScore = when (riskLevel) {
            OutbreakRiskLevel.CRITICAL -> 0.38
            OutbreakRiskLevel.WARNING -> 0.54
            OutbreakRiskLevel.WATCH -> 0.68
        }

        val actionPlan = when (diseaseName.lowercase()) {
            "blast", "fungal blight", "late blight" ->
                "Apply preemptive Bio-Barrier: Spray Pseudomonas fluorescens @ 10g/L along border ridges. Maintain 3-meter buffer zone."
            "fall armyworm", "spodoptera", "pest" ->
                "Deploy Neemastra (5% neem oil) + Pheromone Traps @ 8 traps/acre along windward perimeter."
            else ->
                "Quarantine affected sector. Apply Trichoderma viride bio-culture to soil and monitor within 5km radius."
        }

        return OutbreakCluster(
            clusterId = "BIO-CLUST-${System.currentTimeMillis() % 100000}",
            diseaseName = diseaseName,
            cropName = cropName,
            epicenter = epicenter,
            radiusKm = maxRadiusKm,
            totalScansDetected = proximateScans,
            riskSeverity = riskLevel,
            avgMicroclimateHumidity = humidityPct,
            ndviStressIndex = ndviScore,
            bioDefenseActionPlan = actionPlan,
            estimatedContainmentDays = if (riskLevel == OutbreakRiskLevel.CRITICAL) 12 else 6
        )
    }

    /**
     * Checks if a user farm is within the danger perimeter of an active cluster
     */
    fun isFarmInDangerZone(userLat: Double, userLon: Double, cluster: OutbreakCluster): Boolean {
        val dist = calculateDistanceKm(userLat, userLon, cluster.epicenter.latitude, cluster.epicenter.longitude)
        return dist <= (cluster.radiusKm + 5.0) // 5km early warning buffer zone
    }
}
