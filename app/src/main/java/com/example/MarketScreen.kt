package com.example

import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.LocationOn
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material.icons.filled.AutoGraph
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
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
import androidx.compose.material.icons.filled.Bolt

@Composable
fun MarketScreen(modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val lang = LanguageManager.currentLanguage.collectAsState().value
    
    var query by remember { mutableStateOf("") }
    var activeSearchQuery by remember { mutableStateOf("") }
    var userState by remember { mutableStateOf("") }
    var activeSearchState by remember { mutableStateOf("") }
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

    // Auto-detect location if available but don't force a search until user hits Search
    LaunchedEffect(Unit) {
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            val loc = LocationHelper.getCurrentLocationStateAndMandi(context)
            if (loc != null) {
                if (userState.isEmpty()) userState = loc.first
                if (userMandi.isEmpty()) userMandi = loc.second
            }
        }
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

    Column(
        modifier = modifier.fillMaxSize().background(Color(0xFF0D1208))
    ) {
        // Header
        Column(Modifier.fillMaxWidth().statusBarsPadding().padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(AppStrings.get("market_rates", lang), fontSize = 24.sp, fontWeight = FontWeight.ExtraBold, color = NuKropText)
                Spacer(Modifier.width(12.dp))
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
            Text("Direct Agmarknet Govt API Integration Gov & Redis", fontSize = 12.sp, color = NuKropTextMuted)
            
            Spacer(Modifier.height(24.dp))

            // Search Bar Row 1
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp), verticalAlignment = Alignment.CenterVertically) {
                OutlinedTextField(
                    value = query,
                    onValueChange = { query = it },
                    placeholder = { Text("Enter crop (e.g. Tomato, Wheat...)", fontSize = 14.sp, color = NuKropTextDim) },
                    modifier = Modifier.weight(1f),
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
                    shape = RoundedCornerShape(16.dp),
                    enabled = !loading,
                    colors = ButtonDefaults.buttonColors(containerColor = NuKropAccent),
                    contentPadding = PaddingValues(horizontal = 20.dp, vertical = 16.dp)
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
                    modifier = Modifier.weight(1f),
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
                    modifier = Modifier.weight(1f),
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
                val crops = listOf("Tomato", "Wheat", "Onion", "Cotton", "Potato")
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

        Divider(color = Color(0x30FFFFFF))

        // Results Section
        Box(Modifier.fillMaxSize().padding(16.dp)) {
            if (activeSearchQuery.isEmpty() || activeSearchState.isEmpty()) {
                // Empty state handled naturally (just blank area below)
            } else if (loading && records.isNullOrEmpty()) {
                CircularProgressIndicator(color = NuKropAccent, modifier = Modifier.align(Alignment.Center))
            } else if (!records.isNullOrEmpty()) {
                Column(Modifier.verticalScroll(scrollState).padding(bottom = 100.dp)) {
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
                        records.filter { it.market.contains(userMandi, ignoreCase = true) }
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
                Text("No data available from Gov API.", color = NuKropTextMuted, modifier = Modifier.align(Alignment.Center))
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
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(Modifier.clip(RoundedCornerShape(8.dp)).background(NuKropAccent.copy(alpha=0.15f)).padding(8.dp)) {
                        Icon(Icons.Filled.AutoGraph, null, tint = NuKropAccent, modifier = Modifier.size(20.dp))
                    }
                    Spacer(Modifier.width(12.dp))
                    Column {
                        Text(record.market, fontSize = 16.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                        Text("${record.district}, ${record.state}", fontSize = 12.sp, color = NuKropTextMuted)
                    }
                }
                Text("s ${record.modalPrice}", fontSize = 18.sp, fontWeight = FontWeight.ExtraBold, color = NuKropAccent)
            }
            Spacer(Modifier.height(16.dp))
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Column {
                    Text("Commodity", fontSize = 10.sp, color = NuKropTextDim)
                    Text(record.commodity, fontSize = 14.sp, color = NuKropText, fontWeight = FontWeight.Bold)
                }
                Column {
                    Text("Min Price", fontSize = 10.sp, color = NuKropTextDim)
                    Text("s ${record.minPrice}", fontSize = 14.sp, color = NuKropText)
                }
                Column {
                    Text("Max Price", fontSize = 10.sp, color = NuKropTextDim)
                    Text("s ${record.maxPrice}", fontSize = 14.sp, color = NuKropText)
                }
            }
            Spacer(Modifier.height(12.dp))
            Text("Data Date: ${record.arrivalDate}", fontSize = 10.sp, color = NuKropTextDim, modifier = Modifier.align(Alignment.End))
        }
    }
}
