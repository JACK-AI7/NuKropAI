package com.example

import android.content.Context
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

object LanguageManager {
    private const val PREFS_NAME = "language_prefs"
    private const val KEY_LANG = "selected_language"

    private val _currentLanguage = MutableStateFlow("en")
    val currentLanguage: StateFlow<String> = _currentLanguage.asStateFlow()

    fun init(context: Context) {
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        _currentLanguage.value = prefs.getString(KEY_LANG, "en") ?: "en"
    }

    fun setLanguage(context: Context, langCode: String) {
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        prefs.edit().putString(KEY_LANG, langCode).apply()
        _currentLanguage.value = langCode
    }

    fun getLanguageName(code: String): String {
        return when (code) {
            "hi" -> "Hindi"
            "te" -> "Telugu"
            "ta" -> "Tamil"
            "mr" -> "Marathi"
            else -> "English"
        }
    }
}
