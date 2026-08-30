package com.example.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.example.ui.theme.*

data class CropItem(
    val name: String,
    val iconEmoji: String,
    val scientificName: String = ""
)

val AllAvailableCrops = listOf(
    CropItem("Cotton", "🌾", "Gossypium"),
    CropItem("Tobacco", "🌿", "Nicotiana tabacum"),
    CropItem("Rice / Paddy", "🌾", "Oryza sativa"),
    CropItem("Chilli", "🌶️", "Capsicum annuum"),
    CropItem("Tomato", "🍅", "Solanum lycopersicum"),
    CropItem("Wheat", "🌾", "Triticum"),
    CropItem("Almond", "🥜", "Prunus dulcis"),
    CropItem("Apple", "🍎", "Malus domestica"),
    CropItem("Apricot", "🍑", "Prunus armeniaca"),
    CropItem("Banana", "🍌", "Musa"),
    CropItem("Barley", "🌾", "Hordeum vulgare"),
    CropItem("Bean", "🫘", "Phaseolus vulgaris"),
    CropItem("Bitter Gourd", "🥒", "Momordica charantia"),
    CropItem("Black & Green Gram", "🌱", "Vigna mungo"),
    CropItem("Brinjal / Eggplant", "🍆", "Solanum melongena"),
    CropItem("Broad Bean", "🫛", "Vicia faba"),
    CropItem("Cabbage", "🥬", "Brassica oleracea"),
    CropItem("Canola / Mustard", "🌼", "Brassica napus"),
    CropItem("Carrot", "🥕", "Daucus carota"),
    CropItem("Sugarcane", "🎋", "Saccharum officinarum"),
    CropItem("Groundnut", "🥜", "Arachis hypogaea"),
    CropItem("Maize / Corn", "🌽", "Zea mays")
)

@Composable
fun CropSelectionDialog(
    selectedCrops: List<String>,
    onCropsUpdated: (List<String>) -> Unit,
    onDismiss: () -> Unit
) {
    var tempSelected by remember { mutableStateOf(selectedCrops.toSet()) }

    Dialog(onDismissRequest = onDismiss) {
        Surface(
            modifier = Modifier
                .fillMaxWidth()
                .fillMaxHeight(0.85f),
            shape = RoundedCornerShape(24.dp),
            color = Color.White
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(20.dp)
            ) {
                // Header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column {
                        Text(
                            "Select your crops",
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold,
                            color = PlantixText
                        )
                        Text(
                            "You can always change it later.",
                            fontSize = 12.sp,
                            color = PlantixTextMuted
                        )
                    }
                    IconButton(onClick = onDismiss) {
                        Icon(Icons.Default.Close, contentDescription = "Close", tint = PlantixTextMuted)
                    }
                }

                Spacer(Modifier.height(16.dp))

                // Grid of crops matching screenshot
                LazyVerticalGrid(
                    columns = GridCells.Fixed(3),
                    modifier = Modifier.weight(1f),
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(AllAvailableCrops) { crop ->
                        val isSelected = tempSelected.contains(crop.name)
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            modifier = Modifier
                                .clip(RoundedCornerShape(16.dp))
                                .clickable {
                                    tempSelected = if (isSelected) {
                                        if (tempSelected.size > 1) tempSelected - crop.name else tempSelected
                                    } else {
                                        tempSelected + crop.name
                                    }
                                }
                                .padding(6.dp)
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(72.dp)
                                    .clip(CircleShape)
                                    .background(if (isSelected) PlantixBadgeGreen else Color(0xFFF4F6F4))
                                    .border(
                                        width = if (isSelected) 2.dp else 1.dp,
                                        color = if (isSelected) PlantixPrimary else Color(0xFFE0E6DF),
                                        shape = CircleShape
                                    ),
                                contentAlignment = Alignment.Center
                            ) {
                                Text(crop.iconEmoji, fontSize = 32.sp)
                                if (isSelected) {
                                    Box(
                                        modifier = Modifier
                                            .align(Alignment.TopEnd)
                                            .size(20.dp)
                                            .clip(CircleShape)
                                            .background(PlantixPrimary),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Icon(Icons.Default.Check, contentDescription = null, tint = Color.White, modifier = Modifier.size(14.dp))
                                    }
                                }
                            }
                            Spacer(Modifier.height(6.dp))
                            Text(
                                crop.name,
                                fontSize = 12.sp,
                                fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium,
                                color = if (isSelected) PlantixPrimary else PlantixText,
                                textAlign = TextAlign.Center,
                                maxLines = 2
                            )
                        }
                    }
                }

                Spacer(Modifier.height(16.dp))

                // Bottom CTA Button
                Button(
                    onClick = {
                        onCropsUpdated(tempSelected.toList())
                        onDismiss()
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(50.dp),
                    shape = RoundedCornerShape(25.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = PlantixPrimary)
                ) {
                    Text("Done (${tempSelected.size} Selected)", color = Color.White, fontWeight = FontWeight.Bold, fontSize = 15.sp)
                }
            }
        }
    }
}
