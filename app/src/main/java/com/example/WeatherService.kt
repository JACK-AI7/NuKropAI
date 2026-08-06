package com.example

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.doubleOrNull
import okhttp3.OkHttpClient
import okhttp3.Request
import java.util.concurrent.TimeUnit

data class WeatherData(
    val temperature: Double,
    val feelsLike: Double,
    val humidity: Double,
    val windSpeed: Double,
    val precipitation: Double,
    val weatherCode: Int,
    val description: String,
    val emoji: String,
    val isRainAlert: Boolean,
    val alertMessage: String
)

object WeatherService {
    private val client = OkHttpClient.Builder()
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .build()

    private val jsonParser = Json { ignoreUnknownKeys = true }

    suspend fun getWeather(lat: Double, lon: Double): Result<WeatherData> =
        withContext(Dispatchers.IO) {
            try {
                val url = "https://api.open-meteo.com/v1/forecast" +
                    "?latitude=$lat&longitude=$lon" +
                    "&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,precipitation,weather_code" +
                    "&hourly=precipitation_probability" +
                    "&forecast_days=1&timezone=auto"

                val req = Request.Builder().url(url).build()
                val resp = client.newCall(req).execute()
                val body = resp.body?.string() ?: ""
                val json = jsonParser.parseToJsonElement(body).jsonObject
                val cur = json["current"]?.jsonObject ?: return@withContext Result.failure(Exception("No current data"))

                val temp = cur["temperature_2m"]?.jsonPrimitive?.doubleOrNull ?: 0.0
                val feels = cur["apparent_temperature"]?.jsonPrimitive?.doubleOrNull ?: 0.0
                val humidity = cur["relative_humidity_2m"]?.jsonPrimitive?.doubleOrNull ?: 0.0
                val wind = cur["wind_speed_10m"]?.jsonPrimitive?.doubleOrNull ?: 0.0
                val precip = cur["precipitation"]?.jsonPrimitive?.doubleOrNull ?: 0.0
                val code = cur["weather_code"]?.jsonPrimitive?.doubleOrNull?.toInt() ?: 0

                // Check upcoming rain from hourly (next 6 hours)
                val hourlyPrecip = json["hourly"]?.jsonObject
                    ?.get("precipitation_probability")
                    ?.let { el ->
                        try {
                            val arr = el.toString().trim('[', ']').split(",")
                            arr.take(6).mapNotNull { it.trim().toDoubleOrNull() }
                        } catch (e: Exception) { emptyList() }
                    } ?: emptyList()
                val maxRainProb = hourlyPrecip.maxOrNull() ?: 0.0
                val isRainAlert = maxRainProb > 60.0

                val (desc, emoji) = weatherCodeInfo(code)

                Result.success(
                    WeatherData(
                        temperature = temp,
                        feelsLike = feels,
                        humidity = humidity,
                        windSpeed = wind,
                        precipitation = precip,
                        weatherCode = code,
                        description = desc,
                        emoji = emoji,
                        isRainAlert = isRainAlert,
                        alertMessage = if (isRainAlert) "⚠️ Rain expected in next 6 hours (${maxRainProb.toInt()}% chance). Consider delaying spraying operations." else ""
                    )
                )
            } catch (e: Exception) {
                Result.failure(e)
            }
        }

    private fun weatherCodeInfo(code: Int): Pair<String, String> = when (code) {
        0 -> "Clear Sky" to "☀️"
        1 -> "Mainly Clear" to "🌤️"
        2 -> "Partly Cloudy" to "⛅"
        3 -> "Overcast" to "☁️"
        in 45..48 -> "Foggy" to "🌫️"
        in 51..55 -> "Drizzle" to "🌦️"
        in 61..65 -> "Rain" to "🌧️"
        in 71..75 -> "Snow" to "❄️"
        in 80..82 -> "Rain Showers" to "🌧️"
        95 -> "Thunderstorm" to "⛈️"
        else -> "Cloudy" to "🌥️"
    }
}
