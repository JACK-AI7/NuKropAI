package com.example

import android.Manifest
import android.annotation.SuppressLint
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.view.View
import android.view.ViewGroup
import android.webkit.*
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat

// Sealed class Tab kept so any references in test files or utilities compile without issue
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

    private lateinit var webView: WebView
    private var filePathCallback: ValueCallback<Array<Uri>>? = null

    private val fileChooserLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (filePathCallback != null) {
            val data = result.data
            val results: Array<Uri>? = if (result.resultCode == Activity.RESULT_OK && data != null) {
                if (data.clipData != null) {
                    val count = data.clipData!!.itemCount
                    Array(count) { i -> data.clipData!!.getItemAt(i).uri }
                } else if (data.data != null) {
                    arrayOf(data.data!!)
                } else null
            } else null
            filePathCallback?.onReceiveValue(results)
            filePathCallback = null
        }
    }

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { _ -> }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Request runtime permissions for Camera, Location, Storage
        val permissions = mutableListOf(
            Manifest.permission.CAMERA,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        )
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            permissions.add(Manifest.permission.POST_NOTIFICATIONS)
        }
        permissionLauncher.launch(permissions.toTypedArray())

        // Create full-screen hardware-accelerated WebView
        webView = WebView(this).apply {
            layoutParams = ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
            )
            setLayerType(View.LAYER_TYPE_HARDWARE, null)
            scrollBarStyle = View.SCROLLBARS_INSIDE_OVERLAY
            isVerticalScrollBarEnabled = false
            isHorizontalScrollBarEnabled = false
            setBackgroundColor(0xFFF8FAF8.toInt())

            settings.apply {
                javaScriptEnabled = true
                domStorageEnabled = true
                databaseEnabled = true
                allowFileAccess = true
                allowContentAccess = true
                allowFileAccessFromFileURLs = true
                allowUniversalAccessFromFileURLs = true
                mediaPlaybackRequiresUserGesture = false
                mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                cacheMode = WebSettings.LOAD_DEFAULT
                useWideViewPort = true
                loadWithOverviewMode = true
                setSupportZoom(false)
                builtInZoomControls = false
                displayZoomControls = false
                setGeolocationEnabled(true)
            }

            webChromeClient = object : WebChromeClient() {
                // Auto-grant Camera / Microphone for Disease Scanner
                override fun onPermissionRequest(request: PermissionRequest) {
                    request.grant(request.resources)
                }

                // Auto-grant Geolocation for Live Mandi Rates & Weather Radar
                override fun onGeolocationPermissionsShowPrompt(
                    origin: String,
                    callback: GeolocationPermissions.Callback
                ) {
                    callback.invoke(origin, true, false)
                }

                // File chooser for camera snap or gallery photo upload
                override fun onShowFileChooser(
                    webView: WebView?,
                    filePathCallback: ValueCallback<Array<Uri>>?,
                    fileChooserParams: FileChooserParams?
                ): Boolean {
                    this@MainActivity.filePathCallback?.onReceiveValue(null)
                    this@MainActivity.filePathCallback = filePathCallback

                    val intent = Intent(Intent.ACTION_GET_CONTENT).apply {
                        addCategory(Intent.CATEGORY_OPENABLE)
                        type = "image/*"
                        putExtra(Intent.EXTRA_ALLOW_MULTIPLE, false)
                    }
                    fileChooserLauncher.launch(Intent.createChooser(intent, "Select Leaf Image"))
                    return true
                }
            }

            webViewClient = object : WebViewClient() {
                override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                    val url = request?.url?.toString() ?: return false
                    if (url.startsWith("tel:") || url.startsWith("mailto:") || url.startsWith("whatsapp:")) {
                        try {
                            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                            startActivity(intent)
                            return true
                        } catch (e: Exception) {
                            return true
                        }
                    }
                    return false
                }
            }

            loadUrl("file:///android_asset/index.html")
        }

        setContentView(webView)

        // Handle Android physical/gesture back button
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                // If the emulator has an open modal, close it first
                webView.evaluateJavascript(
                    """
                    (function() {
                      const modals = document.querySelectorAll('[id$="-modal"], .modal-overlay, #farmer-logout-confirm-modal');
                      for (let m of modals) {
                        if (m && m.style.display !== 'none') {
                          m.remove();
                          return true;
                        }
                      }
                      if (typeof currentScreenKey !== 'undefined' && currentScreenKey !== 'home') {
                        if (typeof openScreen === 'function') {
                          openScreen('home');
                          return true;
                        }
                      }
                      return false;
                    })();
                    """.trimIndent()
                ) { result ->
                    if (result != "true") {
                        if (webView.canGoBack()) {
                            webView.goBack()
                        } else {
                            isEnabled = false
                            onBackPressedDispatcher.onBackPressed()
                        }
                    }
                }
            }
        })
    }

    override fun onResume() {
        super.onResume()
        webView.onResume()
    }

    override fun onPause() {
        super.onPause()
        webView.onPause()
    }

    override fun onDestroy() {
        webView.destroy()
        super.onDestroy()
    }
}
