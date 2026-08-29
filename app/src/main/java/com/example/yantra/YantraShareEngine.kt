package com.example.yantra

enum class MachineryCategory(val displayName: String, val icon: String) {
    TRACTOR("Tractor & Tillage", "🚜"),
    DRONE_SPRAYER("Multi-Rotor Spraying Drone", "🛸"),
    COMBINE_HARVESTER("Multi-Crop Combine Harvester", "🌾"),
    LASER_LEVELER("Precision Laser Land Leveler", "📐"),
    SOLAR_PUMP("High-Discharge Solar Pump", "💧")
}

data class YantraEquipmentListing(
    val equipmentId: String,
    val title: String,
    val category: MachineryCategory,
    val ownerName: String,
    val ownerPhone: String,
    val distanceKm: Double,
    val hourlyRateRupees: Double,
    val dailyRateRupees: Double,
    val perAcreRateRupees: Double,
    val hasVettedOperator: Boolean,
    val engineHoursLogged: Double,
    val fuelLevelPct: Int,
    val batteryHealthPct: Int,
    val isGeofencedAndSafe: Boolean,
    val nextServiceDueHours: Int,
    val reliabilityRating: Double // 1.0 to 5.0
)

enum class EscrowStatus(val label: String, val badgeColorHex: Long) {
    FUNDS_LOCKED("FUNDS SECURED IN ESCROW", 0xFF2196F3),
    TASK_IN_PROGRESS("OPERATING IN FIELD", 0xFFFF9800),
    RELEASED_TO_OWNER("PAYMENT COMPLETED", 0xFF4CAF50),
    DISPUTED_REFUND("UNDER MEDIATION", 0xFFF44336)
}

data class EscrowBookingContract(
    val bookingId: String,
    val equipmentTitle: String,
    val renterName: String,
    val ownerName: String,
    val totalEscrowAmount: Double,
    val status: EscrowStatus,
    val bookingDuration: String,
    val operatorIncluded: Boolean
)

object YantraShareEngine {

    fun getSampleListings(): List<YantraEquipmentListing> {
        return listOf(
            YantraEquipmentListing(
                equipmentId = "EQ-TRAC-575",
                title = "Mahindra 575 DI (45 HP PowerPlus)",
                category = MachineryCategory.TRACTOR,
                ownerName = "Verma Agro Solutions",
                ownerPhone = "9876543210",
                distanceKm = 2.4,
                hourlyRateRupees = 450.0,
                dailyRateRupees = 3200.0,
                perAcreRateRupees = 600.0,
                hasVettedOperator = true,
                engineHoursLogged = 1248.5,
                fuelLevelPct = 82,
                batteryHealthPct = 95,
                isGeofencedAndSafe = true,
                nextServiceDueHours = 150,
                reliabilityRating = 4.9
            ),
            YantraEquipmentListing(
                equipmentId = "EQ-DRON-T40",
                title = "DJI Agras T40 40L Pesticide Drone",
                category = MachineryCategory.DRONE_SPRAYER,
                ownerName = "AgriFlight Tech Co-op",
                ownerPhone = "9812345678",
                distanceKm = 4.1,
                hourlyRateRupees = 1200.0,
                dailyRateRupees = 8500.0,
                perAcreRateRupees = 350.0,
                hasVettedOperator = true,
                engineHoursLogged = 340.0,
                fuelLevelPct = 100,
                batteryHealthPct = 98,
                isGeofencedAndSafe = true,
                nextServiceDueHours = 80,
                reliabilityRating = 5.0
            ),
            YantraEquipmentListing(
                equipmentId = "EQ-HARV-900",
                title = "John Deere W70 Paddy Harvester",
                category = MachineryCategory.COMBINE_HARVESTER,
                ownerName = "Reddy Farming Syndicate",
                ownerPhone = "9988776655",
                distanceKm = 6.8,
                hourlyRateRupees = 2200.0,
                dailyRateRupees = 16000.0,
                perAcreRateRupees = 1800.0,
                hasVettedOperator = true,
                engineHoursLogged = 2100.0,
                fuelLevelPct = 65,
                batteryHealthPct = 88,
                isGeofencedAndSafe = true,
                nextServiceDueHours = 45,
                reliabilityRating = 4.8
            ),
            YantraEquipmentListing(
                equipmentId = "EQ-LASER-30",
                title = "Spectra Precision Dual Laser Land Leveler",
                category = MachineryCategory.LASER_LEVELER,
                ownerName = "Kisan Equipment Pool",
                ownerPhone = "9440188291",
                distanceKm = 3.2,
                hourlyRateRupees = 800.0,
                dailyRateRupees = 5500.0,
                perAcreRateRupees = 950.0,
                hasVettedOperator = true,
                engineHoursLogged = 890.0,
                fuelLevelPct = 78,
                batteryHealthPct = 92,
                isGeofencedAndSafe = true,
                nextServiceDueHours = 120,
                reliabilityRating = 4.7
            )
        )
    }

    fun createEscrowContract(listing: YantraEquipmentListing, rentalAcreage: Double, includeOperator: Boolean): EscrowBookingContract {
        val operatorCost = if (includeOperator) 300.0 else 0.0
        val total = (listing.perAcreRateRupees * rentalAcreage) + operatorCost

        return EscrowBookingContract(
            bookingId = "ESCROW-YN-${System.currentTimeMillis() % 100000}",
            equipmentTitle = listing.title,
            renterName = "You (Verified Farmer)",
            ownerName = listing.ownerName,
            totalEscrowAmount = total,
            status = EscrowStatus.FUNDS_LOCKED,
            bookingDuration = "$rentalAcreage Acres Operation",
            operatorIncluded = includeOperator
        )
    }
}
