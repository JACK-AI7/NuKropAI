package com.example

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class Views176MatrixTest {

    private val supportedLanguages = listOf(
        "te", "hi", "ta", "kn", "ml", "mr", "bn", "gu", "pa", "or", "en"
    )

    private val all16Views = listOf(
        "home",
        "community",
        "calculators",
        "autopilot",
        "finance",
        "scan",
        "market",
        "profile",
        "saved_reports",
        "equipment_rental",
        "farm_khata",
        "bioshield_radar",
        "mandipilot",
        "gramhaul",
        "agristack_passport",
        "biorx"
    )

    private val viewKeyMappings = mapOf(
        "home" to listOf("nav_home", "good_farmer", "quick_actions"),
        "community" to listOf("nav_chat", "chat_placeholder", "chat_title"),
        "calculators" to listOf("ai_advisor", "ask_question"),
        "autopilot" to listOf("nav_autopilot", "field_navigator", "gps_route"),
        "finance" to listOf("nav_finance", "loan_subsidy", "govt_schemes"),
        "scan" to listOf("nav_scan", "scanner_title", "take_photo", "ai_disease"),
        "market" to listOf("nav_market", "market_rates", "modal_price"),
        "profile" to listOf("nav_profile", "edit_location", "save"),
        "saved_reports" to listOf("my_tracked", "weather_alerts"),
        "equipment_rental" to listOf("nav_rental", "quick_actions"),
        "farm_khata" to listOf("nav_khata", "modal_price"),
        "bioshield_radar" to listOf("pest_radar", "high_risk", "outbreak_alerts_title"),
        "mandipilot" to listOf("market_impact_title", "predicted_peak_price", "affected_mandis"),
        "gramhaul" to listOf("market_rates_action", "live_mandi_prices"),
        "agristack_passport" to listOf("subsidy_title", "ai_matcher", "find_subsidies"),
        "biorx" to listOf("ai_disease", "ai_soil", "scan_crop")
    )

    @Test
    fun testTotalViewsCountIs176() {
        val totalMatrixCombinations = all16Views.size * supportedLanguages.size
        assertEquals(176, totalMatrixCombinations)
        assertEquals(16, all16Views.size)
        assertEquals(11, supportedLanguages.size)
    }

    @Test
    fun testAll176ViewsLocalizationResolution() {
        var evaluatedCount = 0
        val failureLog = mutableListOf<String>()

        for (screen in all16Views) {
            val requiredKeys = viewKeyMappings[screen] ?: listOf("nav_home")
            for (lang in supportedLanguages) {
                evaluatedCount++
                for (key in requiredKeys) {
                    val resolvedString = AppStrings.get(key, lang)
                    if (resolvedString.isBlank() || resolvedString == key) {
                        failureLog.add("Screen: $screen, Lang: $lang, Missing Key: $key")
                    }
                }
            }
        }

        assertTrue("Failures detected in 176-view matrix: $failureLog", failureLog.isEmpty())
        assertEquals(176, evaluatedCount)
    }
}
