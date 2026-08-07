package com.example

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.result.PickVisualMediaRequest
import androidx.camera.core.*
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.compose.animation.core.*
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.content.ContextCompat
import androidx.lifecycle.compose.LocalLifecycleOwner
import com.example.ui.theme.*
import dev.jeziellago.compose.markdowntext.MarkdownText
import kotlinx.coroutines.launch
import org.json.JSONObject
import java.io.File
import android.os.Environment
import android.content.ContentValues
import android.provider.MediaStore
import android.widget.Toast
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Download

enum class ScanMode { CROP, SOIL }

// ── Data classes parsed from Gemini JSON ──────────────────────────────────────
data class Store(val name: String, val url: String, val icon: String)

data class CropScanData(
    val status: String, val name: String, val confidence: Int, val severity: String,
    val symptoms: String, val cause: String, val treatment: String, val prevention: String,
    val details: String,
    val products: List<Pair<Pair<String, String>, List<Store>>> // Pair(Name to Dose, Stores)
)

data class SoilScanData(
    val soilType: String, val estimatedPH: String, val texture: String,
    val organicMatter: String, val deficiencies: List<String>,
    val suitableCrops: List<String>, val improvements: String,
    val details: String,
    val fertilizers: List<Pair<Pair<String, String>, List<Store>>>
)

fun parseCropJson(raw: String): CropScanData? = runCatching {
    val cleanRaw = raw.replace(Regex("<think>.*?</think>", RegexOption.DOT_MATCHES_ALL), "").trim()
    val start = cleanRaw.indexOf('{'); val end = cleanRaw.lastIndexOf('}'); if (start == -1 || end == -1) throw Exception("No JSON found")
    val j = org.json.JSONObject(cleanRaw.substring(start, end + 1))
    val prods = j.optJSONArray("products")?.let { arr ->
        (0 until arr.length()).mapNotNull { i ->
            val obj = arr.optJSONObject(i) ?: return@mapNotNull null
            val storesArr = obj.optJSONArray("stores")
            val stores = mutableListOf<Store>()
            if (storesArr != null) {
                for (s in 0 until storesArr.length()) {
                    val sObj = storesArr.optJSONObject(s)
                    if (sObj != null) stores.add(Store(sObj.optString("name", "Store"), sObj.optString("url", ""), sObj.optString("icon", "🛒")))
                }
            }
            Pair(obj.optString("name") to obj.optString("dose"), stores)
        }
    } ?: emptyList()
    CropScanData(j.optString("status"), j.optString("name"), j.optInt("confidence"), j.optString("severity"),
        j.optString("symptoms"), j.optString("cause"), j.optString("treatment"), j.optString("prevention"),
        j.optString("details"), prods)
}.getOrNull()

fun parseSoilJson(raw: String): SoilScanData? = runCatching {
    val cleanRaw = raw.replace(Regex("<think>.*?</think>", RegexOption.DOT_MATCHES_ALL), "").trim()
    val start = cleanRaw.indexOf('{'); val end = cleanRaw.lastIndexOf('}'); if (start == -1 || end == -1) throw Exception("No JSON found")
    val j = org.json.JSONObject(cleanRaw.substring(start, end + 1))
    val defs = j.optJSONArray("likelyDeficiencies")?.let { arr -> (0 until arr.length()).map { i -> arr.optString(i) } } ?: emptyList()
    val crops = j.optJSONArray("suitableCrops")?.let { arr -> (0 until arr.length()).map { i -> arr.optString(i) } } ?: emptyList()
    val ferts = j.optJSONArray("fertilizers")?.let { arr ->
        (0 until arr.length()).mapNotNull { i ->
            val obj = arr.optJSONObject(i) ?: return@mapNotNull null
            val storesArr = obj.optJSONArray("stores")
            val stores = mutableListOf<Store>()
            if (storesArr != null) {
                for (s in 0 until storesArr.length()) {
                    val sObj = storesArr.optJSONObject(s)
                    if (sObj != null) stores.add(Store(sObj.optString("name", "Store"), sObj.optString("url", ""), sObj.optString("icon", "🛒")))
                }
            }
            Pair(obj.optString("name") to obj.optString("dose"), stores)
        }
    } ?: emptyList()
    SoilScanData(j.optString("soilType"), j.optString("estimatedPH"), j.optString("texture"),
        j.optString("organicMatter"), defs, crops, j.optString("improvements"), j.optString("details"), ferts)
}.getOrNull()
@Composable
fun DiseaseScannerScreen(modifier: Modifier = Modifier) {
    var mode by remember { mutableStateOf<ScanMode?>(null) }
    when (val m = mode) {
        null -> ScanHub(modifier, onSelect = { mode = it })
        else -> CameraScanner(modifier, m, onBack = { mode = null })
    }
}

