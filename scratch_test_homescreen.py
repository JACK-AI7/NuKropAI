import re

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\app\src\main\java\com\example\HomeScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Fix header icon
content = content.replace('Text("👨‍🌾", fontSize = 22.sp)', 'Icon(Icons.Filled.Person, contentDescription = null, tint = NuKropDark, modifier = Modifier.size(24.dp))')

# Fix WeatherCard radar sync text
content = content.replace('Text("📡 Radar Sync", fontSize = 10.sp, color = NuKropAccent, fontWeight = FontWeight.Bold)', 'Row(horizontalArrangement = Arrangement.spacedBy(4.dp), verticalAlignment = Alignment.CenterVertically) { Icon(Icons.Filled.Sensors, contentDescription=null, tint=NuKropAccent, modifier=Modifier.size(12.dp)); Text("Radar Sync", fontSize = 10.sp, color = NuKropAccent, fontWeight = FontWeight.Bold) }')

# QuickActionTile calls
content = content.replace('QuickActionTile(Modifier.weight(1f), "🔬", "Scan Crop", "AI Disease & Pest Detect", NuKropAccent, onNavigateToScan)', 'QuickActionTile(Modifier.weight(1f), Icons.Filled.Science, "Scan Crop", "AI Disease & Pest Detect", NuKropAccent, onNavigateToScan)')
content = content.replace('QuickActionTile(Modifier.weight(1f), "🪨", "Scan Soil", "AI Soil Health Analysis", Color(0xFF8BC34A), onNavigateToScan)', 'QuickActionTile(Modifier.weight(1f), Icons.Filled.Landscape, "Scan Soil", "AI Soil Health Analysis", Color(0xFF8BC34A), onNavigateToScan)')
content = content.replace('QuickActionTile(Modifier.weight(1f), "📊", "Market Rates", "Live Crop Prices", Color(0xFF64B5F6), onNavigateToMarket)', 'QuickActionTile(Modifier.weight(1f), Icons.Filled.Analytics, "Market Rates", "Live Crop Prices", Color(0xFF64B5F6), onNavigateToMarket)')
content = content.replace('QuickActionTile(Modifier.weight(1f), "🤖", "AI Advisor", "Ask Farming Questions", Color(0xFFBA68C8), onNavigateToChat)', 'QuickActionTile(Modifier.weight(1f), Icons.Filled.SmartToy, "AI Advisor", "Ask Farming Questions", Color(0xFFBA68C8), onNavigateToChat)')

# Add Subsidy feature in quick actions
subsidy_feature = """
            Spacer(modifier = Modifier.height(10.dp))
            Row(
                modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                QuickActionTile(Modifier.weight(1f), Icons.Filled.AccountBalance, "Loan & Subsidy", "AI Govt Forms Assistant", Color(0xFFFFB74D)) {}
                QuickActionTile(Modifier.weight(1f), Icons.Filled.Agriculture, "Tractor AutoPilot", "GPS Row Following", Color(0xFFE57373)) {}
            }"""
content = content.replace('QuickActionTile(Modifier.weight(1f), Icons.Filled.SmartToy, "AI Advisor", "Ask Farming Questions", Color(0xFFBA68C8), onNavigateToChat)\n            }', 'QuickActionTile(Modifier.weight(1f), Icons.Filled.SmartToy, "AI Advisor", "Ask Farming Questions", Color(0xFFBA68C8), onNavigateToChat)\n            }' + subsidy_feature)

# Fix Pest Radar title and icon
content = content.replace('Text("Pest Influx Radar Network"', 'Text("Hyperlocal 5-Day Pest Prediction AI"')
content = content.replace('Text("📡", fontSize = 20.sp)', 'Icon(Icons.Filled.Radar, contentDescription = null, tint = NuKropError, modifier = Modifier.size(20.dp))')
content = content.replace('Text("$pestAlertCount Active Outbreaks Nearby",', 'Text("$pestAlertCount High-Risk Vectors Nearby",')
content = content.replace('Text("🚨 Report Outbreak in My Field", color = NuKropDark, fontWeight = FontWeight.Bold)', 'Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) { Icon(Icons.Filled.Warning, contentDescription=null, tint=NuKropDark, modifier=Modifier.size(16.dp)); Text("Report Outbreak in My Field", color = NuKropDark, fontWeight = FontWeight.Bold) }')

# Fix Tracked Crops icon
content = content.replace('Text("🔥", fontSize = 14.sp)', 'Icon(Icons.Filled.LocalFireDepartment, contentDescription = null, tint = NuKropWarning, modifier = Modifier.size(14.dp))')

# Fix Tips
content = content.replace('val tips = listOf(\n                Triple("💧"', 'val tips = listOf(\n                Triple(Icons.Filled.WaterDrop')
content = content.replace('Triple("🌱"', 'Triple(Icons.Filled.Spa')
content = content.replace('Triple("🐛"', 'Triple(Icons.Filled.BugReport')
content = content.replace('Triple("🌡️"', 'Triple(Icons.Filled.Thermostat')

# Fix WeatherStats
content = content.replace('WeatherStat("💧", "${weather.humidity.toInt()}%", "Humidity")', 'WeatherStat(Icons.Filled.WaterDrop, "${weather.humidity.toInt()}%", "Humidity")')
content = content.replace('WeatherStat("💨", "${weather.windSpeed.toInt()} km/h", "Wind")', 'WeatherStat(Icons.Filled.Air, "${weather.windSpeed.toInt()} km/h", "Wind")')
content = content.replace('WeatherStat("🌧️", "${weather.precipitation} mm", "Rain")', 'WeatherStat(Icons.Filled.Cloud, "${weather.precipitation} mm", "Rain")')

# Fix Signatures
content = content.replace('fun WeatherStat(icon: String,', 'fun WeatherStat(icon: androidx.compose.ui.graphics.vector.ImageVector,')
content = content.replace('Text(icon, fontSize = 14.sp)', 'Icon(icon, contentDescription = null, tint = NuKropAccent, modifier = Modifier.size(16.dp))')

content = content.replace('fun QuickActionTile(modifier: Modifier, icon: String,', 'fun QuickActionTile(modifier: Modifier, icon: androidx.compose.ui.graphics.vector.ImageVector,')
content = content.replace('Text(icon, fontSize = 28.sp)', 'Icon(icon, contentDescription = null, tint = accentColor, modifier = Modifier.size(28.dp))')

content = content.replace('fun TipCard(icon: String,', 'fun TipCard(icon: androidx.compose.ui.graphics.vector.ImageVector,')
content = content.replace('Text(icon, fontSize = 22.sp)', 'Box(Modifier.clip(CircleShape).background(NuKropSurface).padding(8.dp)) { Icon(icon, contentDescription = null, tint = NuKropAccent, modifier = Modifier.size(20.dp)) }')

# Fix Weather Card main emoji
content = content.replace('Text(weather.emoji, fontSize = 36.sp, modifier = Modifier.offset(y = offset.dp))', 'Icon(Icons.Filled.WbSunny, contentDescription = null, tint = Color(0xFFFFCA28), modifier = Modifier.size(40.dp).offset(y = offset.dp))')

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\app\src\main\java\com\example\HomeScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
