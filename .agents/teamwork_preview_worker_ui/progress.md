# Progress — UI Alignment & Polish Worker

**Last visited:** 2026-08-24T16:22:00Z  
**Status:** In Progress

## Tasks & Checklist
- [x] Read ORIGINAL_REQUEST.md, survey_ui_report.md, and PROJECT.md
- [ ] 1. MainActivity.kt: Fix root Scaffold insets (`contentWindowInsets = WindowInsets(0.dp)`)
- [ ] 2. ChatScreen.kt, PeerChatScreen.kt, LoginScreen.kt: Add `Modifier.imePadding()` to input rows/fields & fix button shapes/leading icons
- [ ] 3. MarketScreen.kt, PeerChatScreen.kt, ProfileScreen.kt, FarmKhataScreen.kt, EquipmentRentalScreen.kt, SavedReportsScreen.kt, FieldNavigationScreen.kt: Add `Modifier.weight(1f)` and text ellipsis
- [ ] 4. DiseaseScannerScreen.kt (ScanHub), TractorAutopilotScreen.kt, SplashScreen.kt, DevicePairingScreen.kt: Add `.verticalScroll(rememberScrollState())`
- [ ] 5. KnowledgeScreen.kt: Add `Modifier.weight(1f)` to nested LazyColumn
- [ ] 6. DiseaseScannerScreen.kt (BuyCard): Wrap store buttons in horizontalScroll / FlowRow
- [ ] 7. Bottom Clearance (80.dp) across all screens (HomeScreen, MarketScreen, DiseaseScannerScreen, LoanScreen, ProfileScreen, DroneOpsScreen, AgentsScreen, FoodSecurityScreen, RegionalIntelligenceScreen, ScientificValidationScreen, SavedReportsScreen, KnowledgeScreen, EquipmentRentalScreen, FarmKhataScreen, SoilScreen, FarmDigitalTwinScreen, etc.)
- [ ] 8. Run `./gradlew compileDebugKotlin` to verify compilation
- [ ] 9. Write handoff.md and report to parent orchestrator via send_message
