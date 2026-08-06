package com.example

data class Subsidy(
    val name: String,
    val description: String,
    val amount: String,
    val url: String
)

object SubsidiesApiService {
    fun getSubsidiesForState(state: String): List<Subsidy> {
        val central = listOf(
            Subsidy(
                "PM-KISAN Samman Nidhi",
                "Direct income support of ₹6,000 per year for landholding farmer families.",
                "₹6,000 / Year",
                "https://pmkisan.gov.in/"
            ),
            Subsidy(
                "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
                "Comprehensive crop insurance scheme against non-preventable natural risks.",
                "Variable",
                "https://pmfby.gov.in/"
            ),
            Subsidy(
                "PM Kusum Yojana",
                "Subsidy for setting up standalone solar pumps and solarization of grid connected pumps.",
                "Up to 60% Subsidy",
                "https://pmkusum.mnre.gov.in/"
            )
        )
        
        val stateSpecific = when (state.lowercase()) {
            "punjab", "haryana" -> listOf(
                Subsidy(
                    "Crop Residue Management Scheme",
                    "Subsidy for machinery to manage paddy straw and prevent stubble burning.",
                    "50%-80% Subsidy",
                    "https://agrimachinery.nic.in/"
                )
            )
            "maharashtra" -> listOf(
                Subsidy(
                    "MahaDBT Agriculture Scheme",
                    "Tractor and agriculture implement subsidy for registered farmers.",
                    "Up to 50% Subsidy",
                    "https://mahadbtmahait.gov.in/"
                )
            )
            "telangana" -> listOf(
                Subsidy(
                    "Rythu Bandhu",
                    "Investment support scheme providing ₹10,000 per acre per year.",
                    "₹10,000 / Acre",
                    "http://rythubandhu.telangana.gov.in/"
                )
            )
            "andhra pradesh" -> listOf(
                Subsidy(
                    "YSR Rythu Bharosa",
                    "Financial assistance of ₹13,500 per farmer family per year.",
                    "₹13,500 / Year",
                    "https://ysrrythubharosa.ap.gov.in/"
                )
            )
            else -> listOf(
                Subsidy(
                    "Paramparagat Krishi Vikas Yojana",
                    "Financial assistance for adopting organic farming practices.",
                    "₹50,000 / Hectare",
                    "https://pgsindia-ncof.gov.in/"
                )
            )
        }
        
        return central + stateSpecific
    }
}
