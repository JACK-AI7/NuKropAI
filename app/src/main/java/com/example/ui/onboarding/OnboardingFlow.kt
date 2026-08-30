package com.example.ui.onboarding

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.*
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.example.ui.AllAvailableCrops
import com.example.ui.CropItem
import com.example.ui.theme.*
import kotlinx.coroutines.launch

enum class OnboardingStep {
    LANGUAGE,
    CROPS,
    PERSONA,
    LOCATION_PERMISSION,
    NOTIFICATION_PERMISSION,
    FEATURE_CAROUSEL
}

data class LanguageOption(
    val code: String,
    val nativeName: String,
    val englishSubtext: String
)

val SupportedLanguages = listOf(
    LanguageOption("te", "తెలుగు", "మీ భాషలో వ్యవసాయం"),
    LanguageOption("hi", "हिन्दी", "आपकी भाषा में खेती"),
    LanguageOption("ta", "தமிழ்", "உங்கள் மொழியில் வேளாண்மை"),
    LanguageOption("kn", "ಕನ್ನಡ", "ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಕೃಷಿ"),
    LanguageOption("mr", "मराठी", "स्वतःच्या भाषेत शेती"),
    LanguageOption("pa", "ਪੰਜਾਬੀ", "ਤੁਹਾਡੀ ਭਾਸ਼ਾ ਵਿੱਚ ਖੇਤੀਬਾੜੀ"),
    LanguageOption("gu", "ગુજરાતી", "ખેતી તમારી ભાષામાં"),
    LanguageOption("bn", "বাংলা", "চাষাবাদের কথা আপনার ভাষায়"),
    LanguageOption("en", "English", "Smart farming in your language")
)

@Composable
fun OnboardingFlow(
    onFinished: () -> Unit
) {
    val context = LocalContext.current
    val prefs = remember { context.getSharedPreferences("nukrop_onboarding", Context.MODE_PRIVATE) }
    var currentStep by remember { mutableStateOf(OnboardingStep.LANGUAGE) }

    var selectedLang by remember { mutableStateOf("en") }
    var selectedCrops by remember { mutableStateOf(setOf("Cotton", "Rice / Paddy", "Chilli", "Tobacco")) }
    var selectedPersona by remember { mutableStateOf("I grow crops in fields") }

    fun completeOnboarding() {
        prefs.edit()
            .putBoolean("completed", true)
            .putString("language", selectedLang)
            .putStringSet("crops", selectedCrops)
            .putString("persona", selectedPersona)
            .apply()
        onFinished()
    }

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = Color.White
    ) {
        AnimatedContent(
            targetState = currentStep,
            transitionSpec = {
                fadeIn() togetherWith fadeOut()
            },
            label = "OnboardingTransition"
        ) { step ->
            when (step) {
                OnboardingStep.LANGUAGE -> LanguageSelectionStep(
                    selectedLang = selectedLang,
                    onLangSelected = { selectedLang = it },
                    onNext = { currentStep = OnboardingStep.CROPS }
                )
                OnboardingStep.CROPS -> CropSelectionStep(
                    selectedCrops = selectedCrops,
                    onCropsChanged = { selectedCrops = it },
                    onNext = { currentStep = OnboardingStep.PERSONA }
                )
                OnboardingStep.PERSONA -> PersonaSelectionStep(
                    selectedPersona = selectedPersona,
                    onPersonaSelected = { selectedPersona = it },
                    onNext = { currentStep = OnboardingStep.LOCATION_PERMISSION },
                    onSkip = { currentStep = OnboardingStep.LOCATION_PERMISSION }
                )
                OnboardingStep.LOCATION_PERMISSION -> LocationPermissionStep(
                    onNext = { currentStep = OnboardingStep.NOTIFICATION_PERMISSION },
                    onSkip = { currentStep = OnboardingStep.NOTIFICATION_PERMISSION }
                )
                OnboardingStep.NOTIFICATION_PERMISSION -> NotificationPermissionStep(
                    onNext = { currentStep = OnboardingStep.FEATURE_CAROUSEL },
                    onSkip = { currentStep = OnboardingStep.FEATURE_CAROUSEL }
                )
                OnboardingStep.FEATURE_CAROUSEL -> FeatureCarouselStep(
                    onComplete = { completeOnboarding() },
                    onSkip = { completeOnboarding() }
                )
            }
        }
    }
}

