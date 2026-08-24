# NuKropAI Android App — Kotlin Codebase Bug & Stability Audit Report

**Audit Date**: 2026-08-24  
**Auditor**: Kotlin Bug Hunter & Codebase Stability Explorer (Replacement 3)  
**Target Codebase**: `c:\Users\bjasw\Downloads\agriculture-ai-os`  

---

## Executive Summary

A comprehensive, line-by-line audit of all 45+ Kotlin source files in the NuKropAI codebase was conducted. The audit spanned ViewModels, Repositories, DataSources, Network Services, Room Database components, Background Workers, Coroutine Scopes, and Compose UI screens.

A total of **16 distinct stability and logical bugs** were identified across 6 categories:
1. **Critical Crashes & Fatal Runtime Exceptions** (5 bugs)
2. **Infinite Loading States & Unrecoverable UI Freezes** (3 bugs)
3. **Room Database Multi-Instance Anti-Pattern & State Loss** (2 bugs)
4. **OkHttp Connection & File Descriptor Leaks** (1 systemic pattern across 8 files)
5. **Concurrency & Thread Safety Issues** (2 bugs)
6. **Logical, Formatting, and Authentication State Bugs** (3 bugs)

---

## Detailed Findings & Root Cause Analysis

### 1. Critical Crashes & Fatal Runtime Exceptions

#### BUG-01: Background Thread Toast Crash in UpdateManager
- **File**: `app/src/main/java/com/example/UpdateManager.kt`
- **Lines**: 45–46
- **Code**:
  ```kotlin
  fun checkAndUpdate(context: Context) {
      scope.launch {
          Toast.makeText(context, "Checking for updates...", Toast.LENGTH_SHORT).show()
          ...
      }
  }
  ```
- **Root Cause**: `scope` is configured with `Dispatchers.IO`. Calling `Toast.makeText().show()` from a background thread that does not possess a Looper immediately throws `java.lang.RuntimeException: Can't toast on a thread that has not called Looper.prepare()`.
- **Severity**: Critical (Immediate crash on update check).
- **Recommended Fix**: Wrap the initial Toast invocation in `withContext(Dispatchers.Main)` or dispatch it on the main thread.

---

#### BUG-02: Missing MediaStore API Compatibility Crash on Android < 10 (API < 29)
- **File**: `app/src/main/java/com/example/SavedReportsScreen.kt` (lines 58, 70–75) & `app/src/main/java/com/example/DiseaseScannerScreen.kt` (lines 587–592)
- **Code in SavedReportsScreen**:
  ```kotlin
  val projection = arrayOf(
      MediaStore.Files.FileColumns._ID,
      MediaStore.Files.FileColumns.DISPLAY_NAME,
      MediaStore.Files.FileColumns.DATE_MODIFIED,
      MediaStore.Files.FileColumns.SIZE,
      MediaStore.Files.FileColumns.RELATIVE_PATH // <--- Added in API 29
  )
  ```
- **Code in DiseaseScannerScreen**:
  ```kotlin
  val contentValues = ContentValues().apply {
      put(MediaStore.MediaColumns.DISPLAY_NAME, "NuKropAI_Report_${System.currentTimeMillis()}.json")
      put(MediaStore.MediaColumns.MIME_TYPE, "application/json")
      put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS) // <--- Added in API 29
  }
  ```
- **Root Cause**: `MediaStore.MediaColumns.RELATIVE_PATH` does not exist on Android 9 and below (API < 29). Querying or inserting this column causes `IllegalArgumentException: column 'relative_path' does not exist` or write failures on older Android versions.
- **Severity**: High (Crashes/fails file saving on devices running API < 29).
- **Recommended Fix**: Check `Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q` before adding `RELATIVE_PATH` to projections or content values, and use standard external storage directory fallback on legacy devices.

---

#### BUG-03: Out-Of-Memory (OOM) & HTTP 413 Payload Too Large on Camera / Gallery Scans
- **File**: `app/src/main/java/com/example/DiseaseScannerScreen.kt` (lines 313, 485)
- **Code**:
  ```kotlin
  val bytes = context.contentResolver.openInputStream(uri)?.readBytes()
  ...
  val bytes = file.readBytes() // Uncompressed image from CameraX CAPTURE_MODE_MAXIMIZE_QUALITY
  ```
