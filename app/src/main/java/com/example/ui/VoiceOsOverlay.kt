package com.example.ui

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.VolumeUp
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.theme.*
import com.example.voice.FarmVoiceContext
import com.example.voice.IndicLanguage
import com.example.voice.VoiceIntentResult
import com.example.voice.VoiceOsEngine
import kotlinx.coroutines.launch

@Composable
fun VoiceOsOverlay(
    onDismiss: () -> Unit,
    onNavigateToRoute: (String) -> Unit = {}
) {
    var selectedLanguage by remember { mutableStateOf(IndicLanguage.TELUGU) }
    var isListening by remember { mutableStateOf(false) }
    var result by remember { mutableStateOf<VoiceIntentResult?>(null) }
    val scope = rememberCoroutineScope()

    val infiniteTransition = rememberInfiniteTransition(label = "wave")
    val pulseScale by infiniteTransition.animateFloat(
        initialValue = 1.0f,
        targetValue = if (isListening) 1.35f else 1.0f,
        animationSpec = infiniteRepeatable(
            animation = tween(650, easing = FastOutSlowInEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "pulse"
    )

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xEE090E07))
            .padding(16.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(24.dp))
                .background(NuKropCard)
                .border(1.dp, NuKropAccent.copy(alpha = 0.4f), RoundedCornerShape(24.dp))
                .padding(20.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Header
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("🎙️", fontSize = 22.sp)
                    Spacer(Modifier.width(8.dp))
                    Column {
                        Text("Vernacular VoiceOS", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                        Text("Sub-800ms Multilingual Speech AI", fontSize = 11.sp, color = NuKropAccent)
                    }
                }
                IconButton(onClick = onDismiss) {
                    Icon(Icons.Default.Close, contentDescription = "Close", tint = NuKropTextMuted)
                }
            }

            Spacer(Modifier.height(16.dp))

            // Language Selector Chips
            Text("Select Voice Dialect:", fontSize = 12.sp, color = NuKropTextMuted, modifier = Modifier.align(Alignment.Start))
            Spacer(Modifier.height(8.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                listOf(IndicLanguage.TELUGU, IndicLanguage.HINDI, IndicLanguage.TAMIL, IndicLanguage.ENGLISH).forEach { lang ->
                    val isSelected = selectedLanguage == lang
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(12.dp))
                            .background(if (isSelected) NuKropAccent else NuKropSurface)
                            .clickable { selectedLanguage = lang }
                            .padding(horizontal = 10.dp, vertical = 6.dp)
                    ) {
                        Text(
                            lang.displayName,
                            color = if (isSelected) NuKropDark else NuKropText,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }

            Spacer(Modifier.height(24.dp))

            // Animated Mic Button
            Box(
                modifier = Modifier
                    .size(90.dp)
                    .clip(CircleShape)
                    .background(
                        Brush.radialGradient(
                            listOf(
                                NuKropAccent.copy(alpha = if (isListening) 0.6f else 0.2f),
                                Color.Transparent
                            )
                        )
                    ),
                contentAlignment = Alignment.Center
            ) {
                IconButton(
                    onClick = {
                        isListening = !isListening
                        if (isListening) {
                            scope.launch {
                                // Simulate real-time speech query processing
                                val res = VoiceOsEngine.processSpeechQuery(
                                    selectedLanguage.samplePrompt,
                                    selectedLanguage,
                                    FarmVoiceContext()
                                )
                                result = res
                                isListening = false
                            }
                        }
                    },
                    modifier = Modifier
                        .size(70.dp)
                        .clip(CircleShape)
                        .background(if (isListening) NuKropAccent else NuKropBadgeGreen)
                ) {
                    Icon(
                        Icons.Default.Mic,
                        contentDescription = "Microphone",
                        tint = NuKropDark,
                        modifier = Modifier.size(32.dp)
                    )
                }
            }

            Spacer(Modifier.height(12.dp))
            Text(
                if (isListening) "Listening (Background Noise Suppressed)..." else "Tap Mic to Speak in ${selectedLanguage.displayName}",
                color = if (isListening) NuKropAccent else NuKropTextMuted,
                fontSize = 12.sp,
                fontWeight = FontWeight.Medium
            )

            Spacer(Modifier.height(20.dp))

            // Result Display Card
            result?.let { res ->
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(NuKropSurface)
                        .border(1.dp, Color(0x30FFFFFF), RoundedCornerShape(16.dp))
                        .padding(14.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text("🗣️ \"${res.transcript}\"", fontSize = 13.sp, color = NuKropTextMuted, fontWeight = FontWeight.SemiBold)
                        Text("⚡ ${res.latencyMs}ms", fontSize = 10.sp, color = NuKropAccent, fontWeight = FontWeight.Bold)
                    }
                    Spacer(Modifier.height(8.dp))
                    Text(res.actionableAnswer, fontSize = 14.sp, color = NuKropText, lineHeight = 20.sp)
                    Spacer(Modifier.height(10.dp))

                    res.suggestedActionRoute?.let { route ->
                        Button(
                            onClick = {
                                onDismiss()
                                onNavigateToRoute(route)
                            },
                            modifier = Modifier.fillMaxWidth().height(40.dp),
                            shape = RoundedCornerShape(10.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = NuKropAccent)
                        ) {
                            Text("Open ${res.intentCategory.replace("_", " ")}", color = NuKropDark, fontWeight = FontWeight.Bold, fontSize = 12.sp)
                        }
                    }
                }
            }
        }
    }
}