// ----------------------------------------------------
// 1. Language Selection Step
// ----------------------------------------------------
@Composable
fun LanguageSelectionStep(
    selectedLang: String,
    onLangSelected: (String) -> Unit,
    onNext: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .statusBarsPadding()
            .navigationBarsPadding()
            .padding(horizontal = 24.dp, vertical = 16.dp)
    ) {
        Spacer(Modifier.height(16.dp))

        // Logo & Namaste
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .background(PlantixBadgeGreen),
                contentAlignment = Alignment.Center
            ) {
                Text("🌿", fontSize = 22.sp)
            }
            Spacer(Modifier.width(10.dp))
            Text(
                "Namaste!",
                fontSize = 28.sp,
                fontWeight = FontWeight.ExtraBold,
                color = PlantixDarkGreen
            )
        }

        Spacer(Modifier.height(6.dp))
        Text(
            "Select your NuKropAI language",
            fontSize = 14.sp,
            color = PlantixTextMuted,
            textAlign = TextAlign.Center,
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(Modifier.height(20.dp))

        // Language List
        Column(
            modifier = Modifier
                .weight(1f)
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            SupportedLanguages.forEach { lang ->
                val isSelected = selectedLang == lang.code
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(if (isSelected) PlantixBadgeGreen else Color.White)
                        .border(
                            width = if (isSelected) 2.dp else 1.dp,
                            color = if (isSelected) PlantixPrimary else Color(0xFFE2ECE2),
                            shape = RoundedCornerShape(16.dp)
                        )
                        .clickable { onLangSelected(lang.code) }
                        .padding(horizontal = 16.dp, vertical = 14.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Text(
                                lang.nativeName,
                                fontSize = 18.sp,
                                fontWeight = FontWeight.Bold,
                                color = if (isSelected) PlantixPrimaryDark else PlantixText
                            )
                            Spacer(Modifier.height(2.dp))
                            Text(
                                lang.englishSubtext,
                                fontSize = 12.sp,
                                color = PlantixTextMuted
                            )
                        }

                        RadioButton(
                            selected = isSelected,
                            onClick = { onLangSelected(lang.code) },
                            colors = RadioButtonDefaults.colors(
                                selectedColor = PlantixPrimary,
                                unselectedColor = Color(0xFFBDC7BE)
                            )
                        )
                    }
                }
            }
        }

        Spacer(Modifier.height(16.dp))

        // Accept Button
        Button(
            onClick = onNext,
            modifier = Modifier
                .fillMaxWidth()
                .height(52.dp),
            shape = RoundedCornerShape(26.dp),
            colors = ButtonDefaults.buttonColors(containerColor = PlantixActionBlue)
        ) {
            Text("Accept", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
        }

        Spacer(Modifier.height(8.dp))
        Text(
            "I read and accept the terms of use and the privacy policy.",
            fontSize = 11.sp,
            color = PlantixTextMuted,
            textAlign = TextAlign.Center,
            modifier = Modifier.fillMaxWidth()
        )
    }
}

