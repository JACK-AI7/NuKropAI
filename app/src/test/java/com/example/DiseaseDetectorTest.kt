package com.example

import android.graphics.Bitmap
import android.graphics.Color
import androidx.test.core.app.ApplicationProvider
import com.example.ml.DetectionSource
import com.example.ml.DiseaseDetector
import com.example.ml.DiseaseSeverityLevel
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [33])
class DiseaseDetectorTest {

    private lateinit var detector: DiseaseDetector

    @Before
    fun setup() {
        val context = ApplicationProvider.getApplicationContext<android.content.Context>()
        detector = DiseaseDetector(context)
    }

    @Test
    fun testDetectorInitializesGracefullyWithoutCrash() {
        assertNotNull(detector)
    }

    @Test
    fun testHealthyGreenBitmapClassification() {
        // Create an all-healthy green leaf bitmap
        val bitmap = Bitmap.createBitmap(128, 128, Bitmap.Config.ARGB_8888)
        for (x in 0 until 128) {
            for (y in 0 until 128) {
                bitmap.setPixel(x, y, Color.rgb(34, 139, 34)) // Forest Green
            }
        }

        val result = detector.classify(bitmap, "Tomato")
        assertTrue("All green leaf should be diagnosed as healthy", result.isHealthy)
        assertEquals(DiseaseSeverityLevel.HEALTHY, result.severity)
        assertTrue("Confidence should be in 70..98 range", result.confidence in 70..98)
        assertEquals(DetectionSource.BOTANICAL_FEATURE_EXTRACTION, result.executionSource)
    }

    @Test
    fun testNecroticLesionSpotClassification() {
        // Create a green leaf bitmap with dark necrotic brown spots in the center
        val bitmap = Bitmap.createBitmap(128, 128, Bitmap.Config.ARGB_8888)
        for (x in 0 until 128) {
            for (y in 0 until 128) {
                if (x in 40..88 && y in 40..88) {
                    bitmap.setPixel(x, y, Color.rgb(90, 40, 20)) // Dark necrotic brown
                } else {
                    bitmap.setPixel(x, y, Color.rgb(40, 140, 40)) // Green
                }
            }
        }

        val result = detector.classify(bitmap, "Tomato")
        assertFalse("Leaf with heavy brown spots must be diagnosed as diseased", result.isHealthy)
        assertTrue("Confidence must be dynamically calculated between 72 and 97", result.confidence in 72..97)
        assertTrue("Must provide symptoms and CIBRC treatments", result.treatment.isNotBlank())
        assertTrue("Must provide products with retail links", result.products.isNotEmpty())
    }

    @Test
    fun testClassifyToScanDataMapping() {
        val bitmap = Bitmap.createBitmap(128, 128, Bitmap.Config.ARGB_8888)
        for (x in 0 until 128) {
            for (y in 0 until 128) {
                bitmap.setPixel(x, y, Color.rgb(220, 220, 220)) // White powdery mildew
            }
        }

        val scanData = detector.classifyToScanData(bitmap, "Chilli")
        assertNotNull(scanData)
        assertTrue("Confidence must be in 70..98", scanData.confidence in 70..98)
        assertTrue(scanData.treatment.isNotBlank())
        assertTrue(scanData.products.isNotEmpty())
    }

    @Test
    fun testOptimizeInferenceEdgeMetrics() {
        val metrics = detector.optimizeInferenceEdge()
        assertNotNull(metrics)
        assertTrue(metrics.containsKey("averageInferenceLatencyMs"))
        assertTrue(metrics.containsKey("cpuCoresAvailable"))
        assertTrue(metrics.containsKey("nativeBufferPoolBytes"))
    }
}
