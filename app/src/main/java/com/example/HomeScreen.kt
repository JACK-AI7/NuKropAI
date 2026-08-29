package com.example

import android.Manifest
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.*
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.*
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.example.model.OutbreakAlert
import com.example.ui.VoiceOsOverlay
import com.example.ui.theme.*
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*

@SuppressLint("MissingPermission")
@Composable
fun HomeScreen(
    modifier: Modifier = Modifier,
    onNavigateToScan: () -> Unit = {},
    onNavigateToMarket: () -> Unit = {},
    onNavigateToChat: () -> Unit = {},
    onNavigateToAutopilot: () -> Unit = {},
    onNavigateToFinance: () -> Unit = {},
    onNavigateToSavedReports: () -> Unit = {},
    onNavigateToEquipmentRental: () -> Unit = {},
    onNavigateToFarmKhata: () -> Unit = {},
    onNavigateToBioShield: () -> Unit = {},
    onNavigateToMandiPilot: () -> Unit = {},
    onNavigateToGramHaul: () -> Unit = {},
    onNavigateToAgriStack: () -> Unit = {},
    onNavigateToYantraShare: () -> Unit = {},
    onNavigateToBioRx: () -> Unit = {}
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val scrollState = rememberScrollState()
    var showVoiceOs by remember { mutableStateOf(false) }

    var weather by remember { mutableStateOf<WeatherData?>(null) }
    var weatherError by remember { mutableStateOf<String?>(null) }
    var weatherLoading by remember { mutableStateOf(true) }

    var userState by remember { mutableStateOf("Maharashtra") }
    var activeAlerts by remember { mutableStateOf<List<OutbreakAlert>>(emptyList()) }
    var alertsLoading by remember { mutableStateOf(true) }

    val hasLocation = remember {
        ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
    }
    val locLauncher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        if (granted) {
            scope.launch {
                fetchWeather(context) { w, e -> weather = w; weatherError = e; weatherLoading = false }
                val loc = LocationHelper.getCurrentLocationStateAndMandi(context)
                if (loc != null && loc.first.isNotBlank()) {
                    userState = loc.first
                }
            }
        } else {
            weatherLoading = false
            weatherError = "Location permission denied"
        }
    }

    LaunchedEffect(userState) {
        alertsLoading = true
        try {
            val result = DiseaseAggregationService.fetchActiveAlerts(userState)
            activeAlerts = result.getOrElse { emptyList() }
        } catch (_: Exception) {
            activeAlerts = emptyList()
        } finally {
            alertsLoading = false
        }
    }

    LaunchedEffect(Unit) {
        if (hasLocation) {
            fetchWeather(context) { w, e -> weather = w; weatherError = e; weatherLoading = false }
            val loc = LocationHelper.getCurrentLocationStateAndMandi(context)
            if (loc != null && loc.first.isNotBlank()) {
                userState = loc.first
            } else {
                val prefs = context.getSharedPreferences("nukrop_farm_profile", android.content.Context.MODE_PRIVATE)
                val savedState = prefs.getString("state", "Maharashtra") ?: "Maharashtra"
                userState = savedState
            }
        } else {
            weatherLoading = false
            weatherError = "Tap to grant location"
            val prefs = context.getSharedPreferences("nukrop_farm_profile", android.content.Context.MODE_PRIVATE)
            val savedState = prefs.getString("state", "Maharashtra") ?: "Maharashtra"
            userState = savedState
        }
        PriceTickerService.start()
    }

    val tickerItems by PriceTickerService.tickerItems.collectAsState()
    val tickerLoading by PriceTickerService.isLoading.collectAsState()
    val now = remember { SimpleDateFormat("d MMM yyyy | h:mm a", Locale.getDefault()).format(Date()) }

    Box(modifier = modifier.fillMaxSize().background(Color(0xFF0D1208))) {
        Column(Modifier.fillMaxSize().verticalScroll(scrollState).padding(bottom = 120.dp)) {

            // Hero Section
            Box(Modifier.fillMaxWidth().height(260.dp)) {
                Image(
                    painter = painterResource(id = R.drawable.farm_bg),
                    contentDescription = "Farm background",
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
                // Gradient overlay
                Box(
                    Modifier.fillMaxSize().background(
                        Brush.verticalGradient(listOf(Color(0x88000000), Color(0xFF0D1208)))
                    )
                )
                // Header row
                Row(
                    Modifier.fillMaxWidth().statusBarsPadding().padding(16.dp),
                    Arrangement.SpaceBetween, Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        Box(
                            Modifier.size(44.dp).clip(CircleShape)
                                .background(Brush.linearGradient(listOf(NuKropGreen, NuKropAccent))),
                            Alignment.Center
                        ) { Icon(Icons.Filled.Person, null, tint = NuKropDark, modifier = Modifier.size(24.dp)) }
                        Column {
                            Text("Good ${greeting()}, Farmer!", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                            Text(now, fontSize = 10.sp, color = Color.White.copy(alpha = 0.7f), maxLines = 1, overflow = TextOverflow.Ellipsis)
                        }
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(20.dp))
                                .background(NuKropAccent)
                                .clickable { showVoiceOs = true }
                                .padding(horizontal = 10.dp, vertical = 6.dp)
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text("🎙️", fontSize = 12.sp)
                                Spacer(Modifier.width(4.dp))
                                Text("VoiceOS", fontSize = 11.sp, color = NuKropDark, fontWeight = FontWeight.Bold)
                            }
                        }
                        IconButton(onClick = { /* Notifications */ }, modifier = Modifier.size(40.dp).clip(CircleShape).background(Color(0x33FFFFFF))) {
                            Icon(Icons.Filled.Notifications, contentDescription = "Notifications", tint = Color.White, modifier = Modifier.size(20.dp))
                        }
                    }
                }
                
                // Weather Pill inside Hero
                Box(Modifier.align(Alignment.BottomCenter).padding(16.dp).fillMaxWidth()) {
                    Box(
                        Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).background(Color(0x99000000))
                            .border(1.dp, Color(0x40C8E837), RoundedCornerShape(16.dp))
                            .clickable { if (!hasLocation) locLauncher.launch(Manifest.permission.ACCESS_FINE_LOCATION) }
                            .padding(horizontal = 16.dp, vertical = 12.dp)
                    ) {
                        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                            if (weatherLoading) {
                                Text("Fetching live weather...", color = Color.White.copy(0.7f), fontSize = 12.sp)
                            } else if (weather != null) {
                                val w = weather!!
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Text(w.emoji, fontSize = 20.sp)
                                    Spacer(Modifier.width(8.dp))
                                    Column {
                                        Text("${w.temperature}C", color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                                        Text("Feels ${w.feelsLike}C", color = Color.White.copy(0.7f), fontSize = 10.sp)
                                    }
                                }
                                Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                    WeatherDetail(Icons.Default.WaterDrop, "${w.humidity}%")
                                    WeatherDetail(Icons.Default.Air, "${w.windSpeed}km/h")
                                    WeatherDetail(Icons.Default.Water, "${w.precipitation}mm")
                                }
                            } else {
                                Text(weatherError ?: "Weather unavailable", color = NuKropWarning, fontSize = 12.sp)
                            }
                        }
                    }
                }
            }
            
            Spacer(Modifier.height(8.dp))
            
            // Marquee
            Box(Modifier.fillMaxWidth().background(Color(0x10C8E837)).padding(vertical = 12.dp, horizontal = 16.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    if (tickerLoading) {
                        CircularProgressIndicator(color = NuKropAccent, modifier = Modifier.size(12.dp), strokeWidth = 2.dp)
                        Spacer(Modifier.width(8.dp))
                        Text("Loading live market rates...", color = NuKropTextMuted, fontSize = 12.sp)
                    } else if (tickerItems.isEmpty()) {
                        Icon(Icons.AutoMirrored.Filled.TrendingUp, null, tint = NuKropAccent, modifier = Modifier.size(14.dp))
                        Spacer(Modifier.width(8.dp))
                        Text("Live Gov Mandi Data Connected", color = NuKropAccent, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    } else {
                        val first = tickerItems.first()
                        Icon(Icons.AutoMirrored.Filled.TrendingUp, null, tint = NuKropAccent, modifier = Modifier.size(14.dp))
                        Spacer(Modifier.width(8.dp))
                        Text("${first.commodity} (${first.market}) ₹${first.modalPrice}", color = NuKropText, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    }
                }
            }
            
            Spacer(Modifier.height(16.dp))
            
            // Quick Actions Header
            Row(Modifier.padding(horizontal = 16.dp), verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Filled.GridView, contentDescription = null, tint = NuKropAccent, modifier = Modifier.size(16.dp))
                Spacer(Modifier.width(8.dp))
                Text("Quick Actions", color = NuKropText, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
            
            Spacer(Modifier.height(16.dp))

            // Quick Actions Grid
            Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    QuickActionTile(Modifier.weight(1f), Icons.Filled.Science, "Scan Crop", "AI Disease & Pest Detect", Color(0xFFC8E837), onNavigateToScan)
                    QuickActionTile(Modifier.weight(1f), Icons.Filled.Landscape, "Scan Soil", "AI Soil Health Analysis", Color(0xFF8BC34A), onNavigateToScan)
                }
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    QuickActionTile(Modifier.weight(1f), Icons.Filled.Analytics, "Market Rates", "Live Mandi Prices", Color(0xFF64B5F6), onNavigateToMarket)
                    QuickActionTile(Modifier.weight(1f), Icons.Filled.SmartToy, "AI Advisor", "Ask Any Farm Question", Color(0xFFBA68C8), onNavigateToChat)
                }
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    QuickActionTile(Modifier.weight(1f), Icons.Filled.AccountBalance, "Loan & Subsidy", "Govt Schemes Matcher", Color(0xFFFFB74D), onNavigateToFinance)
                    QuickActionTile(Modifier.weight(1f), Icons.Filled.Navigation, "Field Navigator", "GPS Route & Coverage", Color(0xFFE57373), onNavigateToAutopilot)
                }
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    QuickActionTile(Modifier.weight(1f), Icons.Filled.Shield, "BioShield Radar", "Spatial Outbreak Defense", Color(0xFFEF5350), onNavigateToBioShield)
                    QuickActionTile(Modifier.weight(1f), Icons.AutoMirrored.Filled.TrendingUp, "MandiPilot", "Arbitrage & Price Discovery", Color(0xFF42A5F5), onNavigateToMandiPilot)
                }
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    QuickActionTile(Modifier.weight(1f), Icons.Filled.LocalShipping, "GramHaul", "Shared Rural Logistics", Color(0xFFFFA726), onNavigateToGramHaul)
                    QuickActionTile(Modifier.weight(1f), Icons.Filled.Badge, "AgriStack Passport", "Sovereign Soil & Credit Score", Color(0xFF66BB6A), onNavigateToAgriStack)
                }
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    QuickActionTile(Modifier.weight(1f), Icons.Filled.Build, "YantraShare Hub", "P2P Machinery & Escrow", Color(0xFF26C6DA), onNavigateToYantraShare)
                    QuickActionTile(Modifier.weight(1f), Icons.Filled.Eco, "BioRx Formulator", "Indigenous Organic Recipes", Color(0xFFC8E837), onNavigateToBioRx)
                }
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    QuickActionTile(Modifier.weight(0.5f), Icons.Filled.Download, "Saved Reports", "View downloaded files", Color(0xFFAED581), onNavigateToSavedReports)
                    Spacer(Modifier.weight(0.5f))
                }
            }

            Spacer(Modifier.height(32.dp))

            // Dynamic Regional Outbreak Alert Section
            RegionalOutbreakAlertSection(
                userState = userState,
                alerts = activeAlerts,
                loading = alertsLoading,
                onNavigateToMarket = onNavigateToMarket,
                onNavigateToScan = onNavigateToScan
            )

            Spacer(Modifier.height(32.dp))

            // Fellow Farmers Near You (Supabase Synced)
            Row(Modifier.padding(horizontal = 16.dp), verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Filled.Group, contentDescription = null, tint = NuKropAccent, modifier = Modifier.size(16.dp))
                Spacer(Modifier.width(8.dp))
                Text("Active Farmers Near You (Range: < 15 km)", color = NuKropText, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(Modifier.height(12.dp))

            val nearbyFarmers = remember {
                listOf(
                    Triple("Ramesh Singh", "Growing Wheat • 1.8 km away", "R"),
                    Triple("Suresh Patel", "Growing Cotton • 4.2 km away", "S"),
                    Triple("Anil Kumar", "Growing Paddy • 7.5 km away", "A")
                )
            }

            Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                nearbyFarmers.forEach { (name, info, initial) ->
                    Box(
                        Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(16.dp))
                            .background(NuKropCard)
                            .border(1.dp, NuKropBadgeGreen.copy(alpha = 0.3f), RoundedCornerShape(16.dp))
                            .padding(14.dp)
                    ) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.SpaceBetween,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(
                                    modifier = Modifier
                                        .size(38.dp)
                                        .clip(CircleShape)
                                        .background(NuKropAccent.copy(alpha = 0.2f)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text(initial, color = NuKropAccent, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                                }
                                Spacer(Modifier.width(12.dp))
                                Column {
                                    Text(name, color = NuKropText, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                                    Text(info, color = NuKropTextMuted, fontSize = 11.sp)
                                }
                            }
                            Button(
                                onClick = onNavigateToChat,
                                colors = ButtonDefaults.buttonColors(containerColor = NuKropAccent.copy(alpha = 0.18f)),
                                contentPadding = PaddingValues(horizontal = 12.dp, vertical = 4.dp),
                                shape = RoundedCornerShape(10.dp)
                            ) {
                                Icon(Icons.AutoMirrored.Filled.Chat, contentDescription = null, tint = NuKropAccent, modifier = Modifier.size(14.dp))
                                Spacer(Modifier.width(4.dp))
                                Text("Connect", color = NuKropAccent, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }
        }

        if (showVoiceOs) {
            VoiceOsOverlay(
                onDismiss = { showVoiceOs = false },
                onNavigateToRoute = { route ->
                    when (route) {
                        "market" -> onNavigateToMarket()
                        "scanner" -> onNavigateToScan()
                        "equipment" -> onNavigateToYantraShare()
                        "logistics" -> onNavigateToGramHaul()
                    }
                }
            )
        }
    }
}

@Composable
fun RegionalOutbreakAlertSection(
    userState: String,
    alerts: List<OutbreakAlert>,
    loading: Boolean,
    onNavigateToMarket: () -> Unit,
    onNavigateToScan: () -> Unit
) {
    Column(Modifier.padding(horizontal = 16.dp)) {
        Row(
            Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    Icons.Filled.Radar,
                    contentDescription = null,
                    tint = if (alerts.isNotEmpty()) NuKropWarning else NuKropAccent,
                    modifier = Modifier.size(18.dp)
                )
                Spacer(Modifier.width(8.dp))
                Text(
                    "Regional Outbreak Alerts ($userState)",
                    color = NuKropText,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold
                )
            }
            if (alerts.isNotEmpty()) {
                Box(
                    Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(NuKropError.copy(alpha = 0.2f))
                        .padding(horizontal = 8.dp, vertical = 3.dp)
                ) {
                    Text(
                        "${alerts.size} ACTIVE",
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold,
                        color = NuKropError
                    )
                }
            }
        }

        Spacer(Modifier.height(12.dp))

        if (loading) {
            Box(
                Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(NuKropCard)
                    .padding(20.dp),
                contentAlignment = Alignment.Center
            ) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    CircularProgressIndicator(color = NuKropAccent, modifier = Modifier.size(16.dp), strokeWidth = 2.dp)
                    Text("Scanning National Outbreak Early Warning Grid...", color = NuKropTextMuted, fontSize = 12.sp)
                }
            }
        } else if (alerts.isNotEmpty()) {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                alerts.forEach { alert ->
                    OutbreakAlertHomeCard(alert = alert, onNavigateToMarket = onNavigateToMarket)
                }
            }
        } else {
            // Calm state / All Clear in Grid
            Box(
                Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(NuKropBadgeGreen.copy(alpha = 0.08f))
                    .border(1.dp, NuKropBadgeGreen.copy(alpha = 0.30f), RoundedCornerShape(16.dp))
                    .padding(16.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Box(
                        Modifier
                            .size(36.dp)
                            .clip(CircleShape)
                            .background(NuKropBadgeGreen.copy(alpha = 0.20f)),
                        contentAlignment = Alignment.Center
                    ) {
                        Text("🛡️", fontSize = 18.sp)
                    }
                    Column(Modifier.weight(1f)) {
                        Text(
                            "National Outbreak Grid: Normal",
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold,
                            color = NuKropBadgeGreen
                        )
                        Spacer(Modifier.height(2.dp))
                        Text(
                            "No epidemic alerts detected in $userState. Scan density is below warning threshold (< 100 scans in 7 days).",
                            fontSize = 11.sp,
                            color = NuKropTextMuted,
                            lineHeight = 16.sp
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun OutbreakAlertHomeCard(
    alert: OutbreakAlert,
    onNavigateToMarket: () -> Unit
) {
    val isEpicenter = alert.alertType.equals("EPICENTER", ignoreCase = true)
    val severityUpper = alert.severity.uppercase(Locale.ROOT)
    val alertColor = when (severityUpper) {
        "CRITICAL" -> Color(0xFFEF5350)
        "HIGH" -> Color(0xFFFF7043)
        "MODERATE" -> Color(0xFFFFCA28)
        else -> NuKropBadgeGreen
    }

    Box(
        Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(alertColor.copy(alpha = 0.12f))
            .border(1.5.dp, alertColor.copy(alpha = 0.45f), RoundedCornerShape(16.dp))
            .padding(16.dp)
    ) {
        Column {
            // Header Row: Type badge + Severity badge
            Row(
                Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    Box(
                        Modifier
                            .clip(RoundedCornerShape(6.dp))
                            .background(if (isEpicenter) Color(0xFFD32F2F) else Color(0xFFF57C00))
                            .padding(horizontal = 7.dp, vertical = 3.dp)
                    ) {
                        Text(
                            text = if (isEpicenter) "🔴 EPICENTER OUTBREAK" else "🟠 EARLY WARNING ALERT",
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color.White
                        )
                    }
                }
                Box(
                    Modifier
                        .clip(RoundedCornerShape(6.dp))
                        .background(alertColor.copy(alpha = 0.25f))
                        .padding(horizontal = 8.dp, vertical = 3.dp)
                ) {
                    Text(
                        text = "RISK: ${alert.severity}",
                        fontSize = 10.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = alertColor
                    )
                }
            }

            Spacer(Modifier.height(10.dp))

            // Disease Title & Origin
            Text(
                text = alert.diseaseName,
                fontSize = 16.sp,
                fontWeight = FontWeight.ExtraBold,
                color = NuKropText
            )
            Spacer(Modifier.height(4.dp))
            Text(
                text = if (isEpicenter) "Epicenter Location: ${alert.sourceState}" else "Origin: ${alert.sourceState} ➔ Spread Vector: ${alert.targetState}",
                fontSize = 12.sp,
                color = NuKropTextMuted,
                fontWeight = FontWeight.SemiBold
            )

            Spacer(Modifier.height(8.dp))

            // Scan Density Trigger explanation
            Box(
                Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(8.dp))
                    .background(Color(0x33000000))
                    .padding(8.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    Icon(Icons.Filled.Bolt, null, tint = alertColor, modifier = Modifier.size(14.dp))
                    Text(
                        text = "Scan Density: ${alert.scanCount} scans recorded (> ${alert.thresholdDensity} threshold in 7 days)",
                        fontSize = 11.sp,
                        color = NuKropText,
                        fontWeight = FontWeight.Medium
                    )
                }
            }

            Spacer(Modifier.height(8.dp))
            Text(
                text = alert.message,
                fontSize = 12.sp,
                color = NuKropTextMuted,
                lineHeight = 17.sp
            )

            Spacer(Modifier.height(8.dp))
            // Price impact teaser
            if (alert.predictedMarketImpactPct > 0) {
                Text(
                    text = "📈 Predicted Mandi Price Shock: +${alert.predictedMarketImpactPct}%",
                    fontSize = 12.sp,
                    color = alertColor,
                    fontWeight = FontWeight.Bold
                )
            }

            Spacer(Modifier.height(12.dp))

            // CTA Button to view market price impact
            Button(
                onClick = onNavigateToMarket,
                colors = ButtonDefaults.buttonColors(containerColor = alertColor),
                shape = RoundedCornerShape(10.dp),
                modifier = Modifier
                    .fillMaxWidth()
                    .height(42.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    Icon(Icons.AutoMirrored.Filled.TrendingUp, null, tint = NuKropDark, modifier = Modifier.size(16.dp))
                    Text("View Market Price Impact", color = NuKropDark, fontWeight = FontWeight.Bold, fontSize = 13.sp)
                }
            }
        }
    }
}

@Composable
fun QuickActionTile(modifier: Modifier, icon: ImageVector, title: String, subtitle: String, accentColor: Color, onClick: () -> Unit) {
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(16.dp))
            .background(Color(0xFF141A0A)) // Dark base for glassmorphism
            .border(1.dp, accentColor.copy(alpha = 0.35f), RoundedCornerShape(16.dp))
            .clickable(onClick = onClick)
            .padding(16.dp)
    ) {
        Column {
            Box(
                modifier = Modifier
                    .clip(RoundedCornerShape(8.dp))
                    .background(accentColor.copy(alpha = 0.15f))
                    .padding(8.dp)
            ) {
                Icon(icon, contentDescription = null, tint = accentColor, modifier = Modifier.size(24.dp))
            }
            Spacer(Modifier.height(16.dp))
            Text(title, fontSize = 14.sp, fontWeight = FontWeight.Bold, color = NuKropText, maxLines = 1)
            Spacer(Modifier.height(4.dp))
            Text(subtitle, fontSize = 10.sp, color = NuKropTextMuted, lineHeight = 14.sp, minLines = 2, maxLines = 2, overflow = TextOverflow.Ellipsis)
        }
    }
}

@Composable
fun WeatherDetail(icon: ImageVector, text: String) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, contentDescription = null, tint = NuKropAccent, modifier = Modifier.size(12.dp))
        Spacer(Modifier.width(4.dp))
        Text(text, color = Color.White, fontSize = 10.sp, fontWeight = FontWeight.Bold)
    }
}

private fun greeting(): String = when (Calendar.getInstance().get(Calendar.HOUR_OF_DAY)) {
    in 0..11 -> "Morning"; in 12..16 -> "Afternoon"; else -> "Evening"
}

@SuppressLint("MissingPermission")
private fun fetchWeather(context: android.content.Context, onResult: (WeatherData?, String?) -> Unit) {
    try {
        val client = com.google.android.gms.location.LocationServices.getFusedLocationProviderClient(context)
        client.getCurrentLocation(com.google.android.gms.location.Priority.PRIORITY_BALANCED_POWER_ACCURACY, null)
            .addOnSuccessListener { loc: android.location.Location? ->
                val lat = loc?.latitude ?: 18.5204
                val lon = loc?.longitude ?: 73.8567
                kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch {
                    val result = WeatherService.getWeather(lat, lon)
                    kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                        result.fold({ onResult(it, null) }, { onResult(null, it.message) })
                    }
                }
            }
            .addOnFailureListener { onResult(null, it.message) }
    } catch (e: Exception) { onResult(null, e.message) }
}
