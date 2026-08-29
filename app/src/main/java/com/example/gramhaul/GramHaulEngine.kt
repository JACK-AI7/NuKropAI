package com.example.gramhaul

import kotlin.math.roundToInt

enum class HaulVehicleType(val displayName: String, val capacityQuintals: Double, val baseRatePerKm: Double, val icon: String) {
    PICKUP_TRUCK("Mahindra Bolero Maxi Truck", 18.0, 18.0, "🛻"),
    TRACTOR_TROLLEY("Dual-Axle Tractor Trolley", 45.0, 24.0, "🚜"),
    MINI_TRUCK("Tata Ace (Chhota Hathi)", 10.0, 14.0, "🚚"),
    COLD_CHAIN_REEFER("Insulated Cold-Chain Reefer", 25.0, 32.0, "❄️")
}

data class PooledLoadBatch(
    val farmerName: String,
    val commodity: String,
    val weightQuintals: Double,
    val pickupVillage: String,
    val allocatedCostRupees: Double,
    val costSavedPctVsSoloHire: Int
)

data class GramHaulTripPlan(
    val tripId: String,
    val vehicle: HaulVehicleType,
    val driverName: String,
    val driverPhone: String,
    val originCluster: String,
    val destinationMandi: String,
    val totalDistanceKm: Double,
    val totalTripCost: Double,
    val totalCapacityQuintals: Double,
    val bookedWeightQuintals: Double,
    val availableSpaceQuintals: Double,
    val batches: List<PooledLoadBatch>,
    val departureTimeFormatted: String,
    val milestoneStatus: String
)

object GramHaulEngine {

    /**
     * Calculates proportional cost-sharing for pooled batches.
     * Total Fare = Base Vehicle Cost + (Distance * RatePerKm)
     * Farmer Share = Total Fare * (Farmer Weight / Total Trip Weight)
     */
    fun calculatePooledFareSharing(
        vehicle: HaulVehicleType,
        totalDistanceKm: Double,
        batches: List<Pair<String, Double>> // Pair(FarmerName, WeightQuintals)
    ): List<PooledLoadBatch> {
        val totalTripWeight = batches.sumOf { it.second }.coerceAtLeast(1.0)
        val totalTripCost = (vehicle.baseRatePerKm * totalDistanceKm) + 200.0 // Base fuel + loading buffer

        return batches.map { (name, weight) ->
            val proportionalFare = (totalTripCost * (weight / totalTripWeight))
            val soloCost = totalTripCost // Solo hiring would require paying for full vehicle
            val savedPct = (((soloCost - proportionalFare) / soloCost) * 100.0).roundToInt().coerceIn(15, 78)

            PooledLoadBatch(
                farmerName = name,
                commodity = "Harvest Produce",
                weightQuintals = weight,
                pickupVillage = "Village Hub Station",
                allocatedCostRupees = (proportionalFare * 10.0).roundToInt() / 10.0,
                costSavedPctVsSoloHire = savedPct
            )
        }
    }

    /**
     * Matches best available pooled vehicle for smallholder harvest batch within sub-2 seconds
     */
    fun findAvailablePooledTrips(
        farmerAcreageYieldQuintals: Double = 8.0,
        isPerishable: Boolean = false,
        destinationMandi: String = "Guntur APMC Mandi"
    ): List<GramHaulTripPlan> {
        val targetVehicle = if (isPerishable) HaulVehicleType.COLD_CHAIN_REEFER else HaulVehicleType.PICKUP_TRUCK

        val sampleBatches = listOf(
            "Ramesh Patel" to 6.0,
            "Srinivas Rao" to 4.5,
            "You (Active Farm)" to farmerAcreageYieldQuintals
        )

        val pooledAllocation = calculatePooledFareSharing(targetVehicle, 38.0, sampleBatches)
        val totalBooked = sampleBatches.sumOf { it.second }
        val remainingSpace = (targetVehicle.capacityQuintals - totalBooked).coerceAtLeast(0.0)

        val trip1 = GramHaulTripPlan(
            tripId = "GH-TRIP-704",
            vehicle = targetVehicle,
            driverName = "K. Balakrishna",
            driverPhone = "9848022338",
            originCluster = "Tenali-Chebrolu Cluster",
            destinationMandi = destinationMandi,
            totalDistanceKm = 38.0,
            totalTripCost = (targetVehicle.baseRatePerKm * 38.0) + 200.0,
            totalCapacityQuintals = targetVehicle.capacityQuintals,
            bookedWeightQuintals = totalBooked,
            availableSpaceQuintals = remainingSpace,
            batches = pooledAllocation,
            departureTimeFormatted = "Today @ 04:30 PM",
            milestoneStatus = "En Route to Pickup Hub #2"
        )

        val trip2 = GramHaulTripPlan(
            tripId = "GH-TRIP-812",
            vehicle = HaulVehicleType.TRACTOR_TROLLEY,
            driverName = "M. Gurunath",
            driverPhone = "9440188291",
            originCluster = "Mangalagiri North Hub",
            destinationMandi = "Vijayawada Wholesale Yard",
            totalDistanceKm = 24.0,
            totalTripCost = (HaulVehicleType.TRACTOR_TROLLEY.baseRatePerKm * 24.0) + 200.0,
            totalCapacityQuintals = 45.0,
            bookedWeightQuintals = 28.0,
            availableSpaceQuintals = 17.0,
            batches = calculatePooledFareSharing(HaulVehicleType.TRACTOR_TROLLEY, 24.0, listOf("Farmer Cooperative" to 28.0)),
            departureTimeFormatted = "Tomorrow @ 06:00 AM",
            milestoneStatus = "Scheduled - Open for Pooling"
        )

        return listOf(trip1, trip2)
    }
}
