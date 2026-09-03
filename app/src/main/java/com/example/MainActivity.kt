package com.example

import android.Manifest
import android.annotation.SuppressLint
import android.app.Activity
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.os.Looper
import android.provider.MediaStore
import android.view.View
import android.view.ViewGroup
import android.webkit.*
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import androidx.core.content.FileProvider
import java.io.File
import java.io.IOException

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
    private var cameraPhotoUri: Uri? = null
    private val CHANNEL_ID = "nukrop_farmer_alerts"

    inner class WebAppInterface {
        @JavascriptInterface
        fun requestDeviceLocation() {
            runOnUiThread {
                fetchAndSendLocationToWebView()
            }
        }

        @JavascriptInterface
        fun requestNativePermissions() {
            runOnUiThread {
                val permissions = mutableListOf(
                    Manifest.permission.CAMERA,
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION
                )
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                    permissions.add(Manifest.permission.POST_NOTIFICATIONS)
                }
                permissionLauncher.launch(permissions.toTypedArray())
            }
        }

        @JavascriptInterface
        fun postSystemNotification(title: String, message: String) {
            runOnUiThread {
                showSystemNotification(title, message)
            }
        }
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val name = "NuKropAI Farmer Alerts"
            val descriptionText = "Real-time crop disease alerts, mandi prices, and weather warnings"
            val importance = NotificationManager.IMPORTANCE_HIGH
            val channel = NotificationChannel(CHANNEL_ID, name, importance).apply {
                description = descriptionText
                enableLights(true)
                enableVibration(true)
                setShowBadge(true)
            }
            val notificationManager: NotificationManager =
                getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }

    fun showSystemNotification(title: String, message: String) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
                return
            }
        }

        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        val pendingIntent = PendingIntent.getActivity(
            this,
            System.currentTimeMillis().toInt(),
            intent,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) PendingIntent.FLAG_IMMUTABLE else 0
        )

        val builder = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.mipmap.ic_launcher)
            .setContentTitle(title)
            .setContentText(message)
            .setStyle(NotificationCompat.BigTextStyle().bigText(message))
            .setPriority(NotificationCompat.PRIORITY_MAX)
            .setDefaults(NotificationCompat.DEFAULT_ALL)
            .setAutoCancel(true)
            .setContentIntent(pendingIntent)

        try {
            with(NotificationManagerCompat.from(this)) {
                notify(System.currentTimeMillis().toInt(), builder.build())
            }
        } catch (e: SecurityException) {
            // Ignored if permission revoked
        }
    }

    private val fileChooserLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (filePathCallback != null) {
            var results: Array<Uri>? = null
            if (result.resultCode == Activity.RESULT_OK) {
                val data = result.data
                if (data != null && (data.data != null || data.clipData != null)) {
                    if (data.clipData != null) {
                        val count = data.clipData!!.itemCount
                        results = Array(count) { i -> data.clipData!!.getItemAt(i).uri }
                    } else if (data.data != null) {
                        results = arrayOf(data.data!!)
                    }
                } else if (cameraPhotoUri != null) {
                    // Direct camera photo captured
                    results = arrayOf(cameraPhotoUri!!)
                }
            }
            filePathCallback?.onReceiveValue(results)
            filePathCallback = null
            cameraPhotoUri = null
        }
    }

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        if (permissions[Manifest.permission.CAMERA] == true) {
            webView.evaluateJavascript("if (typeof onNativeCameraPermissionGranted === 'function') onNativeCameraPermissionGranted();", null)
        }
        if (permissions[Manifest.permission.ACCESS_FINE_LOCATION] == true || permissions[Manifest.permission.ACCESS_COARSE_LOCATION] == true) {
            fetchAndSendLocationToWebView()
        }
    }

    fun fetchAndSendLocationToWebView() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED ||
            ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            val locationManager = getSystemService(Context.LOCATION_SERVICE) as? LocationManager ?: return

            // 1. Immediately send best cached location
            val lastGps = try { locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER) } catch (e: Exception) { null }
            val lastNet = try { locationManager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER) } catch (e: Exception) { null }
            val bestLocation = lastGps ?: lastNet

            if (bestLocation != null) {
                val lat = bestLocation.latitude
                val lon = bestLocation.longitude
                runOnUiThread {
                    webView.evaluateJavascript("if (typeof onNativeLocationReceived === 'function') onNativeLocationReceived($lat, $lon);", null)
                }
            }

            // 2. Also request fresh hardware GPS fix
            try {
                val provider = if (locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)) LocationManager.GPS_PROVIDER else LocationManager.NETWORK_PROVIDER
                locationManager.requestSingleUpdate(provider, object : LocationListener {
                    override fun onLocationChanged(loc: Location) {
                        runOnUiThread {
                            webView.evaluateJavascript("if (typeof onNativeLocationReceived === 'function') onNativeLocationReceived(${loc.latitude}, ${loc.longitude});", null)
                        }
                    }
                    @Deprecated("Deprecated in Java")
                    override fun onStatusChanged(p: String?, s: Int, b: Bundle?) {}
                    override fun onProviderEnabled(p: String) {}
                    override fun onProviderDisabled(p: String) {}
                }, Looper.getMainLooper())
            } catch (e: Exception) {
                // Ignore fallback
            }
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Create System Notification Channel
        createNotificationChannel()

        // Native Android Status Bar & Navigation Bar styling to match app theme
        window.statusBarColor = 0xFFF8FAF8.toInt()
        window.navigationBarColor = 0xFFFFFFFF.toInt()
        androidx.core.view.WindowCompat.getInsetsController(window, window.decorView).apply {
            isAppearanceLightStatusBars = true
            isAppearanceLightNavigationBars = true
        }

        // Request runtime permissions for Camera, Location, Storage, Notifications
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
                setSupportMultipleWindows(true)
                javaScriptCanOpenWindowsAutomatically = true
            }

            // Expose native bridge to Javascript
            addJavascriptInterface(WebAppInterface(), "AndroidBridge")

            webChromeClient = object : WebChromeClient() {
                // Auto-grant Camera & Microphone for live crop scanner stream
                override fun onPermissionRequest(request: PermissionRequest) {
                    runOnUiThread {
                        request.grant(request.resources)
                    }
                }

                // Auto-grant Geolocation for Live Mandi Rates & Weather Radar
                override fun onGeolocationPermissionsShowPrompt(
                    origin: String,
                    callback: GeolocationPermissions.Callback
                ) {
                    callback.invoke(origin, true, false)
                }

                // Handle window.open to launch device browser for government schemes & external portals
                override fun onCreateWindow(
                    view: WebView?,
                    isDialog: Boolean,
                    isUserGesture: Boolean,
                    resultMsg: android.os.Message?
                ): Boolean {
                    val transport = resultMsg?.obj as? WebView.WebViewTransport ?: return false
                    val tempWebView = WebView(this@MainActivity)
                    tempWebView.webViewClient = object : WebViewClient() {
                        override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                            val targetUrl = request?.url?.toString() ?: return false
                            try {
                                val intent = Intent(Intent.ACTION_VIEW, Uri.parse(targetUrl))
                                startActivity(intent)
                            } catch (e: Exception) {}
                            return true
                        }
                    }
                    transport.webView = tempWebView
                    resultMsg.sendToTarget()
                    return true
                }

                // Native Camera Snap & File Chooser for Scanner
                override fun onShowFileChooser(
                    webView: WebView?,
                    filePathCallback: ValueCallback<Array<Uri>>?,
                    fileChooserParams: FileChooserParams?
                ): Boolean {
                    this@MainActivity.filePathCallback?.onReceiveValue(null)
                    this@MainActivity.filePathCallback = filePathCallback

                    // Prepare native Camera Intent
                    val takePictureIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
                    var photoFile: File? = null
                    try {
                        val storageDir = getExternalFilesDir(Environment.DIRECTORY_PICTURES)
                        photoFile = File.createTempFile("crop_scan_${System.currentTimeMillis()}", ".jpg", storageDir)
                        cameraPhotoUri = FileProvider.getUriForFile(
                            this@MainActivity,
                            "${applicationContext.packageName}.provider",
                            photoFile
                        )
                        takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, cameraPhotoUri)
                    } catch (ex: IOException) {
                        cameraPhotoUri = null
                    }

                    // Prepare Gallery Intent
                    val pickIntent = Intent(Intent.ACTION_GET_CONTENT).apply {
                        addCategory(Intent.CATEGORY_OPENABLE)
                        type = "image/*"
                    }

                    // Build System Chooser with Camera + Gallery options
                    val chooserIntent = Intent(Intent.ACTION_CHOOSER).apply {
                        putExtra(Intent.EXTRA_INTENT, pickIntent)
                        putExtra(Intent.EXTRA_TITLE, "Capture Crop Leaf or Select Image")
                        if (photoFile != null) {
                            putExtra(Intent.EXTRA_INITIAL_INTENTS, arrayOf(takePictureIntent))
                        }
                    }

                    try {
                        fileChooserLauncher.launch(chooserIntent)
                    } catch (e: Exception) {
                        this@MainActivity.filePathCallback = null
                        return false
                    }
                    return true
                }
            }

            webViewClient = object : WebViewClient() {
                override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                    val url = request?.url?.toString() ?: return false
                    // Keep internal app assets inside local WebView
                    if (url.startsWith("file:///android_asset/") || url.startsWith("file:///android_res/")) {
                        return false
                    }
                    // For ANY external link (http, https, tel, mailto, whatsapp): launch device browser/app!
                    try {
                        val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                        startActivity(intent)
                        return true
                    } catch (e: Exception) {
                        return true
                    }
                }

                override fun onPageFinished(view: WebView?, url: String?) {
                    super.onPageFinished(view, url)
                    fetchAndSendLocationToWebView()
                }
            }

            loadUrl("file:///android_asset/index.html")
        }

        setContentView(webView)

        // Handle Android physical/gesture back button
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                // If live camera is running or modal open, close it cleanly
                webView.evaluateJavascript(
                    """
                    (function() {
                      if (typeof stopLiveCameraStream === 'function') {
                        stopLiveCameraStream();
                      }
                      const modals = document.querySelectorAll('[id$="-modal"], .custom-modal-overlay');
                      for (let m of modals) {
                        if (m && m.style.display === 'flex') {
                          m.style.display = 'none';
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
        fetchAndSendLocationToWebView()
    }

    override fun onPause() {
        super.onPause()
        webView.onPause()
        webView.evaluateJavascript("if (typeof stopLiveCameraStream === 'function') stopLiveCameraStream();", null)
    }

    override fun onDestroy() {
        webView.destroy()
        super.onDestroy()
    }
}