// ── Hub screen ─────────────────────────────────────────────────────────────────
@Composable
fun ScanHub(modifier: Modifier, onSelect: (ScanMode) -> Unit) {
    val lang = LanguageManager.currentLanguage.collectAsState().value
    Column(
        modifier = modifier.fillMaxSize()
            .background(Brush.verticalGradient(listOf(Color(0xFF0D1208), NuKropDark)))
            .statusBarsPadding().padding(24.dp),
        verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("🌿", fontSize = 52.sp)
        Spacer(Modifier.height(12.dp))
        Text(AppStrings.get("scanner_title", lang), fontSize = 24.sp, fontWeight = FontWeight.ExtraBold, color = NuKropAccent)
        Text("Point your camera • Get instant AI diagnosis", fontSize = 13.sp, color = NuKropTextMuted, textAlign = TextAlign.Center)
        Spacer(Modifier.height(40.dp))

        ScanCard(
            icon = "🔬", title = "Crop Disease & Pest Scan",
            bullets = listOf("Real OpenRouter Vision AI analysis", "Detects 600+ plant problems & diseases", "Recommends treatments + buy links"),
            accent = NuKropAccent
        ) { onSelect(ScanMode.CROP) }

        Spacer(Modifier.height(16.dp))

        ScanCard(
            icon = "🪨", title = "Soil Health Analysis",
            bullets = listOf("Visual soil texture & color analysis", "Estimates pH & organic matter", "Fertilizer recommendations"),
            accent = Color(0xFF8BC34A)
        ) { onSelect(ScanMode.SOIL) }
    }
}

@Composable
fun ScanCard(icon: String, title: String, bullets: List<String>, accent: Color, onClick: () -> Unit) {
    Box(
        Modifier.fillMaxWidth()
            .clip(RoundedCornerShape(24.dp))
            .background(NuKropCard)
            .border(1.5.dp, accent.copy(alpha = 0.45f), RoundedCornerShape(24.dp))
            .clickable(onClick = onClick).padding(20.dp)
    ) {
        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            Box(Modifier.size(64.dp).clip(RoundedCornerShape(16.dp)).background(accent.copy(alpha = 0.12f)),
                Alignment.Center) { Text(icon, fontSize = 32.sp) }
            Column(Modifier.weight(1f)) {
                Text(title, fontSize = 15.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                Spacer(Modifier.height(8.dp))
                bullets.forEach { b ->
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text("•", color = accent, fontWeight = FontWeight.Bold)
                        Text(b, fontSize = 12.sp, color = NuKropTextMuted, lineHeight = 17.sp)
                    }
                }
                Spacer(Modifier.height(10.dp))
                Box(Modifier.clip(RoundedCornerShape(20.dp)).background(accent).padding(horizontal = 14.dp, vertical = 6.dp)) {
                    Text("Start Scanning →", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = NuKropDark)
                }
            }
        }
    }
}

