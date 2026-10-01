package com.example

import org.junit.Assert.*
import org.junit.Test

class SprayAdvisoryStressTest {

    @Test
    fun stressTestAll24HoursWindowContinuityAndCoverage() {
        val windowCounts = mutableMapOf<String, Int>()
        val validWindows = listOf(
            "00:00 - 03:00",
            "03:00 - 06:00",
            "06:00 - 09:00",
            "09:00 - 12:00",
            "12:00 - 15:00",
            "15:00 - 18:00",
            "18:00 - 21:00",
            "21:00 - 24:00"
        )

        for (hour in 0..23) {
            val label = WeatherService.getSprayWindowLabel(hour)
            assertNotNull("Hour $hour window label must not be null", label)
            assertTrue("Window label '$label' must be in 8 standard windows", validWindows.contains(label))
            
            // Check parsing format HH:00 - HH:00
            val parts = label.split(" - ")
            assertEquals("Window must have start and end time", 2, parts.size)
            val startHour = parts[0].substringBefore(":").toInt()
            val endHour = parts[1].substringBefore(":").toInt()
            assertEquals("Window must span exactly 3 hours", 3, endHour - startHour)
            assertTrue("Start hour must be <= current hour", startHour <= hour)
            assertTrue("End hour must be > current hour", endHour > hour)

            windowCounts[label] = (windowCounts[label] ?: 0) + 1
        }

        // Verify exactly 8 windows, each covering exactly 3 hours
        assertEquals("Must have exactly 8 unique windows across 24h", 8, windowCounts.size)
        for ((window, count) in windowCounts) {
            assertEquals("Window '$window' must cover exactly 3 distinct hours", 3, count)
        }
    }

    @Test
    fun stressTestHourBoundaryClamping() {
        // Out of bounds hours should be clamped gracefully without crash
        val negativeHour = WeatherService.getSprayWindowLabel(-5)
        assertEquals("00:00 - 03:00", negativeHour)

        val overflowHour = WeatherService.getSprayWindowLabel(25)
        assertEquals("21:00 - 24:00", overflowHour)

        val largeOverflowHour = WeatherService.getSprayWindowLabel(100)
        assertEquals("21:00 - 24:00", largeOverflowHour)
    }

    @Test
    fun stressTestDeltaTCalculationsAcrossExtremeTemperaturesAndHumidities() {
        // 1. Extreme Humidity: 0.0% RH (Should coerce to 1.0% and evaluate without NaN/Inf)
        val deltaT_RH0 = WeatherService.calculateDeltaT(tempC = 25.0, humidityPct = 0.0)
        assertFalse("Delta-T at 0% RH must not be NaN", deltaT_RH0.isNaN())
        assertFalse("Delta-T at 0% RH must not be Infinite", deltaT_RH0.isInfinite())
        assertTrue("Delta-T at 0% RH should be large (> 10.0)", deltaT_RH0 > 10.0)

        // 2. Extreme Humidity: 100.0% RH (Wet bulb ~= Dry bulb, Delta-T ~= 0.0)
        val deltaT_RH100 = WeatherService.calculateDeltaT(tempC = 25.0, humidityPct = 100.0)
        assertFalse("Delta-T at 100% RH must not be NaN", deltaT_RH100.isNaN())
        assertTrue("Delta-T at 100% RH must be near 0.0 (got $deltaT_RH100)", deltaT_RH100 <= 1.0)
        assertTrue("Delta-T must never be negative", deltaT_RH100 >= 0.0)

        // 3. Extreme High Temperature: 50.0°C (Desert heatwave)
        val deltaT_HighTemp = WeatherService.calculateDeltaT(tempC = 50.0, humidityPct = 15.0)
        assertFalse("Delta-T at 50°C must not be NaN", deltaT_HighTemp.isNaN())
        assertTrue("Delta-T at 50°C / 15% RH should be extreme (> 15.0)", deltaT_HighTemp > 15.0)

        // 4. Freezing Temperature: 0.0°C
        val deltaT_Freezing = WeatherService.calculateDeltaT(tempC = 0.0, humidityPct = 80.0)
        assertFalse("Delta-T at 0°C must not be NaN", deltaT_Freezing.isNaN())
        assertTrue("Delta-T at 0°C must be non-negative", deltaT_Freezing >= 0.0)

        // 5. Sub-zero Temperature: -5.0°C
        val deltaT_SubZero = WeatherService.calculateDeltaT(tempC = -5.0, humidityPct = 70.0)
        assertFalse("Delta-T at -5°C must not be NaN", deltaT_SubZero.isNaN())
        assertTrue("Delta-T at -5°C must be non-negative", deltaT_SubZero >= 0.0)
    }