- **Root Cause**: High-resolution camera photos (12MP–48MP) are 10MB–25MB uncompressed JPEGs. Reading raw bytes into byte arrays and converting them to Base64 strings consumes up to 50MB–80MB heap memory, causing `OutOfMemoryError` on budget Android devices. Additionally, sending 20MB Base64 payloads exceeds Groq API request size limits (HTTP 413 Request Entity Too Large).
- **Severity**: High (OOM crashes & network rejection).
- **Recommended Fix**: Downsample and compress bitmaps to max 1024x1024 / 85% JPEG quality before Base64 encoding.

---

#### BUG-04: Unencoded URL Parameters Causing IllegalArgumentException in Supabase Calls
- **File**: `app/src/main/java/com/example/SupabaseClient.kt` (line 40)
- **Code**:
  ```kotlin
  val url = "$SUPABASE_URL/rest/v1/mandi_live_rates?select=*&state=ilike.*${state.trim()}*&commodity=ilike.*${commodity.trim()}*&order=id.desc&limit=20"
  ```
- **Root Cause**: `state` and `commodity` strings are directly interpolated into the URL without `URLEncoder.encode()`. If `state` contains spaces (e.g. `"Madhya Pradesh"`, `"Uttar Pradesh"`) or commodity has special characters (`"Cotton (Raw)"`), OkHttp's `Request.Builder().url(url)` throws `IllegalArgumentException: Unexpected char %#x at ... in URL`.
- **Severity**: High (Mandi live rates queries fail silently or crash).
- **Recommended Fix**: Use `URLEncoder.encode(param, "UTF-8")` for all dynamic query params.

---

### 2. Infinite Loading States & UI Freezes

#### BUG-05: Infinite Loading / Permanent Lockout on Chat Uncaught Exception
- **File**: `app/src/main/java/com/example/ChatViewModel.kt`
- **Lines**: 71, 80–91, 148–156
- **Code**:
  ```kotlin
  fun sendMessage(prompt: String, imageBytes: ByteArray? = null) {
      if (prompt.isBlank() && imageBytes == null) return
      if (_generatingStatus.value.isNotEmpty()) return // Early return guard

      _messages.update { it + userMsg + assistantMsgPlaceholder }
      _generatingStatus.value = if (imageBytes != null) "Analyzing image..." else "Thinking..."

      viewModelScope.launch {
          repository.insertMessage(...)
          if (imageBytes != null) streamImageResponse(...) else streamResponse(...)
      }
  }
  ```
- **Root Cause**: `viewModelScope.launch` has no try/catch around `streamResponse` / `streamImageResponse`. If `LocationHelper.getCurrentLocationStateAndMandi` or any other subcall throws an unhandled runtime exception, `_generatingStatus` is never reset to `""`. Because of line 71 (`if (_generatingStatus.value.isNotEmpty()) return`), the user can NEVER send another message again until the app is force killed. The loading message also spins indefinitely.
- **Severity**: High (Permanent UI freeze of core chat feature).
- **Recommended Fix**: Wrap `viewModelScope.launch` body in a `try ... finally { _generatingStatus.value = "" }` block and update the assistant placeholder with an error state on exception.

---

#### BUG-06: Infinite Shimmer / Loading State in PriceTickerService on Offline / Error
- **File**: `app/src/main/java/com/example/PriceTickerService.kt`
- **Lines**: 43, 79–82
- **Code**:
  ```kotlin
  private val _isLoading = MutableStateFlow(true)
  ...
  if (fetched.isNotEmpty()) {
      _tickerItems.value = fetched
      _isLoading.value = false
  }
  ```
- **Root Cause**: `_isLoading` is initialized to `true` and only updated to `false` when `fetched.isNotEmpty()`. When offline or if all requests fail, `_isLoading` remains `true` FOREVER, leaving the HomeScreen market ticker in an infinite loading state.
- **Severity**: Medium (HomeScreen UI shimmer never terminates).
- **Recommended Fix**: Invert loading state to `_isLoading.value = false` regardless of whether `fetched` is empty after the initial poll attempt.

---

