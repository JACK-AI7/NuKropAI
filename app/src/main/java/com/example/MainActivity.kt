package com.example

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.animation.*
import androidx.compose.animation.core.tween
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
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
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.ExistingPeriodicWorkPolicy
import java.util.concurrent.TimeUnit
import com.example.ui.theme.*
import android.Manifest
import android.os.Build
import androidx.activity.result.contract.ActivityResultContracts

sealed class Tab(val route: String, val icon: String, val labelKey: String) {
    object Home   : Tab("home",    "🏠", "nav_home")
    object Scan   : Tab("scan",    "🔬", "nav_scan")
    object Chat   : Tab("chat",    "💬", "nav_chat")
    object Market : Tab("market",  "📊", "nav_market")
    object Profile: Tab("profile", "👤", "nav_profile")
    object Autopilot: Tab("autopilot", "🚜", "nav_autopilot")
    object Finance: Tab("finance", "💰", "nav_finance")
    object SavedReports: Tab("saved_reports", "📂", "nav_reports")
    object EquipmentRental: Tab("equipment_rental", "🚜", "nav_rental")
    object FarmKhata: Tab("farm_khata", "🧾", "nav_khata")
    object BioShieldRadar: Tab("bioshield_radar", "🛡️", "nav_bioshield")
    object MandiPilot: Tab("mandipilot", "📈", "nav_mandipilot")
    object GramHaul: Tab("gramhaul", "🚚", "nav_gramhaul")
    object AgriStackPassport: Tab("agristack_passport", "🪪", "nav_agristack")
    object YantraShare: Tab("yantrashare", "🚜", "nav_yantra")
    object BioRx: Tab("biorx", "🌿", "nav_biorx")
    data class PeerChat(val name: String, val info: String, val phone: String) : Tab("peer_chat", "💬", "nav_chat")
}

class MainActivity : ComponentActivity() {
    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        // Handle permission responses if needed
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        LanguageManager.init(this)
        
        // Request essential permissions on startup
        val permissionsToRequest = mutableListOf(Manifest.permission.ACCESS_FINE_LOCATION)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            permissionsToRequest.add(Manifest.permission.POST_NOTIFICATIONS)
        }
        requestPermissionLauncher.launch(permissionsToRequest.toTypedArray())

        val workRequest = PeriodicWorkRequestBuilder<AlertWorker>(1, TimeUnit.HOURS).build()
        WorkManager.getInstance(this).enqueueUniquePeriodicWork("AlertWorker", ExistingPeriodicWorkPolicy.KEEP, workRequest)

        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                val authViewModel: AuthViewModel = androidx.lifecycle.viewmodel.compose.viewModel()
                val currentUser by authViewModel.currentUser.collectAsState()

                var splashDone by remember { mutableStateOf(false) }

                when {
                    !splashDone -> {
                        SplashScreen(onStartFarming = { splashDone = true })
                    }
                    currentUser == null -> {
                        LoginScreen(onLoginSuccess = { /* Auth state auto-updates via collectAsState */ })
                    }
                    else -> {
                        MainApp(authViewModel = authViewModel)
                    }
                }
            }
        }
    }
}

