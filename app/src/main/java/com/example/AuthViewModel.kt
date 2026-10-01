package com.example

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import io.github.jan.supabase.auth.auth
import io.github.jan.supabase.auth.providers.builtin.Email
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import android.app.Application
import android.content.Context
import androidx.lifecycle.AndroidViewModel
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.contentOrNull

data class NuKropUser(
    val id: String,
    val email: String,
    val name: String,
    val avatarUrl: String? = null
)

sealed class AuthState {
    object Idle : AuthState()
    object Loading : AuthState()
    object Success : AuthState()
    data class Error(val message: String) : AuthState()
}

class AuthViewModel(application: Application) : AndroidViewModel(application) {
    private val prefs = application.getSharedPreferences("nukrop_auth", Context.MODE_PRIVATE)

    private val _authState = MutableStateFlow<AuthState>(AuthState.Idle)
    val authState: StateFlow<AuthState> = _authState.asStateFlow()

    private val _currentUser = MutableStateFlow<NuKropUser?>(null)
    val currentUser: StateFlow<NuKropUser?> = _currentUser.asStateFlow()

    init {
        // Immediately load saved session to prevent cold-start auto-logout
        val savedUserId = prefs.getString("user_id", "") ?: ""
        val savedEmail = prefs.getString("user_email", "") ?: ""
        val savedName = prefs.getString("user_name", null)
        val savedAvatar = prefs.getString("user_avatar", null)
        if (savedName != null && savedName.isNotBlank() && savedName != "Guest" && savedName != "Google Farmer") {
            _currentUser.value = NuKropUser(
                id = savedUserId.ifBlank { "user_${System.currentTimeMillis()}" },
                email = savedEmail,
                name = savedName,
                avatarUrl = savedAvatar
            )
            _authState.value = AuthState.Success
        } else if (savedName == "Guest" || savedName == "Google Farmer") {
            prefs.edit().clear().apply()
        }

        // Collect supabase session updates without wiping preferences on cold start
        viewModelScope.launch {
            try {
                supabase.auth.sessionStatus.collect { status ->
                    when (status) {
                        is io.github.jan.supabase.auth.status.SessionStatus.Authenticated -> {
                            val user = status.session.user
                            val meta = user?.userMetadata
                            val name = meta?.get("full_name")?.jsonPrimitive?.contentOrNull
                                ?: meta?.get("name")?.jsonPrimitive?.contentOrNull
                                ?: prefs.getString("user_name", null)
                                ?: user?.email?.substringBefore("@")
                                ?: "Farmer"
                            val email = user?.email ?: prefs.getString("user_email", "") ?: ""
                            val avatar = meta?.get("avatar_url")?.jsonPrimitive?.contentOrNull
                                ?: meta?.get("picture")?.jsonPrimitive?.contentOrNull
                                ?: prefs.getString("user_avatar", null)
                            val u = NuKropUser(
                                id = user?.id ?: prefs.getString("user_id", "") ?: "",
                                email = email,
                                name = name,
                                avatarUrl = avatar
                            )
                            _currentUser.value = u
                            prefs.edit()
                                .putString("user_id", u.id)
                                .putString("user_email", u.email)
                                .putString("user_name", u.name)
                                .putString("user_avatar", u.avatarUrl)
                                .apply()
                            _authState.value = AuthState.Success
                        }
                        else -> {
                            // Do NOT clear prefs on cold start during Initializing or NotAuthenticated to prevent race conditions
                        }
                    }
                }
            } catch (e: Throwable) {
                android.util.Log.e("AuthViewModel", "Session status collect error: ${e.message}")
            }
        }
    }

    fun signUp(email: String, pass: String, name: String) {
        if (email.isBlank() || pass.isBlank() || name.isBlank()) {
            _authState.value = AuthState.Error("All fields are required")
            return
        }
        _authState.value = AuthState.Loading
        viewModelScope.launch {
            try {
                supabase.auth.signUpWith(Email) {
                    this.email = email
                    this.password = pass
                    data = buildJsonObject {
                        put("full_name", JsonPrimitive(name))
                        put("name", JsonPrimitive(name))
                    }
                }
                val currentSessionUser = supabase.auth.currentUserOrNull()
                val u = NuKropUser(
                    id = currentSessionUser?.id ?: "user_${System.currentTimeMillis()}",
                    email = email,
                    name = name
                )
                _currentUser.value = u
                prefs.edit()
                    .putString("user_id", u.id)
                    .putString("user_email", u.email)
                    .putString("user_name", u.name)
                    .apply()

                // Sync user profile to Supabase user_profiles
                try {
                    SupabaseApi.syncProfile(email, name, "", "", "", 0.0, 0.0)
                } catch (_: Exception) {}

                _authState.value = AuthState.Success
            } catch (e: Throwable) {
                _authState.value = AuthState.Error(e.message ?: "Sign up failed")
            }
        }
    }

