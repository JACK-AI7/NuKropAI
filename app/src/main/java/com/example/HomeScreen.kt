package com.example

import android.Manifest
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import android.location.Location
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.*
import androidx.compose.animation.core.*
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.TrendingDown
import androidx.compose.material.icons.automirrored.filled.TrendingUp
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import coil.compose.AsyncImage
import com.example.ui.theme.*
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import kotlinx.coroutines.delay
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
    onNavigateToFinance: () -> Unit = {}
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val scrollState = rememberScrollState()

    var weather by remember { mutableStateOf<WeatherData?>(null) }
    var weatherError by remember { mutableStateOf<String?>(null) }
    var weatherLoading by remember { mutableStateOf(true) }

    val hasLocation = remember {
        ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
    }
    val locLauncher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        if (granted) scope.launch { fetchWeather(context) { w, e -> weather = w; weatherError = e; weatherLoading = false } }
        else { weatherLoading = false; weatherError = "Location permission denied" }
    }
    LaunchedEffect(Unit) {
        if (hasLocation) {
            fetchWeather(context) { w, e -> weather = w; weatherError = e; weatherLoading = false }
        } else {
            weatherLoading = false
            weatherError = "Tap to grant location"
        }
        PriceTickerService.start()
    }

    val tickerItems by PriceTickerService.tickerItems.collectAsState()
    val tickerLoading by PriceTickerService.isLoading.collectAsState()
    val now = remember { SimpleDateFormat("d MMM yyyy | h:mm a", Locale.getDefault()).format(Date()) }
    var trackedCrops by remember { mutableStateOf(PriceTracker.getTrackedCrops(context)) }
    LaunchedEffect(Unit) { trackedCrops = PriceTracker.getTrackedCrops(context) }

    Box(modifier = modifier.fillMaxSize().background(Color(0xFF0D1208))) {
        Column(Modifier.fillMaxSize().verticalScroll(scrollState)) {

            // ── Hero Section ──────────────────────────────────────
            Box(Modifier.fillMaxWidth().height(260.dp)) {
                AsyncImage(
                    model = "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&q=80",
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
                        Box(Modifier.size(44.dp).clip(CircleShape)
                            .background(Brush.linearGradient(listOf(NuKropGreen, NuKropAccent))),
                            Alignment.Center
                        ) { Icon(Icons.Filled.Person, null, tint = NuKropDark, modifier = Modifier.size(24.dp)) }
                        Column {
                            Text("Good ${greeting()}, Farmer!", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                            Text(now, fontSize = 10.sp, color = Color.White.copy(alpha = 0.7f), maxLines = 1, overflow = TextOverflow.Ellipsis)
                        }
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        IconButton(
                            onClick = { UpdateManager.checkAndUpdate(context) },
                            modifier = Modifier.size(36.dp).clip(CircleShape).background(Color(0x88000000))
                        ) { Icon(Icons.Default.Refresh, null, tint = NuKropAccent, modifier = Modifier.size(18.dp)) }
                        IconButton(
                            onClick = {},
                            modifier = Modifier.size(36.dp).clip(CircleShape).background(Color(0x88000000))
                        ) { Icon(Icons.Default.Notifications, null, tint = Color.White.copy(0.7f), modifier = Modifier.size(18.dp)) }
                    }
                }
                // Glassmorphism weather pill at bottom of hero
                Box(
                    Modifier.align(Alignment.BottomCenter).padding(16.dp).fillMaxWidth()
                        .clip(RoundedCornerShape(16.dp))
                        .background(Color(0x99000000))
                        .border(1.dp, Color(0x40C8E837), RoundedCornerShape(16.dp))
                        .padding(horizontal = 16.dp, vertical = 10.dp)
                ) {
                    when {
                        weatherLoading -> Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            CircularProgressIndicator(color = NuKropAccent, modifier = Modifier.size(14.dp), strokeWidth = 2.dp)
                            Text("Fetching live weather...", fontSize = 12.sp, color = Color.White.copy(0.7f))
                        }
                        weatherError != null -> Row(
                            verticalAlignment = Alignment.CenterVertically, 
                            horizontalArrangement = Arrangement.spacedBy(6.dp),
                            modifier = Modifier.clickable { 
                                if (!hasLocation) locLauncher.launch(Manifest.permission.ACCESS_FINE_LOCATION) 
                            }
                        ) {
                            Icon(Icons.Default.Warning, null, tint = NuKropWarning, modifier = Modifier.size(14.dp))
                            Text("Weather: $weatherError", fontSize = 12.sp, color = NuKropWarning)
                        }
                        weather != null -> Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween, Alignment.CenterVertically) {
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                Icon(Icons.Filled.WbSunny, null, tint = Color(0xFFFFCA28), modifier = Modifier.size(28.dp))
                                Column {
                                    Text("${weather!!.temperature.toInt()}°C  •  ${weather!!.description}", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                                    Text("Feels ${weather!!.feelsLike.toInt()}°C", fontSize = 10.sp, color = Color.White.copy(0.6f))
                                }
                            }
                            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                WeatherPill(Icons.Filled.WaterDrop, "${weather!!.humidity.toInt()}%")
                                WeatherPill(Icons.Filled.Air, "${weather!!.windSpeed.toInt()}km/h")
                                WeatherPill(Icons.Filled.Cloud, "${weather!!.precipitation}mm")
                            }
                        }
                    }
                }
            }

            // ── Rain Alert ────────────────────────────────────────
            if (weather?.isRainAlert == true) {
                Row(
                    Modifier.padding(horizontal = 16.dp, vertical = 6.dp).fillMaxWidth()
                        .clip(RoundedCornerShape(10.dp))
                        .background(Color(0xFF3A2000))
                        .border(1.dp, NuKropWarning.copy(0.5f), RoundedCornerShape(10.dp))
                        .padding(10.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Icon(Icons.Filled.Warning, null, tint = NuKropWarning, modifier = Modifier.size(16.dp))
                    Text(weather!!.alertMessage, fontSize = 12.sp, color = NuKropWarning, lineHeight = 17.sp)
                }
            }

            // ── Live Price Ticker ─────────────────────────────────
            Spacer(Modifier.height(10.dp))
            Box(
                Modifier.fillMaxWidth()
                    .background(Color(0xFF141A0A))
                    .border(Dp = 0.5.dp, color = NuKropAccent.copy(0.2f))
            ) {
                if (tickerLoading || tickerItems.isEmpty()) {
                    Row(
                        Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        CircularProgressIndicator(color = NuKropAccent, modifier = Modifier.size(10.dp), strokeWidth = 2.dp)
                        Text("Loading live market rates...", fontSize = 11.sp, color = NuKropTextMuted)
                    }
                } else {
                    LiveTickerRow(tickerItems, onNavigateToMarket)
                }
            }

            Spacer(Modifier.height(16.dp))

            // ── Quick Actions ─────────────────────────────────────
            SectionHeader("Quick Actions", Icons.Filled.GridView)
            Spacer(Modifier.height(10.dp))
            Column(Modifier.padding(horizontal = 16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    QuickActionTile(Modifier.weight(1f), Icons.Filled.Science, "Scan Crop", "AI Disease & Pest Detect", NuKropAccent, onNavigateToScan)
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
            }

            Spacer(Modifier.height(20.dp))

            // ── Tracked Prices ────────────────────────────────────
            if (trackedCrops.isNotEmpty()) {
                SectionHeader("My Tracked Prices", Icons.Filled.Favorite)
                Spacer(Modifier.height(10.dp))
                Row(
                    Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).padding(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    trackedCrops.forEach { crop ->
                        Box(
                            Modifier.width(160.dp).clip(RoundedCornerShape(14.dp))
                                .background(Brush.verticalGradient(listOf(Color(0xFF1E2A12), Color(0xFF141A0A))))
                                .border(1.dp, NuKropAccent.copy(0.3f), RoundedCornerShape(14.dp))
                                .clickable { onNavigateToMarket() }
                                .padding(12.dp)
                        ) {
                            Column {
                                Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween, Alignment.CenterVertically) {
                                    Text(crop.crop, fontSize = 14.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                                    if (crop.basePrice >= crop.targetPrice && crop.targetPrice > 0)
                                        Icon(Icons.Filled.LocalFireDepartment, null, tint = NuKropWarning, modifier = Modifier.size(14.dp))
                                }
                                Text("${crop.mandi}, ${crop.state}", fontSize = 10.sp, color = NuKropTextMuted, maxLines = 1, overflow = TextOverflow.Ellipsis)
                                Spacer(Modifier.height(8.dp))
                                Text("₹${crop.basePrice.toInt()}", fontSize = 18.sp, fontWeight = FontWeight.ExtraBold, color = NuKropAccent)
                                if (crop.targetPrice > 0) Text("Target: ₹${crop.targetPrice.toInt()}", fontSize = 10.sp, color = NuKropWarning)
                            }
                        }
                    }
                }
                Spacer(Modifier.height(20.dp))
            }

            // ── Pest Radar ────────────────────────────────────────
            var pestAlertCount by remember { mutableStateOf(3) }
            var reportingPest by remember { mutableStateOf(false) }
            var reportedSuccess by remember { mutableStateOf(false) }

            SectionHeader("Hyperlocal Pest Prediction AI", Icons.Filled.Radar)
            Spacer(Modifier.height(10.dp))
            Card(
                colors = CardDefaults.cardColors(containerColor = Color(0xFF1A1F0F)),
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp)
                    .border(1.dp, NuKropError.copy(0.3f), RoundedCornerShape(16.dp))
            ) {
                Column(Modifier.padding(16.dp)) {
                    Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween, Alignment.CenterVertically) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Icon(Icons.Filled.Radar, null, tint = NuKropError, modifier = Modifier.size(20.dp))
                            Text("$pestAlertCount High-Risk Vectors", fontWeight = FontWeight.Bold, color = NuKropError, fontSize = 14.sp)
                        }
                        Box(Modifier.clip(RoundedCornerShape(6.dp)).background(NuKropError.copy(0.15f)).padding(horizontal = 8.dp, vertical = 3.dp)) {
                            Text("HIGH RISK", color = NuKropError, fontSize = 9.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                    Spacer(Modifier.height(8.dp))
                    Text(
                        "Fall Armyworm detected 4.2km West in Rampur.\nWind: East 12 km/h. Arrival: ~18 hours.\nAction: Spray neem oil within 48 hours.",
                        color = NuKropTextMuted, fontSize = 12.sp, lineHeight = 18.sp
                    )
                    Spacer(Modifier.height(12.dp))
                    Button(
                        onClick = { reportingPest = true; reportedSuccess = false },
                        colors = ButtonDefaults.buttonColors(containerColor = NuKropError),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        if (reportingPest) CircularProgressIndicator(color = NuKropDark, modifier = Modifier.size(18.dp), strokeWidth = 2.dp)
                        else Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Filled.Warning, null, tint = NuKropDark, modifier = Modifier.size(16.dp))
                            Text("Report Outbreak in My Field", color = NuKropDark, fontWeight = FontWeight.Bold)
                        }
                    }
                    if (reportingPest) {
                        LaunchedEffect(Unit) { delay(2000); reportingPest = false; reportedSuccess = true; pestAlertCount++ }
                    }
                    if (reportedSuccess) {
                        Spacer(Modifier.height(8.dp))
                        Box(Modifier.fillMaxWidth().clip(RoundedCornerShape(8.dp)).background(NuKropBadgeGreen.copy(0.2f)).padding(8.dp), Alignment.Center) {
                            Text("Outbreak logged. 14 neighboring farmers alerted!", color = NuKropBadgeGreen, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            }

            Spacer(Modifier.height(20.dp))

            // ── Task Schedules ────────────────────────────────────
            SectionHeader("AI Task Schedules", Icons.Filled.CalendarMonth)
            Spacer(Modifier.height(10.dp))
            Row(Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                TaskScheduleCard("Tomato", "Day 45", "Apply organic fungicide", NuKropError)
                TaskScheduleCard("Wheat", "Day 12", "First irrigation cycle", Color(0xFF64B5F6))
                TaskScheduleCard("Cotton", "Day 60", "Pest inspection due", NuKropWarning)
            }

            Spacer(Modifier.height(20.dp))

            // ── Farm Tips ─────────────────────────────────────────
            SectionHeader("Today's Farm Tips", Icons.Filled.Lightbulb)
            Spacer(Modifier.height(10.dp))
            val tips = listOf(
                Triple(Icons.Filled.WaterDrop, "Irrigation", "Best time to irrigate: 6-8 AM to minimize evaporation losses."),
                Triple(Icons.Filled.Spa, "Sowing", "Check soil moisture before sowing. Optimal germination needs 50-60% moisture."),
                Triple(Icons.Filled.BugReport, "Pest Watch", "Inspect crop undersides for eggs/larvae weekly during kharif season."),
                Triple(Icons.Filled.Thermostat, "Heat Stress", "If temperature exceeds 35C, consider shade nets for vegetable crops.")
            )
            tips.forEach { (icon, title, desc) -> TipCard(icon, title, desc); Spacer(Modifier.height(8.dp)) }

        }
    }
}

