package com.example.biorx

import kotlin.math.roundToInt

enum class OrganicFormulationType(
    val title: String,
    val purpose: String,
    val baseAcreDose: String,
    val icon: String
) {
    JEEVAMRUTHA("Jeevamrutha (జీవామృతం / जीवामृत)", "Soil Microbiome & Nitrogen Activation", "200 Liters / Acre", "🌿"),
    BEEJAMRUTHA("Beejamrutha (బీజామృతం / बीजामृत)", "Organic Seed Coating & Anti-Fungal Shield", "For 50 kg Seeds", "🌱"),
    NEEMASTRA("Neemastra (వేప అస్త్రం / नीमास्त्र)", "Broad-Spectrum Sucking Pest & Caterpillar Control", "100 Liters / Acre (5% Spray)", "🍃"),
    DASHAPARNI_ARK("Dashaparni Ark (దశపర్ణి కషాయం / दशपर्णी अर्क)", "Severe Pest Infestation & Stem Borer Defense", "200 Liters / Acre (10% Dilution)", "🛡️"),
    AGNIASTRA("Agniastra (అగ్ని అస్త్రం / अग्न्यास्त्र)", "Leaf Miner, Borer & Hard-Shelled Beetle Annihilator", "100 Liters / Acre", "🔥"),
    TRICHODERMA_BIO("Trichoderma viride Bio-Culture", "Root Rot, Wilt & Soil-Borne Fungal Inoculation", "2.5 kg + 100 kg FYM / Acre", "🧪")
}

data class ScaledIngredient(
    val ingredientName: String,
    val scaledQuantityFormatted: String,
    val roleInFormulation: String
)

data class BioRxPrescription(
    val formulation: OrganicFormulationType,
    val farmAcreage: Double,
    val cropStage: String, // "Seedling / Nursery", "Vegetative Growth", "Flowering", "Grain Filling / Fruiting"
    val scaledIngredients: List<ScaledIngredient>,
    val preparationSteps: List<String>,
    val applicationMethod: String,
    val recommendedSprayIntervalDays: Int,
    val costSavedVsChemicalPesticidesRupees: Double,
    val soilRegenerationScoreGain: Int // +1 to +10 points towards organic certification
)

object BioRxEngine {

