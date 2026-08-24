## 2026-08-24T16:33:27Z

You are the UI Alignment & Polish Worker (teamwork_preview_worker) for NuKropAI Android App.

Working directory: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_m1_ui
Workspace root: c:\Users\bjasw\Downloads\agriculture-ai-os

Mandatory input files to read first:
- c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\ORIGINAL_REQUEST.md
- c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\PROJECT.md
- c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_explorer_survey_ui\survey_ui_report.md

Your Assigned Scope (Milestone M1: UI Alignment & Polish):
You have exclusive write ownership of Jetpack Compose UI files:
- app/src/main/java/com/example/MainActivity.kt
- app/src/main/java/com/example/HomeScreen.kt
- app/src/main/java/com/example/MarketScreen.kt
- app/src/main/java/com/example/DiseaseScannerScreen.kt
- app/src/main/java/com/example/LoanScreen.kt
- app/src/main/java/com/example/ChatScreen.kt
- app/src/main/java/com/example/PeerChatScreen.kt
- app/src/main/java/com/example/ProfileScreen.kt
- app/src/main/java/com/example/SoilScreen.kt
- app/src/main/java/com/example/LoginScreen.kt
- app/src/main/java/com/example/SplashScreen.kt
- app/src/main/java/com/example/FarmDigitalTwinScreen.kt
- app/src/main/java/com/example/FarmKhataScreen.kt
- app/src/main/java/com/example/EquipmentRentalScreen.kt
- app/src/main/java/com/example/SavedReportsScreen.kt
- app/src/main/java/com/example/TractorAutopilotScreen.kt
- app/src/main/java/com/example/DroneOpsScreen.kt
- app/src/main/java/com/example/FarmMapScreen.kt
- app/src/main/java/com/example/FieldNavigationScreen.kt
- app/src/main/java/com/example/DevicePairingScreen.kt
- app/src/main/java/com/example/AgentsScreen.kt
- app/src/main/java/com/example/FoodSecurityScreen.kt
- app/src/main/java/com/example/KnowledgeScreen.kt
- app/src/main/java/com/example/RegionalIntelligenceScreen.kt
- app/src/main/java/com/example/ScientificValidationScreen.kt

Tasks to execute:
1. Root Scaffold Insets: In MainActivity.kt, set `contentWindowInsets = WindowInsets(0.dp)` on Scaffold to eliminate double top status bar padding while preserving individual screen top bar styling.
2. Keyboard IME Insets: Add `Modifier.imePadding()` to input bars in ChatScreen.kt, PeerChatScreen.kt, and the scrollable column in LoginScreen.kt.
3. Row Child Weights & Text Ellipsis: Add `Modifier.weight(1f)` and `maxLines = 1, overflow = TextOverflow.Ellipsis` to left/inner content across MandiRecordCard in MarketScreen.kt, PeerChatScreen header, SettingsItem & FarmListItem in ProfileScreen.kt, FarmKhata transaction cards, EquipmentRental cards, SavedReports cards, and FieldNavigation metric cards.
4. Vertical Scrolling on Fixed Layouts: Add `.verticalScroll(rememberScrollState())` to ScanHub in DiseaseScannerScreen.kt, TractorAutopilotScreen.kt, SplashScreen.kt, and DevicePairingScreen.kt.
5. Nested LazyColumn Height Constraint: In KnowledgeScreen.kt, add `Modifier.weight(1f)` to the nested LazyColumn inside Column to eliminate measurement crash risks.
6. Multi-Store Tag Wrapping: In DiseaseScannerScreen.kt (BuyCard), wrap store link buttons with `Modifier.horizontalScroll(rememberScrollState())` or FlowRow so they don't clip horizontally.
7. Bottom Navigation Bar Clearance: Ensure all scrollable lists (LazyColumn, LazyVerticalGrid, scrollable Columns) have proper 80.dp bottom clearance (`item { Spacer(Modifier.height(80.dp)) }` or `contentPadding = PaddingValues(bottom = 80.dp)`) across all screens (HomeScreen, MarketScreen, DiseaseScannerScreen, LoanScreen, ProfileScreen, DroneOpsScreen, AgentsScreen, FoodSecurityScreen, RegionalIntelligenceScreen, ScientificValidationScreen, SavedReportsScreen, KnowledgeScreen, EquipmentRentalScreen, FarmKhataScreen, SoilScreen, FarmDigitalTwinScreen, etc.). Clean up excessive home screen spacing to a clean 24dp trailing spacer.
8. Button Shapes: In ChatScreen.kt, standardize camera/voice/send action buttons to `Modifier.size(48.dp)` with `CircleShape`.
9. Verify compilation by running `./gradlew compileDebugKotlin` or `./gradlew assembleDebug` via run_command. Ensure 0 build errors.
10. Write `handoff.md` and `progress.md` in your working directory and notify the parent orchestrator with send_message.
