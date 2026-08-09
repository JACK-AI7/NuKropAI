package com.example

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.Chat
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.theme.*

data class EquipmentItem(
    val id: String = java.util.UUID.randomUUID().toString(),
    val name: String,
    val category: String,
    val rate: String,
    val owner: String,
    val distance: String,
    val phone: String,
    val isAvailable: Boolean,
    val icon: String
)

@Composable
fun EquipmentRentalScreen(
    onNavigateBack: () -> Unit,
    onNavigateToPeerChat: (name: String, info: String, phone: String) -> Unit
) {
    val context = LocalContext.current
    val scrollState = rememberScrollState()
    var showAddDialog by remember { mutableStateOf(false) }

    var equipmentList by remember {
        mutableStateOf(
            listOf(
                EquipmentItem(
                    name = "Mahindra 575 DI Tractor (45 HP)",
                    category = "Tractor & Tillage",
                    rate = "₹450 / Hour",
                    owner = "Verma Farms (Rajesh Verma)",
                    distance = "3.2 km away",
                    phone = "9876543210",
                    isAvailable = true,
                    icon = "🚜"
                ),
                EquipmentItem(
                    name = "DJI Agras T40 Spraying Drone",
                    category = "Pesticide Drone Spraying",
                    rate = "₹350 / Acre",
                    owner = "AgriTech Kisan Co-op",
                    distance = "5.0 km away",
                    phone = "9812345678",
                    isAvailable = true,
                    icon = "🛸"
                ),
                EquipmentItem(
                    name = "CLAAS Crop Combine Harvester",
                    category = "Harvester",
                    rate = "₹1,200 / Hour",
                    owner = "Suresh Patel",
                    distance = "8.5 km away",
                    phone = "9765432109",
                    isAvailable = false,
                    icon = "⚙️"
                ),
                EquipmentItem(
                    name = "Solar Drip Irrigation Pump (5 HP)",
                    category = "Irrigation Pump",
                    rate = "₹150 / Day",
                    owner = "Ramesh Singh",
                    distance = "2.1 km away",
                    phone = "9988776655",
                    isAvailable = true,
                    icon = "💧"
                )
            )
        )
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Brush.verticalGradient(listOf(Color(0xFF0D1208), NuKropDark)))
    ) {
        // Header
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xCC141A0A))
                .statusBarsPadding()
                .padding(horizontal = 8.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                IconButton(onClick = onNavigateBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = NuKropText)
                }
                Spacer(Modifier.width(4.dp))
                Column {
                    Text("P2P Equipment & Drone Rental", fontSize = 16.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                    Text("Rent tractors, drones & machinery directly", fontSize = 11.sp, color = NuKropTextMuted)
                }
            }

            Button(
                onClick = { showAddDialog = true },
                colors = ButtonDefaults.buttonColors(containerColor = NuKropAccent),
                contentPadding = PaddingValues(horizontal = 10.dp, vertical = 4.dp),
                shape = RoundedCornerShape(8.dp)
            ) {
                Icon(Icons.Default.Add, null, tint = NuKropDark, modifier = Modifier.size(14.dp))
                Spacer(Modifier.width(4.dp))
                Text("List Mine", color = NuKropDark, fontSize = 11.sp, fontWeight = FontWeight.Bold)
            }
        }

        Column(
            modifier = Modifier
                .weight(1f)
                .verticalScroll(scrollState)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            // Banner
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(16.dp))
                    .background(NuKropBadgeGreen.copy(alpha = 0.12f))
                    .border(1.dp, NuKropBadgeGreen.copy(alpha = 0.3f), RoundedCornerShape(16.dp))
                    .padding(16.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text("🚜", fontSize = 32.sp)
                    Column {
                        Text("Nearby Rental Marketplace", color = NuKropBadgeGreen, fontSize = 14.sp, fontWeight = FontWeight.Bold)
                        Text("Save 60% machinery cost by renting directly from verified nearby farmers.", color = NuKropTextMuted, fontSize = 11.sp)
                    }
                }
            }

            equipmentList.forEach { item ->
                EquipmentCard(
                    item = item,
                    onChatClick = { onNavigateToPeerChat(item.owner, item.name, item.phone) },
                    onCallClick = {
                        try {
                            val intent = Intent(Intent.ACTION_DIAL, Uri.parse("tel:${item.phone}"))
                            context.startActivity(intent)
                        } catch (_: Exception) {}
                    }
                )
            }

            Spacer(Modifier.height(80.dp))
        }
    }

    if (showAddDialog) {
        var nameInput by remember { mutableStateOf("") }
        var categoryInput by remember { mutableStateOf("Tractor") }
        var rateInput by remember { mutableStateOf("") }
        var phoneInput by remember { mutableStateOf("") }
        var locationInput by remember { mutableStateOf("Pune, Maharashtra") }

        AlertDialog(
            onDismissRequest = { showAddDialog = false },
            containerColor = NuKropCard,
            title = { Text("List Vehicle / Equipment", color = NuKropText, fontWeight = FontWeight.Bold) },
            text = {
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    OutlinedTextField(
                        value = nameInput,
                        onValueChange = { nameInput = it },
                        label = { Text("Vehicle Name (e.g. Swaraj 744 FE)", color = NuKropTextMuted) },
                        colors = OutlinedTextFieldDefaults.colors(focusedTextColor = NuKropText, unfocusedTextColor = NuKropText)
                    )
                    OutlinedTextField(
                        value = rateInput,
                        onValueChange = { rateInput = it },
                        label = { Text("Rental Rate (e.g. ₹400 / Hour)", color = NuKropTextMuted) },
                        colors = OutlinedTextFieldDefaults.colors(focusedTextColor = NuKropText, unfocusedTextColor = NuKropText)
                    )
                    OutlinedTextField(
                        value = phoneInput,
                        onValueChange = { phoneInput = it },
                        label = { Text("Phone Number", color = NuKropTextMuted) },
                        colors = OutlinedTextFieldDefaults.colors(focusedTextColor = NuKropText, unfocusedTextColor = NuKropText)
                    )
                    OutlinedTextField(
                        value = locationInput,
                        onValueChange = { locationInput = it },
                        label = { Text("Location / District", color = NuKropTextMuted) },
                        colors = OutlinedTextFieldDefaults.colors(focusedTextColor = NuKropText, unfocusedTextColor = NuKropText)
                    )
                }
            },
            confirmButton = {
                Button(
                    onClick = {
                        if (nameInput.isNotBlank() && rateInput.isNotBlank()) {
                            val newItem = EquipmentItem(
                                name = nameInput.trim(),
                                category = categoryInput,
                                rate = rateInput.trim(),
                                owner = "My Listed Vehicle",
                                distance = locationInput,
                                phone = if (phoneInput.isBlank()) "9876543210" else phoneInput.trim(),
                                isAvailable = true,
                                icon = if (categoryInput.contains("Drone", ignoreCase = true)) "🛸" else "🚜"
                            )
                            equipmentList = listOf(newItem) + equipmentList
                        }
                        showAddDialog = false
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = NuKropAccent)
                ) {
                    Text("Publish Listing", color = NuKropDark, fontWeight = FontWeight.Bold)
                }
            },
            dismissButton = {
                TextButton(onClick = { showAddDialog = false }) {
                    Text("Cancel", color = NuKropTextMuted)
                }
            }
        )
    }
}