#### BUG-07: Dead CoroutineScope on Service Restart in PriceTickerService
- **File**: `app/src/main/java/com/example/PriceTickerService.kt`
- **Lines**: 28, 48–50, 90
- **Code**:
  ```kotlin
  private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())
  ...
  fun start() {
      if (!isStarted.compareAndSet(false, true)) return
      scope.launch { ... }
  }
  fun stop() {
      scope.cancel()
  }
  ```
- **Root Cause**: Calling `scope.cancel()` cancels the `CoroutineScope` and its `SupervisorJob` permanently. Subsequent calls to `start()` launch coroutines on an already-cancelled scope, which are immediately cancelled. Furthermore, `isStarted` is not reset in `stop()`.
- **Severity**: Medium (Ticker permanently disabled after first stop).
- **Recommended Fix**: Manage a nullable `tickerJob: Job?` instead of cancelling the entire scope, and cancel only the job on `stop()`.

---

### 3. Room Database Multi-Instance Anti-Pattern & State Loss

#### BUG-08: Duplicate Room Database Instances Across App
- **File**: `app/src/main/java/com/example/ChatScreen.kt` (lines 51–55) vs `app/src/main/java/com/example/AiApplication.kt` (lines 42–47)
- **Code in ChatScreen**:
  ```kotlin
  val repository = remember { 
      ChatRepository(
          Room.databaseBuilder(application, AppDatabase::class.java, "chat_db").build().chatDao()
      )
  }
  ```
- **Code in AiApplication**:
  ```kotlin
  database = Room.databaseBuilder(
      applicationContext,
      AppDatabase::class.java,
      "ai_chat_database"
  )...
  ```
- **Root Cause**: `ChatScreen` builds a brand new unmanaged `RoomDatabase` instance targeting `"chat_db"`, completely ignoring `AiApplication`'s singleton database targeting `"ai_chat_database"`. This opens two distinct SQLite database files, causing data divergence and memory leaks.
- **Severity**: High (Data persistence fragmentation and SQLite resource leaks).
- **Recommended Fix**: Obtain `(application as AiApplication).chatRepository` in `ChatScreen.kt` instead of building a new database.

---

#### BUG-09: Optimistic UI Overwrite Race Condition in ChatViewModel
- **File**: `app/src/main/java/com/example/ChatViewModel.kt` (lines 38–65, 80–85)
- **Root Cause**: In `sendMessage`, `_messages` is updated with `userMsg + assistantMsgPlaceholder`. Then `repository.insertMessage(userMsg)` executes. When Room finishes inserting `userMsg`, Room's `allMessages.collect` emits the list from SQLite (which only has `userMsg` and does NOT have `assistantMsgPlaceholder`), overwriting `_messages.value` and erasing the loading indicator from the UI while the network call is still running.
- **Severity**: Medium (UI flicker and lost loading indicator).
- **Recommended Fix**: Merge pending in-flight messages with DB entities in `allMessages.collect` or decouple in-memory state.

---

### 4. OkHttp Connection & Socket Leaks (Missing `.use { }` / `.close()`)

#### BUG-10: Systemic OkHttp ResponseBody Leaks Across Network Callers
- **Files**:
  1. `app/src/main/java/com/example/GeminiVisionService.kt` (lines 95, 137, 179)
  2. `app/src/main/java/com/example/SupabaseClient.kt` (lines 49, 103)
  3. `app/src/main/java/com/example/WeatherService.kt` (line 44)
  4. `app/src/main/java/com/example/UpdateManager.kt` (line 53)
  5. `app/src/main/java/com/example/FarmKhataScreen.kt` (lines 76, 302)
  6. `app/src/main/java/com/example/EquipmentRentalScreen.kt` (line 79)
  7. `app/src/main/java/com/example/PeerChatScreen.kt` (lines 60, 92)
  8. `app/src/main/java/com/example/telemetry/NuKropIotManager.kt` (line 186)
- **Root Cause**: Calling `client.newCall(req).execute()` without closing `response` or enclosing in `.use { }` leaves socket connections and HTTP streams open in OkHttp's connection pool. Over prolonged app usage, this leads to `SocketTimeoutException`, file descriptor exhaustion, and network stall.
- **Severity**: Medium-High (Progressive degradation and connection exhaustion).
- **Recommended Fix**: Enclose all `client.newCall(...).execute()` in `use { response -> ... }`.

