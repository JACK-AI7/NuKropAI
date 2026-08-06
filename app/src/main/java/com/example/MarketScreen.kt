package com.example

import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material.icons.filled.AutoGraph
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
import androidx.compose.ui.platform.LocalContext
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import android.Manifest
import android.content.pm.PackageManager
import androidx.core.content.ContextCompat
import com.example.ui.theme.*
import kotlinx.coroutines.launch

@Composable
fun MarketScreen(modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val lang = LanguageManager.currentLanguage.collectAsState().value
    
    var query by remember { mutableStateOf("") }
    var activeSearchQuery by remember { mutableStateOf("") }
    var activeSearchState by remember { mutableStateOf("") }
    
    var userState by remember { mutableStateOf("") }
    var userMandi by remember { mutableStateOf("") }
    var detectingLoc by remember { mutableStateOf(false) }
    
    val scope = rememberCoroutineScope()
    val scrollState = rememberScrollState()

    val permLauncher = rememberLauncherForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { perms ->
        if (perms[Manifest.permission.ACCESS_FINE_LOCATION] == true || perms[Manifest.permission.ACCESS_COARSE_LOCATION] == true) {
            detectingLoc = true
            scope.launch {
                val loc = LocationHelper.getCurrentLocationStateAndMandi(context)
                if (loc != null) {
                    userState = loc.first
                    userMandi = loc.second
                }
                detectingLoc = false
            }
        }
    }

    // Collect Flow dynamically
    val mandiFlow = remember(activeSearchQuery, activeSearchState) {
        if (activeSearchQuery.isNotBlank() && activeSearchState.isNotBlank()) {
            MandiApiService.watchLiveMandiPrices(activeSearchState, activeSearchQuery)
        } else null
    }
    // FIX: Always call collectAsState to avoid Compose tree structural changes
    val dummyFlow = remember { kotlinx.coroutines.flow.MutableStateFlow<MandiState?>(null) }
    val activeFlow = mandiFlow ?: dummyFlow
    val mandiState = activeFlow.collectAsState().value

    // Cleanup watcher when leaving
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

    Column(
        modifier = modifier.fillMaxSize()
            .background(Brush.verticalGradient(listOf(NuKropDark, Color(0xFF1A2010))))
    ) {
        // Header with Location
        Box(
            Modifier.fillMaxWidth()
                .background(Brush.verticalGradient(listOf(Color(0xFF2D3A1C), NuKropDark)))
                .statusBarsPadding().padding(16.dp)
        ) {
            Column {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(AppStrings.get("market_rates", lang), fontSize = 22.sp, fontWeight = FontWeight.ExtraBold, color = NuKropText)
                        Box(Modifier.clip(RoundedCornerShape(4.dp)).background(NuKropBadgeGreen.copy(alpha=0.2f)).padding(horizontal = 4.dp, vertical = 2.dp)) {
                            Text("⚡ Live Cached", fontSize = 9.sp, color = NuKropBadgeGreen, fontWeight = FontWeight.Bold)
                        }
                    }
                    
                    // Location Pill
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Box(
                            Modifier.clip(RoundedCornerShape(20.dp))
                                .background(if (userMandi.isNotEmpty() || userState.isNotEmpty()) NuKropAccent.copy(alpha=0.15f) else Color(0x30FFFFFF))
                                .border(1.dp, if (userMandi.isNotEmpty() || userState.isNotEmpty()) NuKropAccent.copy(alpha=0.5f) else Color.Transparent, RoundedCornerShape(20.dp))
                                .clickable {
                                    if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
                                        detectingLoc = true
                                        scope.launch {
                                            val loc = LocationHelper.getCurrentLocationStateAndMandi(context)
                                            if (loc != null) { userState = loc.first; userMandi = loc.second }
                                            detectingLoc = false
                                        }
                                    } else {
                                        permLauncher.launch(arrayOf(Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION))
                                    }
                                }
                                .padding(horizontal = 12.dp, vertical = 6.dp)
                        ) {
                            if (detectingLoc) {
                                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                    CircularProgressIndicator(color = NuKropAccent, modifier = Modifier.size(12.dp), strokeWidth = 2.dp)
                                    Text(AppStrings.get("detecting", lang), fontSize = 11.sp, color = NuKropTextMuted)
                                }
                            } else {
                                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                    Icon(Icons.Filled.LocationOn, contentDescription = null, tint = NuKropAccent, modifier = Modifier.size(14.dp))
                                    val locText = if (userMandi.isNotEmpty()) "$userMandi, $userState" else if (userState.isNotEmpty()) userState else AppStrings.get("auto_detect", lang)
                                    Text(locText, fontSize = 11.sp, color = if (userState.isNotEmpty()) NuKropAccent else NuKropTextMuted, fontWeight = FontWeight.Bold)
                                }
                            }
                        }
                    }
                }
                Spacer(Modifier.height(4.dp))
                Text(AppStrings.get("powered_by", lang) + " Gov & Redis", fontSize = 12.sp, color = NuKropTextMuted)
            }
        }

        // Search bar
        Row(
            Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            OutlinedTextField(
                value = query,
                onValueChange = { query = it },
                placeholder = { Text(AppStrings.get("search_placeholder", lang), fontSize = 13.sp, color = NuKropTextDim) },
                modifier = Modifier.weight(1f),
                shape = RoundedCornerShape(16.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedContainerColor = NuKropCard,
                    unfocusedContainerColor = NuKropCard,
                    focusedBorderColor = NuKropAccent,
                    unfocusedBorderColor = Color(0x30FFFFFF),
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
                shape = RoundedCornerShape(16.dp),
                enabled = !loading,
                colors = ButtonDefaults.buttonColors(containerColor = NuKropAccent),
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 16.dp)
            ) {
                if (loading) CircularProgressIndicator(color = NuKropDark, modifier = Modifier.size(18.dp), strokeWidth = 2.dp)
                else Text(AppStrings.get("search_btn", lang), color = NuKropDark, fontWeight = FontWeight.Bold)
            }
        }

        // Location Editor
        if (mandiState == null) {
            Row(Modifier.fillMaxWidth().padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                OutlinedTextField(
                    value = userState, onValueChange = { userState = it },
                    label = { Text(AppStrings.get("enter_state", lang), fontSize = 12.sp, color = NuKropTextDim) },
                    modifier = Modifier.weight(1f), singleLine = true,
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = NuKropCard, unfocusedContainerColor = NuKropCard,
                        focusedBorderColor = NuKropAccent, unfocusedBorderColor = Color(0x30FFFFFF),
                        cursorColor = NuKropAccent, focusedTextColor = NuKropText, unfocusedTextColor = NuKropText
                    )
                )
                OutlinedTextField(
                    value = userMandi, onValueChange = { userMandi = it },
                    label = { Text(AppStrings.get("enter_mandi", lang), fontSize = 12.sp, color = NuKropTextDim) },
                    modifier = Modifier.weight(1f), singleLine = true,
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = NuKropCard, unfocusedContainerColor = NuKropCard,
                        focusedBorderColor = NuKropAccent, unfocusedBorderColor = Color(0x30FFFFFF),
                        cursorColor = NuKropAccent, focusedTextColor = NuKropText, unfocusedTextColor = NuKropText
                    )
                )
            }
            Spacer(Modifier.height(16.dp))
        }

        // Quick crop suggestions (Emoji Glyph Fixed using Material Icons)
        if (mandiState == null) {
            Text(AppStrings.get("popular_crops", lang), fontSize = 13.sp, color = NuKropTextMuted, modifier = Modifier.padding(horizontal = 16.dp))
            Spacer(Modifier.height(8.dp))
            Row(
                Modifier.fillMaxWidth().padding(horizontal = 16.dp).horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                listOf("Tomato", "Wheat", "Onion", "Cotton", "Potato").forEach { crop ->
                    Box(
                        Modifier.clip(RoundedCornerShape(20.dp)).background(NuKropCard)
                            .border(1.dp, NuKropAccent.copy(alpha = 0.3f), RoundedCornerShape(20.dp))
                            .clickable { query = crop }
                            .padding(horizontal = 12.dp, vertical = 7.dp)
                    ) { Text(crop, fontSize = 12.sp, color = NuKropTextMuted) }
                }
            }
        }

        // Results
        if (loading) {
            Box(Modifier.fillMaxSize(), Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    CircularProgressIndicator(color = NuKropAccent)
                    Spacer(Modifier.height(12.dp))
                    Text("${AppStrings.get("fetching_live", lang)} \"$activeSearchQuery\"...", color = NuKropTextMuted, fontSize = 13.sp)
                    Spacer(Modifier.height(8.dp))
                    Text("Radar network syncing real-time prices...", color = NuKropAccent, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                }
            }
        }

        error?.let {
            Box(Modifier.padding(16.dp).fillMaxWidth().clip(RoundedCornerShape(12.dp))
                .background(NuKropError.copy(alpha = 0.1f)).padding(12.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) { Icon(Icons.Filled.Warning, contentDescription=null, tint=NuKropError, modifier=Modifier.size(14.dp)); Text(it, color = NuKropError, fontSize = 13.sp) }
            }
        }

        records?.let { recs ->
            Column(Modifier.verticalScroll(scrollState)) {
                if (recs.isEmpty()) {
                    Box(Modifier.padding(16.dp).fillMaxWidth().clip(RoundedCornerShape(12.dp))
                        .background(NuKropWarning.copy(alpha = 0.1f)).padding(12.dp)) {
                        Text("${AppStrings.get("no_live_data", lang)} '$activeSearchQuery'. ${AppStrings.get("try_different", lang)}", color = NuKropWarning, fontSize = 13.sp)
                    }
                } else {
                    AIPricePredictorCard(activeSearchQuery)
                    recs.forEach { record ->
                        MandiLiveCard(record, lang, context)
                    }
                }
            }
        }
    }
}

