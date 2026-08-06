package com.example

import android.app.Application
import android.util.Log
import androidx.room.Room
import com.example.data.AppDatabase
import com.example.data.ChatRepository
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.ExistingPeriodicWorkPolicy
import java.util.concurrent.TimeUnit

class AiApplication : Application() {
    lateinit var database: AppDatabase
        private set
    lateinit var chatRepository: ChatRepository
        private set

    override fun onCreate() {
        super.onCreate()
        
        // Global Exception Handler to prevent immediate silent crash
        val defaultHandler = Thread.getDefaultUncaughtExceptionHandler()
        Thread.setDefaultUncaughtExceptionHandler { thread, exception ->
            Log.e("NuKropAI_CRASH", "Uncaught exception in thread ${thread.name}: ${exception.message}", exception)
            // Still let the app crash eventually so the OS cleans it up, but log it first
            defaultHandler?.uncaughtException(thread, exception)
        }
        
        // Start background alerts sync
        try {
            val alertRequest = PeriodicWorkRequestBuilder<AlertWorker>(15, TimeUnit.MINUTES).build()
            WorkManager.getInstance(this).enqueueUniquePeriodicWork(
                "nukrop_alerts",
                ExistingPeriodicWorkPolicy.KEEP,
                alertRequest
            )
        } catch(e: Exception) { e.printStackTrace() }

        // Database initialization
        try {
            database = Room.databaseBuilder(
                applicationContext,
                AppDatabase::class.java,
                "ai_chat_database"
            ).fallbackToDestructiveMigration(dropAllTables = true).build()
            chatRepository = ChatRepository(database.chatDao())
        } catch (e: Exception) {
            Log.e("NuKropAI", "Database init failed: ${e.message}")
        }
    }
}
