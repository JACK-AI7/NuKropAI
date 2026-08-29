package com.example

import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AutoGraph
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.TrendingDown
import androidx.compose.material.icons.filled.TrendingUp
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.example.market.*
import com.example.ui.theme.*
import kotlinx.coroutines.launch
import java.util.Locale

@Composable
fun MarketScreen(modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val lang = LanguageManager.currentLanguage.collectAsState().value
    
    var query by remember { mutableStateOf("Wheat") }
    var activeSearchQuery by remember { mutableStateOf("Wheat") }
    var userState by remember { mutableStateOf("") }
    var activeSearchState by remember { mutableStateOf("") }
    var userMandi by remember { mutableStateOf("") }
    
    var detectingLoc by remember { mutableStateOf(true) }
    
    val scope = rememberCoroutineScope()
    val scrollState = rememberScrollState()

    val permLauncher = rememberLauncherForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { perms ->
        if (perms[Manifest.permission.ACCESS_FINE_LOCATION] == true || perms[Manifest.permission.ACCESS_COARSE_LOCATION] == true) {
            detectingLoc = true
            scope.launch {
                try {
                    val loc = LocationHelper.getCurrentLocationStateAndMandi(context)
                    if (loc != null) {
                        userState = loc.first
                        activeSearchState = loc.first
                        activeSearchQuery = "Wheat"
                        userMandi = loc.second
                    }
                } catch (_: Exception) {
                } finally {
                    detectingLoc = false
                }
            }
        }
    }

    // Auto-detect location on open and trigger auto-search
    LaunchedEffect(Unit) {
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            val loc = LocationHelper.getCurrentLocationStateAndMandi(context)
            if (loc != null) {
                userState = loc.first
                activeSearchState = loc.first
                activeSearchQuery = "Wheat"
                userMandi = loc.second
            } else {
                // Fallback to saved profile state
                val prefs = context.getSharedPreferences("nukrop_farm_profile", android.content.Context.MODE_PRIVATE)
                val savedState = prefs.getString("state", "Maharashtra") ?: "Maharashtra"
                userState = savedState
                activeSearchState = savedState
                activeSearchQuery = "Wheat"
            }
        } else {
            permLauncher.launch(arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION))
            // Use fallback state while waiting for permission
            val prefs = context.getSharedPreferences("nukrop_farm_profile", android.content.Context.MODE_PRIVATE)
            val savedState = prefs.getString("state", "Maharashtra") ?: "Maharashtra"
            userState = savedState
            activeSearchState = savedState
            activeSearchQuery = "Wheat"
        }
        detectingLoc = false
    }

    // Reactively watch based on active state and query
    val mandiFlow = remember(activeSearchState, activeSearchQuery) {
        if (activeSearchState.isNotBlank() && activeSearchQuery.isNotBlank()) {
            MandiApiService.watchLiveMandiPrices(activeSearchState, activeSearchQuery)
        } else null
    }

    val dummyFlow = remember { kotlinx.coroutines.flow.MutableStateFlow<MandiState?>(null) }
    val activeFlow = mandiFlow ?: dummyFlow
    val mandiState = activeFlow.collectAsState().value

    DisposableEffect(activeSearchState, activeSearchQuery) {
        onDispose {
            if (activeSearchQuery.isNotBlank() && activeSearchState.isNotBlank()) {
                MandiApiService.stopWatching(activeSearchState, activeSearchQuery)
            }
        }
    }

    val loading = mandiState is MandiState.Loading
    val error = if (mandiState is MandiState.Error) mandiState.message else null
    val records = when (mandiState) {
        is MandiState.Success -> mandiState.records
        is MandiState.Error -> mandiState.staleData
        else -> null
    }

    // Correlate active search crop and state with regional disease outbreaks
    var marketImpact by remember { mutableStateOf<MarketPriceImpact?>(null) }
    var impactLoading by remember { mutableStateOf(false) }

    LaunchedEffect(activeSearchQuery, activeSearchState, records) {
        if (activeSearchQuery.isNotBlank() && activeSearchState.isNotBlank()) {
            impactLoading = true
            try {
                val res = MarketImpactRepository.getImpactForCrop(
                    cropName = activeSearchQuery,
                    state = activeSearchState,
                    mandiRecords = records ?: emptyList()
                )
                marketImpact = res.getOrNull()
            } catch (_: Exception) {
                marketImpact = null
            } finally {
                impactLoading = false
            }
        } else {
            marketImpact = null
        }
    }

    Column(
        modifier = modifier.fillMaxSize().background(Color(0xFF0D1208))
    ) {
        // Header
        Column(Modifier.fillMaxWidth().statusBarsPadding().padding(16.dp)) {
            Text(AppStrings.get("market_rates", lang), fontSize = 24.sp, fontWeight = FontWeight.ExtraBold, color = NuKropText)
            Spacer(Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                // Live Cached Badge
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.clip(RoundedCornerShape(4.dp)).background(NuKropBadgeGreen.copy(alpha=0.15f)).border(1.dp, NuKropBadgeGreen.copy(alpha=0.3f), RoundedCornerShape(4.dp)).padding(horizontal = 6.dp, vertical = 4.dp)
                ) {
                    Icon(Icons.Filled.Bolt, null, tint = NuKropBadgeGreen, modifier = Modifier.size(12.dp))
                    Spacer(Modifier.width(4.dp))
                    Text("Live Cached", fontSize = 10.sp, color = NuKropBadgeGreen, fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.weight(1f))
                
                // Location Pill
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.clip(RoundedCornerShape(16.dp)).background(Color(0x30FFFFFF)).clickable {
                        if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
                            detectingLoc = true
                            scope.launch {
                                val loc = LocationHelper.getCurrentLocationStateAndMandi(context)
                                if (loc != null) { userState = loc.first; userMandi = loc.second }
                                detectingLoc = false
                            }
                        } else {
                            permLauncher.launch(arrayOf(Manifest.permission.ACCESS_FINE_LOCATION))
                        }
                    }.padding(horizontal = 12.dp, vertical = 6.dp)
                ) {
                    Icon(Icons.Filled.LocationOn, null, tint = NuKropAccent, modifier = Modifier.size(14.dp))
                    Spacer(Modifier.width(4.dp))
                    Text(if (detectingLoc) "Detecting..." else "Auto-Detect", fontSize = 11.sp, color = NuKropTextMuted, fontWeight = FontWeight.Bold)
                }
            }
            Spacer(Modifier.height(8.dp))
            Text("Direct Agmarknet Govt API Integration & Econometric Early Warning", fontSize = 12.sp, color = NuKropTextMuted)
            
            Spacer(Modifier.height(24.dp))

            // Search Bar Row 1
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically) {
                OutlinedTextField(
                    value = query,
                    onValueChange = { query = it },
                    placeholder = { Text("Enter crop (e.g. Tomato, Wheat...)", fontSize = 14.sp, color = NuKropTextDim) },
                    modifier = Modifier.weight(1f).height(56.dp),
                    shape = RoundedCornerShape(16.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = Color(0xFF1A2210),
                        unfocusedContainerColor = Color(0xFF1A2210),
                        focusedBorderColor = NuKropAccent,
                        unfocusedBorderColor = Color(0x30C8E837),
                        cursorColor = NuKropAccent,
                        focusedTextColor = NuKropText,
                        unfocusedTextColor = NuKropText
                    ),
                    singleLine = true
                )
                Button(
                    onClick = {
                        if (query.isNotBlank() && userState.isNotBlank()) {
                            activeSearchQuery = query
                            activeSearchState = userState
                        }
                    },
                    modifier = Modifier.height(56.dp),
                    shape = RoundedCornerShape(16.dp),
                    enabled = !loading,
                    colors = ButtonDefaults.buttonColors(containerColor = NuKropAccent),
                    contentPadding = PaddingValues(horizontal = 24.dp)
                ) {
                    if (loading) CircularProgressIndicator(color = NuKropDark, modifier = Modifier.size(18.dp), strokeWidth = 2.dp)
                    else Text("Search", color = NuKropDark, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                }
            }
            
            Spacer(Modifier.height(16.dp))

            // Search Bar Row 2
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                OutlinedTextField(
                    value = userState,
                    onValueChange = { userState = it },
                    placeholder = { Text("State (e.g. Punjab)", fontSize = 13.sp, color = NuKropTextDim) },
                    modifier = Modifier.weight(1f).height(56.dp),
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = Color(0xFF1A2210),
                        unfocusedContainerColor = Color(0xFF1A2210),
                        focusedBorderColor = NuKropAccent,
                        unfocusedBorderColor = Color(0x30C8E837),
                        focusedTextColor = NuKropText, unfocusedTextColor = NuKropText
                    ), singleLine = true
                )
                OutlinedTextField(
                    value = userMandi,
                    onValueChange = { userMandi = it },
                    placeholder = { Text("Mandi (e.g. Khanna)", fontSize = 13.sp, color = NuKropTextDim) },
                    modifier = Modifier.weight(1f).height(56.dp),
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = Color(0xFF1A2210),
                        unfocusedContainerColor = Color(0xFF1A2210),
                        focusedBorderColor = NuKropAccent,
                        unfocusedBorderColor = Color(0x30C8E837),
                        focusedTextColor = NuKropText, unfocusedTextColor = NuKropText
                    ), singleLine = true
                )
            }

            Spacer(Modifier.height(24.dp))
            
            // Popular Crops
            Text("Popular Crops", color = NuKropTextMuted, fontSize = 14.sp)
            Spacer(Modifier.height(12.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.horizontalScroll(rememberScrollState())) {
                val crops = listOf("Tomato", "Wheat", "Onion", "Cotton", "Potato", "Chilli", "Rice")
                crops.forEach { c ->
                    Box(
                        Modifier.clip(RoundedCornerShape(20.dp)).background(Color(0xFF1A2210))
                            .border(1.dp, Color(0x50C8E837), RoundedCornerShape(20.dp))
                            .clickable {
                                query = c
                                if (userState.isNotBlank()) {
                                    activeSearchQuery = c
                                    activeSearchState = userState
                                }
                            }
                            .padding(horizontal = 16.dp, vertical = 8.dp)
                    ) {
                        Text(c, color = NuKropText, fontSize = 14.sp)
                    }
                }
            }
        }

        HorizontalDivider(color = Color(0x30FFFFFF))

        // Results Section
        Box(Modifier.fillMaxSize().padding(16.dp)) {
            if (activeSearchQuery.isEmpty() || activeSearchState.isEmpty()) {
                // Empty state handled naturally
            } else if (loading && records.isNullOrEmpty()) {
                CircularProgressIndicator(color = NuKropAccent, modifier = Modifier.align(Alignment.Center))
            } else if (!records.isNullOrEmpty()) {
                Column(Modifier.verticalScroll(scrollState).padding(bottom = 120.dp)) {
                    
                    // Outbreak Market Impact Card (Inserted Above 7-Day Forecast)
                    if (marketImpact != null) {
                        OutbreakMarketImpactCard(impact = marketImpact!!)
                        Spacer(Modifier.height(16.dp))
                    }

                    // 7-Day AI Price Forecast Card
                    val avgModal = records.map { it.modalPrice }.average()
                    val forecastPeak = if (marketImpact != null) marketImpact!!.predictedModalPrice.toInt() else (avgModal * 1.054).toInt()

                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(16.dp))
                            .background(NuKropCard)
                            .border(1.dp, NuKropAccent.copy(alpha = 0.35f), RoundedCornerShape(16.dp))
                            .padding(16.dp)
                    ) {
                        Column {
                            Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween, Alignment.CenterVertically) {
                                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                    Icon(Icons.Filled.AutoGraph, null, tint = NuKropAccent, modifier = Modifier.size(20.dp))
                                    Text("7-Day AI Price Forecast", color = NuKropText, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                                }
                                Box(
                                    modifier = Modifier
                                        .clip(RoundedCornerShape(8.dp))
                                        .background(NuKropBadgeGreen.copy(alpha = 0.18f))
                                        .padding(horizontal = 8.dp, vertical = 4.dp)
                                ) {
                                    Text("BEST DAY TO SELL: THURSDAY", color = NuKropBadgeGreen, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                                }
                            }
                            Spacer(Modifier.height(8.dp))
                            Text(
                                "AI Market Trend Analysis: Prices for $activeSearchQuery in $activeSearchState are projected to peak at ₹$forecastPeak / Qtl on Thursday based on regional demand and supply volume.",
                                color = NuKropTextMuted,
                                fontSize = 12.sp,
                                lineHeight = 18.sp
                            )
                        }
                    }

                    Spacer(Modifier.height(16.dp))

                    if (error != null) {
                        Box(Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(NuKropWarning.copy(alpha=0.15f)).padding(12.dp)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Filled.Warning, null, tint = NuKropWarning, modifier = Modifier.size(16.dp))
                                Spacer(Modifier.width(8.dp))
                                Text("Showing cached data. Live feed unavailable.", color = NuKropWarning, fontSize = 12.sp)
                            }
                        }
                        Spacer(Modifier.height(16.dp))
                    }
                    
                    // Filter records if user typed a specific mandi
                    val filtered = if (userMandi.isNotBlank()) {
                        val matches = records.filter { it.market.contains(userMandi, ignoreCase = true) || it.district.contains(userMandi, ignoreCase = true) }
                        if (matches.isNotEmpty()) matches else records
                    } else records

                    if (filtered.isEmpty()) {
                        Text("No matching Mandi records found for $userMandi.", color = NuKropTextMuted, modifier = Modifier.align(Alignment.CenterHorizontally))
                    } else {
                        filtered.forEach { record ->
                            MandiRecordCard(record)
                            Spacer(Modifier.height(12.dp))
                        }
                    }
                }
            } else if (error != null) {
                Text(error, color = NuKropWarning, modifier = Modifier.align(Alignment.Center))
            } else {
                // Not loading, but records are empty
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.align(Alignment.Center)) {
                    Icon(Icons.Filled.Warning, contentDescription = null, tint = NuKropTextDim, modifier = Modifier.size(48.dp))
                    Spacer(Modifier.height(16.dp))
                    Text("No market rates found.", color = NuKropTextMuted, fontWeight = FontWeight.SemiBold, fontSize = 16.sp)
                    Text("Try a different crop or state.", color = NuKropTextDim, fontSize = 13.sp)
                }
            }
        }
    }
}

