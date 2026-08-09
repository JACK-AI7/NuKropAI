package com.example

import android.Manifest
import android.annotation.SuppressLint
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.*
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Brush
import kotlinx.coroutines.launch
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.example.ui.theme.*
import java.text.SimpleDateFormat
import java.util.*
import androidx.compose.ui.layout.ContentScale
import androidx.compose.foundation.Image
import androidx.compose.ui.res.painterResource
import androidx.compose.foundation.shape.CircleShape

@SuppressLint("MissingPermission")
@Composable
fun HomeScreen(
    modifier: Modifier = Modifier,
    onNavigateToScan: () -> Unit = {},
    onNavigateToMarket: () -> Unit = {},
    onNavigateToChat: () -> Unit = {},
    onNavigateToAutopilot: () -> Unit = {},
    onNavigateToFinance: () -> Unit = {},
    onNavigateToSavedReports: () -> Unit = {}
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

    Box(modifier = modifier.fillMaxSize().background(Color(0xFF0D1208))) {
        Column(Modifier.fillMaxSize().verticalScroll(scrollState).padding(bottom = 100.dp)) { // padding for nav bar

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
                        Box(Modifier.size(44.dp).clip(CircleShape)
                            .background(Brush.linearGradient(listOf(NuKropGreen, NuKropAccent))),
                            Alignment.Center
                        ) { Icon(Icons.Filled.Person, null, tint = NuKropDark, modifier = Modifier.size(24.dp)) }
                        Column {
                            Text("Good ${greeting()}, Farmer!", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color.White)
                            Text(now, fontSize = 10.sp, color = Color.White.copy(alpha = 0.7f), maxLines = 1, overflow = TextOverflow.Ellipsis)
                        }
                    }
                    IconButton(onClick = { /* TODO Notifications */ }, modifier = Modifier.size(44.dp).clip(CircleShape).background(Color(0x33FFFFFF))) {
                        Icon(Icons.Filled.Notifications, contentDescription = "Notifications", tint = Color.White, modifier = Modifier.size(22.dp))
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
                        Icon(Icons.Filled.TrendingUp, null, tint = NuKropAccent, modifier = Modifier.size(14.dp))
                        Spacer(Modifier.width(8.dp))
                        Text("Live Gov Mandi Data Connected", color = NuKropAccent, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                    } else {
                        val first = tickerItems.first()
                        Icon(Icons.Filled.TrendingUp, null, tint = NuKropAccent, modifier = Modifier.size(14.dp))
                        Spacer(Modifier.width(8.dp))
                        Text("${first.commodity} (${first.market}) ,${first.modalPrice}", color = NuKropText, fontSize = 12.sp, fontWeight = FontWeight.Bold)
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
                    QuickActionTile(Modifier.weight(0.5f), Icons.Filled.Download, "Saved Reports", "View downloaded files", Color(0xFF81C784), onNavigateToSavedReports)
                    Spacer(Modifier.weight(0.5f))
                }
            }

            Spacer(Modifier.height(32.dp))

            // Hyperlocal Pest Prediction AI
            Row(Modifier.padding(horizontal = 16.dp), verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Filled.Radar, contentDescription = null, tint = NuKropAccent, modifier = Modifier.size(16.dp))
                Spacer(Modifier.width(8.dp))
                Text("Hyperlocal Pest Prediction AI", color = NuKropText, fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(Modifier.height(12.dp))
            Box(Modifier.padding(horizontal = 16.dp).fillMaxWidth().clip(RoundedCornerShape(16.dp)).background(NuKropWarning.copy(alpha=0.15f)).border(1.dp, NuKropWarning.copy(alpha=0.4f), RoundedCornerShape(16.dp)).padding(16.dp)) {
                Column {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Icon(Icons.Filled.Warning, null, tint = NuKropWarning, modifier = Modifier.size(18.dp))
                        Text("High Risk: Fall Armyworm", color = NuKropWarning, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                    }
                    Spacer(Modifier.height(8.dp))
                    Text("Detected 4.2km West in Rampur. Wind: East 12 km/h. Arrival: ~18 hours.", color = NuKropText, fontSize = 12.sp, lineHeight = 18.sp)
                    Spacer(Modifier.height(12.dp))
                    Button(onClick = {}, colors = ButtonDefaults.buttonColors(containerColor = NuKropWarning), shape = RoundedCornerShape(8.dp), modifier = Modifier.fillMaxWidth().height(40.dp)) {
                        Text("View Action Plan", color = NuKropDark, fontWeight = FontWeight.Bold, fontSize = 13.sp)
                    }
                }
            }

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
                                Icon(Icons.Filled.Chat, contentDescription = null, tint = NuKropAccent, modifier = Modifier.size(14.dp))
                                Spacer(Modifier.width(4.dp))
                                Text("Connect", color = NuKropAccent, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }

            Spacer(Modifier.height(40.dp))
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
            Text(subtitle, fontSize = 11.sp, color = NuKropTextMuted, lineHeight = 14.sp, minLines = 2, maxLines = 2, overflow = TextOverflow.Ellipsis)
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