// ── Camera Scanner ─────────────────────────────────────────────────────────────
@Composable
fun CameraScanner(modifier: Modifier, scanMode: ScanMode, onBack: () -> Unit) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current
    val scope = rememberCoroutineScope()
    val accent = if (scanMode == ScanMode.CROP) NuKropAccent else Color(0xFF8BC34A)

    var hasPerm by remember {
        mutableStateOf(ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED)
    }
    val permLauncher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { hasPerm = it }

    var scanning by remember { mutableStateOf(false) }
    var rawResult by remember { mutableStateOf<String?>(null) }
    var cameraError by remember { mutableStateOf<String?>(null) }
    val imageCapture = remember { ImageCapture.Builder().setCaptureMode(ImageCapture.CAPTURE_MODE_MAXIMIZE_QUALITY).build() }

    val pickMedia = rememberLauncherForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri ->
        if (uri != null) {
            scanning = true
            scope.launch {
                try {
                    val bytes = context.contentResolver.openInputStream(uri)?.readBytes()
                    if (bytes != null) {
                        val prompt = if (scanMode == ScanMode.CROP) GeminiVisionService.cropScanPrompt() else GeminiVisionService.soilScanPrompt()
                        val res = GeminiVisionService.analyzeImage("", bytes, prompt)
                        rawResult = res.getOrElse { "ERROR: ${it.message}" }
                    } else {
                        cameraError = "Could not read image from gallery"
                    }
                } catch(e: Exception) {
                    cameraError = e.message
                } finally {
                    scanning = false
                }
            }
        }
    }

    val scanAnim = rememberInfiniteTransition(label = "scan")
    val scanY by scanAnim.animateFloat(0f, 1f, infiniteRepeatable(tween(1800, easing = LinearEasing), RepeatMode.Reverse), label = "scanY")
    val pulseAlpha by scanAnim.animateFloat(0.4f, 1f, infiniteRepeatable(tween(900), RepeatMode.Reverse), label = "pulse")

    // Permission screen
    if (!hasPerm) {
        Box(modifier.fillMaxSize().background(NuKropDark), Alignment.Center) {
            Column(Modifier.padding(32.dp), Arrangement.Center, Alignment.CenterHorizontally) {
                Text("📷", fontSize = 64.sp)
                Spacer(Modifier.height(20.dp))
                Text("Camera Permission Required", fontSize = 20.sp, fontWeight = FontWeight.Bold, color = NuKropText, textAlign = TextAlign.Center)
                Spacer(Modifier.height(8.dp))
                Text("NuKropAI needs camera access to scan your crops and soil with real AI analysis.", fontSize = 14.sp, color = NuKropTextMuted, textAlign = TextAlign.Center)
                Spacer(Modifier.height(28.dp))
                Button(onClick = { permLauncher.launch(Manifest.permission.CAMERA) },
                    modifier = Modifier.fillMaxWidth().height(52.dp),
                    shape = RoundedCornerShape(26.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = accent)
                ) { Text("Grant Camera Access", color = NuKropDark, fontWeight = FontWeight.Bold, fontSize = 15.sp) }
            }
        }
        return
    }

    // Result screen
    if (rawResult != null) {
        ScanResultView(modifier, rawResult!!, scanMode, accent, onBack) { rawResult = null; scanning = false; cameraError = null }
        return
    }

    // Camera view
    Box(modifier.fillMaxSize().background(Color.Black)) {

        // Camera preview
        AndroidView(
            factory = { ctx ->
                PreviewView(ctx).apply {
                    scaleType = PreviewView.ScaleType.FILL_CENTER
                    implementationMode = PreviewView.ImplementationMode.COMPATIBLE
                }.also { pv ->
                    val future = ProcessCameraProvider.getInstance(ctx)
                    future.addListener({
                        try {
                            val provider = future.get()
                            val preview = Preview.Builder().build().also { it.setSurfaceProvider(pv.surfaceProvider) }
                            provider.unbindAll()
                            provider.bindToLifecycle(lifecycleOwner, CameraSelector.DEFAULT_BACK_CAMERA, preview, imageCapture)
                        } catch (e: Exception) {
                            cameraError = e.message
                        }
                    }, ContextCompat.getMainExecutor(ctx))
                }
            },
            modifier = Modifier.fillMaxSize()
        )

        // Semi-transparent vignette
        Box(Modifier.fillMaxSize().background(Color(0x30000000)))

        // Scan overlay frame with animation
        Canvas(Modifier.fillMaxSize()) {
            val fw = size.width; val fh = size.height
            val s = minOf(fw, fh) * 0.7f
            val l = (fw - s) / 2f; val t = (fh - s) / 2f
            val corner = 50f; val stroke = 5f
            val c = android.graphics.Color.parseColor(if (scanMode == ScanMode.CROP) "#C8E837" else "#8BC34A")
            val cc = Color(c).copy(alpha = pulseAlpha)

            // Corners
            drawLine(cc, Offset(l, t + corner), Offset(l, t), stroke)
            drawLine(cc, Offset(l, t), Offset(l + corner, t), stroke)
            drawLine(cc, Offset(l + s - corner, t), Offset(l + s, t), stroke)
            drawLine(cc, Offset(l + s, t), Offset(l + s, t + corner), stroke)
            drawLine(cc, Offset(l + s, t + s - corner), Offset(l + s, t + s), stroke)
            drawLine(cc, Offset(l + s, t + s), Offset(l + s - corner, t + s), stroke)
            drawLine(cc, Offset(l + corner, t + s), Offset(l, t + s), stroke)
            drawLine(cc, Offset(l, t + s), Offset(l, t + s - corner), stroke)

            // Animated scan line
            if (scanning) {
                val lineY = t + s * scanY
                drawLine(Color(c).copy(alpha = 0.8f), Offset(l + 8f, lineY), Offset(l + s - 8f, lineY), 2.5f)
            }
        }

        // Top bar
        Row(
            Modifier.fillMaxWidth().background(Color(0xDD0D1208)).statusBarsPadding().padding(4.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            IconButton(onBack) { Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = NuKropText) }
            Column {
                Text(if (scanMode == ScanMode.CROP) "Crop Disease & Pest Scan" else "Soil Health Analysis",
                    fontSize = 15.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                Text("Powered by NuKrop Vision AI", fontSize = 10.sp, color = accent)
            }
        }

        // Center hint
        Box(Modifier.align(Alignment.BottomCenter).padding(bottom = 230.dp)) {
            Box(Modifier.clip(RoundedCornerShape(20.dp)).background(Color(0xBB0D1208)).padding(horizontal = 16.dp, vertical = 8.dp)) {
                Text(
                    if (scanning) "🔬 Analyzing with NuKrop AI..."
                    else if (scanMode == ScanMode.CROP) "📍 Point at crop leaves / stem / fruit"
                    else "📍 Point at soil sample clearly",
                    fontSize = 13.sp, color = if (scanning) accent else NuKropTextMuted
                )
            }
        }

        // Error
        cameraError?.let { err ->
            Box(Modifier.align(Alignment.Center).padding(24.dp).clip(RoundedCornerShape(12.dp))
                .background(Color(0xDDFF0000)).padding(12.dp)) {
                Text("Camera error: $err", color = Color.White, fontSize = 13.sp)
            }
        }

        // Bottom controls
        Column(
            Modifier.align(Alignment.BottomCenter).fillMaxWidth()
                .background(Color(0xDD0D1208)).navigationBarsPadding().padding(vertical = 24.dp, horizontal = 32.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Gallery Button
                Box(
                    Modifier.size(56.dp).clip(CircleShape).background(NuKropCard)
                        .border(1.dp, Color.White.copy(alpha = 0.1f), CircleShape)
                        .clickable(enabled = !scanning) {
                            pickMedia.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
                        },
                    contentAlignment = Alignment.Center
                ) {
                    Text("🖼️", fontSize = 24.sp)
                }

                Spacer(Modifier.width(32.dp))

                // Main scan button
                Box(
                    Modifier.size(80.dp).clip(CircleShape)
                        .background(if (scanning) SolidColor(NuKropSurface) else Brush.radialGradient(listOf(accent, accent.copy(alpha = 0.7f))))
                        .border(3.dp, Color.White.copy(alpha = 0.2f), CircleShape)
                        .clickable(enabled = !scanning && cameraError == null) {
                            scanning = true
                            val file = File(context.cacheDir, "nukrop_scan.jpg")
                            val opts = ImageCapture.OutputFileOptions.Builder(file).build()
                            imageCapture.takePicture(opts, ContextCompat.getMainExecutor(context),
                                object : ImageCapture.OnImageSavedCallback {
                                    override fun onImageSaved(out: ImageCapture.OutputFileResults) {
                                        val bytes = file.readBytes()
                                        file.delete()
                                        val prompt = if (scanMode == ScanMode.CROP) GeminiVisionService.cropScanPrompt()
                                                     else GeminiVisionService.soilScanPrompt()
                                        scope.launch {
                                            val res = GeminiVisionService.analyzeImage("", bytes, prompt)
                                            rawResult = res.getOrElse { "ERROR: ${it.message}" }
                                            scanning = false
                                        }
                                    }
                                    override fun onError(e: ImageCaptureException) {
                                        cameraError = e.message; scanning = false
                                    }
                                })
                        },
                    contentAlignment = Alignment.Center
                ) {
                    if (scanning) {
                        CircularProgressIndicator(color = accent, modifier = Modifier.size(36.dp), strokeWidth = 3.dp)
                    } else {
                        Text("📷", fontSize = 34.sp)
                    }
                }

                Spacer(Modifier.width(32.dp))

                // Empty box for symmetry
                Box(Modifier.size(56.dp))
            }
            Spacer(Modifier.height(90.dp))
            Text(
                if (scanning) "Analyzing... please wait" else "Tap camera or select from album",
                fontSize = 13.sp, color = NuKropTextMuted, fontWeight = if (scanning) FontWeight.SemiBold else FontWeight.Normal
            )
        }
    }
}

