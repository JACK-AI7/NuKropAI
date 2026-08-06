import re

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\app\src\main\java\com\example\SoilScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Add missing imports for Switch, etc.
if "import androidx.compose.material3.Switch" not in content:
    content = content.replace('import androidx.compose.material3.*', 'import androidx.compose.material3.*\nimport androidx.compose.material.icons.filled.WaterDrop\nimport androidx.compose.material.icons.filled.PowerSettingsNew\nimport androidx.compose.material.icons.filled.Message\nimport androidx.compose.material.icons.filled.TrendingDown')

# Add state variables
state_vars = """    var autoMotorEnabled by remember { mutableStateOf(false) }
    var motorStatus by remember { mutableStateOf(false) }
    var whatsappAlerts by remember { mutableStateOf(true) }"""

content = content.replace('var soilMoisture by remember { mutableStateOf("48%") }', 'var soilMoisture by remember { mutableStateOf("48%") }\n' + state_vars)

# Add logic for motor status
motor_logic = """
                val moistureValue = (46..50).random()
                soilMoisture = "${moistureValue}%"
                if (autoMotorEnabled) {
                    motorStatus = moistureValue < 48 // Simulating Auto ON below 48%
                }"""
content = content.replace('soilMoisture = "${(46..50).random()}%"', motor_logic)

# Build the AI Irrigation UI
ai_irrigation_ui = """
        // AI Irrigation Automation
        Spacer(modifier = Modifier.height(24.dp))
        Text(
            text = "AI Irrigation Automation",
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold,
            color = NuKropText
        )
        Spacer(modifier = Modifier.height(12.dp))

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .clip(RoundedCornerShape(20.dp))
                .background(NuKropCard)
                .border(1.5.dp, Color(0xFF64B5F6).copy(alpha = 0.3f), RoundedCornerShape(20.dp))
                .padding(16.dp)
        ) {
            Column {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Icon(Icons.Default.PowerSettingsNew, null, tint = if (motorStatus) NuKropBadgeGreen else NuKropTextMuted, modifier = Modifier.size(24.dp))
                        Column {
                            Text("Borewell Motor", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                            Text(if (motorStatus) "Status: RUNNING" else "Status: OFF", fontSize = 11.sp, color = if (motorStatus) NuKropBadgeGreen else NuKropTextMuted)
                        }
                    }
                    Switch(
                        checked = autoMotorEnabled,
                        onCheckedChange = { autoMotorEnabled = it; if (!it) motorStatus = false },
                        colors = SwitchDefaults.colors(checkedThumbColor = NuKropCard, checkedTrackColor = Color(0xFF64B5F6))
                    )
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                Row(
                    modifier = Modifier.fillMaxWidth().clip(RoundedCornerShape(12.dp)).background(NuKropSurface).padding(12.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Icon(Icons.Default.Message, null, tint = Color(0xFF25D366), modifier = Modifier.size(20.dp))
                        Column {
                            Text("WhatsApp Alerts", fontSize = 13.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                            Text("Get notified when motor runs", fontSize = 10.sp, color = NuKropTextMuted)
                        }
                    }
                    Switch(
                        checked = whatsappAlerts,
                        onCheckedChange = { whatsappAlerts = it },
                        colors = SwitchDefaults.colors(checkedThumbColor = NuKropCard, checkedTrackColor = Color(0xFF25D366))
                    )
                }

                Spacer(modifier = Modifier.height(12.dp))

                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    Box(Modifier.weight(1f).clip(RoundedCornerShape(12.dp)).background(NuKropSurface).padding(12.dp)) {
                        Column {
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                                Icon(Icons.Default.WaterDrop, null, tint = Color(0xFF64B5F6), modifier = Modifier.size(14.dp))
                                Text("Predicted Need", fontSize = 11.sp, color = NuKropTextMuted)
                            }
                            Spacer(Modifier.height(4.dp))
                            Text("450 Liters", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                            Text("Next 48 Hours", fontSize = 10.sp, color = NuKropTextDim)
                        }
                    }
                    
                    Box(Modifier.weight(1f).clip(RoundedCornerShape(12.dp)).background(NuKropSurface).padding(12.dp)) {
                        Column {
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                                Icon(Icons.Default.TrendingDown, null, tint = NuKropBadgeGreen, modifier = Modifier.size(14.dp))
                                Text("Water Saved", fontSize = 11.sp, color = NuKropTextMuted)
                            }
                            Spacer(Modifier.height(4.dp))
                            Text("22%", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = NuKropBadgeGreen)
                            Text("This Month vs Avg", fontSize = 10.sp, color = NuKropTextDim)
                        }
                    }
                }
            }
        }
"""

content = content.replace('Spacer(modifier = Modifier.height(16.dp))\n        Button(', ai_irrigation_ui + '\n        Spacer(modifier = Modifier.height(24.dp))\n        Button(')

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\app\src\main\java\com\example\SoilScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