---

### 5. Concurrency & Thread Safety Issues

#### BUG-11: Unsynchronized ArrayList Access in NuKropIotManager
- **File**: `app/src/main/java/com/example/telemetry/NuKropIotManager.kt` (lines 37, 64, 160)
- **Code**:
  ```kotlin
  private val offlineCommandQueue = mutableListOf<Pair<String, String>>()
  ```
- **Root Cause**: `offlineCommandQueue` is written from the UI thread (`sendAsyncCommand`) and read/cleared from OkHttp WebSocket background threads (`onOpen`) without synchronization. Concurrent modification throws `ConcurrentModificationException` and corrupts queued commands.
- **Severity**: Medium (Crash / race condition during network reconnection).
- **Recommended Fix**: Use `ConcurrentLinkedQueue<Pair<String, String>>` or synchronize access.

---

#### BUG-12: Unmanaged Thread Spawning and Timer Collisions in NuKropIotManager
- **File**: `app/src/main/java/com/example/telemetry/NuKropIotManager.kt` (lines 136, 161, 189–194)
- **Code**:
  ```kotlin
  kotlin.concurrent.thread {
      Thread.sleep(10000)
      if (_commandState.value == CommandState.VERIFICATION) {
          _commandState.value = CommandState.FAILED
      }
  }
  ```
- **Root Cause**: Spawning unmanaged OS threads (`kotlin.concurrent.thread`) bypasses coroutine cancellation. If a user triggers command 1 and then command 2 five seconds later, the 10-second timer from command 1 will expire and erroneously force `_commandState.value = CommandState.FAILED` for command 2.
- **Severity**: Medium (False-positive command failure reporting).
- **Recommended Fix**: Replace OS threads with managed coroutine jobs with proper cancellation.

---

### 6. Logical, Formatting & Auth State Bugs

#### BUG-13: Typo in Market Price Display String on HomeScreen
- **File**: `app/src/main/java/com/example/HomeScreen.kt`
- **Line**: 167
- **Code**:
  ```kotlin
  Text("${first.commodity} (${first.market}) ,${first.modalPrice}", color = NuKropText, ...)
  ```
- **Root Cause**: Typo `,${first.modalPrice}` where a comma was written instead of the Rupee currency symbol `₹`.
- **Severity**: Low (UI formatting defect).
- **Recommended Fix**: Change `,${first.modalPrice}` to `₹${first.modalPrice}`.

---

#### BUG-14: Incompatible Type in AuthViewModel `_currentUser` Breaking ProfileScreen
- **File**: `app/src/main/java/com/example/AuthViewModel.kt` (lines 28, 35, 46, 127) vs `app/src/main/java/com/example/ProfileScreen.kt` (lines 36–37)
- **Code**:
  ```kotlin
  // AuthViewModel:
  private val _currentUser = MutableStateFlow<Any?>(null) // Holds String OR UserInfo
  
  // ProfileScreen:
  val currentUser by authViewModel.currentUser.collectAsState()
  val user = currentUser as? UserInfo
  ```
- **Root Cause**: When a user logs in via Google or restores a saved session, `_currentUser` is assigned a `String` (email / display name). `ProfileScreen` attempts to cast `currentUser as? UserInfo`, which evaluates to `null` for non-Supabase `UserInfo` objects. As a result, `ProfileScreen` always displays "Guest Farmer" and "No Email Found" even for authenticated users.
- **Severity**: High (Broken user profile display after login).
- **Recommended Fix**: Define a strongly-typed domain `UserSession` model containing `name`, `email`, `avatarUrl`, and `id`.

---

#### BUG-15: Auth State Desynchronization on Session Expiry
- **File**: `app/src/main/java/com/example/AuthViewModel.kt`
- **Lines**: 49–55
- **Code**:
  ```kotlin
  else -> {
      if (_currentUser.value != "Guest" && _currentUser.value != "Google Farmer") {
          _currentUser.value = null
          prefs.edit().clear().apply()
      }
  }
  ```