    fun signIn(email: String, pass: String) {
        if (email.isBlank() || pass.isBlank()) {
            _authState.value = AuthState.Error("Email and password are required")
            return
        }
        _authState.value = AuthState.Loading
        viewModelScope.launch {
            try {
                supabase.auth.signInWith(Email) {
                    this.email = email
                    this.password = pass
                }
                val user = supabase.auth.currentUserOrNull()
                val meta = user?.userMetadata
                val name = meta?.get("full_name")?.jsonPrimitive?.contentOrNull
                    ?: meta?.get("name")?.jsonPrimitive?.contentOrNull
                    ?: prefs.getString("user_name", null)
                    ?: email.substringBefore("@")
                val avatar = meta?.get("avatar_url")?.jsonPrimitive?.contentOrNull
                    ?: meta?.get("picture")?.jsonPrimitive?.contentOrNull
                    ?: prefs.getString("user_avatar", null)
                val u = NuKropUser(
                    id = user?.id ?: "user_${System.currentTimeMillis()}",
                    email = email,
                    name = name,
                    avatarUrl = avatar
                )
                _currentUser.value = u
                prefs.edit()
                    .putString("user_id", u.id)
                    .putString("user_email", u.email)
                    .putString("user_name", u.name)
                    .putString("user_avatar", u.avatarUrl)
                    .apply()
                _authState.value = AuthState.Success
            } catch (e: Throwable) {
                _authState.value = AuthState.Error(e.message ?: "Login failed")
            }
        }
    }

    fun signInWithGoogle(context: android.content.Context) {
        _authState.value = AuthState.Loading
        viewModelScope.launch {
            try {
                val serverClientId = try {
                    BuildConfig.GOOGLE_WEB_CLIENT_ID.ifBlank { "" }
                } catch (_: Throwable) { "" }

                if (serverClientId.isBlank() || !serverClientId.contains(".apps.googleusercontent.com")) {
                    _authState.value = AuthState.Error("Google Sign-In requires configured GOOGLE_WEB_CLIENT_ID. Please use Email/Password.")
                    return@launch
                }

                val credentialManager = androidx.credentials.CredentialManager.create(context)
                val googleIdOption = com.google.android.libraries.identity.googleid.GetGoogleIdOption.Builder()
                    .setFilterByAuthorizedAccounts(false)
                    .setServerClientId(serverClientId)
                    .setAutoSelectEnabled(false)
                    .build()
                val request = androidx.credentials.GetCredentialRequest.Builder()
                    .addCredentialOption(googleIdOption)
                    .build()
                val result = credentialManager.getCredential(context, request)
                val credential = result.credential
                if (credential is androidx.credentials.CustomCredential && credential.type == com.google.android.libraries.identity.googleid.GoogleIdTokenCredential.TYPE_GOOGLE_ID_TOKEN_CREDENTIAL) {
                    val googleIdTokenCredential = com.google.android.libraries.identity.googleid.GoogleIdTokenCredential.createFrom(credential.data)
                    
                    // Attempt Supabase IDToken Auth
                    try {
                        supabase.auth.signInWith(io.github.jan.supabase.auth.providers.builtin.IDToken) {
                            provider = io.github.jan.supabase.auth.providers.Google
                            idToken = googleIdTokenCredential.idToken
                        }
                    } catch (_: Exception) {}

                    val userName = googleIdTokenCredential.displayName ?: googleIdTokenCredential.id.substringBefore("@")
                    val userEmail = googleIdTokenCredential.id
                    val avatar = googleIdTokenCredential.profilePictureUri?.toString()
                    val u = NuKropUser(
                        id = googleIdTokenCredential.id,
                        email = userEmail,
                        name = userName,
                        avatarUrl = avatar
                    )
                    _currentUser.value = u
                    prefs.edit()
                        .putString("user_id", u.id)
                        .putString("user_email", u.email)
                        .putString("user_name", u.name)
                        .putString("user_avatar", u.avatarUrl)
                        .apply()
                    _authState.value = AuthState.Success
                } else {
                    _authState.value = AuthState.Error("Google Sign-In failed to obtain valid credential.")
                }
            } catch (e: Throwable) {
                _authState.value = AuthState.Error("Google Sign-In failed: ${e.message ?: "Please use Email/Password."}")
            }
        }
    }

    fun signOut() {
        viewModelScope.launch {
            try { supabase.auth.signOut() } catch (_: Exception) {}
            _currentUser.value = null
            prefs.edit().clear().apply()
            _authState.value = AuthState.Idle
        }
    }

    fun continueAsGuest() {
        _authState.value = AuthState.Error("Guest mode is disabled. Please create an account.")
    }

    fun setError(message: String) {
        _authState.value = AuthState.Error(message)
    }
}
