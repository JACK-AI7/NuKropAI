import re

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\app\src\main\java\com\example\MarketScreen.kt", "r", encoding="utf-8") as f:
    content = f.read()

# Replace 🔥
content = content.replace('Text("🔥", fontSize = 14.sp)', 'Icon(Icons.Filled.LocalFireDepartment, contentDescription = null, tint = NuKropWarning, modifier = Modifier.size(14.dp))')

# Quick crop suggestions
content = content.replace('// Quick crop suggestions (REMOVED EMOJIS FOR GLYPH FIX)', '// Quick crop suggestions (Emoji Glyph Fixed using Material Icons)')

# Error box
content = content.replace('Text("⚠️ $it", color = NuKropError, fontSize = 13.sp)', 'Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) { Icon(Icons.Filled.Warning, contentDescription=null, tint=NuKropError, modifier=Modifier.size(14.dp)); Text(it, color = NuKropError, fontSize = 13.sp) }')

# Blockchain Button
content = content.replace('Text(\n                        if (isSold) "✅ Blockchain Contract Signed" else "🔗 Sell Direct (Blockchain Contract)",', 'Text(\n                        if (isSold) "Blockchain Contract Signed" else "Sell Direct (Blockchain Contract)",')
content = content.replace('Text("🔒 FUNDS LOCKED (BigBasket Escrow)"', 'Text("FUNDS LOCKED (BigBasket Escrow)"')
content = content.replace('Text("🌀 VERIFYING DROP-OFF..."', 'Text("VERIFYING DROP-OFF..."')
content = content.replace('Text("🟢 FUNDS RELEASED TO WALLET"', 'Text("FUNDS RELEASED TO WALLET"')
content = content.replace('Text("📷 Scan Delivery Agent QR Code",', 'Text("Scan Delivery Agent QR Code",')
content = content.replace('Text("🎉 ₹85,000 credited to mobile wallet instantly!",', 'Text("₹85,000 credited to mobile wallet instantly!",')

# AI Price Predictor changes -> add Profit Predictor
content = content.replace('Text("📈 AI Price Predictor", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = NuKropText)', 'Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) { Icon(Icons.Filled.AutoGraph, contentDescription=null, tint=NuKropText, modifier=Modifier.size(18.dp)); Text("AI Crop Profit Predictor", fontSize = 15.sp, fontWeight = FontWeight.Bold, color = NuKropText) }')
content = content.replace('Text("Current Trend: Bullish ↗️", fontSize = 11.sp, color = NuKropAccent, fontWeight = FontWeight.Bold)', 'Text("Current Trend: Bullish", fontSize = 11.sp, color = NuKropAccent, fontWeight = FontWeight.Bold)')
content = content.replace('Text("Forecast Crash: June 15 📉", fontSize = 11.sp, color = NuKropWarning, fontWeight = FontWeight.Bold)', 'Text("Forecast Crash: June 15", fontSize = 11.sp, color = NuKropWarning, fontWeight = FontWeight.Bold)')

# Scam warning injection
scam_warning_code = """
                // Scam Detector Warning
                if (record.modalPrice < record.maxPrice * 0.75) {
                    Spacer(Modifier.height(8.dp))
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(NuKropError.copy(alpha = 0.1f))
                            .border(1.dp, NuKropError.copy(alpha = 0.4f), RoundedCornerShape(12.dp))
                            .padding(12.dp)
                    ) {
                        Row(verticalAlignment = Alignment.Top, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            Icon(Icons.Filled.Warning, contentDescription = null, tint = NuKropError, modifier = Modifier.size(18.dp))
                            Column {
                                Text("Real-Time Scam Alert", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = NuKropError)
                                Text("This mandi's price is suspiciously low compared to the regional maximum. AI detects potential cartel pricing.", fontSize = 11.sp, color = NuKropTextMuted, lineHeight = 16.sp)
                            }
                        }
                    }
                }
"""
content = content.replace('Text("${AppStrings.get("variety", lang)} ${record.variety}", fontSize = 12.sp, color = NuKropText)', 'Text("${AppStrings.get("variety", lang)} ${record.variety}", fontSize = 12.sp, color = NuKropText)' + scam_warning_code)

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\app\src\main\java\com\example\MarketScreen.kt", "w", encoding="utf-8") as f:
    f.write(content)
