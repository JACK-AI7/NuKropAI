package com.example

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.animation.*
import androidx.compose.animation.core.tween
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.ExistingPeriodicWorkPolicy
import java.util.concurrent.TimeUnit
import com.example.ui.PlantixBottomBar
import com.example.ui.onboarding.OnboardingFlow
import com.example.ui.theme.*
import android.Manifest
import android.content.Context
import android.os.Build
import androidx.activity.result.contract.ActivityResultContracts

sealed class Tab(val route: String, val icon: String, val labelKey: String) {
    object Home   : Tab("home",    "🏠", "nav_home")
    object Community : Tab("community", "👥", "nav_community")
    object Scan   : Tab("scan",    "🔬", "nav_scan")
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
    data class Calculators(val type: CalculatorType) : Tab("calculators", "🧮", "nav_calculators")
    data class PeerChat(val name: String, val info: String, val phone: String) : Tab("peer_chat", "💬", "nav_chat")
}

class MainActivity : ComponentActivity() {
    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { _ -> }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        LanguageManager.init(this)
        
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
                val context = LocalContext.current
                val prefs = remember { context.getSharedPreferences("nukrop_onboarding", Context.MODE_PRIVATE) }
                var onboardingDone by remember { mutableStateOf(prefs.getBoolean("completed", false)) }

                val authViewModel: AuthViewModel = androidx.lifecycle.viewmodel.compose.viewModel()
                val currentUser by authViewModel.currentUser.collectAsState()

                var splashDone by remember { mutableStateOf(false) }

                when {
                    !splashDone -> {
                        SplashScreen(onStartFarming = { splashDone = true })
                    }
                    !onboardingDone -> {
                        OnboardingFlow(onFinished = { onboardingDone = true })
                    }
                    currentUser == null -> {
                        LoginScreen(onLoginSuccess = { /* Auth state auto-updates */ })
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
    var current by remember { mutableStateOf<Tab>(Tab.Home) }

    Scaffold(
        containerColor = PlantixBackground,
        contentWindowInsets = WindowInsets(0.dp),
        bottomBar = {
            // Plantix Docked Curved Bottom Navigation Bar
            PlantixBottomBar(
                currentTab = current,
                onTabSelected = { tab -> current = tab },
                onScannerClick = { current = Tab.Scan }
            )
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
                        onNavigateToChat = { current = Tab.Community },
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
                        onNavigateToBioRx = { current = Tab.BioRx },
                        onNavigateToCalculators = { calcType -> current = Tab.Calculators(calcType) },
                        onNavigateToCommunity = { current = Tab.Community }
                    )
                    Tab.Community -> CommunityScreen(onNavigateToChat = { current = Tab.Community })
                    is Tab.Calculators -> CalculatorsScreen(
                        initialTab = (tab as Tab.Calculators).type,
                        onNavigateBack = { current = Tab.Home }
                    )
                    Tab.Autopilot -> TractorAutopilotScreen(onNavigateBack = { current = Tab.Home })
                    Tab.Finance   -> LoanScreen(onNavigateBack = { current = Tab.Home })
                    Tab.Scan    -> DiseaseScannerScreen()
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
