package com.example.satellite

object SatelliteTelemetryManager {
    // In a real application, inject Retrofit interface for NASA/Sentinel APIs
    fun fetchNDVI(lat: Double, lng: Double): String {
        return "Healthy Vegetation Density"
    }
    
    fun getSoilMoisture(lat: Double, lng: Double): String {
        return "Low Soil Moisture"
    }
}