@Composable
fun MandiLiveCard(record: MandiRecord, lang: String, context: android.content.Context) {
    var isTracked by remember { mutableStateOf(PriceTracker.isTracked(context, record.state, record.market, record.commodity)) }
    var showTrackDialog by remember { mutableStateOf(false) }
    var targetPriceInput by remember { mutableStateOf("") }
    
    if (showTrackDialog) {
        AlertDialog(
            onDismissRequest = { showTrackDialog = false },
            containerColor = NuKropCard,
            title = { Text("Set Target Price Alert", color = NuKropText, fontWeight = FontWeight.Bold) },
            text = {
                Column {
                    Text("Notify me when the price reaches:", fontSize = 14.sp, color = NuKropTextMuted)
                    Spacer(Modifier.height(8.dp))
                    OutlinedTextField(
                        value = targetPriceInput,
                        onValueChange = { targetPriceInput = it.filter { char -> char.isDigit() } },
                        label = { Text("Target Price (₹)", color = NuKropTextDim) },
                        singleLine = true,
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedContainerColor = NuKropSurface,
                            unfocusedContainerColor = NuKropSurface,
                            focusedBorderColor = NuKropAccent,
                            unfocusedBorderColor = Color(0x30FFFFFF),
                            focusedTextColor = NuKropText,
                            unfocusedTextColor = NuKropText
                        )
                    )
                }
            },
            confirmButton = {
                Button(
                    onClick = {
                        val target = targetPriceInput.toDoubleOrNull() ?: (record.modalPrice + 100)
                        PriceTracker.addOrUpdateTrackedCrop(context, record.state, record.market, record.commodity, record.modalPrice, target)
                        isTracked = true
                        showTrackDialog = false
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = NuKropAccent)
                ) {
                    Text("Save Alert", color = NuKropDark, fontWeight = FontWeight.Bold)
                }
            },
            dismissButton = {
                TextButton(onClick = { showTrackDialog = false }) {
                    Text("Cancel", color = NuKropTextDim)
                }
            }
        )
    }
    
    Column(Modifier.padding(horizontal = 16.dp, vertical = 8.dp)) {
        Box(
            Modifier.fillMaxWidth().clip(RoundedCornerShape(20.dp))
                .background(NuKropCard)
                .border(1.dp, NuKropAccent.copy(alpha = 0.2f), RoundedCornerShape(20.dp))
                .padding(16.dp)
        ) {
            Column {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        Box(Modifier.size(40.dp).clip(CircleShape).background(NuKropSurface), Alignment.Center) {
                            Icon(Icons.Filled.LocationOn, contentDescription = null, tint = NuKropAccent)
                        }
                        Column {
                            Text("${record.market} ${AppStrings.get("mandi", lang)}", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                            Text("${record.district}, ${record.state}", fontSize = 12.sp, color = NuKropTextMuted)
                        }
                    }
                    Box(Modifier.clip(RoundedCornerShape(8.dp)).background(NuKropAccent.copy(alpha=0.15f)).padding(6.dp)) {
                        Text(record.arrivalDate, fontSize = 10.sp, color = NuKropAccent, fontWeight = FontWeight.Bold)
                    }
                }
                
                Spacer(Modifier.height(16.dp))
                
                Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween, Alignment.Bottom) {
                    Column {
                        Text(record.commodity, fontSize = 14.sp, color = NuKropTextMuted)
                        Text("₹${record.modalPrice.toInt()}", fontSize = 30.sp, fontWeight = FontWeight.ExtraBold, color = NuKropAccent)
                        Text(AppStrings.get("modal_price", lang), fontSize = 11.sp, color = NuKropTextMuted)
                    }
                    
                    Column(horizontalAlignment = Alignment.End) {
                        Text("${AppStrings.get("variety", lang)} ${record.variety}", fontSize = 12.sp, color = NuKropText)
                // Scam Detector Warning
                if (record.modalPrice < record.maxPrice * 0.75) {
                    Spacer(Modifier.height(8.dp))
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(NuKropError.copy(alpha = 0.1f))
                            .border(1.dp, NuKropError.copy(alpha = 0.4f), RoundedCornerShape(12.dp))
                            .padding(12.dp)
                    ) {
                        Row(verticalAlignment = Alignment.Top, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Icon(Icons.Filled.Warning, contentDescription = null, tint = NuKropError, modifier = Modifier.size(18.dp))
                            Column {
                                Text("Real-Time Scam Alert", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = NuKropError)
                                Text("This mandi's price is suspiciously low compared to the regional maximum. AI detects potential cartel pricing.", fontSize = 11.sp, color = NuKropTextMuted, lineHeight = 16.sp)
                            }
                        }
                    }
                }

                        Spacer(Modifier.height(4.dp))
                        Text("${AppStrings.get("min", lang)} ₹${record.minPrice.toInt()}", fontSize = 11.sp, color = NuKropTextDim)
                        Text("${AppStrings.get("max", lang)} ₹${record.maxPrice.toInt()}", fontSize = 11.sp, color = NuKropTextDim)
                    }
                }
                
                Spacer(Modifier.height(16.dp))
                
                // Track Price Button
                Button(
                    onClick = {
                        if (!isTracked) {
                            targetPriceInput = (record.modalPrice + 100).toInt().toString()
                            showTrackDialog = true
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = if (isTracked) NuKropBadgeGreen.copy(alpha=0.2f) else Color(0x30FFFFFF))
                ) {
                    Text(
                        if (isTracked) AppStrings.get("tracking_active", lang) else AppStrings.get("track_price", lang), 
                        color = if (isTracked) NuKropBadgeGreen else NuKropText, 
                        fontWeight = FontWeight.Bold
                    )
                }

                Spacer(Modifier.height(8.dp))
                
                // Blockchain Contract Button
                var isSold by remember { mutableStateOf(false) }
                var escrowStatus by remember { mutableStateOf("LOCKED") } // LOCKED, VERIFYING, RELEASED
                
                Button(
                    onClick = { 
                        isSold = !isSold 
                        if (!isSold) {
                            escrowStatus = "LOCKED"
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = if (isSold) NuKropBadgeGreen.copy(alpha=0.2f) else NuKropAccent)
                ) {
                    Text(
                        if (isSold) "Blockchain Contract Signed" else "Sell Direct (Blockchain Contract)",
                        color = if (isSold) NuKropBadgeGreen else NuKropDark,
                        fontWeight = FontWeight.Bold
                    )
                }
                
                if (isSold) {
                    Spacer(Modifier.height(10.dp))
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(NuKropSurface)
                            .border(1.dp, Color(0x20FFFFFF), RoundedCornerShape(12.dp))
                            .padding(12.dp)
                    ) {
                        Column {
                            Text("Escrow Ledger Info", fontSize = 11.sp, color = NuKropTextMuted, fontWeight = FontWeight.Bold)
                            Spacer(Modifier.height(6.dp))
                            Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween) {
                                Text("Contract Address", fontSize = 11.sp, color = NuKropTextMuted)
                                Text("0x5F3d...b89A", fontSize = 11.sp, color = NuKropAccent, fontWeight = FontWeight.SemiBold)
                            }
                            Spacer(Modifier.height(4.dp))
                            Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween) {
                                Text("Escrow Funds", fontSize = 11.sp, color = NuKropTextMuted)
                                Text("₹85,000", fontSize = 11.sp, color = NuKropText, fontWeight = FontWeight.Bold)
                            }
                            Spacer(Modifier.height(4.dp))
                            Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween) {
                                Text("Escrow Status", fontSize = 11.sp, color = NuKropTextMuted)
                                Text(
                                    text = when (escrowStatus) {
                                        "LOCKED" -> "🔒 FUNDS LOCKED (BigBasket Escrow)"
                                        "VERIFYING" -> "🌀 VERIFYING DROP-OFF..."
                                        else -> "🟢 FUNDS RELEASED TO WALLET"
                                    },
                                    fontSize = 11.sp,
                                    color = when (escrowStatus) {
                                        "LOCKED" -> NuKropWarning
                                        "VERIFYING" -> NuKropAccent
                                        else -> NuKropBadgeGreen
                                    },
                                    fontWeight = FontWeight.Bold
                                )
                            }
                            
                            if (escrowStatus != "RELEASED") {
                                Spacer(Modifier.height(10.dp))
                                Button(
                                    onClick = {
                                        escrowStatus = "VERIFYING"
                                    },
                                    colors = ButtonDefaults.buttonColors(containerColor = NuKropAccent),
                                    modifier = Modifier.fillMaxWidth(),
                                    shape = RoundedCornerShape(8.dp)
                                ) {
                                    if (escrowStatus == "VERIFYING") {
                                        CircularProgressIndicator(color = NuKropDark, modifier = Modifier.size(16.dp), strokeWidth = 2.dp)
                                    } else {
                                        Text("Scan Delivery Agent QR Code", color = NuKropDark, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                                    }
                                }
                                
                                if (escrowStatus == "VERIFYING") {
                                    LaunchedEffect(Unit) {
                                        kotlinx.coroutines.delay(2000)
                                        escrowStatus = "RELEASED"
                                    }
                                }
                            } else {
                                Spacer(Modifier.height(8.dp))
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clip(RoundedCornerShape(6.dp))
                                        .background(NuKropBadgeGreen.copy(alpha = 0.2f))
                                        .padding(8.dp),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text("₹85,000 credited to mobile wallet instantly!", color = NuKropBadgeGreen, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun AIPricePredictorCard(crop: String) {
    Box(
        modifier = Modifier
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .fillMaxWidth()
            .clip(RoundedCornerShape(20.dp))
            .background(Color(0xFF2D3A1C))
            .border(1.5.dp, NuKropAccent.copy(alpha = 0.5f), RoundedCornerShape(20.dp))
            .padding(16.dp)
    ) {
        Column {
            Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween, Alignment.CenterVertically) {
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) { Icon(Icons.Filled.AutoGraph, contentDescription=null, tint=NuKropText, modifier=Modifier.size(18.dp)); Text("AI Crop Profit Predictor", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = NuKropText) }
                Box(Modifier.clip(RoundedCornerShape(8.dp)).background(NuKropWarning.copy(alpha=0.2f)).padding(horizontal = 6.dp, vertical = 4.dp)) {
                    Text("Crash Warning", fontSize = 10.sp, color = NuKropWarning, fontWeight = FontWeight.Bold)
                }
            }
            Spacer(Modifier.height(8.dp))
            Text(
                text = "Forecast for $crop: Prices are projected to peak in 6 days, followed by a sharp 25% decline in 3 weeks due to harvesting surges in adjacent districts. Optimal window to sell is coming up.",
                fontSize = 12.sp,
                color = NuKropTextMuted,
                lineHeight = 18.sp
            )
            Spacer(Modifier.height(12.dp))
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Text("Current Trend: Bullish", fontSize = 11.sp, color = NuKropAccent, fontWeight = FontWeight.Bold)
                Text("Forecast Crash: June 15", fontSize = 11.sp, color = NuKropWarning, fontWeight = FontWeight.Bold)
            }
        }
    }
}
