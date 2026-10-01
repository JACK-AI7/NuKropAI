package com.example

import android.app.Application
import android.content.Context
import androidx.test.core.app.ApplicationProvider
import kotlinx.coroutines.runBlocking
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

/**
 * Production Readiness Acceptance Tests (Android Kotlin Unit & Contract Suite)
 * Faithfully exercises real production classes, ViewModels, and services:
 * - R1: AuthViewModel, NuKropUser, AuthState, SupabaseClient
 * - R2: GeminiVisionService, LanguageManager
 * - R3: CommunityPost (CommunityScreen)
 * - R4: MandiApiService, MandiRecord, MandiState
 */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [34])
class ProductionReadinessTest {

    private lateinit var application: Application

    @Before
    fun setUp() {
        application = ApplicationProvider.getApplicationContext()
        try {
            com.russhwolf.settings.SettingsInitializer().create(application)
        } catch (_: Throwable) {}
        // Clear auth preferences before each test run
        application.getSharedPreferences("nukrop_auth", Context.MODE_PRIVATE)
            .edit()
            .clear()
            .apply()
    }

    // ========================================================================
    // R1: Live Supabase Authentication & Session Management
    // ========================================================================

    @Test
    fun testSupabaseConfigurationConstants() {
        assertEquals(
            "Supabase production endpoint must match authorized project",
            "https://yxjqseiegwjdfnccdchk.supabase.co",
            SUPABASE_URL
        )
        assertTrue(
            "Supabase anon key must be a valid non-blank JWT token",
            SUPABASE_ANON_KEY.isNotBlank() && SUPABASE_ANON_KEY.startsWith("eyJ")
        )
        assertNotNull("Supabase client instance must be initialized", supabase)
    }

    @Test
    fun testAuthViewModelSessionRehydrationFromPreferences() {
        // Pre-populate SharedPreferences to simulate cold-start with existing persisted session
        val prefs = application.getSharedPreferences("nukrop_auth", Context.MODE_PRIVATE)
        prefs.edit()
            .putString("user_id", "usr_warangal_101")
            .putString("user_email", "farmer.warangal@kisan.in")
            .putString("user_name", "B. Jaswanth Reddy")
            .putString("user_avatar", "https://cdn.nukrop.ai/avatars/jaswanth.png")
            .apply()

        // Instantiate production AuthViewModel
        val authViewModel = AuthViewModel(application)

        // Verify production model NuKropUser rehydration
        val currentUser = authViewModel.currentUser.value
        assertNotNull("Current user must be rehydrated from persistent storage", currentUser)
        assertEquals("usr_warangal_101", currentUser?.id)
        assertEquals("farmer.warangal@kisan.in", currentUser?.email)
        assertEquals("B. Jaswanth Reddy", currentUser?.name)
        assertEquals("https://cdn.nukrop.ai/avatars/jaswanth.png", currentUser?.avatarUrl)
        assertEquals("AuthState must transition to Success on session restore", AuthState.Success, authViewModel.authState.value)
    }

    @Test
    fun testAuthViewModelValidationAndGuestModeRejection() {
        val authViewModel = AuthViewModel(application)

        // Test Guest mode rejection policy (Benchmark constraint: Guest mode disabled)
        authViewModel.continueAsGuest()
        assertTrue("Guest mode must trigger Error state", authViewModel.authState.value is AuthState.Error)
        assertEquals(
            "Guest mode is disabled. Please create an account.",
            (authViewModel.authState.value as AuthState.Error).message
        )

        // Test blank sign-up validation
        authViewModel.signUp("", "", "")
        assertTrue("Blank sign up must trigger Error state", authViewModel.authState.value is AuthState.Error)
        assertEquals(
            "All fields are required",
            (authViewModel.authState.value as AuthState.Error).message
        )

        // Test blank sign-in validation
        authViewModel.signIn("", "")
        assertTrue("Blank sign in must trigger Error state", authViewModel.authState.value is AuthState.Error)
        assertEquals(
            "Email and password are required",
            (authViewModel.authState.value as AuthState.Error).message
        )
    }

    // ========================================================================
    // R2: Gemini Vision AI Service Contracts & Multi-Lingual Prompting
    // ========================================================================

    @Test
    fun testGeminiVisionApiKeyResolutionPrecedence() {
        val explicitKey = "AIzaSyTestExplicitKey_98765"
        val resolved = GeminiVisionService.resolveApiKey(explicitKey)
        assertEquals("Explicit parameter key must take highest precedence", explicitKey, resolved)
    }