    fun calculatePrescription(
        formulation: OrganicFormulationType,
        acreage: Double = 4.5,
        cropStage: String = "Vegetative Growth"
    ): BioRxPrescription {
        val multiplier = acreage.coerceAtLeast(0.5)

        val (ingredients, prepSteps, appMethod, sprayInterval, chemSavings, scoreGain) = when (formulation) {
            OrganicFormulationType.JEEVAMRUTHA -> {
                val cowDungKg = (10.0 * multiplier * 10).roundToInt() / 10.0
                val cowUrineL = (10.0 * multiplier * 10).roundToInt() / 10.0
                val jaggeryKg = (2.0 * multiplier * 10).roundToInt() / 10.0
                val besanFlourKg = (2.0 * multiplier * 10).roundToInt() / 10.0
                val virginSoilHandfuls = (2.0 * multiplier).toInt().coerceAtLeast(2)
                val waterLiters = (200.0 * multiplier * 10).roundToInt() / 10.0

                Tuple6(
                    listOf(
                        ScaledIngredient("Fresh Desi Cow Dung", "$cowDungKg kg", "Microbial culture source"),
                        ScaledIngredient("Desi Cow Urine (Gomutra)", "$cowUrineL Liters", "Organic nitrogen & anti-microbial agent"),
                        ScaledIngredient("Organic Black Jaggery", "$jaggeryKg kg", "Carbohydrate energy for bacteria fermentation"),
                        ScaledIngredient("Gram/Besan Flour (Pulse)", "$besanFlourKg kg", "Protein substrate for fungal propagation"),
                        ScaledIngredient("Virgin Farm Ridge Soil", "$virginSoilHandfuls Handfuls", "Native microbial inoculant"),
                        ScaledIngredient("Chlorine-Free Well Water", "$waterLiters Liters", "Fermentation medium")
                    ),
                    listOf(
                        "1. Take $waterLiters Liters water in a large plastic barrel under shade.",
                        "2. Add $cowDungKg kg cow dung and $cowUrineL L cow urine; mix well with a wooden stick.",
                        "3. Mix $jaggeryKg kg jaggery and $besanFlourKg kg flour thoroughly without lumps.",
                        "4. Add $virginSoilHandfuls handfuls of virgin ridge soil. Stir clockwise for 5 minutes twice daily.",
                        "5. Cover with gunny bag and ferment for 48 to 72 hours. Apply within 7 days."
                    ),
                    "Apply through drip irrigation or flooding with irrigation water @ $waterLiters Liters for your $acreage-acre field.",
                    15,
                    multiplier * 1450.0,
                    8
                )
            }

            OrganicFormulationType.NEEMASTRA -> {
                val neemLeavesKg = (10.0 * multiplier * 10).roundToInt() / 10.0
                val cowDungKg = (2.0 * multiplier * 10).roundToInt() / 10.0
                val cowUrineL = (5.0 * multiplier * 10).roundToInt() / 10.0
                val waterL = (100.0 * multiplier * 10).roundToInt() / 10.0

                Tuple6(
                    listOf(
                        ScaledIngredient("Crushed Neem Leaves / Pulp", "$neemLeavesKg kg", "Azadirachtin insect anti-feedant"),
                        ScaledIngredient("Desi Cow Dung", "$cowDungKg kg", "Binding & fermenting catalyst"),
                        ScaledIngredient("Desi Cow Urine", "$cowUrineL Liters", "Alkaline repellent medium"),
                        ScaledIngredient("Clean Water", "$waterL Liters", "Aerosol spray carrier")
                    ),
                    listOf(
                        "1. Crush $neemLeavesKg kg fresh neem leaves into paste.",
                        "2. Mix paste with $cowDungKg kg cow dung and $cowUrineL L cow urine in a barrel.",
                        "3. Add $waterL Liters water and stir well.",
                        "4. Ferment in shade for 48 hours, stirring twice daily.",
                        "5. Filter through muslin cloth and spray directly without dilution."
                    ),
                    "Foliar spray during early morning or late afternoon targeting undersides of leaves.",
                    10,
                    multiplier * 1200.0,
                    6
                )
            }

            else -> {
                val bioPowderKg = (2.5 * multiplier * 10).roundToInt() / 10.0
                val fymCompostKg = (100.0 * multiplier * 10).roundToInt() / 10.0

                Tuple6(
                    listOf(
                        ScaledIngredient("Trichoderma viride 1% WP", "$bioPowderKg kg", "Beneficial bio-fungicide"),
                        ScaledIngredient("Well-Decomposed FYM / Vermicompost", "$fymCompostKg kg", "Organic carrier substrate")
                    ),
                    listOf(
                        "1. Mix $bioPowderKg kg Trichoderma powder with $fymCompostKg kg moist farmyard manure.",
                        "2. Keep under shade covered with moist gunny bags for 7 days to allow fungal mycelium proliferation.",
                        "3. Broadcast uniformly near root zones before sowing or during inter-cultivation."
                    ),
                    "Soil incorporation near active root feeder zones followed by light watering.",
                    21,
                    multiplier * 1800.0,
                    9
                )
            }
        }

        return BioRxPrescription(
            formulation = formulation,
            farmAcreage = acreage,
            cropStage = cropStage,
            scaledIngredients = ingredients,
            preparationSteps = prepSteps,
            applicationMethod = appMethod,
            recommendedSprayIntervalDays = sprayInterval,
            costSavedVsChemicalPesticidesRupees = chemSavings,
            soilRegenerationScoreGain = scoreGain
        )
    }
}

private data class Tuple6<A, B, C, D, E, F>(
    val first: A, val second: B, val third: C, val fourth: D, val fifth: E, val sixth: F
)
