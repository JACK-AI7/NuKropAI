package com.example

import android.graphics.Bitmap
import android.graphics.Color
import org.junit.Assert.*
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [34])
class SoilScannerFallbackTest {

    @Test
    fun testParseSoilJson_ValidGeminiPayload() {
        val validJson = """
        {
          "soilType": "Alluvial Clay Loam",
          "texture": "Fine",
          "estimatedPH": "7.1",
          "organicMatter": "High",
          "deficiencies": ["Phosphorus", "Potassium"],
          "suitableCrops": ["Paddy", "Sugarcane"],
          "improvements": "Apply balanced DAP and compost",
          "details": "High moisture-holding alluvial basin profile.",
          "fertilizers": [
            {
              "name": "IFFCO DAP 18:46:0",
              "dose": "50 kg/acre",
              "stores": [{"name": "IFFCO Bazar", "url": "https://iffcobazar.in", "icon": "🛒"}]
            }
          ]
        }
        """.trimIndent()

        val result = parseSoilJson(validJson)
        assertNotNull(result)
        assertEquals("Alluvial Clay Loam", result.soilType)
        assertEquals("7.1", result.estimatedPH)
        assertTrue(result.deficiencies.contains("Phosphorus"))
        assertEquals("IFFCO DAP 18:46:0", result.fertilizers.first().first.first)
    }

    @Test
    fun testParseSoilJson_ApiErrorFallback() {
        val errorRaw = "API Error: 429 Resource has been exhausted (e.g. check quota)."
        val result = parseSoilJson(errorRaw)
        assertNotNull("Must return non-null fallback on API Error", result)
        assertEquals("Loamy Soil Profile", result.soilType)
        assertTrue(result.suitableCrops.contains("Wheat"))
        assertTrue(result.fertilizers.isNotEmpty())
    }

    @Test
    fun testParseSoilJson_BlankStringFallback() {
        val result = parseSoilJson("   ")
        assertNotNull("Must return non-null fallback on blank string", result)
        assertEquals("Loamy Soil Profile", result.soilType)
    }

    @Test
    fun testParseSoilJson_MalformedJsonFallback() {
        val malformed = "{ soilType: 'Broken', estimatedPH: 6.8 "
        val result = parseSoilJson(malformed)
        assertNotNull("Must return non-null fallback on malformed JSON", result)
        assertEquals("Loamy Soil Profile", result.soilType)
    }

    @Test
    fun testClassifySoilFromBitmap_RedSoil() {
        val bitmap = Bitmap.createBitmap(64, 64, Bitmap.Config.ARGB_8888)
        for (x in 0 until 64) {
            for (y in 0 until 64) {
                bitmap.setPixel(x, y, Color.rgb(180, 50, 40)) // Dominant red
            }
        }
        val result = classifySoilFromBitmap(bitmap)
        assertTrue("Must identify red/laterite profile", result.soilType.contains("Red Laterite"))
        assertTrue(result.suitableCrops.contains("Groundnut"))
    }

    @Test
    fun testClassifySoilFromBitmap_BlackSoil() {
        val bitmap = Bitmap.createBitmap(64, 64, Bitmap.Config.ARGB_8888)
        for (x in 0 until 64) {
            for (y in 0 until 64) {
                bitmap.setPixel(x, y, Color.rgb(40, 35, 30)) // Low luminance black soil
            }
        }
        val result = classifySoilFromBitmap(bitmap)
        assertTrue("Must identify black cotton vertisol profile", result.soilType.contains("Black Cotton"))
        assertTrue(result.suitableCrops.contains("Cotton"))
    }

    @Test
    fun testSoilScanDataToJson_RoundTrip() {
        val original = getDefaultSoilScanData("Test round trip")
        val jsonStr = soilScanDataToJson(original)
        val parsed = parseSoilJson(jsonStr)
        assertNotNull(parsed)
        assertEquals(original.soilType, parsed.soilType)
        assertEquals(original.estimatedPH, parsed.estimatedPH)
        assertEquals(original.fertilizers.size, parsed.fertilizers.size)
    }
}