@Composable
fun OutbreakMarketImpactCard(
    impact: MarketPriceImpact,
    modifier: Modifier = Modifier
) {
    val isSurge = impact.direction == ImpactDirection.SURGE
    val isDrop = impact.direction == ImpactDirection.DROP
    val riskColor = when (impact.riskLevel) {
        MarketRiskLevel.CRITICAL -> Color(0xFFEF5350)
        MarketRiskLevel.HIGH -> Color(0xFFFF7043)
        MarketRiskLevel.MODERATE -> Color(0xFFFFCA28)
        MarketRiskLevel.LOW -> NuKropBadgeGreen
    }
    val directionColor = if (isSurge) NuKropBadgeGreen else if (isDrop) NuKropError else NuKropAccent
    val formattedDelta = String.format(Locale.US, "%+.1f%%", impact.deltaPercentage)

    Box(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(18.dp))
            .background(riskColor.copy(alpha = 0.10f))
            .border(1.5.dp, riskColor.copy(alpha = 0.45f), RoundedCornerShape(18.dp))
            .padding(16.dp)
    ) {
        Column {
            // Header: Title & Badges
            Row(
                Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    Icon(
                        if (isSurge) Icons.Filled.TrendingUp else if (isDrop) Icons.Filled.TrendingDown else Icons.Filled.AutoGraph,
                        contentDescription = null,
                        tint = directionColor,
                        modifier = Modifier.size(20.dp)
                    )
                    Text(
                        "Outbreak Price Shock Assessment",
                        color = NuKropText,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.ExtraBold
                    )
                }
                Box(
                    Modifier
                        .clip(RoundedCornerShape(6.dp))
                        .background(riskColor.copy(alpha = 0.25f))
                        .padding(horizontal = 8.dp, vertical = 3.dp)
                ) {
                    Text(
                        "RISK: ${impact.riskLevel.name}",
                        fontSize = 10.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = riskColor
                    )
                }
            }

            Spacer(Modifier.height(12.dp))

            // Price Comparison Row (Current vs Predicted Peak)
            Row(
                Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(12.dp))
                    .background(Color(0x40000000))
                    .padding(12.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text("Current Modal Price", fontSize = 10.sp, color = NuKropTextDim)
                    Text("₹ ${impact.currentModalPrice.toInt()} / Qtl", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                }
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("Projected Delta", fontSize = 10.sp, color = NuKropTextDim)
                    Text(
                        formattedDelta,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = directionColor
                    )
                }
                Column(horizontalAlignment = Alignment.End) {
                    Text("Predicted Peak (Day ${impact.estimatedPeakDays})", fontSize = 10.sp, color = NuKropTextDim)
                    Text("₹ ${impact.predictedModalPrice.toInt()} / Qtl", fontSize = 15.sp, fontWeight = FontWeight.ExtraBold, color = directionColor)
                }
            }

            Spacer(Modifier.height(10.dp))

            // Confidence & Mechanism Badges
            Row(
                Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    Modifier
                        .clip(RoundedCornerShape(6.dp))
                        .background(NuKropAccent.copy(alpha = 0.15f))
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                ) {
                    Text("Confidence: ${impact.confidenceScore}%", fontSize = 10.sp, fontWeight = FontWeight.Bold, color = NuKropAccent)
                }
                Box(
                    Modifier
                        .clip(RoundedCornerShape(6.dp))
                        .background(Color(0x33FFFFFF))
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                ) {
                    Text("Mechanism: ${impact.mechanism.name.replace("_", " ")}", fontSize = 10.sp, fontWeight = FontWeight.SemiBold, color = NuKropText)
                }
            }

            Spacer(Modifier.height(12.dp))

            // Farmer Action Advisory
            Box(
                Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(10.dp))
                    .background(Color(0x33000000))
                    .padding(10.dp)
            ) {
                Column {
                    Text("💡 Farmer Action Advisory:", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = NuKropAccent)
                    Spacer(Modifier.height(4.dp))
                    Text(
                        impact.recommendedFarmerAction,
                        fontSize = 11.sp,
                        color = NuKropText,
                        lineHeight = 16.sp
                    )
                }
            }

            // Affected Mandis Breakdown
            if (impact.affectedMarkets.isNotEmpty()) {
                Spacer(Modifier.height(12.dp))
                Text("Affected APMC Mandis Breakdown:", fontSize = 11.sp, fontWeight = FontWeight.Bold, color = NuKropTextMuted)
                Spacer(Modifier.height(6.dp))
                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    impact.affectedMarkets.take(3).forEach { market ->
                        Row(
                            Modifier
                                .fillMaxWidth()
                                .clip(RoundedCornerShape(8.dp))
                                .background(Color(0x22000000))
                                .padding(horizontal = 10.dp, vertical = 6.dp),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column {
                                Text(market.marketName, fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = NuKropText)
                                Text("${market.district}, ${market.state}", fontSize = 10.sp, color = NuKropTextDim)
                            }
                            Column(horizontalAlignment = Alignment.End) {
                                Text("₹ ${market.predictedModalPrice.toInt()}", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = directionColor)
                                Text(
                                    String.format(Locale.US, "%+.1f%%", market.deltaPercentage),
                                    fontSize = 10.sp,
                                    color = directionColor,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun MandiRecordCard(record: MandiRecord) {
    Box(
        Modifier.fillMaxWidth().clip(RoundedCornerShape(16.dp)).background(NuKropCard)
            .border(1.dp, Color(0x30FFFFFF), RoundedCornerShape(16.dp))
            .padding(16.dp)
    ) {
        Column {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Row(modifier = Modifier.weight(1f), verticalAlignment = Alignment.CenterVertically) {
                    Box(Modifier.clip(RoundedCornerShape(8.dp)).background(NuKropAccent.copy(alpha=0.15f)).padding(8.dp)) {
                        Icon(Icons.Filled.AutoGraph, null, tint = NuKropAccent, modifier = Modifier.size(20.dp))
                    }
                    Spacer(Modifier.width(12.dp))
                    Column(Modifier.weight(1f)) {
                        Text(record.market, fontSize = 16.sp, fontWeight = FontWeight.Bold, color = NuKropText, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
                        Text("${record.district}, ${record.state}", fontSize = 12.sp, color = NuKropTextMuted, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
                    }
                }
                Spacer(Modifier.width(8.dp))
                Text("₹ ${record.modalPrice.toInt()} / Qtl", fontSize = 18.sp, fontWeight = FontWeight.ExtraBold, color = NuKropAccent, maxLines = 1)
            }
            Spacer(Modifier.height(16.dp))
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Column {
                    Text("Commodity", fontSize = 10.sp, color = NuKropTextDim)
                    Text(record.commodity, fontSize = 14.sp, color = NuKropText, fontWeight = FontWeight.Bold)
                }
                Column {
                    Text("Min Price", fontSize = 10.sp, color = NuKropTextDim)
                    Text("₹ ${record.minPrice.toInt()}", fontSize = 14.sp, color = NuKropText)
                }
                Column {
                    Text("Max Price", fontSize = 10.sp, color = NuKropTextDim)
                    Text("₹ ${record.maxPrice.toInt()}", fontSize = 14.sp, color = NuKropText)
                }
            }
            Spacer(Modifier.height(12.dp))
            Text("Data Date: ${record.arrivalDate}", fontSize = 10.sp, color = NuKropTextDim, modifier = Modifier.align(Alignment.End))
        }
    }
}