@Composable
fun LiveTickerRow(items: List<TickerItem>, onClick: () -> Unit) {
    val infiniteTransition = rememberInfiniteTransition(label = "ticker")
    val scrollOffset by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(items.size * 4000, easing = LinearEasing), RepeatMode.Restart),
        label = "ticker_scroll"
    )

    Row(
        Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()).padding(horizontal = 8.dp, vertical = 7.dp),
        horizontalArrangement = Arrangement.spacedBy(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // "LIVE" badge
        Box(Modifier.clip(RoundedCornerShape(4.dp)).background(NuKropError).padding(horizontal = 6.dp, vertical = 2.dp)) {
            Text("LIVE", color = Color.White, fontSize = 9.sp, fontWeight = FontWeight.ExtraBold)
        }
        Text("MANDI PRICES", fontSize = 9.sp, color = NuKropAccent, fontWeight = FontWeight.Bold)
        Box(Modifier.width(1.dp).height(14.dp).background(Color(0x30FFFFFF)))

        // Duplicate list for seamless loop effect
        (items + items).forEach { item ->
            TickerChip(item, onClick)
        }
    }
}

@Composable
fun TickerChip(item: TickerItem, onClick: () -> Unit) {
    Row(
        Modifier.clickable(onClick = onClick).padding(horizontal = 4.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        Text(item.commodity, fontSize = 11.sp, fontWeight = FontWeight.Bold, color = NuKropText)
        Text("₹${item.modalPrice.toInt()}", fontSize = 11.sp, fontWeight = FontWeight.ExtraBold,
            color = if (item.isUp) NuKropBadgeGreen else if (item.isDown) NuKropError else NuKropTextMuted)
        when {
            item.isUp -> Icon(Icons.AutoMirrored.Filled.TrendingUp, null, tint = NuKropBadgeGreen, modifier = Modifier.size(12.dp))
            item.isDown -> Icon(Icons.AutoMirrored.Filled.TrendingDown, null, tint = NuKropError, modifier = Modifier.size(12.dp))
            else -> Icon(Icons.Filled.Remove, null, tint = NuKropTextMuted, modifier = Modifier.size(12.dp))
        }
        if (item.delta != 0.0) {
            Text(
                "${if (item.isUp) "+" else ""}${String.format("%.1f", item.changePercent)}%",
                fontSize = 9.sp, color = if (item.isUp) NuKropBadgeGreen else NuKropError, fontWeight = FontWeight.Bold
            )
        }
        Box(Modifier.width(1.dp).height(10.dp).background(Color(0x20FFFFFF)))
    }
}

@Composable
fun WeatherPill(icon: ImageVector, value: String) {
    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(3.dp)) {
        Icon(icon, null, tint = NuKropAccent, modifier = Modifier.size(12.dp))
        Text(value, fontSize = 10.sp, color = Color.White.copy(0.8f), fontWeight = FontWeight.SemiBold)
    }
}