// ----------------------------------------------------
// 2. Crop Selection Step
// ----------------------------------------------------
@Composable
fun CropSelectionStep(
    selectedCrops: Set<String>,
    onCropsChanged: (Set<String>) -> Unit,
    onNext: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .statusBarsPadding()
            .navigationBarsPadding()
            .padding(horizontal = 20.dp, vertical = 16.dp)
    ) {
        Text(
            "Select your crops",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            color = PlantixText
        )
        Text(
            "You can always change it later.",
            fontSize = 13.sp,
            color = PlantixTextMuted
        )

        Spacer(Modifier.height(16.dp))

        LazyVerticalGrid(
            columns = GridCells.Fixed(3),
            modifier = Modifier.weight(1f),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            items(AllAvailableCrops) { crop ->
                val isSelected = selectedCrops.contains(crop.name)
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier
                        .clip(RoundedCornerShape(16.dp))
                        .clickable {
                            onCropsChanged(
                                if (isSelected) {
                                    if (selectedCrops.size > 1) selectedCrops - crop.name else selectedCrops
                                } else {
                                    selectedCrops + crop.name
                                }
                            )
                        }
                        .padding(4.dp)
                ) {
                    Box(
                        modifier = Modifier
                            .size(72.dp)
                            .clip(CircleShape)
                            .background(if (isSelected) PlantixBadgeGreen else Color(0xFFF4F7F4))
                            .border(
                                width = if (isSelected) 2.dp else 1.dp,
                                color = if (isSelected) PlantixPrimary else Color(0xFFE0E8DF),
                                shape = CircleShape
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(crop.iconEmoji, fontSize = 32.sp)
                        if (isSelected) {
                            Box(
                                modifier = Modifier
                                    .align(Alignment.TopEnd)
                                    .size(20.dp)
                                    .clip(CircleShape)
                                    .background(PlantixPrimary),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(Icons.Default.Check, contentDescription = null, tint = Color.White, modifier = Modifier.size(14.dp))
                            }
                        }
                    }
                    Spacer(Modifier.height(4.dp))
                    Text(
                        crop.name.split(" / ")[0],
                        fontSize = 12.sp,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                        color = if (isSelected) PlantixPrimaryDark else PlantixText,
                        textAlign = TextAlign.Center,
                        maxLines = 1
                    )
                }
            }
        }

        Spacer(Modifier.height(16.dp))

        Button(
            onClick = onNext,
            modifier = Modifier
                .fillMaxWidth()
                .height(52.dp),
            shape = RoundedCornerShape(26.dp),
            colors = ButtonDefaults.buttonColors(containerColor = PlantixActionBlue)
        ) {
            Text("Next (${selectedCrops.size} Selected)", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = Color.White)
        }
    }
}

// ----------------------------------------------------
// 3. Persona Selection Step
// ----------------------------------------------------
@Composable
fun PersonaSelectionStep(
    selectedPersona: String,
    onPersonaSelected: (String) -> Unit,
    onNext: () -> Unit,
    onSkip: () -> Unit
) {
    val options = listOf(
        "I grow crops in fields",
        "I grow crops in my home garden",
        "I grow crops in pots"
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .statusBarsPadding()
            .navigationBarsPadding()
            .padding(horizontal = 24.dp, vertical = 16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(Modifier.height(20.dp))

        // Illustrated Avatar Header
        Box(
            modifier = Modifier
                .size(160.dp)
                .clip(CircleShape)
                .background(
                    Brush.radialGradient(
                        listOf(Color(0xFFB2EBF2), Color(0xFFE0F7FA))
                    )
                ),
            contentAlignment = Alignment.Center
        ) {
            Text("👨‍🌾👩‍🌾", fontSize = 64.sp)
        }

        Spacer(Modifier.height(24.dp))

        Text(
            "Choose what describes you best",
            fontSize = 20.sp,
            fontWeight = FontWeight.Bold,
            color = PlantixText,
            textAlign = TextAlign.Center
        )

        Spacer(Modifier.height(24.dp))

        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
            options.forEach { option ->
                val isSelected = selectedPersona == option
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(if (isSelected) PlantixBadgeGreen else Color.White)
                        .border(
                            width = if (isSelected) 2.dp else 1.dp,
                            color = if (isSelected) PlantixPrimary else Color(0xFFE2ECE2),
                            shape = RoundedCornerShape(16.dp)
                        )
                        .clickable { onPersonaSelected(option) }
                        .padding(horizontal = 18.dp, vertical = 16.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            option,
                            fontSize = 15.sp,
                            fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                            color = if (isSelected) PlantixPrimaryDark else PlantixText
                        )
                        RadioButton(
                            selected = isSelected,
                            onClick = { onPersonaSelected(option) },
                            colors = RadioButtonDefaults.colors(
                                selectedColor = PlantixPrimary,
                                unselectedColor = Color(0xFFBDC7BE)
                            )
                        )
                    }
                }
            }
        }

        Spacer(Modifier.weight(1f))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            TextButton(onClick = onSkip) {
                Text("Skip", fontSize = 15.sp, color = PlantixTextMuted, fontWeight = FontWeight.Bold)
            }

            Button(
                onClick = onNext,
                modifier = Modifier
                    .width(140.dp)
                    .height(48.dp),
                shape = RoundedCornerShape(24.dp),
                colors = ButtonDefaults.buttonColors(containerColor = PlantixActionBlue)
            ) {
                Text("Next", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = Color.White)
            }
        }
    }
}