// ── Results ────────────────────────────────────────────────────────────────────
@Composable
fun ScanResultView(modifier: Modifier, raw: String, mode: ScanMode, accent: Color, onBack: () -> Unit, onRescan: () -> Unit) {
    val context = LocalContext.current
    val scroll = rememberScrollState()

    Column(modifier.fillMaxSize().background(NuKropDark).verticalScroll(scroll)) {
        // Header
        Row(Modifier.fillMaxWidth().background(NuKropSurface).statusBarsPadding().padding(8.dp), verticalAlignment = Alignment.CenterVertically) {
            IconButton(onBack) { Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = NuKropText) }
            Column {
                Text("AI Analysis Complete", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                Text("Results powered by NuKrop Vision AI", fontSize = 10.sp, color = NuKropTextMuted)
            }
        }

        if (raw.startsWith("ERROR:")) {
            Box(Modifier.padding(16.dp).fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(NuKropError.copy(alpha = 0.12f)).border(1.dp, NuKropError.copy(alpha = 0.4f), RoundedCornerShape(12.dp)).padding(16.dp)) {
                Text(raw, fontSize = 13.sp, color = NuKropError)
            }
        } else if (mode == ScanMode.CROP) {
            val data = parseCropJson(raw)
            if (data != null) CropResultUI(data, accent, context)
            else RawResultFallback(raw)
        } else {
            val data = parseSoilJson(raw)
            if (data != null) SoilResultUI(data, accent, context)
            else RawResultFallback(raw)
        }

        Spacer(Modifier.height(8.dp))
        Column(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Button(
                onClick = { saveReportToDownloads(context, raw) },
                modifier = Modifier.fillMaxWidth().height(50.dp),
                shape = RoundedCornerShape(25.dp),
                colors = ButtonDefaults.buttonColors(containerColor = NuKropCard)
            ) {
                Icon(Icons.Filled.Download, contentDescription = "Save", tint = accent, modifier = Modifier.size(20.dp))
                Spacer(Modifier.width(8.dp))
                Text("Save to Mobile", color = accent, fontWeight = FontWeight.Bold)
            }
            
            Row(Modifier.fillMaxWidth(), Arrangement.spacedBy(12.dp)) {
                OutlinedButton(onBack, Modifier.weight(1f).height(50.dp), shape = RoundedCornerShape(25.dp),
                    border = BorderStroke(1.dp, NuKropTextDim)) { 
                    Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = NuKropTextMuted, modifier = Modifier.size(18.dp))
                    Spacer(Modifier.width(6.dp))
                    Text("Back", color = NuKropTextMuted) 
                }
                Button(onRescan, Modifier.weight(1f).height(50.dp), shape = RoundedCornerShape(25.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = accent)) {
                    Text("Scan Again", color = NuKropDark, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}

fun saveReportToDownloads(context: android.content.Context, content: String) {
    try {
        val cleanRaw = content.replace(Regex("<think>.*?</think>", RegexOption.DOT_MATCHES_ALL), "").trim()
        val resolver = context.contentResolver
        val contentValues = ContentValues().apply {
            put(MediaStore.MediaColumns.DISPLAY_NAME, "NuKropAI_Report_${System.currentTimeMillis()}.json")
            put(MediaStore.MediaColumns.MIME_TYPE, "application/json")
            put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS)
        }
        val uri = resolver.insert(MediaStore.Files.getContentUri("external"), contentValues)
        if (uri != null) {
            resolver.openOutputStream(uri)?.use { os ->
                os.write(cleanRaw.toByteArray())
            }
            Toast.makeText(context, "Saved to Downloads!", Toast.LENGTH_SHORT).show()
        } else {
            Toast.makeText(context, "Failed to save file", Toast.LENGTH_SHORT).show()
        }
    } catch (e: Exception) {
        Toast.makeText(context, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
    }
}

@Composable
fun CropResultUI(d: CropScanData, accent: Color, context: android.content.Context) {
    val isHealthy = d.status.equals("Healthy", true)
    val hColor = if (isHealthy) NuKropBadgeGreen else NuKropError

    // Status card
    Box(Modifier.padding(16.dp).fillMaxWidth().clip(RoundedCornerShape(20.dp))
        .background(hColor.copy(alpha = 0.08f)).border(1.5.dp, hColor.copy(alpha = 0.5f), RoundedCornerShape(20.dp)).padding(18.dp)) {
        Column {
            Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween, Alignment.Top) {
                Column(Modifier.weight(1f)) {
                    Text(if (isHealthy) "✅ Healthy Crop!" else "⚠️  ${d.name}", fontSize = 22.sp, fontWeight = FontWeight.ExtraBold, color = hColor)
                    if (d.cause.isNotEmpty()) Text(d.cause, fontSize = 12.sp, color = NuKropTextMuted)
                }
                if (!isHealthy && d.severity.isNotEmpty()) {
                    Box(Modifier.clip(RoundedCornerShape(10.dp)).background(hColor.copy(alpha = 0.2f)).padding(horizontal = 10.dp, vertical = 5.dp)) {
                        Text(d.severity, fontSize = 12.sp, color = hColor, fontWeight = FontWeight.Bold)
                    }
                }
            }
            Spacer(Modifier.height(14.dp))
            Text("AI Confidence: ${d.confidence}%", fontSize = 12.sp, color = NuKropTextMuted)
        }
    }

    if (d.symptoms.isNotEmpty()) ResultBlock("🦠 Symptoms Observed", d.symptoms)
    if (d.treatment.isNotEmpty()) ResultBlock("💉 Treatment Plan", d.treatment)
    if (d.prevention.isNotEmpty()) ResultBlock("🛡️ Prevention", d.prevention)
    if (d.details.isNotEmpty()) ResultBlock("ℹ️ Detailed Insights", d.details)
    if (d.products.isNotEmpty()) {
        Text("🛒 Buy Recommended Products", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = NuKropText,
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 10.dp))
        d.products.forEach { (info, stores) -> BuyCard(info.first, info.second, stores, context, accent) }
    }
}

@Composable
fun SoilResultUI(d: SoilScanData, accent: Color, context: android.content.Context) {
    Box(Modifier.padding(16.dp).fillMaxWidth().clip(RoundedCornerShape(20.dp))
        .background(accent.copy(alpha = 0.08f)).border(1.5.dp, accent.copy(alpha = 0.4f), RoundedCornerShape(20.dp)).padding(18.dp)) {
        Column {
            Text("📊 Soil Analysis Complete", fontSize = 20.sp, fontWeight = FontWeight.ExtraBold, color = accent)
            Spacer(Modifier.height(14.dp))
            Row(Modifier.fillMaxWidth(), Arrangement.SpaceEvenly) {
                SoilChip("Type", d.soilType, accent)
                SoilChip("Est. pH", d.estimatedPH, accent)
                SoilChip("Organic", d.organicMatter, accent)
                SoilChip("Texture", d.texture, accent)
            }
        }
    }
    if (d.deficiencies.isNotEmpty()) ResultBlock("📉 Likely Deficiencies", d.deficiencies.joinToString(" • "))
    if (d.suitableCrops.isNotEmpty()) ResultBlock("🌱 Best Crops to Grow", d.suitableCrops.joinToString(", "))
    if (d.improvements.isNotEmpty()) ResultBlock("🛠 Improvement Tips", d.improvements)
    if (d.details.isNotEmpty()) ResultBlock("ℹ️ Detailed Insights", d.details)
    if (d.fertilizers.isNotEmpty()) {
        Text("🛒 Recommended Fertilizers", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = NuKropText,
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 10.dp))
        d.fertilizers.forEach { (info, stores) -> BuyCard(info.first, info.second, stores, context, accent) }
    }
}

@Composable fun RawResultFallback(raw: String) {
    Box(Modifier.padding(16.dp).fillMaxWidth().clip(RoundedCornerShape(16.dp)).background(NuKropCard).padding(16.dp)) {
        MarkdownText(raw, style = androidx.compose.ui.text.TextStyle(color = NuKropText, fontSize = 14.sp))
    }
}

@Composable fun ResultBlock(title: String, content: String) {
    Column(Modifier.padding(horizontal = 16.dp, vertical = 6.dp)) {
        Text(title, fontSize = 14.sp, fontWeight = FontWeight.Bold, color = NuKropAccent)
        Spacer(Modifier.height(5.dp))
        Box(Modifier.fillMaxWidth().clip(RoundedCornerShape(14.dp)).background(NuKropCard).padding(14.dp)) {
            Text(content, fontSize = 13.sp, color = NuKropTextMuted, lineHeight = 21.sp)
        }
    }
}

@Composable
fun BuyCard(name: String, dose: String, stores: List<Store>, context: android.content.Context, accent: Color) {
    Row(
        Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 6.dp)
            .clip(RoundedCornerShape(12.dp)).background(NuKropCard)
            .border(1.dp, Color.White.copy(alpha=0.05f), RoundedCornerShape(12.dp))
            .padding(14.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(Modifier.weight(1f)) {
            Text(name, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, color = NuKropText)
            Text("Usage: $dose", fontSize = 12.sp, color = NuKropTextMuted)
            
            if (stores.isNotEmpty()) {
                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    stores.forEach { store ->
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(6.dp))
                                .background(accent.copy(alpha = 0.15f))
                                .clickable {
                                    if (store.url.isNotBlank()) {
                                        try {
                                            context.startActivity(android.content.Intent(android.content.Intent.ACTION_VIEW, android.net.Uri.parse(store.url)))
                                        } catch (e: Exception) { }
                                    }
                                }
                                .padding(horizontal = 8.dp, vertical = 4.dp)
                        ) {
                            Text("${store.icon} ${store.name}", fontSize = 11.sp, color = accent, fontWeight = FontWeight.SemiBold)
                        }
                    }
                }
            }
        }
    }
}

@Composable fun SoilChip(label: String, value: String, accent: Color) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(value.ifEmpty { "—" }, fontSize = 14.sp, fontWeight = FontWeight.Bold, color = accent)
        Text(label, fontSize = 9.sp, color = NuKropTextDim)
    }
}




