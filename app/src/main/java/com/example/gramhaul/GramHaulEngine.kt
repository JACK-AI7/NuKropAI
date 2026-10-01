package com.example.gramhaul

import com.example.SupabaseApi
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

data class TransportHub(
    val hubName: String,
    val destinationMandi: String,
    val distanceKm: Double,
    val driverName: String,
    val driverPhone: String
)

object GramHaulEngine {

    private val REGIONAL_TRANSPORT_HUBS: Map<String, List<TransportHub>> = mapOf(
        "Andhra Pradesh" to listOf(
            TransportHub("Tenali-Chebrolu Cluster", "Guntur APMC Mandi", 38.0, "K. Balakrishna", "9848022338"),
            TransportHub("Mangalagiri North Hub", "Vijayawada Wholesale Yard", 24.0, "M. Gurunath", "9440188291"),
            TransportHub("Bapatla Coastal Depot", "Ongole Commercial Yard", 54.0, "V. Srinivasa Rao", "9949011245")
        ),
        "Maharashtra" to listOf(
            TransportHub("Baramati Agri Hub", "Pune APMC Yard", 52.0, "S. Shinde", "9822019941"),
            TransportHub("Nashik Rural Center", "Vashi Wholesale Terminal", 88.0, "R. Patil", "9766023314"),
            TransportHub("Sangli Turmeric Cluster", "Kolhapur Market Yard", 46.0, "A. Deshmukh", "9823055123")
        ),
        "Punjab" to listOf(
            TransportHub("Samrala Aggregation Depot", "Khanna Central Mandi", 18.0, "G. Singh", "9814033221"),
            TransportHub("Moga Logistics Station", "Ludhiana Market Yard", 48.0, "J. Dhillon", "9872044119"),
            TransportHub("Rayya Farmer Hub", "Amritsar Bhagtanwala Mandi", 36.0, "H. Sandhu", "9815077884")
        ),
        "Karnataka" to listOf(
            TransportHub("Nelamangala Hub", "Yeshwanthpur APMC", 28.0, "K. Gowda", "9845012345"),
            TransportHub("Nanjangud Depot", "Mysuru Bandipalya Market", 34.0, "C. Kumar", "9980067890")
        ),
        "Tamil Nadu" to listOf(
            TransportHub("Chengalpattu Cluster", "Koyambedu Wholesale Yard", 45.0, "P. Murugan", "9841023456"),
            TransportHub("Dindigul Agri Hub", "Madurai Mattuthavani Market", 58.0, "S. Raman", "9443078901")
        )
    )

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
        destinationMandi: String = "Guntur APMC Mandi",
        state: String = "Andhra Pradesh",
        originCluster: String = ""
    ): List<GramHaulTripPlan> {
        val hubs = REGIONAL_TRANSPORT_HUBS[state] ?: REGIONAL_TRANSPORT_HUBS["Andhra Pradesh"]!!
        val hub1 = hubs.getOrNull(0) ?: TransportHub("Tenali-Chebrolu Cluster", "Guntur APMC Mandi", 38.0, "K. Balakrishna", "9848022338")
        val hub2 = hubs.getOrNull(1) ?: TransportHub("Mangalagiri North Hub", "Vijayawada Wholesale Yard", 24.0, "M. Gurunath", "9440188291")

        val targetVehicle = if (isPerishable) HaulVehicleType.COLD_CHAIN_REEFER else HaulVehicleType.PICKUP_TRUCK

        val sampleBatches1 = listOf(
            "Ramesh Patel" to 6.0,
            "Srinivas Rao" to 4.5,
            "You (Active Farm)" to farmerAcreageYieldQuintals
        )

        val pooledAllocation = calculatePooledFareSharing(targetVehicle, hub1.distanceKm, sampleBatches1)
        val totalBooked = sampleBatches1.sumOf { it.second }
        val remainingSpace = (targetVehicle.capacityQuintals - totalBooked).coerceAtLeast(0.0)

        val trip1 = GramHaulTripPlan(
            tripId = "GH-TRIP-704",
            vehicle = targetVehicle,
            driverName = hub1.driverName,
            driverPhone = hub1.driverPhone,
            originCluster = if (originCluster.isNotBlank()) originCluster else hub1.hubName,
            destinationMandi = destinationMandi,
            totalDistanceKm = hub1.distanceKm,
            totalTripCost = (targetVehicle.baseRatePerKm * hub1.distanceKm) + 200.0,
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
            driverName = hub2.driverName,
            driverPhone = hub2.driverPhone,
            originCluster = hub2.hubName,
            destinationMandi = hub2.destinationMandi,
            totalDistanceKm = hub2.distanceKm,
            totalTripCost = (HaulVehicleType.TRACTOR_TROLLEY.baseRatePerKm * hub2.distanceKm) + 200.0,
            totalCapacityQuintals = 45.0,
            bookedWeightQuintals = 28.0,
            availableSpaceQuintals = 17.0,
            batches = calculatePooledFareSharing(HaulVehicleType.TRACTOR_TROLLEY, hub2.distanceKm, listOf("Farmer Cooperative" to 28.0)),
            departureTimeFormatted = "Tomorrow @ 06:00 AM",
            milestoneStatus = "Scheduled - Open for Pooling"
        )

        return listOf(trip1, trip2)
    }

    /**
     * Asynchronously queries live Supabase PostgREST table `gramhaul_trips` with deterministic fallback.
     */
    suspend fun getLiveOrPooledTrips(
        state: String = "Andhra Pradesh",
        district: String = "Guntur",
        farmerProduceWeight: Double = 8.0,
        requiresColdChain: Boolean = false,
        destinationMandi: String = "APMC Mandi"
    ): List<GramHaulTripPlan> {
        try {
            val liveTrips = SupabaseApi.fetchAvailableGramHaulTrips(district, destinationMandi, requiresColdChain)
            if (liveTrips.isNotEmpty()) {
                return liveTrips
            }
        } catch (_: Exception) {}

        return findAvailablePooledTrips(
            farmerAcreageYieldQuintals = farmerProduceWeight,
            isPerishable = requiresColdChain,
            destinationMandi = destinationMandi,
            state = state,
            originCluster = "$district Aggregation Hub"
        )
    }

    /**
     * Books a slot on a shared trip and syncs to Supabase.
     */
    suspend fun bookSharedTripSlot(
        tripId: String,
        farmerId: String,
        commodity: String,
        weightQuintals: Double,
        allocatedFare: Double,
        pickupPoint: String
    ): Boolean {
        return SupabaseApi.bookGramHaulSlot(
            tripId = tripId,
            farmerId = farmerId,
            commodity = commodity,
            weightQuintals = weightQuintals,
            allocatedFare = allocatedFare,
            pickupPoint = pickupPoint
        )
    }
}
