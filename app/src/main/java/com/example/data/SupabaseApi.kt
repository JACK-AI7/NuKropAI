package com.example.data

import com.example.SupabaseApi as CoreSupabaseApi
import com.example.MandiRecord
import com.example.mandipilot.MandiArbitrageOption
import com.example.agristack.AgriStackPassport
import com.example.gramhaul.GramHaulTripPlan
import com.example.bioshield.OutbreakCluster
import com.example.model.DiseaseScanPayload
import com.example.model.OutbreakAlertRecord

/**
 * Data package bridge for Supabase PostgREST endpoints.
 */
object SupabaseApi {
    suspend fun fetchMandiRates(state: String, commodity: String): List<MandiRecord> =
        CoreSupabaseApi.fetchMandiRates(state, commodity)

    suspend fun syncProfile(userEmail: String, name: String, state: String, district: String, crop: String, lat: Double, lng: Double) =
        CoreSupabaseApi.syncProfile(userEmail, name, state, district, crop, lat, lng)

    suspend fun recordDiseaseScan(payload: DiseaseScanPayload): Boolean =
        CoreSupabaseApi.recordDiseaseScan(payload)

    suspend fun fetchOutbreakAlerts(state: String): List<OutbreakAlertRecord> =
        CoreSupabaseApi.fetchOutbreakAlerts(state)

    suspend fun fetchMandiArbitrageQuotes(commodity: String, state: String, originDistrict: String = ""): List<MandiArbitrageOption> =
        CoreSupabaseApi.fetchMandiArbitrageQuotes(commodity, state, originDistrict)

    suspend fun fetchAgriStackPassport(farmerId: String): AgriStackPassport? =
        CoreSupabaseApi.fetchAgriStackPassport(farmerId)

    suspend fun fetchAvailableGramHaulTrips(originDistrict: String = "", destinationMandi: String = "", isColdChain: Boolean = false): List<GramHaulTripPlan> =
        CoreSupabaseApi.fetchAvailableGramHaulTrips(originDistrict, destinationMandi, isColdChain)

    suspend fun bookGramHaulSlot(tripId: String, farmerId: String, commodity: String, weightQuintals: Double, allocatedFare: Double, pickupPoint: String): Boolean =
        CoreSupabaseApi.bookGramHaulSlot(tripId, farmerId, commodity, weightQuintals, allocatedFare, pickupPoint)

    suspend fun fetchSpatialOutbreakClusters(state: String = ""): List<OutbreakCluster> =
        CoreSupabaseApi.fetchSpatialOutbreakClusters(state)
}
