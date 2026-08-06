package com.example

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import android.Manifest
import android.content.pm.PackageManager
import androidx.core.content.ContextCompat
import kotlinx.coroutines.flow.first

class AlertWorker(appContext: Context, workerParams: WorkerParameters) :
    CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result = withContext(Dispatchers.IO) {
        try {
            // First, process any manually Tracked Crops for price increases
            val trackedCrops = PriceTracker.getTrackedCrops(applicationContext)
            
            for (crop in trackedCrops) {
                // Fetch the live govt prices for this specific crop and state using the flow
                val flow = MandiApiService.watchLiveMandiPrices(crop.state, crop.crop)
                val state = flow.first { it !is MandiState.Loading }
                MandiApiService.stopWatching(crop.state, crop.crop)
                
                val liveRecords = when (state) {
                    is MandiState.Success -> state.records
                    is MandiState.Error -> state.staleData ?: emptyList()
                    else -> emptyList()
                }
                
                // Find the specific Mandi we are tracking
                val specificMandiRecord = liveRecords.find { it.market.equals(crop.mandi, ignoreCase = true) }
                
                if (specificMandiRecord != null) {
                    val currentModalPrice = specificMandiRecord.modalPrice
                    val threshold = if (crop.targetPrice > 0.0) crop.targetPrice else crop.basePrice
                    
                    if (currentModalPrice >= threshold && currentModalPrice > crop.basePrice) {
                        val increaseAmt = currentModalPrice - crop.basePrice
                        val lang = LanguageManager.currentLanguage.value
                        val title = AppStrings.get("weather_alerts", lang)
                        val msg = if (crop.targetPrice > 0.0) {
                            "Target Price Reached! ${crop.crop} in ${crop.mandi} has hit Rs.$currentModalPrice (Target: Rs.${crop.targetPrice})."
                        } else {
                            "Price Alert: ${crop.crop} in ${crop.mandi} has increased by Rs.$increaseAmt! Current price is Rs.$currentModalPrice."
                        }
                        
                        sendNotification(title, msg)
                        
                        // Update the base price and clear the target so we don't spam them
                        PriceTracker.addOrUpdateTrackedCrop(applicationContext, crop.state, crop.mandi, crop.crop, currentModalPrice, 0.0)
                    }
                }
            }

            // Second, check for REAL Weather Alerts based on precise GPS Location
            if (ContextCompat.checkSelfPermission(applicationContext, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
                val coords = LocationHelper.getCurrentLocationCoords(applicationContext)
                if (coords != null) {
                    val weatherResult = WeatherService.getWeather(coords.first, coords.second)
                    weatherResult.onSuccess { weatherData ->
                        if (weatherData.isRainAlert && weatherData.alertMessage.isNotBlank()) {
                            sendNotification("NuKropAI Weather Alert", weatherData.alertMessage)
                        }
                    }
                }
            }
            Result.success()
        } catch (e: Exception) {
            e.printStackTrace()
            Result.retry()
        }
    }

    private fun sendNotification(title: String, message: String) {
        val notificationManager = applicationContext.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val channelId = "nukrop_alerts_channel"

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                "NuKropAI Market & Weather Alerts",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Real-time alerts for local mandi prices and rain warnings."
            }
            notificationManager.createNotificationChannel(channel)
        }

        val notification = NotificationCompat.Builder(applicationContext, channelId)
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle(title)
            .setContentText(message)
            .setStyle(NotificationCompat.BigTextStyle().bigText(message))
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .build()

        notificationManager.notify(System.currentTimeMillis().toInt(), notification)
    }
}
