## 2026-08-24T16:20:35Z

You are the Senior UI Alignment & Polish Specialist Worker (Worker 1) for the NuKropAI Android App audit project.
Working directory: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_ui
Target codebase: c:\Users\bjasw\Downloads\agriculture-ai-os
Original user request file: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\ORIGINAL_REQUEST.md
Survey UI report: c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_explorer_survey_ui\survey_ui_report.md
Project plan: c:\Users\bjasw\Downloads\agriculture-ai-os\PROJECT.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Instructions:
1. Read ORIGINAL_REQUEST.md and survey_ui_report.md.
2. Implement all UI fixes across the Jetpack Compose screens:
   - In MainActivity.kt: Fix root Scaffold insets by setting `contentWindowInsets = WindowInsets(0.dp)`.
   - In ChatScreen.kt, PeerChatScreen.kt, LoginScreen.kt: Add `Modifier.imePadding()` to input rows/fields.
   - In MarketScreen.kt (MandiRecordCard), PeerChatScreen.kt, ProfileScreen.kt (SettingsItem, FarmListItem), FarmKhataScreen.kt, EquipmentRentalScreen.kt (EquipmentCard), SavedReportsScreen.kt (ReportCard), FieldNavigationScreen.kt (MetricCard): Add `Modifier.weight(1f)` and text ellipsis (`maxLines = 1, overflow = TextOverflow.Ellipsis`) to prevent flexible titles from pushing trailing badges, prices, and buttons off-screen.
   - In DiseaseScannerScreen.kt (ScanHub), TractorAutopilotScreen.kt, SplashScreen.kt, DevicePairingScreen.kt: Add `.verticalScroll(rememberScrollState())` to prevent clipping on small screens.
   - In KnowledgeScreen.kt: Add `Modifier.weight(1f)` to the nested LazyColumn.
   - In DiseaseScannerScreen.kt (BuyCard): Wrap store buttons in a horizontalScroll Row or FlowRow to prevent clipping.
   - Across ALL scrollable lists (LazyColumn, LazyVerticalGrid, scrollable Column) in all screens (HomeScreen, MarketScreen, DiseaseScannerScreen, LoanScreen, ProfileScreen, DroneOpsScreen, AgentsScreen, FoodSecurityScreen, RegionalIntelligenceScreen, ScientificValidationScreen, SavedReportsScreen, KnowledgeScreen, EquipmentRentalScreen, FarmKhataScreen): Ensure bottom clearance `Spacer(Modifier.height(80.dp))` or `contentPadding = PaddingValues(bottom = 80.dp)` is in place to guarantee content is never obscured by the bottom navigation bar.
3. Run `./gradlew compileDebugKotlin` to verify that all modified screens compile cleanly without errors.
4. Write your implementation summary to c:\Users\bjasw\Downloads\agriculture-ai-os\.agents\teamwork_preview_worker_ui\handoff.md with all modified files, line numbers, and build results.
5. Use send_message to report completion to parent orchestrator.
