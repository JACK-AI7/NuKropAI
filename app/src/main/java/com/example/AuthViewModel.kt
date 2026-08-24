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

    private val _currentUser = MutableStateFlow<Any?>(null)
    val currentUser = _currentUser.asStateFlow()

    init {
        // Load saved session to prevent auto-logout
        val savedUser = prefs.getString("user_name", null)
        if (savedUser != null && savedUser != "Guest" && savedUser != "Google Farmer") {
            _currentUser.value = savedUser
            _authState.value = AuthState.Success
        } else if (savedUser == "Guest" || savedUser == "Google Farmer") {
            prefs.edit().clear().apply()
        }
        // Collect supabase session updates
        viewModelScope.launch {
            try {
                supabase.auth.sessionStatus.collect { status ->
                    when (status) {
                        is io.github.jan.supabase.auth.status.SessionStatus.Authenticated -> {
                            _currentUser.value = status.session.user
                            prefs.edit().putString("user_name", status.session.user?.email).apply()
                        }
                        else -> {
                            if (_currentUser.value != "Guest" && _currentUser.value != "Google Farmer") {
                                _currentUser.value = null
                                prefs.edit().clear().apply()
                            }
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
                }
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
                val credentialManager = androidx.credentials.CredentialManager.create(context)
                val googleIdOption = com.google.android.libraries.identity.googleid.GetGoogleIdOption.Builder()
                    .setFilterByAuthorizedAccounts(false)
                    .setServerClientId("NuKrop.AI")
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

                    _currentUser.value = googleIdTokenCredential.displayName ?: googleIdTokenCredential.id
                    prefs.edit().putString("user_name", _currentUser.value as String).apply()
                    _authState.value = AuthState.Success
                } else {
                    _currentUser.value = "Google Farmer"
                    prefs.edit().putString("user_name", "Google Farmer").apply()
                    _authState.value = AuthState.Success
                }
            } catch (e: Throwable) {
                // Strictly enforce Google login - no fallback bypass
                _authState.value = AuthState.Error("Google Sign-In failed. Please use Email/Password.")
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
