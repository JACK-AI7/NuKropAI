package com.example

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.theme.*
import kotlinx.coroutines.delay

@Composable
fun LoanScreen(onNavigateBack: () -> Unit) {
    var isAnalyzing by remember { mutableStateOf(false) }
    var showResults by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(NuKropDark)
            .padding(16.dp)
    ) {
        // Header
        Row(verticalAlignment = Alignment.CenterVertically) {
            IconButton(onClick = onNavigateBack) {
                Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = NuKropText)
            }
            Spacer(Modifier.width(8.dp))
            Text("Government Schemes AI", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = NuKropText)
        }

        Spacer(modifier = Modifier.height(24.dp))

        if (!showResults) {
            Text("AI Scheme Matcher", fontSize = 24.sp, fontWeight = FontWeight.ExtraBold, color = NuKropAccent)
            Spacer(Modifier.height(8.dp))
            Text("Let AI analyze your farm profile (Size, Crop, State) to instantly find eligible subsidies and loans you are missing.", color = NuKropTextMuted)
            
            Spacer(Modifier.height(32.dp))

            Button(
                onClick = {
                    isAnalyzing = true
                },
                modifier = Modifier.fillMaxWidth().height(60.dp),
                colors = ButtonDefaults.buttonColors(containerColor = NuKropAccent)
            ) {
                if (isAnalyzing) {
                    CircularProgressIndicator(color = NuKropDark, modifier = Modifier.size(24.dp))
                    Spacer(Modifier.width(12.dp))
                    Text("Scanning Gov Databases...", color = NuKropDark, fontWeight = FontWeight.Bold)
                } else {
                    Icon(Icons.Default.Search, contentDescription = null, tint = NuKropDark)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("FIND MY SUBSIDIES", color = NuKropDark, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                }
            }

            LaunchedEffect(isAnalyzing) {
                if (isAnalyzing) {
                    delay(2000) // Simulate AI API Call
                    isAnalyzing = false
                    showResults = true
                }
            }
        } else {
            Column(Modifier.verticalScroll(rememberScrollState())) {
                Box(Modifier.clip(RoundedCornerShape(8.dp)).background(NuKropBadgeGreen.copy(alpha=0.15f)).padding(8.dp)) {
                    Text("✓ AI Found 3 Eligible Schemes for your 5-Acre Tomato Farm in Maharashtra.", color = NuKropBadgeGreen, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.height(16.dp))

                SchemeCard("PM-KISAN Samman Nidhi", "₹6,000 / year", "Direct income support. You are fully eligible based on land holding.", Color(0xFF64B5F6))
                Spacer(Modifier.height(12.dp))
                SchemeCard("PMFBY (Crop Insurance)", "90% Premium Subsidy", "Protect against weather damage. Deadline in 12 days.", NuKropWarning)
                Spacer(Modifier.height(12.dp))
                SchemeCard("Solar Pump Subsidy (KUSUM)", "60% Cost Coverage", "Available for upgrading your currently tracked Borewell Motor to solar.", NuKropAccent)
            }
        }
    }
}

@Composable
fun SchemeCard(title: String, amount: String, desc: String, accent: Color) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(NuKropCard)
            .border(1.dp, accent.copy(alpha=0.3f), RoundedCornerShape(16.dp))
            .padding(16.dp)
    ) {
        Column {
            Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween, Alignment.Top) {
                Text(title, fontSize = 16.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                Box(Modifier.clip(RoundedCornerShape(4.dp)).background(accent.copy(alpha=0.2f)).padding(horizontal=6.dp, vertical=2.dp)) {
                    Text(amount, color = accent, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                }
            }
            Spacer(Modifier.height(8.dp))
            Text(desc, fontSize = 12.sp, color = NuKropTextMuted, lineHeight = 18.sp)
            Spacer(Modifier.height(12.dp))
            Button(
                onClick = {},
                modifier = Modifier.fillMaxWidth().height(40.dp),
                colors = ButtonDefaults.buttonColors(containerColor = NuKropSurface)
            ) {
                Text("Auto-Fill Application", color = NuKropText, fontSize = 12.sp)
            }
        }
    }
}
