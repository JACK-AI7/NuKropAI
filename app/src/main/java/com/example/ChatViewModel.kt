package com.example

import kotlinx.serialization.json.Json
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import android.app.Application
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.data.ChatMessageEntity
import com.example.data.ChatRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

data class ChatMessage(
    val id: String = java.util.UUID.randomUUID().toString(),
    val text: String,
    val isUser: Boolean,
    val isError: Boolean = false,
    val isLoading: Boolean = false
)

class ChatViewModel(private val repository: ChatRepository, private val application: Application) : ViewModel() {
    private val _messages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val messages: StateFlow<List<ChatMessage>> = _messages.asStateFlow()

    private val _generatingStatus = MutableStateFlow("")
    val generatingStatus: StateFlow<String> = _generatingStatus.asStateFlow()

    init {
        viewModelScope.launch {
            repository.allMessages.collect { entities ->
                val msgs = entities.map {
                    ChatMessage(
                        id = it.id,
                        text = it.text,
                        isUser = it.isUser,
                        isError = it.isError,
                        isLoading = false
                    )
                }
                if (msgs.isEmpty() && _generatingStatus.value.isEmpty()) {
                    val welcomeMsg = ChatMessageEntity(
                        id = java.util.UUID.randomUUID().toString(),
                        text = "Initialize",
                        isUser = true // Dummy logic skipped
                    )
                    // Wait, let me just add the default message to repo
                }
                
                _messages.value = msgs.ifEmpty { 
                     listOf(
                        ChatMessage(
                            text = "Hello! I am your AI Assistant powered by OpenRouter. Cloud memory is active.",
                            isUser = false
                        )
                    )
                }
            }
        }
    }

    fun sendMessage(prompt: String, imageBytes: ByteArray? = null) {
        if (prompt.isBlank() && imageBytes == null) return
        if (_generatingStatus.value.isNotEmpty()) return

        // Add user message
        val displayPrompt = if (imageBytes != null && prompt.isBlank()) "[Image Attached]" else prompt
        val userMsg = ChatMessage(text = displayPrompt, isUser = true)
        val assistantPlaceholderId = java.util.UUID.randomUUID().toString()
        val assistantMsgPlaceholder = ChatMessage(id = assistantPlaceholderId, text = "", isUser = false, isLoading = true)
        
        // Save to repo asynchronously, but update local state immediately for fast UI
        _messages.update { it + userMsg + assistantMsgPlaceholder }
        _generatingStatus.value = if (imageBytes != null) "Analyzing image..." else "Thinking..."

        viewModelScope.launch {
            try {
                // Persist user prompt
                repository.insertMessage(ChatMessageEntity(userMsg.id, userMsg.text, userMsg.isUser, false))
                if (imageBytes != null) {
                    streamImageResponse(prompt, imageBytes, assistantPlaceholderId)
                } else {
                    streamResponse(prompt, assistantPlaceholderId)
                }
            } catch (e: Throwable) {
                val err = e.message ?: "Failed to process message"
                updateMessage(assistantPlaceholderId, "Error connecting to AI: $err", isLoading = false, isError = true)
                repository.insertMessage(ChatMessageEntity(assistantPlaceholderId, "Error connecting to AI: $err", false, true))
            } finally {
                _generatingStatus.value = ""
            }
        }
    }

    private suspend fun streamResponse(prompt: String, messageId: String) {
        withContext(Dispatchers.IO) {
            // Compile conversation history into a single text block
            val sb = java.lang.StringBuilder()
            sb.append("System: You are NuKropAI, an extremely intelligent, helpful, and concise agricultural AI assistant. You help farmers with crop diseases, soil health, market trends, and general farming advice. Format your responses with clean Markdown, using emojis where appropriate.\n")
            
            // Inject context
            val loc = LocationHelper.getCurrentLocationStateAndMandi(application)
            if (loc != null) sb.append("User Context: Location is State '${loc.first}', Mandi '${loc.second}'. ")
            
            val tracked = PriceTracker.getTrackedCrops(application).joinToString { it.crop }
            if (tracked.isNotEmpty()) sb.append("User is currently tracking prices for: $tracked. ")
            
            sb.append("\nCRITICAL INSTRUCTION: If the user explicitly asks you to notify them, track, or set an alert for a specific crop's price hike, respond normally and APPEND EXACTLY the following tag at the very end of your message: `[TRACK_CROP: CropName, TargetPrice]`. If they don't specify a target price, use a reasonable default based on current market trends.\n\n")

            _messages.value.filter { !it.isLoading && !it.isError && it.id != messageId }.takeLast(10).forEach { msg ->
                val role = if (msg.isUser) "User" else "NuKropAI"
                sb.append("$role: ${msg.text}\n")
            }
            sb.append("NuKropAI:")

            val res = GeminiVisionService.chatQuery(sb.toString())
            handleApiResponse(res, messageId)
        }
    }

    private suspend fun streamImageResponse(prompt: String, imageBytes: ByteArray, messageId: String) {
        withContext(Dispatchers.IO) {
            val res = GeminiVisionService.analyzeImage("", imageBytes, prompt)
            handleApiResponse(res, messageId)
        }
    }

    private suspend fun handleApiResponse(res: Result<String>, messageId: String) {
        if (res.isSuccess) {
            var currentText = res.getOrNull() ?: "Empty response"
            
            // Intent Parsing: Look for [TRACK_CROP: Name, Price]
            val trackRegex = Regex("""\[TRACK_CROP:\s*([^,]+),\s*([0-9.]+)\]""")
            val match = trackRegex.find(currentText)
            if (match != null) {
                val crop = match.groupValues[1].trim()
                val price = match.groupValues[2].toDoubleOrNull() ?: 0.0
                
                val loc = LocationHelper.getCurrentLocationStateAndMandi(application)
                val state = loc?.first ?: ""
                val mandi = loc?.second ?: ""
                
                PriceTracker.addOrUpdateTrackedCrop(application, state, mandi, crop, price - 100, price)
                
                // Strip the tag from the UI
                currentText = currentText.replace(match.value, "").trim()
            }
            
            updateMessage(messageId, currentText, isLoading = false)
            repository.insertMessage(ChatMessageEntity(messageId, currentText, false, false))
        } else {
            val err = res.exceptionOrNull()?.message ?: "Unknown error"
            updateMessage(messageId, "Error connecting to AI: $err", isLoading = false, isError = true)
            repository.insertMessage(ChatMessageEntity(messageId, "Error connecting to AI: $err", false, true))
        }
        _generatingStatus.value = ""
    }

    private fun updateMessage(id: String, newText: String, isLoading: Boolean, isError: Boolean = false) {
        _messages.update { msgs ->
            msgs.map { msg ->
                if (msg.id == id) msg.copy(text = newText, isLoading = isLoading, isError = isError) else msg
            }
        }
    }

    class Factory(private val repository: ChatRepository, private val application: Application) : ViewModelProvider.Factory {
        override fun <T : ViewModel> create(modelClass: Class<T>): T {
            if (modelClass.isAssignableFrom(ChatViewModel::class.java)) {
                @Suppress("UNCHECKED_CAST")
                return ChatViewModel(repository, application) as T
            }
            throw IllegalArgumentException("Unknown ViewModel class")
        }
    }
}
