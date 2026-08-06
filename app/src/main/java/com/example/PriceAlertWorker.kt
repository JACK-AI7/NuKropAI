package com.example

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import kotlinx.coroutines.flow.first

class PriceAlertWorker(
    private val context: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(context, workerParams) {

    override suspend fun doWork(): Result {
        // Load tracked prices from SharedPreferences
        val prefs = context.getSharedPreferences("price_tracker", Context.MODE_PRIVATE)
        val allEntries = prefs.all
        
        var alertTriggered = false
        
        allEntries.forEach { (key, targetPriceObj) ->
            if (targetPriceObj is Float) {
                val targetPrice = targetPriceObj.toDouble()
                val parts = key.split("_")
                if (parts.size >= 3) {
                    val state = parts[0]
                    val market = parts[1]
                    val commodity = parts[2]
                    
                    // Fetch live price
                    val flow = MandiApiService.watchLiveMandiPrices(state, commodity)
                    val result = flow.first { it is MandiState.Success || it is MandiState.Error }
                    
                    if (result is MandiState.Success) {
                        val record = result.records.find { it.market.equals(market, true) }
                        if (record != null) {
                            if (record.modalPrice >= targetPrice) {
                                sendNotification(
                                    "Price Target Reached! 🚀",
                                    "${record.commodity} at ${record.market} is now ₹${record.modalPrice} (Target: ₹$targetPrice)"
                                )
                                alertTriggered = true
                                // Optionally untrack after reaching target
                                // prefs.edit().remove(key).apply()
                            } else if (record.modalPrice < record.maxPrice * 0.75) {
                                sendNotification(
                                    "Crash Alert! 📉",
                                    "${record.commodity} at ${record.market} has dropped to ₹${record.modalPrice}! Sell cautiously."
                                )
                                alertTriggered = true
                            }
                        }
                    }
                }
            }
        }
        
        return Result.success()
    }

    private fun sendNotification(title: String, message: String) {
        val channelId = "nukrop_price_alerts"
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                "Price Alerts",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Real-time crop price alerts"
            }
            val nm = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            nm.createNotificationChannel(channel)
        }
        
        val builder = NotificationCompat.Builder(context, channelId)
            .setSmallIcon(android.R.drawable.ic_dialog_info) // TODO: use real app icon
            .setContentTitle(title)
            .setContentText(message)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .setDefaults(NotificationCompat.DEFAULT_ALL)
            
        try {
            with(NotificationManagerCompat.from(context)) {
                notify(System.currentTimeMillis().toInt(), builder.build())
            }
        } catch (e: SecurityException) {
            // Missing POST_NOTIFICATIONS permission
        }
    }
}
