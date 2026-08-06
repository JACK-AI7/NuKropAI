package com.example.telemetry

import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import okhttp3.*
import java.io.IOException

data class IotDeviceTelemetry(
    val deviceId: String,
    val status: String, // 'online', 'offline', 'fault', 'demo'
    val isRunning: Boolean,
    val voltage: Double,
    val amperage: Double,
    val moisture: Double
)

enum class CommandState {
    IDLE, PENDING, VERIFICATION, CONFIRMED, FAILED
}

/**
 * Enterprise IoT Manager for NuKropAI.
 * Connects to real WebSocket when backend is running.
 * Falls back to graceful offline/demo mode on physical devices without local backend.
 */
object NuKropIotManager {
    private val client = OkHttpClient()
    private var webSocket: WebSocket? = null

    // Local backend: 10.0.2.2 = emulator host, works on emulator only.
    // On a physical device without a backend, the connection will fail gracefully.
    private const val WS_URL = "ws://10.0.2.2:3000/api/v1/iot/telemetry/stream"
    private const val API_URL = "http://10.0.2.2:3000/api/v1/iot"

    private val offlineCommandQueue = mutableListOf<Pair<String, String>>()
    private var reconnectAttempt = 0
    private var isConnected = false
    private const val MAX_RECONNECT_ATTEMPTS = 3 // Stop after 3 tries, don't spam
    private const val MAX_RECONNECT_DELAY_MS = 30000L

    private val _deviceState = MutableStateFlow(
        IotDeviceTelemetry("demo_pump_1", "demo", false, 230.0, 0.0, 65.0)
    )
    val deviceState: StateFlow<IotDeviceTelemetry> = _deviceState.asStateFlow()

    private val _commandState = MutableStateFlow(CommandState.IDLE)
    val commandState: StateFlow<CommandState> = _commandState.asStateFlow()

    fun connectWebSocket(deviceId: String) {
        if (isConnected || webSocket != null) return // Already connected

        val request = Request.Builder().url("$WS_URL?deviceId=$deviceId").build()
        val listener = object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                Log.d("NuKropIoT", "WebSocket Connected to backend")
                isConnected = true
                reconnectAttempt = 0
                _deviceState.value = _deviceState.value.copy(status = "online")

                // Flush offline queue
                if (offlineCommandQueue.isNotEmpty()) {
                    val queueCopy = offlineCommandQueue.toList()
                    offlineCommandQueue.clear()
                    queueCopy.forEach { sendAsyncCommand(it.first, it.second) }
                }
            }

            override fun onMessage(webSocket: WebSocket, text: String) {
                try {
                    val json = org.json.JSONObject(text)
                    if (json.has("isRunning")) {
                        val isRunning = json.getBoolean("isRunning")
                        val amp = json.optDouble("amperage", 0.0)
                        val vol = json.optDouble("voltage", 230.0)
                        val moisture = json.optDouble("moisture", _deviceState.value.moisture)

                        _deviceState.value = _deviceState.value.copy(
                            isRunning = isRunning,
                            amperage = amp,
                            voltage = vol,
                            moisture = moisture,
                            status = "online"
                        )

                        // State verification
                        if (_commandState.value == CommandState.VERIFICATION || _commandState.value == CommandState.PENDING) {
                            when {
                                isRunning && amp > 1.0 -> _commandState.value = CommandState.CONFIRMED
                                isRunning && amp <= 0.1 -> {
                                    _deviceState.value = _deviceState.value.copy(status = "fault")
                                    _commandState.value = CommandState.FAILED
                                }
                                !isRunning -> _commandState.value = CommandState.CONFIRMED
                            }
                        }
                    }
                } catch (e: Exception) {
                    Log.e("NuKropIoT", "Parse error", e)
                }
            }

            override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                Log.d("NuKropIoT", "WebSocket closed: $reason")
                isConnected = false
                this@NuKropIotManager.webSocket = null
                _deviceState.value = _deviceState.value.copy(status = "offline", isRunning = false)
                scheduleReconnect(deviceId)
            }

            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                // Backend not reachable — switch to demo mode gracefully
                Log.w("NuKropIoT", "Backend unreachable (${t.message}). Running in demo mode.")
                isConnected = false
                this@NuKropIotManager.webSocket = null
                // Only show demo mode (not error) — app stays functional
                _deviceState.value = _deviceState.value.copy(status = "demo")
                // Schedule limited reconnects
                scheduleReconnect(deviceId)
            }
        }
        webSocket = client.newWebSocket(request, listener)
    }

    private fun scheduleReconnect(deviceId: String) {
        if (reconnectAttempt >= MAX_RECONNECT_ATTEMPTS) {
            Log.w("NuKropIoT", "Max reconnect attempts reached. Staying in offline/demo mode.")
            return
        }

        val delayMs = minOf((1000 * Math.pow(2.0, reconnectAttempt.toDouble())).toLong(), MAX_RECONNECT_DELAY_MS)
        reconnectAttempt++
        Log.w("NuKropIoT", "Reconnect attempt $reconnectAttempt in ${delayMs}ms...")

        kotlin.concurrent.thread {
            Thread.sleep(delayMs)
            webSocket = null // Allow new connection
            connectWebSocket(deviceId)
        }
    }

    fun disconnect() {
        webSocket?.close(1000, "App closed")
        webSocket = null
        isConnected = false
        reconnectAttempt = 0
    }

    /**
     * In demo mode (no backend): simulates toggle locally so UI is still useful.
     * In online mode: sends command to backend and waits for WebSocket verification.
     */
    fun sendAsyncCommand(deviceId: String, command: String) {
        _commandState.value = CommandState.PENDING

        if (!isConnected) {
            // Demo mode: simulate command instantly so UI doesn't freeze
            Log.w("NuKropIoT", "Demo mode: simulating $command locally")
            offlineCommandQueue.add(Pair(deviceId, command))
            kotlin.concurrent.thread {
                Thread.sleep(800) // Simulate network latency
                val turningOn = command.contains("ON", ignoreCase = true)
                _deviceState.value = _deviceState.value.copy(
                    isRunning = turningOn,
                    amperage = if (turningOn) 4.2 else 0.0,
                    status = if (_deviceState.value.status == "demo") "demo" else "offline"
                )
                _commandState.value = CommandState.CONFIRMED
            }
            return
        }

        // Real command to backend
        val body = FormBody.Builder().add("command", command).build()
        val request = Request.Builder()
            .url("$API_URL/devices/$deviceId/command")
            .post(body)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                _commandState.value = CommandState.FAILED
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    _commandState.value = CommandState.VERIFICATION
                    kotlin.concurrent.thread {
                        Thread.sleep(10000)
                        if (_commandState.value == CommandState.VERIFICATION) {
                            _commandState.value = CommandState.FAILED
                        }
                    }
                } else {
                    _commandState.value = CommandState.FAILED
                }
            }
        })
    }
}