- **Root Cause**: When Supabase reports session unauthenticated, `_currentUser` is cleared to `null`, but `_authState` is NOT reset (remains `AuthState.Success`). This causes the app UI to remain in an invalid half-authenticated state where `currentUser == null` but `authState == Success`.
- **Severity**: Medium (State desynchronization).
- **Recommended Fix**: Set `_authState.value = AuthState.Idle` in the unauthenticated branch.

---

#### BUG-16: Invalid OAuth Client ID in Google Sign-In
- **File**: `app/src/main/java/com/example/AuthViewModel.kt`
- **Line**: 108
- **Code**:
  ```kotlin
  .setServerClientId("NuKrop.AI")
  ```
- **Root Cause**: `"NuKrop.AI"` is not a valid Google OAuth 2.0 Web Client ID (which must follow the format `xxx.apps.googleusercontent.com`). `CredentialManager.getCredential` fails immediately and drops into the catch block.
- **Severity**: Medium (Google Sign-In fails).
- **Recommended Fix**: Move the Google Web Client ID to `BuildConfig` or string resource and configure a valid client ID.

---

## Summary Matrix of Findings

| ID | Location | Category | Severity | Impact |
|---|---|---|---|---|
| BUG-01 | `UpdateManager.kt:46` | Crash | **Critical** | Crash on update check due to Toast on background thread |
| BUG-02 | `SavedReportsScreen.kt:58` & `DiseaseScannerScreen.kt:587` | Compatibility Crash | **High** | Crashes on Android API < 29 due to `RELATIVE_PATH` |
| BUG-03 | `DiseaseScannerScreen.kt:313,485` | OOM & Network Error | **High** | OutOfMemory & HTTP 413 on camera photos |
| BUG-04 | `SupabaseClient.kt:40` | Network Crash | **High** | Unencoded URLs with spaces/special chars fail |
| BUG-05 | `ChatViewModel.kt:71,80-91` | Infinite Loading | **High** | Chat permanently locks up on any network/location failure |
| BUG-06 | `PriceTickerService.kt:43,81` | Infinite Loading | **Medium** | Market ticker spins infinitely when offline |
| BUG-07 | `PriceTickerService.kt:28,90` | Lifecycle Bug | **Medium** | Cancelled CoroutineScope prevents service restart |
| BUG-08 | `ChatScreen.kt:53` vs `AiApplication.kt:42` | Architectural Bug | **High** | Duplicate Room DB instances split data and leak memory |
| BUG-09 | `ChatViewModel.kt:38-65` | Race Condition | **Medium** | Room DB emission wipes in-flight assistant loading bubble |
| BUG-10 | Multiple files (8 files) | Resource Leak | **Medium-High** | Unclosed OkHttp `ResponseBody` exhausts socket pool |
| BUG-11 | `NuKropIotManager.kt:37` | Concurrency Bug | **Medium** | Unsynchronized `ArrayList` causes `ConcurrentModificationException` |
| BUG-12 | `NuKropIotManager.kt:189` | Concurrency Bug | **Medium** | Unmanaged OS thread timer overrides subsequent commands |
| BUG-13 | `HomeScreen.kt:167` | UI Formatting | **Low** | Currency typo `,${modalPrice}` instead of `₹${modalPrice}` |
| BUG-14 | `AuthViewModel.kt:28` & `ProfileScreen.kt:37` | Logical Bug | **High** | `_currentUser` Any? casting causes Profile to show Guest Farmer |
| BUG-15 | `AuthViewModel.kt:49` | State Sync Bug | **Medium** | Auth state remains `Success` when user session expires |
| BUG-16 | `AuthViewModel.kt:108` | Configuration Bug | **Medium** | Invalid Google OAuth client ID string `"NuKrop.AI"` |

---

## Next Steps for Fix Phase
1. Fix BUG-01, BUG-02, BUG-03, BUG-04 (Crashes & compatibility).
2. Fix BUG-05, BUG-06, BUG-07 (Infinite loading states and CoroutineScope lifecycle).
3. Consolidate Room Database singleton to `AiApplication.database` (BUG-08).
4. Wrap all OkHttp `execute()` calls with `.use { }` (BUG-10).
5. Standardize `_currentUser` domain model and fix UI typos (BUG-13, BUG-14, BUG-15).