    @Test
    fun stressTestHighWindEdgeCases() {
        // High wind speeds: 30 km/h, 50 km/h, 120 km/h (Cyclone)
        val testWinds = listOf(20.1, 25.0, 30.0, 45.0, 80.0, 150.0)
        for (wind in testWinds) {
            val advisory = WeatherService.calculateSprayAdvisory(
                hour = 8,
                temp = 24.0,
                humidity = 60.0,
                windSpeed = wind,
                precipProb = 0.0
            )
            assertEquals("Wind speed $wind km/h must trigger AVOID_SPRAYING", SprayCondition.AVOID_SPRAYING, advisory.condition)
            assertFalse("Wind speed $wind km/h must not be permitted", advisory.condition.isPermitted)
            assertEquals("Wind speed $wind km/h must have wind extreme advice key", "spray_advice_wind_extreme", advisory.adviceResKey)
            assertTrue("Advice text must mention wind drift", advisory.adviceText.contains("wind drift", ignoreCase = true))
        }
    }

    @Test
    fun stressTestExtremeHeatAdvisory() {
        val testTemps = listOf(35.1, 38.0, 42.0, 50.0)
        for (temp in testTemps) {
            val advisory = WeatherService.calculateSprayAdvisory(
                hour = 10,
                temp = temp,
                humidity = 50.0,
                windSpeed = 10.0,
                precipProb = 0.0
            )
            assertEquals("Temp $temp°C must trigger AVOID_SPRAYING", SprayCondition.AVOID_SPRAYING, advisory.condition)
            assertEquals("Temp $temp°C must trigger extreme evaporation key", "spray_advice_delta_t_extreme", advisory.adviceResKey)
        }
    }

    @Test
    fun stressTestDeadCalmInversionHours() {
        // Night/dawn hours (21..23, 0..5) with wind < 2.0 must trigger inversion risk
        val inversionHours = listOf(0, 1, 2, 3, 4, 5, 21, 22, 23)
        for (h in inversionHours) {
            val advisory = WeatherService.calculateSprayAdvisory(
                hour = h,
                temp = 20.0,
                humidity = 60.0,
                windSpeed = 1.0,
                precipProb = 0.0
            )
            assertEquals("Hour $h with calm wind (1.0 km/h) must trigger AVOID_SPRAYING due to inversion", 
                SprayCondition.AVOID_SPRAYING, advisory.condition)
            assertEquals("spray_advice_inversion_risk", advisory.adviceResKey)
        }

        // Daytime hours (08:00, 10:00, 16:00) with gentle wind (1.0 km/h) and normal Delta-T (e.g. 5.0)
        // should NOT trigger night inversion risk
        val daytimeAdvisory = WeatherService.calculateSprayAdvisory(
            hour = 8,
            temp = 24.0,
            humidity = 60.0,
            windSpeed = 1.5,
            precipProb = 0.0
        )
        assertNotEquals("spray_advice_inversion_risk", daytimeAdvisory.adviceResKey)
    }

    @Test
    fun stressTestAdvisoryGridAcrossCombinations() {
        // Exhaustive grid evaluation to ensure no unhandled exceptions or NaN values
        val hours = listOf(0, 4, 8, 13, 16, 19, 22)
        val temps = listOf(0.0, 15.0, 25.0, 33.0, 45.0)
        val humidities = listOf(0.0, 20.0, 55.0, 85.0, 100.0)
        val winds = listOf(0.5, 5.0, 14.0, 18.0, 35.0)
        val precips = listOf(0.0, 15.0, 30.0, 75.0)

        var evaluatedCount = 0
        for (h in hours) {
            for (t in temps) {
                for (rh in humidities) {
                    for (w in winds) {
                        for (p in precips) {
                            val advisory = WeatherService.calculateSprayAdvisory(
                                hour = h,
                                temp = t,
                                humidity = rh,
                                windSpeed = w,
                                precipProb = p
                            )
                            assertNotNull(advisory)
                            assertNotNull(advisory.condition)
                            assertNotNull(advisory.windowLabel)
                            assertNotNull(advisory.adviceResKey)
                            assertNotNull(advisory.adviceText)
                            assertFalse("Delta-T must not be NaN", advisory.deltaT.isNaN())
                            assertTrue("Delta-T must be >= 0.0", advisory.deltaT >= 0.0)
                            evaluatedCount++
                        }
                    }
                }
            }
        }
        assertEquals("Should evaluate all 7*5*5*5*4 = 3500 parameter combinations", 3500, evaluatedCount)
    }
}