// ----------------------------------------------------
// 4. Location Permission Step
// ----------------------------------------------------
@Composable
fun LocationPermissionStep(
    onNext: () -> Unit,
    onSkip: () -> Unit
) {
    val context = LocalContext.current
    val launcher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { _ ->
        onNext()
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .statusBarsPadding()
            .navigationBarsPadding()
            .padding(horizontal = 24.dp, vertical = 16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(Modifier.weight(0.5f))

        Box(
            modifier = Modifier
                .size(170.dp)
                .clip(CircleShape)
                .background(
                    Brush.radialGradient(
                        listOf(Color(0xFFFFCDD2), Color(0xFFFCE4EC))
                    )
                ),
            contentAlignment = Alignment.Center
        ) {
            Text("📍🌾", fontSize = 64.sp)
        }

        Spacer(Modifier.height(32.dp))

        Text(
            "Allow location access",
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold,
            color = PlantixText,
            textAlign = TextAlign.Center
        )

        Spacer(Modifier.height(8.dp))

        Text(
            "To see localized weather alerts, APMC mandi arbitrage, and BioShield disease warnings, allow access to your location.",
            fontSize = 14.sp,
            color = PlantixTextMuted,
            textAlign = TextAlign.Center,
            lineHeight = 20.sp,
            modifier = Modifier.padding(horizontal = 16.dp)
        )

        Spacer(Modifier.weight(1f))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            TextButton(onClick = onSkip) {
                Text("Skip", fontSize = 15.sp, color = PlantixTextMuted, fontWeight = FontWeight.Bold)
            }

            Button(
                onClick = {
                    if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
                        onNext()
                    } else {
                        launcher.launch(Manifest.permission.ACCESS_FINE_LOCATION)
                    }
                },
                modifier = Modifier
                    .width(140.dp)
                    .height(48.dp),
                shape = RoundedCornerShape(24.dp),
                colors = ButtonDefaults.buttonColors(containerColor = PlantixActionBlue)
            ) {
                Text("Allow", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = Color.White)
            }
        }
    }
}

// ----------------------------------------------------
// 5. Notification Permission Step
// ----------------------------------------------------
@Composable
fun NotificationPermissionStep(
    onNext: () -> Unit,
    onSkip: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .statusBarsPadding()
            .navigationBarsPadding()
            .padding(horizontal = 24.dp, vertical = 16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(Modifier.weight(0.5f))

        Box(
            modifier = Modifier
                .size(170.dp)
                .clip(CircleShape)
                .background(
                    Brush.radialGradient(
                        listOf(Color(0xFFE1BEE7), Color(0xFFF3E5F5))
                    )
                ),
            contentAlignment = Alignment.Center
        ) {
            Text("🔔📱", fontSize = 64.sp)
        }

        Spacer(Modifier.height(32.dp))

        Text(
            "Allow notifications",
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold,
            color = PlantixText,
            textAlign = TextAlign.Center
        )

        Spacer(Modifier.height(8.dp))

        Text(
            "To receive important regional pest outbreaks, sudden rainfall warnings, and smart fertilizer tips.",
            fontSize = 14.sp,
            color = PlantixTextMuted,
            textAlign = TextAlign.Center,
            lineHeight = 20.sp,
            modifier = Modifier.padding(horizontal = 16.dp)
        )

        Spacer(Modifier.weight(1f))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            TextButton(onClick = onSkip) {
                Text("Skip", fontSize = 15.sp, color = PlantixTextMuted, fontWeight = FontWeight.Bold)
            }

            Button(
                onClick = onNext,
                modifier = Modifier
                    .width(140.dp)
                    .height(48.dp),
                shape = RoundedCornerShape(24.dp),
                colors = ButtonDefaults.buttonColors(containerColor = PlantixActionBlue)
            ) {
                Text("Allow", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = Color.White)
            }
        }
    }
}