@Composable
fun EquipmentCard(item: EquipmentItem, onChatClick: () -> Unit, onCallClick: () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(NuKropCard)
            .border(1.dp, if (item.isAvailable) NuKropAccent.copy(alpha = 0.3f) else Color.Gray.copy(alpha = 0.2f), RoundedCornerShape(16.dp))
            .padding(16.dp)
    ) {
        Column {
            Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween, Alignment.Top) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    Box(
                        modifier = Modifier
                            .size(42.dp)
                            .clip(CircleShape)
                            .background(NuKropAccent.copy(alpha = 0.15f)),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(item.icon, fontSize = 22.sp)
                    }
                    Column {
                        Text(item.name, fontSize = 14.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                        Text("${item.category} • ${item.distance}", fontSize = 11.sp, color = NuKropTextMuted)
                    }
                }
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(if (item.isAvailable) NuKropBadgeGreen.copy(alpha = 0.15f) else Color.Red.copy(alpha = 0.15f))
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                ) {
                    Text(
                        if (item.isAvailable) "AVAILABLE" else "BOOKED",
                        color = if (item.isAvailable) NuKropBadgeGreen else Color.Red,
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }

            Spacer(Modifier.height(12.dp))

            Row(Modifier.fillMaxWidth(), Arrangement.SpaceBetween, Alignment.CenterVertically) {
                Text(item.rate, fontSize = 16.sp, fontWeight = FontWeight.ExtraBold, color = NuKropAccent)
                Text(item.owner, fontSize = 11.sp, color = NuKropTextMuted)
            }

            Spacer(Modifier.height(14.dp))

            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    onClick = onCallClick,
                    enabled = item.isAvailable,
                    modifier = Modifier.weight(1f).height(40.dp),
                    shape = RoundedCornerShape(10.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = NuKropAccent.copy(alpha = 0.2f))
                ) {
                    Icon(Icons.Default.Phone, null, tint = NuKropAccent, modifier = Modifier.size(14.dp))
                    Spacer(Modifier.width(6.dp))
                    Text("Call Owner", color = NuKropAccent, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                }

                Button(
                    onClick = onChatClick,
                    modifier = Modifier.weight(1f).height(40.dp),
                    shape = RoundedCornerShape(10.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = NuKropBadgeGreen.copy(alpha = 0.2f))
                ) {
                    Icon(Icons.AutoMirrored.Filled.Chat, null, tint = NuKropBadgeGreen, modifier = Modifier.size(14.dp))
                    Spacer(Modifier.width(6.dp))
                    Text("Chat / Book", color = NuKropBadgeGreen, fontSize = 11.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}
