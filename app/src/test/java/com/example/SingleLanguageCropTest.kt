package com.example

import com.example.ui.AllAvailableCrops
import com.example.ui.getLocalizedCrops
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class SingleLanguageCropTest {

    private val supportedLanguages = listOf("te", "hi", "ta", "kn", "ml", "mr", "bn", "gu", "pa", "or", "en")

    @Test
    fun testAll11LanguagesHaveLocalizedCrops() {
        for (lang in supportedLanguages) {
            val crops = getLocalizedCrops(lang)
            assertEquals("Language $lang should have 22 localized crops", 22, crops.size)
            for (crop in crops) {
                assertFalse("Crop name in $lang must not be blank", crop.name.isBlank())
                assertFalse("Crop emoji in $lang must not be blank", crop.iconEmoji.isBlank())
            }
        }
    }

    @Test
    fun testStrictSingleLanguageScriptPurity() {
        // Script regex definitions
        val indicScripts = mapOf(
            "hi" to Regex("^[\\u0900-\\u097F\\s]+$"), // Devanagari (Hindi)
            "mr" to Regex("^[\\u0900-\\u097F\\s]+$"), // Devanagari (Marathi)
            "te" to Regex("^[\\u0C00-\\u0C7F\\s]+$"), // Telugu
            "ta" to Regex("^[\\u0B80-\\u0BFF\\s]+$"), // Tamil
            "kn" to Regex("^[\\u0C80-\\u0CFF\\s]+$"), // Kannada
            "ml" to Regex("^[\\u0D00-\\u0D7F\\s]+$"), // Malayalam
            "bn" to Regex("^[\\u0980-\\u09FF\\s]+$"), // Bengali
            "gu" to Regex("^[\\u0A80-\\u0AFF\\s]+$"), // Gujarati
            "pa" to Regex("^[\\u0A00-\\u0A7F\\s]+$"), // Gurmukhi (Punjabi)
            "or" to Regex("^[\\u0B00-\\u0B7F\\s]+$")  // Odia
        )

        val latinRegex = Regex(".*[a-zA-Z].*")

        for ((lang, regex) in indicScripts) {
            val crops = getLocalizedCrops(lang)
            for (crop in crops) {
                assertTrue(
                    "Crop '" + crop.name + "' in language '" + lang + "' must match Indic script",
                    regex.matches(crop.name)
                )
                assertFalse(
                    "Crop '" + crop.name + "' in language '" + lang + "' must not contain Latin characters",
                    latinRegex.matches(crop.name)
                )
            }
        }
    }
}