// ----------------------------------------------------
// 6. Feature Intro Carousel Step (Matching all 4 slides)
// ----------------------------------------------------
data class CarouselSlide(
    val emoji: String,
    val title: String,
    val description: String
)

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun FeatureCarouselStep(
    onComplete: () -> Unit,
    onSkip: () -> Unit
) {
    val slides = listOf(
        CarouselSlide(
            "🩺🌿",
            "Instant Disease Detection",
            "Diagnose crop pests, fungal infections, and get instant organic BioRx cures on-device."
        ),
        CarouselSlide(
            "🚜🌾",
            "Helpful Growing Tips & Tools",
            "Precision fertilizer doses, pesticide calculations, and smart farming budgets for maximum yield."
        ),
        CarouselSlide(
            "📦🤝",
            "Great Product Deals & Mandi Arbitrage",
            "Find the best APMC mandi prices, rent shared machinery on YantraShare, and pool transport on GramHaul."
        ),
        CarouselSlide(
            "👥🎙️",
            "Supportive Farming Community",
            "Ask questions, share photos, and talk in your mother tongue with our Vernacular VoiceOS."
        )
    )

    val pagerState = rememberPagerState(pageCount = { slides.size })
    val scope = rememberCoroutineScope()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .statusBarsPadding()
            .navigationBarsPadding()
            .padding(horizontal = 24.dp, vertical = 16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(Modifier.weight(0.3f))

        HorizontalPager(
            state = pagerState,
            modifier = Modifier.weight(1f)
        ) { page ->
            val slide = slides[page]
            Column(
                modifier = Modifier.fillMaxSize(),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Box(
                    modifier = Modifier
                        .size(180.dp)
                        .clip(CircleShape)
                        .background(
                            Brush.radialGradient(
                                listOf(Color(0xFFE8F5E9), Color(0xFFC8E6C9))
                            )
                        ),
                    contentAlignment = Alignment.Center
                ) {
                    Text(slide.emoji, fontSize = 72.sp)
                }

                Spacer(Modifier.height(36.dp))

                Text(
                    slide.title,
                    fontSize = 22.sp,
                    fontWeight = FontWeight.Bold,
                    color = PlantixText,
                    textAlign = TextAlign.Center
                )

                Spacer(Modifier.height(10.dp))

                Text(
                    slide.description,
                    fontSize = 14.sp,
                    color = PlantixTextMuted,
                    textAlign = TextAlign.Center,
                    lineHeight = 20.sp,
                    modifier = Modifier.padding(horizontal = 16.dp)
                )
            }
        }

        // Indicator Dots
        Row(
            horizontalArrangement = Arrangement.spacedBy(6.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            repeat(slides.size) { index ->
                val isSelected = pagerState.currentPage == index
                Box(
                    modifier = Modifier
                        .size(if (isSelected) 8.dp else 6.dp)
                        .clip(CircleShape)
                        .background(if (isSelected) PlantixActionBlue else Color(0xFFCFD8DC))
                )
            }
        }

        Spacer(Modifier.height(32.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            TextButton(onClick = onSkip) {
                Text("Skip", fontSize = 15.sp, color = PlantixTextMuted, fontWeight = FontWeight.Bold)
            }

            val isLast = pagerState.currentPage == slides.size - 1
            Button(
                onClick = {
                    if (isLast) {
                        onComplete()
                    } else {
                        scope.launch {
                            pagerState.animateScrollToPage(pagerState.currentPage + 1)
                        }
                    }
                },
                modifier = Modifier
                    .width(if (isLast) 150.dp else 130.dp)
                    .height(48.dp),
                shape = RoundedCornerShape(24.dp),
                colors = ButtonDefaults.buttonColors(containerColor = PlantixActionBlue)
            ) {
                Text(
                    if (isLast) "Get Started" else "Next",
                    fontSize = 15.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White
                )
            }
        }
    }
}