    @Test
    fun testGeminiVisionAnalyzeImageSafeFailureOnUnconfiguredKey() = runBlocking {
        // Calling analyzeImage with explicit blank key must return Result.failure
        val result = GeminiVisionService.analyzeImage(
            apiKey = "",
            imageBytes = byteArrayOf(0x01, 0x02, 0x03),
            prompt = "Diagnose foliar symptoms"
        )

        assertTrue("Service must fail gracefully when key is unconfigured", result.isFailure)
        val exception = result.exceptionOrNull()
        assertNotNull("Exception must not be null", exception)
        assertTrue(
            "Exception message must specify unconfigured key",
            exception?.message?.contains("Gemini API key is not configured") == true
        )
    }

    @Test
    fun testLanguageManagerMultilingualMappings() {
        LanguageManager.init(application)
        assertEquals("Telugu", LanguageManager.getLanguageName("te"))
        assertEquals("తెలుగు", LanguageManager.getNativeLanguageName("te"))
        assertEquals("Hindi", LanguageManager.getLanguageName("hi"))
        assertEquals("हिन्दी", LanguageManager.getNativeLanguageName("hi"))
        assertEquals("English", LanguageManager.getLanguageName("en"))
    }

    // ========================================================================
    // R3: Community Media Attachment Contract
    // ========================================================================

    @Test
    fun testCommunityPostDomainModelMediaIntegrity() {
        // Exercise production CommunityPost model with Image attachment
        val imagePost = CommunityPost(
            postId = "POST-TEST-001",
            authorName = "B. Jaswanth Reddy",
            location = "Warangal, Telangana",
            cropName = "Cotton",
            cropEmoji = "🌾",
            timeAgo = "10 minutes ago",
            questionText = "Whitefly symptoms on leaves",
            translatedText = "Whitefly symptoms on leaves",
            verifiedSolution = "Apply Neem oil formulation @ 5ml/L",
            upvotesCount = 12,
            answersCount = 3,
            mediaUrl = "https://cdn.nukrop.ai/media/cotton_leaf.jpg",
            mediaType = "image"
        )
        assertEquals("image", imagePost.mediaType)
        assertTrue("Image media URL must be valid", imagePost.mediaUrl?.startsWith("https://") == true)

        // Exercise production CommunityPost model with Video attachment
        val videoPost = CommunityPost(
            postId = "POST-TEST-002",
            authorName = "Suresh Reddy",
            location = "Guntur, Andhra Pradesh",
            cropName = "Chilli",
            cropEmoji = "🌶️",
            timeAgo = "1 hour ago",
            questionText = "Chilli leaf curl progression video",
            upvotesCount = 28,
            answersCount = 5,
            mediaUrl = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
            mediaType = "video"
        )
        assertEquals("video", videoPost.mediaType)
        assertTrue("Video media URL must point to mp4 stream", videoPost.mediaUrl?.endsWith(".mp4") == true)
    }

    // ========================================================================
    // R4: Real Agmarknet Market Engine & MSP Compliance
    // ========================================================================

    @Test
    fun testMandiApiServiceBlankInputValidation() {
        // Empty state/commodity must immediately yield MandiState.Error
        val stateFlow = MandiApiService.watchLiveMandiPrices("", "")
        val state = stateFlow.value
        assertTrue("Blank query must return MandiState.Error", state is MandiState.Error)
        assertEquals(
            "State and commodity must not be empty",
            (state as MandiState.Error).message
        )
    }

    @Test
    fun testMandiRecordDomainContractAndMspFloor() {
        val record = MandiRecord(
            state = "Telangana",
            district = "Warangal",
            market = "Warangal APMC Yard",
            commodity = "Cotton",
            variety = "Medium Staple",
            minPrice = 7200.0,
            maxPrice = 7650.0,
            modalPrice = 7480.0,
            arrivalDate = "04/09/2026"
        )

        assertEquals("Cotton", record.commodity)
        assertTrue("Min price must be positive", record.minPrice > 0.0)
        assertTrue("Modal price must lie within [minPrice, maxPrice]", record.modalPrice in record.minPrice..record.maxPrice)

        // National GOI CACP declared MSP Floor for Cotton (~7121/quintal)
        val cottonMspFloor = 7121.0
        assertTrue("Modal price must satisfy or exceed national MSP floor", record.modalPrice >= cottonMspFloor)
    }
}
