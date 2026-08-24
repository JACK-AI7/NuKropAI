# NuKropAI Android App — Comprehensive UI Alignment & Polish Audit Report

**Date:** 2026-08-24  
**Auditor:** Teamwork UI Alignment & Polish Explorer  
**Codebase:** `c:\Users\bjasw\Downloads\agriculture-ai-os`  
**Target:** Jetpack Compose UI (Screens, Navigation, Scaffolds, Lists, Dialogs, Cards)

---

## 1. Executive Summary

A comprehensive architectural and visual audit of all Jetpack Compose screens and UI components in NuKropAI was conducted. 

### Key Audit Findings:
1. **Double Inset Padding on Status Bars**: The root `Scaffold` in `MainActivity.kt` consumes `WindowInsets.systemBars` and applies `innerPadding` to the root `Box`. Simultaneously, individual screens apply `.statusBarsPadding()`, causing double top insets on edge-to-edge devices.
2. **Missing IME Keyboard Insets**: `ChatScreen.kt`, `PeerChatScreen.kt`, and `LoginScreen.kt` lack `Modifier.imePadding()`, causing soft keyboards to obscure text inputs and buttons.
3. **Missing Modifier.weight(1f) in Horizontal Rows**: In `MandiRecordCard`, `PeerChatScreen`, `SettingsItem`, `FarmKhataScreen`, `EquipmentCard`, `SavedReportsScreen`, and multiple analytics cards, inner text columns lack `Modifier.weight(1f)` or text ellipsis constraints, causing long text strings to push trailing badges, price labels, and action buttons off-screen.
4. **Non-Scrollable Layouts Risking Viewport Clipping**: `ScanHub` (DiseaseScannerScreen), `TractorAutopilotScreen`, `SplashScreen`, and `DevicePairingScreen` are non-scrollable Columns with tall fixed-height content that overflows and clips on small screens (<5.5") or in landscape orientation.
5. **Unbounded LazyColumn Crash Risk**: `KnowledgeScreen.kt` contains a `LazyColumn` nested inside a parent `Column` without `Modifier.weight(1f)`, which can cause Compose measurement runtime exceptions.
6. **Horizontal Store Tag Overflow**: In `DiseaseScannerScreen.kt` (`BuyCard`), store buttons inside a single `Row` overflow horizontally when multiple store links are provided.
7. **Button Shape Inconsistencies**: In `ChatScreen.kt`, action buttons use asymmetric dimensions (48dp x 56dp) with `CircleShape`, resulting in distorted oval pills instead of uniform circles.

---

## 2. Global Scaffolding, Navigation Bar & Inset Architecture

### 2.1 Status Bar & Bottom Bar Padding Hierarchy
- **File:** `app/src/main/java/com/example/MainActivity.kt`
- **Lines:** 97–151
- **Observation:**
  ```kotlin
  Scaffold(
      containerColor = Color(0xFF0D1208),
      bottomBar = {
          Box(
              Modifier
                  .fillMaxWidth()
                  .background(Brush.verticalGradient(listOf(Color.Transparent, Color(0xF5141A0A))))
                  .navigationBarsPadding()
                  .padding(horizontal = 16.dp, vertical = 10.dp)
          ) { ... }
      }
  ) { innerPadding ->
      Box(Modifier.padding(innerPadding).fillMaxSize()) {
          ...
      }
  }
  ```
- **Issue:**
  The `Scaffold` default `contentWindowInsets` applies `WindowInsets.systemBars`. Because there is no `topBar` defined on the root `Scaffold`, `innerPadding.calculateTopPadding()` is equal to the top status bar height.
  When screens inside `AnimatedContent` also apply `.statusBarsPadding()` (e.g. `HomeScreen.kt:98`, `MarketScreen.kt:122`, `ProfileScreen.kt:54`, etc.), the top status bar inset is added twice!
- **Recommended Strategy:**
  In `MainActivity.kt`, pass `contentWindowInsets = WindowInsets(0, 0, 0, 0)` to `Scaffold`, or have the root `Scaffold` handle system bars and remove redundant `.statusBarsPadding()` from nested screen headers. Passing `contentWindowInsets = WindowInsets(0.dp)` allows individual screens to cleanly manage their own top bars and translucent hero image overlays.

### 2.2 IME (Software Keyboard) Inset Handling
- **Files:** `ChatScreen.kt:163`, `PeerChatScreen.kt:221`, `LoginScreen.kt:114`
- **Issue:** Text input containers lack `.imePadding()`. When the soft keyboard opens, it directly obscures the input field and messages on devices without automatic window pan.
- **Recommended Strategy:** Add `.imePadding()` to input bars in `ChatScreen.kt` and `PeerChatScreen.kt`, and to the scrollable container in `LoginScreen.kt`.

---

## 3. Screen-by-Screen Detailed Audit & Findings

---

### Screen 1: `HomeScreen.kt`
- **File:** `app/src/main/java/com/example/HomeScreen.kt`
- **Line 80:** `Column(Modifier.fillMaxSize().verticalScroll(scrollState).padding(bottom = 100.dp))`
- **Line 98:** `Row(Modifier.fillMaxWidth().statusBarsPadding().padding(16.dp), ...)`
- **Line 295:** `Spacer(Modifier.height(180.dp))`
- **Findings:**
  1. **Excessive Cumulative Bottom Spacing:** `padding(bottom = 100.dp)` plus `Spacer(Modifier.height(180.dp))` plus `innerPadding` from `MainActivity` creates over 280dp of trailing whitespace at the bottom of the home screen.
  2. **Double Status Bar Inset:** `statusBarsPadding()` on line 98 inside a container that already has `innerPadding` top inset.
- **Fix Recommendation:** Reduce bottom spacer to `Spacer(Modifier.height(24.dp))` and remove extra `padding(bottom = 100.dp)` from the Column.

---

### Screen 2: `MarketScreen.kt`
- **File:** `app/src/main/java/com/example/MarketScreen.kt`
- **Lines 358–371:** `MandiRecordCard`
  ```kotlin
  Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
      Row(verticalAlignment = Alignment.CenterVertically) { // Missing Modifier.weight(1f)
          Box(...)
          Spacer(Modifier.width(12.dp))
          Column(Modifier.weight(1f)) {
              Text(record.market, fontSize = 16.sp, fontWeight = FontWeight.Bold, color = NuKropText, maxLines = 1, overflow = TextOverflow.Ellipsis)
              Text("${record.district}, ${record.state}", ...)
          }
      }
      Spacer(Modifier.width(8.dp))
      Text("₹ ${record.modalPrice.toInt()} / Qtl", fontSize = 18.sp, fontWeight = FontWeight.ExtraBold, color = NuKropAccent, maxLines = 1)
  }
  ```
- **Findings:**
  1. **Price Text Truncation / Push Off-Screen:** The inner `Row` wrapping the icon and market name does NOT have `Modifier.weight(1f)`. The `Column(Modifier.weight(1f))` inside it only takes weight relative to the unconstrained inner `Row`. A long market name will cause the inner `Row` to expand and push the price label `₹ ... / Qtl` off-screen to the right.
  2. **Fixed Header Height On Small Screens:** Lines 122–258 contain a large non-scrollable header (Title, Live Badge, Location Pill, 2 Search TextFields of 56dp height each, Popular Crops row). On small screens, this consumes 350dp+ leaving almost no room for results.
- **Fix Recommendation:**
  Apply `Modifier.weight(1f)` to the left `Row` in `MandiRecordCard`, ensuring the price is guaranteed its required width.

---

### Screen 3: `DiseaseScannerScreen.kt`
- **File:** `app/src/main/java/com/example/DiseaseScannerScreen.kt`
- **Lines 229–258 (`ScanHub`):**
  `Column(modifier = modifier.fillMaxSize().background(...).statusBarsPadding().padding(24.dp), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally)`
- **Lines 450–519 (`CameraScanner`):**
  `Column(Modifier.align(Alignment.BottomCenter).fillMaxWidth().background(...).navigationBarsPadding().padding(vertical = 24.dp, horizontal = 32.dp)...)`
  `Spacer(Modifier.height(90.dp))` on line 514.
- **Lines 529–580 (`ScanResultView`):**
  Missing bottom spacer after "Save to Mobile" and "Scan Again" action buttons.
- **Lines 684–720 (`BuyCard`):**
  `Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) { stores.forEach { ... } }`
- **Findings:**
  1. **`ScanHub` Overflow on Small Screens:** `ScanHub` does not have `verticalScroll`. On smaller screens or when font size is increased, the 2 large feature cards (160dp each) and header elements are clipped.
  2. **Camera Controls 90dp Gap:** In `CameraScanner`, `Spacer(Modifier.height(90.dp))` between the shutter button and the instruction text pushes content down into the bottom bar area when navigation insets are applied.
  3. **`BuyCard` Multi-Store Row Clipping:** When 2 or 3 stores are returned by the AI, they are placed in a horizontal `Row` without wrapping or scrolling, clipping beyond the right edge of the card.
  4. **Missing Bottom Padding in `ScanResultView`:** Scrollable results view ends abruptly at the bottom buttons without trailing clearance.
- **Fix Recommendation:**
  1. Add `.verticalScroll(rememberScrollState())` to `ScanHub`.
  2. In `BuyCard`, wrap stores with `horizontalScroll(rememberScrollState())` or `FlowRow`.
  3. Adjust `CameraScanner` bottom spacer to 16dp and add `Spacer(Modifier.height(48.dp))` at the end of `ScanResultView`.

---

### Screen 4: `LoanScreen.kt`
- **File:** `app/src/main/java/com/example/LoanScreen.kt`
- **Lines 133–135:** `Spacer(Modifier.height(40.dp))` inside scrollable list.
- **Lines 163–169 (`SchemeCard`):**
  `Text(title, fontSize = 15.sp, fontWeight = FontWeight.Bold, color = NuKropText, modifier = Modifier.weight(1f))`
  `Box(Modifier.clip(RoundedCornerShape(8.dp)).background(...).padding(...)) { Text(amount, ...) }`
- **Findings:**
  1. **Short Bottom Clearance:** 40dp spacer inside the scrollable column is relatively small for navigating over bottom navigation bars.
  2. **Scheme Title & Amount Alignment:** If `amount` is long (e.g. "Up to ₹50,000 / ha"), missing spacer between `Text(title)` and amount `Box` causes text to touch.
- **Fix Recommendation:** Increase bottom spacer to `Spacer(Modifier.height(80.dp))` and ensure 8dp horizontal spacing between title and amount badge.

---

### Screen 5: `ChatScreen.kt`
- **File:** `app/src/main/java/com/example/ChatScreen.kt`
- **Lines 162–284:** Input Area & Action Buttons
- **Lines 191–216:**
  `Box(modifier = Modifier.height(56.dp).width(48.dp).padding(bottom = 4.dp).clip(CircleShape)...)`
- **Line 304:** `widthIn(max = 280.dp)` on `ChatBubble`.
- **Findings:**
  1. **Missing Keyboard IME Padding:** Input area lacks `.imePadding()`, causing it to be hidden when the soft keyboard appears.
  2. **Non-Circular Button Shape Distortion:** Using `width(48.dp)` and `height(56.dp)` with `.clip(CircleShape)` creates an asymmetrical distorted oval rather than a true circle.
  3. **Chat Bubble Max Width Inelasticity:** Hardcoded `max = 280.dp` is narrow on tablets and wide on ultra-narrow screens.
- **Fix Recommendation:**
  1. Add `.imePadding()` to the input bar container.
  2. Use uniform size `Modifier.size(48.dp)` with `CircleShape` for camera, voice, and send buttons.
  3. Use `Modifier.fillMaxWidth(0.85f)` or `widthIn(min = 48.dp, max = 340.dp)` for `ChatBubble`.

---

### Screen 6: `PeerChatScreen.kt`
- **File:** `app/src/main/java/com/example/PeerChatScreen.kt`
- **Lines 154–175 (Header Bar):**
  ```kotlin
  Row(verticalAlignment = Alignment.CenterVertically) { // Missing Modifier.weight(1f)
      IconButton(onClick = onNavigateBack) { ... }
      Box(...) { Text(...) }
      Spacer(Modifier.width(10.dp))
      Column {
          Text(recipientName, fontSize = 16.sp, fontWeight = FontWeight.Bold, color = NuKropText)
          Text(recipientInfo, fontSize = 11.sp, color = NuKropBadgeGreen)
      }
  }
  IconButton(onClick = { ... }) { Icon(Icons.Default.Phone, ...) }
  ```
- **Lines 220–226 (Input Bar):**
  `Row(modifier = Modifier.fillMaxWidth().background(...).navigationBarsPadding().padding(...))`
- **Findings:**
  1. **Call Icon Push Off-Screen:** If `recipientName` or `recipientInfo` is long (e.g. "Suresh Patel - Cotton Specialist • 4.2 km"), the unconstrained left `Row` pushes the `Phone` call `IconButton` off the right edge.
  2. **Missing IME Padding on Chat Input Bar:** The input bar uses `navigationBarsPadding()` but lacks `imePadding()`.
- **Fix Recommendation:**
  1. Add `Modifier.weight(1f)` to the left header `Row` and set `maxLines = 1, overflow = TextOverflow.Ellipsis` on the texts.
  2. Add `.imePadding()` to the input row.

---

### Screen 7: `ProfileScreen.kt`
- **File:** `app/src/main/java/com/example/ProfileScreen.kt`
- **Lines 364–410 (`FarmListItem`):**
  Left `Row` lacks `Modifier.weight(1f)`. Long farm names push the "Active" badge off-screen.
- **Lines 413–451 (`SettingsItem`):**
  ```kotlin
  Row(modifier = Modifier.fillMaxWidth().clip(...).background(...).clickable { onClick() }.padding(14.dp), ...) {
      Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) { // Missing weight(1f)
          Box(...) { Icon(...) }
          Column {
              Text(title, fontSize = 14.sp, fontWeight = FontWeight.SemiBold, color = NuKropText)
              Text(subtitle, fontSize = 11.sp, color = NuKropTextMuted)
          }
      }
      Icon(Icons.Default.ChevronRight, ...)
  }
  Spacer(modifier = Modifier.height(8.dp)) // Extra internal spacer
  ```
- **Findings:**
  1. **SettingsItem Chevron Push Off-Screen:** Left inner `Row` has no `Modifier.weight(1f)`. A long subtitle (e.g. "English (United States) - Recommended") pushes the `ChevronRight` icon off the card.
  2. **Compounded Uneven Spacers:** `SettingsItem` has `Spacer(Modifier.height(8.dp))` inside its composable, plus `Spacer(Modifier.height(12.dp))` between items in the parent Column, creating 20dp uneven spacing.
- **Fix Recommendation:**
  Add `Modifier.weight(1f)` to the inner row in `SettingsItem` and `FarmListItem`, and remove internal bottom spacer from `SettingsItem` to let parent Column control spacing.

---

### Screen 8: `SoilScreen.kt`
- **File:** `app/src/main/java/com/example/SoilScreen.kt`
- **Lines 142–173:** Borewell Motor Control Card
- **Findings:**
  Left Row in motor status lacks `Modifier.weight(1f)` next to `Switch` or pending spinner.
- **Fix Recommendation:** Add `Modifier.weight(1f)` to the left status column.

---

### Screen 9: `LoginScreen.kt`
- **File:** `app/src/main/java/com/example/LoginScreen.kt`
- **Lines 113–121:**
  `Column(modifier = Modifier.fillMaxSize().verticalScroll(scrollState).statusBarsPadding().navigationBarsPadding().padding(horizontal = 24.dp))`
- **Lines 361–400 (`NuKropTextField`):**
  Placeholder contains emoji icon instead of using `leadingIcon` slot.
- **Findings:**
  1. **Missing Keyboard IME Padding:** When typing on the password field, software keyboard covers the "Sign In" button on smaller screens.
  2. **Placeholder Icon Disappears When Typing:** Because the icon is inside `placeholder = { ... }`, once the user starts typing, the icon vanishes.
- **Fix Recommendation:** Add `.imePadding()` to the Column and move the icon to the `leadingIcon` slot of `OutlinedTextField`.

---

### Screen 10: `SplashScreen.kt`
- **File:** `app/src/main/java/com/example/SplashScreen.kt`
- **Lines 71–76:**
  `Column(modifier = Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.SpaceBetween)`
- **Line 78:** `Column(modifier = Modifier.padding(top = 48.dp))`
- **Findings:**
  1. **No Scroll On Small Devices:** Fixed 200dp hero box + 2 feature cards + start button on a non-scrolling Column with `SpaceBetween` causes vertical clipping on displays < 650dp.
  2. **Hardcoded Top Padding Instead of Status Insets:** Uses `padding(top = 48.dp)` instead of `statusBarsPadding()`.
- **Fix Recommendation:** Add `verticalScroll(rememberScrollState())` and use `statusBarsPadding().padding(top = 16.dp)`.

---

### Screen 11: `FarmDigitalTwinScreen.kt`
- **File:** `app/src/main/java/com/example/FarmDigitalTwinScreen.kt`
- **Lines 391–404:** Moisture Stress Alert Card
- **Lines 410–429 (`ValveRow`):**
  `Row(modifier = Modifier.fillMaxWidth().clickable { onClick() }, horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically)`
- **Findings:**
  1. In `ValveRow`, the left `Column` has no `weight(1f)`. The right status badge ("AI OPENING (2.5 L/min)") can collide with the valve name on narrow screens.
  2. In the Moisture Alert Card, `Column` text lacks `Modifier.weight(1f)` next to the warning icon.
- **Fix Recommendation:** Add `Modifier.weight(1f)` to left columns in `ValveRow` and alert card.

---

### Screen 12: `FarmKhataScreen.kt`
- **File:** `app/src/main/java/com/example/FarmKhataScreen.kt`
- **Lines 205–231 (Transaction Item):**
  ```kotlin
  Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween, Alignment.CenterVertically) {
      Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) { // Missing weight(1f)
          Box(...)
          Column {
              Text(entry.title, fontSize = 13.sp, fontWeight = FontWeight.Bold, color = NuKropText)
              Text("${entry.category} • ${entry.date}", fontSize = 11.sp, color = NuKropTextMuted)
          }
      }
      Text("${if (entry.isIncome) "+" else "-"}₹${String.format("%,.0f", entry.amount)}", ...)
  }
  ```
- **Findings:**
  Inner left `Row` has no `weight(1f)`. Long transaction titles push the price amount `+₹...` off-screen.
- **Fix Recommendation:** Add `Modifier.weight(1f)` to the inner left `Row` and set `maxLines = 1, overflow = TextOverflow.Ellipsis` on `entry.title`.

---

### Screen 13: `EquipmentRentalScreen.kt`
- **File:** `app/src/main/java/com/example/EquipmentRentalScreen.kt`
- **Lines 290–319 (`EquipmentCard`):**
  ```kotlin
  Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween, Alignment.Top) {
      Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) { // Missing weight(1f)
          Box(...)
          Column {
              Text(item.name, fontSize = 14.sp, fontWeight = FontWeight.Bold, color = NuKropText)
              Text("${item.category} • ${item.distance}", fontSize = 11.sp, color = NuKropTextMuted)
          }
      }
      Box(...) { Text(if (item.isAvailable) "AVAILABLE" else "BOOKED", ...) }
  }
  ```
- **Findings:**
  Long vehicle titles (e.g. "Mahindra 575 DI Tractor (45 HP) with Disc Harrow") push the "AVAILABLE" / "BOOKED" status badge off-screen to the right.
- **Fix Recommendation:** Add `Modifier.weight(1f)` to the left inner `Row` and `maxLines = 1, overflow = TextOverflow.Ellipsis` to `Text(item.name)`.

---

### Screen 14: `SavedReportsScreen.kt`
- **File:** `app/src/main/java/com/example/SavedReportsScreen.kt`
- **Lines 205–230 (`ReportCard`):**
  Column next to the icon lacks `Modifier.weight(1f)` and `report.name` lacks `maxLines = 1, overflow = TextOverflow.Ellipsis`.
- **Fix Recommendation:** Add `Modifier.weight(1f)` and text ellipsis to `ReportCard`.

---

### Screen 15: `TractorAutopilotScreen.kt`
- **File:** `app/src/main/java/com/example/TractorAutopilotScreen.kt`
- **Lines 47–111:**
  `Column(modifier = Modifier.fillMaxSize().background(NuKropDark).padding(16.dp))`
  `Spacer(modifier = Modifier.weight(1f))` on line 98.
- **Findings:**
  `TractorAutopilotScreen` does not have `verticalScroll`. On small screen devices or in landscape mode, the telemetry tiles and status card take >400dp, causing the "ENGAGE AUTOPILOT" button to be pushed completely off-screen.
- **Fix Recommendation:** Add `verticalScroll(rememberScrollState())` and replace `.weight(1f)` with `Spacer(Modifier.height(24.dp))` and bottom clearance `Spacer(Modifier.height(80.dp))`.

---

### Screen 16: `DroneOpsScreen.kt`
- **File:** `app/src/main/java/com/example/DroneOpsScreen.kt`
- **Lines 80–263:** `LazyColumn`
- **Findings:**
  Missing trailing spacer at the bottom of the `LazyColumn`. The "Dispatch Autonomous Drone" button sits directly against the bottom edge.
- **Fix Recommendation:** Add `item { Spacer(Modifier.height(80.dp)) }` at the end of `LazyColumn`.

---

### Screen 17: `FarmMapScreen.kt`
- **File:** `app/src/main/java/com/example/FarmMapScreen.kt`
- **Lines 69–103:** Top header row lacks `Modifier.weight(1f)` on plot info Column next to plot selector indicator dots.
- **Lines 108–115:** Bottom `FarmStatsPanel` lacks bottom navigation inset clearance.
- **Fix Recommendation:** Add `Modifier.weight(1f)` to the header Column and `Modifier.navigationBarsPadding().padding(bottom = 80.dp)` to the bottom panel container.

---

### Screen 18: `FieldNavigationScreen.kt`
- **File:** `app/src/main/java/com/example/FieldNavigationScreen.kt`
- **Lines 104–108, 137 (`MetricCard`):**
  `Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) { MetricCard(...); MetricCard(...); MetricCard(...) }`
  where each `MetricCard` has hardcoded `.width(100.dp)`.
- **Findings:**
  3 cards of 100dp + padding = 340dp width required. On screens with width < 360dp, the right card is clipped.
- **Fix Recommendation:** Replace fixed `width(100.dp)` with `Modifier.weight(1f)` for each card in a `spacedBy(8.dp)` row.

---

### Screen 19: `DevicePairingScreen.kt`
- **File:** `app/src/main/java/com/example/DevicePairingScreen.kt`
- **Lines 29–36:** Non-scrollable centered Column.
- **Fix Recommendation:** Add `verticalScroll(rememberScrollState())` to ensure responsiveness on all display sizes.

---

### Screens 20–25: `AgentsScreen`, `FoodSecurityScreen`, `KnowledgeScreen`, `RegionalIntelligenceScreen`, `ScientificValidationScreen`
- **Findings:**
  1. `KnowledgeScreen.kt:42`: `LazyColumn` inside `Column` without `Modifier.weight(1f)` causing unbounded height constraint failure.
  2. Missing bottom spacers in `LazyColumn`s across all these screens (`Spacer(Modifier.height(80.dp))`).
  3. Text columns next to leading icons lack `Modifier.weight(1f)`.
- **Fix Recommendation:** Add `Modifier.weight(1f)` to `KnowledgeScreen` `LazyColumn`, add `Modifier.weight(1f)` to inner text Columns, and add `item { Spacer(Modifier.height(80.dp)) }` to all `LazyColumn`s.

---

## 4. Scroll Container & Bottom Padding Audit Table

| Screen File | Container Type | Current Bottom Spacing | Nav Bar Clipping Risk | Recommended Action |
|---|---|---|---|---|
| `MainActivity.kt` | `Scaffold` | `innerPadding` applied | Low | Pass `contentWindowInsets = WindowInsets(0.dp)` to avoid double top status bar padding |
| `HomeScreen.kt` | `verticalScroll Column` | `100.dp` pad + `180.dp` Spacer | None (Excessive 280dp) | Clean up to `Spacer(Modifier.height(24.dp))` |
| `MarketScreen.kt` | `verticalScroll Column` | `180.dp` pad | None | Keep safe bottom spacing |
| `DiseaseScannerScreen.kt` (ScanHub) | `Column` | None (no scroll) | **HIGH (overflow on small screens)** | Add `verticalScroll` + `Spacer(Modifier.height(80.dp))` |
| `DiseaseScannerScreen.kt` (ScanResult) | `verticalScroll Column` | `0.dp` after buttons | Medium | Add `Spacer(Modifier.height(48.dp))` |
| `LoanScreen.kt` | `verticalScroll Column` | `40.dp` Spacer | Low/Medium | Increase to `Spacer(Modifier.height(80.dp))` |
| `ChatScreen.kt` | `LazyColumn` | `PaddingValues(16.dp)` | Low | Add `imePadding()` to input area |
| `PeerChatScreen.kt` | `LazyColumn` | `PaddingValues(16.dp)` | Low | Add `imePadding()` to input area |
| `ProfileScreen.kt` | `verticalScroll Column` | `180.dp` Spacer | None | Maintain clean layout |
| `SoilScreen.kt` | `verticalScroll Column` | `100.dp` Spacer | None | Safe |
| `LoginScreen.kt` | `verticalScroll Column` | `32.dp` Spacer | Medium with keyboard | Add `imePadding()` |
| `SplashScreen.kt` | `Column` | None (no scroll) | **HIGH (overflow on small screens)** | Add `verticalScroll` |
| `FarmDigitalTwinScreen.kt` | `verticalScroll Column` | `100.dp` Spacer | None | Safe |
| `FarmKhataScreen.kt` | `verticalScroll Column` | `80.dp` Spacer | None | Safe |
| `EquipmentRentalScreen.kt` | `verticalScroll Column` | `80.dp` Spacer | None | Safe |
| `SavedReportsScreen.kt` | `LazyColumn` | `100.dp` Spacer item | None | Safe |
| `TractorAutopilotScreen.kt` | `Column` | `32.dp` Spacer (no scroll) | **HIGH (button cut off on short displays)** | Add `verticalScroll` + `Spacer(Modifier.height(80.dp))` |
| `DroneOpsScreen.kt` | `LazyColumn` | None | Medium | Add `item { Spacer(Modifier.height(80.dp)) }` |
| `FarmMapScreen.kt` | `Box / Column` | None | Medium | Add `padding(bottom = 80.dp)` to bottom stats panel |
| `FieldNavigationScreen.kt` | `Box / Column` | None | Medium | Add `Spacer(Modifier.height(24.dp))` and nav insets |
| `DevicePairingScreen.kt` | `Column` | None (no scroll) | Low/Medium | Add `verticalScroll` |
| `AgentsScreen.kt` | `LazyColumn` | None | Medium | Add `item { Spacer(Modifier.height(80.dp)) }` |
| `FoodSecurityScreen.kt` | `LazyColumn` | None | Medium | Add `item { Spacer(Modifier.height(80.dp)) }` |
| `KnowledgeScreen.kt` | `LazyColumn` in `Column` | None + Unbounded error | **HIGH (unbounded constraint exception)** | Add `Modifier.weight(1f)` + `Spacer(Modifier.height(80.dp))` |
| `RegionalIntelligenceScreen.kt` | `LazyColumn` | None | Medium | Add `item { Spacer(Modifier.height(80.dp)) }` |
| `ScientificValidationScreen.kt` | `LazyColumn` | None | Medium | Add `item { Spacer(Modifier.height(80.dp)) }` |

---

## 5. Text Overflow & Row Child Weight Audit Table

| Component / Screen | Exact Lines | Defect Description | Fix Strategy |
|---|---|---|---|
| `MarketScreen.kt` (`MandiRecordCard`) | Lines 358–371 | Left nested `Row` lacks `weight(1f)`; long market name pushes price off-screen | Wrap left content with `Modifier.weight(1f)` on parent Row; add text ellipsis |
| `PeerChatScreen.kt` (Header) | Lines 154–175 | Left header `Row` lacks `weight(1f)`; long name/status pushes call button off-screen | Add `Modifier.weight(1f)` to left `Row`; apply `maxLines = 1` |
| `ProfileScreen.kt` (`SettingsItem`) | Lines 429–448 | Inner `Row` lacks `weight(1f)`; long subtitle pushes Chevron icon off card | Add `Modifier.weight(1f)` to inner `Row`; remove internal 8dp spacer |
| `ProfileScreen.kt` (`FarmListItem`) | Lines 379–409 | Inner `Row` lacks `weight(1f)`; long farm title pushes Active badge off card | Add `Modifier.weight(1f)` to inner `Row`; apply text ellipsis |
| `FarmKhataScreen.kt` (Entry Card) | Lines 205–231 | Left `Row` lacks `weight(1f)`; long title pushes `+₹...` amount off-screen | Add `Modifier.weight(1f)` to left `Row`; apply text ellipsis |
| `EquipmentRentalScreen.kt` (`EquipmentCard`) | Lines 290–319 | Left `Row` lacks `weight(1f)`; long vehicle name pushes AVAILABLE badge off-screen | Add `Modifier.weight(1f)` to left `Row`; apply text ellipsis |
| `SavedReportsScreen.kt` (`ReportCard`) | Lines 205–230 | Column lacks `weight(1f)`; long file name causes unconstrained wrapping | Add `Modifier.weight(1f)` to text Column; add ellipsis |
| `FieldNavigationScreen.kt` (`MetricCard`) | Lines 104–108, 137 | Fixed `width(100.dp)` x 3 exceeds narrow screen width (<360dp) | Change `MetricCard` modifier to `Modifier.weight(1f)` |
| `DiseaseScannerScreen.kt` (`BuyCard`) | Lines 684–720 | `Row` for store links overflows when multiple stores returned | Wrap store badges with `horizontalScroll` or `FlowRow` |
| `ChatScreen.kt` (Action Buttons) | Lines 191–216 | 48dp x 56dp with `CircleShape` creates distorted oval | Standardize to `Modifier.size(48.dp)` with `CircleShape` |
| `LoginScreen.kt` (`NuKropTextField`) | Lines 370–400 | Icon in placeholder disappears on text input | Move icon to `leadingIcon = { Text(icon, fontSize = 18.sp) }` |

---

## 6. Implementation Readiness & Handoff Recommendations

All findings have been fully documented with exact line numbers and concrete replacement code. The codebase is structurally ready for the implementing agent to apply these non-breaking surgical improvements.
