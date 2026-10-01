package com.example

import org.junit.Assert.*
import org.junit.Test

class SprayAdvisoryCalculatorTest {

    @Test
    fun testContinuous3HourWindowMappingForEveryHour() {
        val expectedWindows = mapOf(
            0 to "00:00 - 03:00",
            1 to "00:00 - 03:00",
            2 to "00:00 - 03:00",
            3 to "03:00 - 06:00",
            4 to "03:00 - 06:00",
            5 to "03:00 - 06:00",
            6 to "06:00 - 09:00",
            7 to "06:00 - 09:00",
            8 to "06:00 - 09:00",
            9 to "09:00 - 12:00",
            10 to "09:00 - 12:00",
            11 to "09:00 - 12:00",
            12 to "12:00 - 15:00",
            13 to "12:00 - 15:00",
            14 to "12:00 - 15:00",
            15 to "15:00 - 18:00",
            16 to "15:00 - 18:00",
            17 to "15:00 - 18:00",
            18 to "18:00 - 21:00",
            19 to "18:00 - 21:00",
            20 to "18:00 - 21:00",
            21 to "21:00 - 24:00",
            22 to "21:00 - 24:00",
            23 to "21:00 - 24:00"
        )

        for (hour in 0..23) {
            val label = WeatherService.getSprayWindowLabel(hour)
            assertEquals("Hour $hour must map to correct 3h continuous window", expectedWindows[hour], label)
        }
    }

    @Test
    fun testPsychrometricDeltaTCalculation() {
        // 25°C, 60% RH -> Delta-T ~ 5.5°C (Ideal zone 2-8°C)
        val deltaTIdeal = WeatherService.calculateDeltaT(25.0, 60.0)
        assertTrue("Delta-T for 25C/60% should be in 4.5..6.5 range (got $deltaTIdeal)", deltaTIdeal in 4.5..6.5)

        // 35°C, 20% RH -> High evaporation (Delta-T > 10°C)
        val deltaTHigh = WeatherService.calculateDeltaT(35.0, 20.0)
        assertTrue("Delta-T for 35C/20% should be > 10.0 (got $deltaTHigh)", deltaTHigh > 10.0)

        // 20°C, 95% RH -> Low Delta-T (< 2°C)
        val deltaTLow = WeatherService.calculateDeltaT(20.0, 95.0)
        assertTrue("Delta-T for 20C/95% should be < 2.0 (got $deltaTLow)", deltaTLow < 2.0)
    }

    @Test
    fun testFavourableSprayConditions() {
        // Morning 07:00, 24°C, 60% RH, 8 km/h wind, 0% rain prob
        val advisory = WeatherService.calculateSprayAdvisory(
            hour = 7,
            temp = 24.0,
            humidity = 60.0,
            windSpeed = 8.0,
            precipProb = 0.0
        )
        assertEquals("06:00 - 09:00", advisory.windowLabel)
        assertEquals(SprayCondition.FAVOURABLE, advisory.condition)
        assertTrue(advisory.deltaT in 2.0..8.0)
    }

    @Test
    fun testHighRainProbabilityForcesAvoidSpraying() {
        val advisory = WeatherService.calculateSprayAdvisory(
            hour = 8,
            temp = 24.0,
            humidity = 60.0,
            windSpeed = 8.0,
            precipProb = 65.0
        )
        assertEquals(SprayCondition.AVOID_SPRAYING, advisory.condition)
        assertEquals("spray_advice_rain_high", advisory.adviceResKey)
    }

    @Test
    fun testHighWindDriftForcesAvoidSpraying() {
        val advisory = WeatherService.calculateSprayAdvisory(
            hour = 8,
            temp = 24.0,
            humidity = 60.0,
            windSpeed = 24.5,
            precipProb = 0.0
        )
        assertEquals(SprayCondition.AVOID_SPRAYING, advisory.condition)
        assertEquals("spray_advice_wind_extreme", advisory.adviceResKey)
    }

    @Test
    fun testExtremeEvaporationForcesAvoidSpraying() {
        val advisory = WeatherService.calculateSprayAdvisory(
            hour = 13,
            temp = 38.0,
            humidity = 18.0,
            windSpeed = 10.0,
            precipProb = 0.0
        )
        assertEquals(SprayCondition.AVOID_SPRAYING, advisory.condition)
        assertEquals("spray_advice_delta_t_extreme", advisory.adviceResKey)
    }

    @Test
    fun testDeadCalmNightInversionRisk() {
        val advisory = WeatherService.calculateSprayAdvisory(
            hour = 23,
            temp = 18.0,
            humidity = 90.0,
            windSpeed = 1.0,
            precipProb = 0.0
        )
        assertEquals(SprayCondition.AVOID_SPRAYING, advisory.condition)
        assertEquals("spray_advice_inversion_risk", advisory.adviceResKey)
    }

    @Test
    fun testMiddaySolarRadiationPenalty() {
        val advisory = WeatherService.calculateSprayAdvisory(
            hour = 13,
            temp = 27.0,
            humidity = 55.0,
            windSpeed = 8.0,
            precipProb = 0.0
        )
        assertEquals("12:00 - 15:00", advisory.windowLabel)
        assertEquals(SprayCondition.MODERATE, advisory.condition)
        assertEquals("spray_advice_midday_sun", advisory.adviceResKey)
    }
}