@Composable
fun MainApp(authViewModel: AuthViewModel) {
    val lang = LanguageManager.currentLanguage.collectAsState().value
    var current by remember { mutableStateOf<Tab>(Tab.Home) }
    val tabs = listOf(Tab.Home, Tab.Chat, Tab.Scan, Tab.Market, Tab.Profile)

    Scaffold(
        containerColor = Color(0xFF0D1208),
        contentWindowInsets = WindowInsets(0.dp),
        bottomBar = {
            Box(
                Modifier
                    .fillMaxWidth()
                    .background(Brush.verticalGradient(listOf(Color.Transparent, Color(0xF5141A0A))))
                    .navigationBarsPadding()
                    .padding(horizontal = 16.dp, vertical = 10.dp)
            ) {
                Row(
                    Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(30.dp))
                        .background(NuKropCard)
                        .border(1.dp, Color(0x30C8E837), RoundedCornerShape(30.dp))
                        .padding(vertical = 6.dp, horizontal = 6.dp),
                    horizontalArrangement = Arrangement.SpaceAround,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    tabs.forEach { tab ->
                        val sel = current == tab
                        val isScan = tab is Tab.Scan
                        if (isScan) {
                            // Floating scan button
                            Box(
                                Modifier.size(56.dp).clip(CircleShape)
                                    .background(if (sel) Brush.radialGradient(listOf(NuKropAccent, NuKropAccentDark))
                                                else Brush.radialGradient(listOf(NuKropGreen, Color(0xFF2D4A10))))
                                    .border(2.dp, if (sel) NuKropAccent else Color(0x50C8E837), CircleShape)
                                    .clickable { current = tab },
                                Alignment.Center
                            ) { Text(tab.icon, fontSize = 24.sp) }
                        } else {
                            Column(
                                Modifier
                                    .clip(RoundedCornerShape(20.dp))
                                    .background(if (sel) NuKropAccent.copy(alpha = 0.15f) else Color.Transparent)
                                    .clickable { current = tab }
                                    .padding(horizontal = 16.dp, vertical = 8.dp),
                                horizontalAlignment = Alignment.CenterHorizontally
                            ) {
                                Text(tab.icon, fontSize = 20.sp)
                                Spacer(Modifier.height(2.dp))
                                Text(AppStrings.get(tab.labelKey, lang), fontSize = 10.sp,
                                    color = if (sel) NuKropAccent else NuKropTextDim,
                                    fontWeight = if (sel) FontWeight.Bold else FontWeight.Normal)
                            }
                        }
                    }
                }
            }
        }
    ) { innerPadding ->
        Box(Modifier.padding(innerPadding).fillMaxSize()) {
            AnimatedContent(
                targetState = current,
                transitionSpec = { fadeIn(tween(200)) togetherWith fadeOut(tween(150)) },
                label = "tab"
            ) { tab ->
                when (tab) {
                    Tab.Home    -> HomeScreen(
                        onNavigateToScan = { current = Tab.Scan },
                        onNavigateToMarket = { current = Tab.Market },
                        onNavigateToChat = { current = Tab.Chat },
                        onNavigateToAutopilot = { current = Tab.Autopilot },
                        onNavigateToFinance = { current = Tab.Finance },
                        onNavigateToSavedReports = { current = Tab.SavedReports },
                        onNavigateToEquipmentRental = { current = Tab.EquipmentRental },
                        onNavigateToFarmKhata = { current = Tab.FarmKhata },
                        onNavigateToBioShield = { current = Tab.BioShieldRadar },
                        onNavigateToMandiPilot = { current = Tab.MandiPilot },
                        onNavigateToGramHaul = { current = Tab.GramHaul },
                        onNavigateToAgriStack = { current = Tab.AgriStackPassport },
                        onNavigateToYantraShare = { current = Tab.YantraShare },
                        onNavigateToBioRx = { current = Tab.BioRx }
                    )
                    Tab.Autopilot -> TractorAutopilotScreen(onNavigateBack = { current = Tab.Home })
                    Tab.Finance   -> LoanScreen(onNavigateBack = { current = Tab.Home })
                    Tab.Scan    -> DiseaseScannerScreen()
                    Tab.Chat    -> ChatScreen()
                    Tab.Market  -> MarketScreen()
                    Tab.Profile -> ProfileScreen(onSignOut = { authViewModel.signOut() })
                    Tab.SavedReports -> SavedReportsScreen(onNavigateBack = { current = Tab.Home })
                    Tab.EquipmentRental -> EquipmentRentalScreen(
                        onNavigateBack = { current = Tab.Home },
                        onNavigateToPeerChat = { name, info, phone -> current = Tab.PeerChat(name, info, phone) }
                    )
                    Tab.FarmKhata -> FarmKhataScreen(onNavigateBack = { current = Tab.Home })
                    Tab.BioShieldRadar -> BioShieldRadarScreen(onNavigateBack = { current = Tab.Home })
                    Tab.MandiPilot -> MandiPilotScreen(onNavigateBack = { current = Tab.Home })
                    Tab.GramHaul -> GramHaulScreen(onNavigateBack = { current = Tab.Home })
                    Tab.AgriStackPassport -> AgriStackPassportScreen(onNavigateBack = { current = Tab.Home })
                    Tab.YantraShare -> YantraShareScreen(onNavigateBack = { current = Tab.Home })
                    Tab.BioRx -> BioRxScreen(onNavigateBack = { current = Tab.Home })
                    is Tab.PeerChat -> PeerChatScreen(
                        recipientName = (tab as Tab.PeerChat).name,
                        recipientInfo = (tab as Tab.PeerChat).info,
                        recipientPhone = (tab as Tab.PeerChat).phone,
                        onNavigateBack = { current = Tab.Home }
                    )
                }
            }
        }
    }
}