@Composable
fun SectionHeader(title: String, icon: ImageVector) {
    Row(
        Modifier.padding(horizontal = 16.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Icon(icon, null, tint = NuKropAccent, modifier = Modifier.size(16.dp))
        Text(title, fontSize = 15.sp, fontWeight = FontWeight.Bold, color = NuKropText)
    }
}

@Composable
fun QuickActionTile(modifier: Modifier, icon: ImageVector, title: String, subtitle: String, accentColor: Color, onClick: () -> Unit) {
    Box(
        modifier = modifier.clip(RoundedCornerShape(16.dp))
            .background(Brush.verticalGradient(listOf(Color(0xFF1E2A12), Color(0xFF141A0A))))
            .border(1.dp, accentColor.copy(alpha = 0.35f), RoundedCornerShape(16.dp))
            .clickable(onClick = onClick)
            .padding(14.dp)
    ) {
        Column {
            Box(Modifier.size(40.dp).clip(RoundedCornerShape(10.dp)).background(accentColor.copy(0.15f)), Alignment.Center) {
                Icon(icon, null, tint = accentColor, modifier = Modifier.size(22.dp))
            }
            Spacer(Modifier.height(10.dp))
            Text(title, fontSize = 13.sp, fontWeight = FontWeight.Bold, color = NuKropText)
            Text(subtitle, fontSize = 10.sp, color = NuKropTextMuted, lineHeight = 14.sp)
        }
    }
}

@Composable
fun TipCard(icon: ImageVector, title: String, desc: String) {
    Row(
        Modifier.fillMaxWidth().padding(horizontal = 16.dp)
            .clip(RoundedCornerShape(14.dp))
            .background(Color(0xFF1A1F0F))
            .padding(12.dp),
        verticalAlignment = Alignment.Top,
        horizontalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        Box(Modifier.clip(CircleShape).background(NuKropSurface).padding(8.dp)) {
            Icon(icon, null, tint = NuKropAccent, modifier = Modifier.size(20.dp))
        }
        Column {
            Text(title, fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = NuKropAccent)
            Text(desc, fontSize = 12.sp, color = NuKropTextMuted, lineHeight = 18.sp)
        }
    }
}

private fun greeting(): String = when (Calendar.getInstance().get(Calendar.HOUR_OF_DAY)) {
    in 0..11 -> "Morning"; in 12..16 -> "Afternoon"; else -> "Evening"
}

@SuppressLint("MissingPermission")
private fun fetchWeather(context: android.content.Context, onResult: (WeatherData?, String?) -> Unit) {
    try {
        val client = LocationServices.getFusedLocationProviderClient(context)
        client.getCurrentLocation(Priority.PRIORITY_BALANCED_POWER_ACCURACY, null)
            .addOnSuccessListener { loc: Location? ->
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

@Composable
fun TaskScheduleCard(crop: String, day: String, task: String, accent: Color) {
    Box(
        Modifier.width(150.dp).clip(RoundedCornerShape(14.dp))
            .background(Color(0xFF1A1F0F))
            .border(1.dp, accent.copy(0.3f), RoundedCornerShape(14.dp))
            .padding(12.dp)
    ) {
        Column {
            Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween) {
                Text(crop, fontSize = 13.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                Text(day, fontSize = 9.sp, color = accent, fontWeight = FontWeight.SemiBold)
            }
            Spacer(Modifier.height(8.dp))
            Text(task, fontSize = 11.sp, color = NuKropTextMuted, lineHeight = 15.sp)
        }
    }
}

// Extension for Border without named Dp param clash
private fun Modifier.border(Dp: androidx.compose.ui.unit.Dp, color: Color): Modifier = this.then(
    Modifier.border(Dp, color)
)
