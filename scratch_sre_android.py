import re

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\app\src\main\java\com\example\telemetry\NuKropIotManager.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Add OfflineSyncQueue and Backoff properties
props = """    private val offlineCommandQueue = mutableListOf<Pair<String, String>>()
    private var reconnectAttempt = 0
    private var isConnected = false
    private const val MAX_RECONNECT_DELAY_MS = 30000L"""

content = content.replace('private val _deviceState = MutableStateFlow(', props + '\n\n    private val _deviceState = MutableStateFlow(')

# Update onOpen and onClosed/onFailure for exponential backoff
old_listener = """            override fun onOpen(webSocket: WebSocket, response: Response) {
                Log.d("NuKropIoT", "WebSocket Connected")
                _deviceState.value = _deviceState.value.copy(status = "online")
            }"""

new_listener = """            override fun onOpen(webSocket: WebSocket, response: Response) {
                Log.d("NuKropIoT", "WebSocket Connected")
                isConnected = true
                reconnectAttempt = 0 // Reset backoff
                _deviceState.value = _deviceState.value.copy(status = "online")
                
                // Flush offline queue!
                if (offlineCommandQueue.isNotEmpty()) {
                    Log.d("NuKropIoT", "Flushing ${offlineCommandQueue.size} offline commands to backend...")
                    val queueCopy = offlineCommandQueue.toList()
                    offlineCommandQueue.clear()
                    queueCopy.forEach { sendAsyncCommand(it.first, it.second) }
                }
            }"""
content = content.replace(old_listener, new_listener)

old_close = """            override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                _deviceState.value = _deviceState.value.copy(status = "offline", isRunning = false)
            }

            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                Log.e("NuKropIoT", "WebSocket Failure", t)
                _deviceState.value = _deviceState.value.copy(status = "offline")
            }"""

new_close = """            override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                isConnected = false
                _deviceState.value = _deviceState.value.copy(status = "offline", isRunning = false)
                scheduleReconnect(deviceId)
            }

            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                isConnected = false
                Log.e("NuKropIoT", "WebSocket Failure", t)
                _deviceState.value = _deviceState.value.copy(status = "offline")
                scheduleReconnect(deviceId)
            }"""
content = content.replace(old_close, new_close)

# Add reconnect method
reconnect_method = """
    private fun scheduleReconnect(deviceId: String) {
        if (webSocket != null) return // Already trying
        
        val delayMs = Math.min((1000 * Math.pow(2.0, reconnectAttempt.toDouble())).toLong(), MAX_RECONNECT_DELAY_MS)
        reconnectAttempt++
        
        Log.w("NuKropIoT", "WebSocket offline. Exponential backoff: Reconnecting in ${delayMs}ms (Attempt $reconnectAttempt)")
        
        kotlin.concurrent.thread {
            Thread.sleep(delayMs)
            Log.d("NuKropIoT", "Attempting reconnection...")
            connectWebSocket(deviceId)
        }
    }
"""
content = content.replace('fun disconnect() {', reconnect_method + '\n    fun disconnect() {')

# Update sendAsyncCommand to use Offline Queue
old_send = """        val body = FormBody.Builder().add("command", command).build()
        val request = Request.Builder()"""

new_send = """        if (!isConnected) {
            Log.w("NuKropIoT", "No network connection. Queuing command $command for Offline Sync.")
            offlineCommandQueue.add(Pair(deviceId, command))
            _commandState.value = CommandState.PENDING // Fake pending state for UI
            return
        }

        val body = FormBody.Builder().add("command", command).build()
        val request = Request.Builder()"""
content = content.replace(old_send, new_send)

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\app\src\main\java\com\example\telemetry\NuKropIotManager.kt", "w", encoding="utf-8") as f:
    f.write(content)
