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

fun getLocalizedCrops(langCode: String): List<CropItem> {
    return when (langCode) {
        "hi" -> listOf(
            CropItem("कपास", "🌾", "Gossypium"),
            CropItem("तंबाकू", "🌿", "Nicotiana tabacum"),
            CropItem("चावल", "🌾", "Oryza sativa"),
            CropItem("मिर्च", "🌶️", "Capsicum annuum"),
            CropItem("टमाटर", "🍅", "Solanum lycopersicum"),
            CropItem("गेहूं", "🌾", "Triticum"),
            CropItem("बादाम", "🥜", "Prunus dulcis"),
            CropItem("सेब", "🍎", "Malus domestica"),
            CropItem("खुबानी", "🍑", "Prunus armeniaca"),
            CropItem("केला", "🍌", "Musa"),
            CropItem("जौ", "🌾", "Hordeum vulgare"),
            CropItem("सेम", "🫘", "Phaseolus vulgaris"),
            CropItem("करेला", "🥒", "Momordica charantia"),
            CropItem("दालें", "🌱", "Vigna mungo"),
            CropItem("बैंगन", "🍆", "Solanum melongena"),
            CropItem("बाकला", "🫛", "Vicia faba"),
            CropItem("पत्तागोभी", "🥬", "Brassica oleracea"),
            CropItem("सरसों", "🌼", "Brassica napus"),
            CropItem("गाजर", "🥕", "Daucus carota"),
            CropItem("गन्ना", "🎋", "Saccharum officinarum"),
            CropItem("मूंगफली", "🥜", "Arachis hypogaea"),
            CropItem("मक्का", "🌽", "Zea mays")
        )
        "te" -> listOf(
            CropItem("పత్తి", "🌾", "Gossypium"),
            CropItem("పొగాకు", "🌿", "Nicotiana tabacum"),
            CropItem("వరి", "🌾", "Oryza sativa"),
            CropItem("మిరప", "🌶️", "Capsicum annuum"),
            CropItem("టమోటా", "🍅", "Solanum lycopersicum"),
            CropItem("గోధుమ", "🌾", "Triticum"),
            CropItem("బాదం", "🥜", "Prunus dulcis"),
            CropItem("ఆపిల్", "🍎", "Malus domestica"),
            CropItem("జర్దాలు", "🍑", "Prunus armeniaca"),
            CropItem("అరటి", "🍌", "Musa"),
            CropItem("బార్లీ", "🌾", "Hordeum vulgare"),
            CropItem("చిక్కుడు", "🫘", "Phaseolus vulgaris"),
            CropItem("కాకరకాయ", "🥒", "Momordica charantia"),
            CropItem("పప్పుధాన్యాలు", "🌱", "Vigna mungo"),
            CropItem("వంకాయ", "🍆", "Solanum melongena"),
            CropItem("పెద్ద చిక్కుడు", "🫛", "Vicia faba"),
            CropItem("క్యాబేజీ", "🥬", "Brassica oleracea"),
            CropItem("ఆవాలు", "🌼", "Brassica napus"),
            CropItem("క్యారెట్", "🥕", "Daucus carota"),
            CropItem("చెరకు", "🎋", "Saccharum officinarum"),
            CropItem("వేరుశెనగ", "🥜", "Arachis hypogaea"),
            CropItem("మొక్కజొన్న", "🌽", "Zea mays")
        )
        "ta" -> listOf(
            CropItem("பருத்தி", "🌾", "Gossypium"),
            CropItem("புகையிலை", "🌿", "Nicotiana tabacum"),
            CropItem("நெல்", "🌾", "Oryza sativa"),
            CropItem("மிளகாய்", "🌶️", "Capsicum annuum"),
            CropItem("தக்காளி", "🍅", "Solanum lycopersicum"),
            CropItem("கோதுமை", "🌾", "Triticum"),
            CropItem("பாதாம்", "🥜", "Prunus dulcis"),
            CropItem("ஆப்பிள்", "🍎", "Malus domestica"),
            CropItem("சர்க்கரை பாதாமி", "🍑", "Prunus armeniaca"),
            CropItem("வாழை", "🍌", "Musa"),
            CropItem("பார்லி", "🌾", "Hordeum vulgare"),
            CropItem("பீன்ஸ்", "🫘", "Phaseolus vulgaris"),
            CropItem("பாகற்காய்", "🥒", "Momordica charantia"),
            CropItem("பருப்பு வகைகள்", "🌱", "Vigna mungo"),
            CropItem("கத்தரிக்காய்", "🍆", "Solanum melongena"),
            CropItem("அவரைக்காய்", "🫛", "Vicia faba"),
            CropItem("முட்டைக்கோஸ்", "🥬", "Brassica oleracea"),
            CropItem("கடுகு", "🌼", "Brassica napus"),
            CropItem("கேரட்", "🥕", "Daucus carota"),
            CropItem("கரும்பு", "🎋", "Saccharum officinarum"),
            CropItem("வேர்க்கடலை", "🥜", "Arachis hypogaea"),
            CropItem("மக்காச்சோளம்", "🌽", "Zea mays")
        )
        "kn" -> listOf(
            CropItem("ಹತ್ತಿ", "🌾", "Gossypium"),
            CropItem("ತಂಬಾಕು", "🌿", "Nicotiana tabacum"),
            CropItem("ಭತ್ತ", "🌾", "Oryza sativa"),
            CropItem("ಮೆಣಸಿನಕಾಯಿ", "🌶️", "Capsicum annuum"),
            CropItem("ಟೊಮೆಟೊ", "🍅", "Solanum lycopersicum"),
            CropItem("ಗೋಧಿ", "🌾", "Triticum"),
            CropItem("ಬಾದಾಮಿ", "🥜", "Prunus dulcis"),
            CropItem("ಸೇಬು", "🍎", "Malus domestica"),
            CropItem("ಜರ್ದಾಳು", "🍑", "Prunus armeniaca"),
            CropItem("ಬಾಳೆಹಣ್ಣು", "🍌", "Musa"),
            CropItem("ಬಾರ್ಲಿ", "🌾", "Hordeum vulgare"),
            CropItem("ಹುರುಳಿ", "🫘", "Phaseolus vulgaris"),
            CropItem("ಹಾಗಲಕಾಯಿ", "🥒", "Momordica charantia"),
            CropItem("ಕಾಳುಗಳು", "🌱", "Vigna mungo"),
            CropItem("ಬದನೆಕಾಯಿ", "🍆", "Solanum melongena"),
            CropItem("ದಪ್ಪ ಹುರುಳಿ", "🫛", "Vicia faba"),
            CropItem("ಎಲೆಕೋಸು", "🥬", "Brassica oleracea"),
            CropItem("ಸಾಸಿವೆ", "🌼", "Brassica napus"),
            CropItem("ಕ್ಯಾರೆಟ್", "🥕", "Daucus carota"),
            CropItem("ಕಬ್ಬು", "🎋", "Saccharum officinarum"),
            CropItem("ಕಡಲೆಕಾಯಿ", "🥜", "Arachis hypogaea"),
            CropItem("ಮೆಕ್ಕೆಜೋಳ", "🌽", "Zea mays")
        )
        "ml" -> listOf(
            CropItem("പരുത്തി", "🌾", "Gossypium"),
            CropItem("പുകയില", "🌿", "Nicotiana tabacum"),
            CropItem("നെല്ല്", "🌾", "Oryza sativa"),
            CropItem("മുളക്", "🌶️", "Capsicum annuum"),
            CropItem("തക്കാളി", "🍅", "Solanum lycopersicum"),
            CropItem("ഗോതമ്പ്", "🌾", "Triticum"),
            CropItem("ബദാം", "🥜", "Prunus dulcis"),
            CropItem("ആപ്പിൾ", "🍎", "Malus domestica"),
            CropItem("ആപ്രിക്കോട്ട്", "🍑", "Prunus armeniaca"),
            CropItem("വാഴപ്പഴം", "🍌", "Musa"),
            CropItem("ബാർലി", "🌾", "Hordeum vulgare"),
            CropItem("പയർ", "🫘", "Phaseolus vulgaris"),
            CropItem("പാവയ്ക്ക", "🥒", "Momordica charantia"),
            CropItem("പയറുവർഗ്ഗങ്ങൾ", "🌱", "Vigna mungo"),
            CropItem("വഴുതന", "🍆", "Solanum melongena"),
            CropItem("അമരപ്പയർ", "🫛", "Vicia faba"),
            CropItem("മുട്ടക്കൂസ്", "🥬", "Brassica oleracea"),
            CropItem("കടുക്", "🌼", "Brassica napus"),
            CropItem("കാരറ്റ്", "🥕", "Daucus carota"),
            CropItem("കരിമ്പ്", "🎋", "Saccharum officinarum"),
            CropItem("നിലക്കടല", "🥜", "Arachis hypogaea"),
            CropItem("ചോളം", "🌽", "Zea mays")
        )
        "mr" -> listOf(
            CropItem("कापूस", "🌾", "Gossypium"),
            CropItem("तंबाखू", "🌿", "Nicotiana tabacum"),
            CropItem("भात", "🌾", "Oryza sativa"),
            CropItem("मिरची", "🌶️", "Capsicum annuum"),
            CropItem("टोमॅटो", "🍅", "Solanum lycopersicum"),
            CropItem("गहू", "🌾", "Triticum"),
            CropItem("बदाम", "🥜", "Prunus dulcis"),
            CropItem("सफरचंद", "🍎", "Malus domestica"),
            CropItem("जर्दाळू", "🍑", "Prunus armeniaca"),
            CropItem("केळी", "🍌", "Musa"),
            CropItem("जव", "🌾", "Hordeum vulgare"),
            CropItem("घेवडा", "🫘", "Phaseolus vulgaris"),
            CropItem("कारले", "🥒", "Momordica charantia"),
            CropItem("कठोळे", "🌱", "Vigna mungo"),
            CropItem("वांगे", "🍆", "Solanum melongena"),
            CropItem("पावटा", "🫛", "Vicia faba"),
            CropItem("कोबी", "🥬", "Brassica oleracea"),
            CropItem("मोहरी", "🌼", "Brassica napus"),
            CropItem("गाजर", "🥕", "Daucus carota"),
            CropItem("ऊस", "🎋", "Saccharum officinarum"),
            CropItem("भुईमूग", "🥜", "Arachis hypogaea"),
            CropItem("मका", "🌽", "Zea mays")
        )
        "bn" -> listOf(
            CropItem("তুলা", "🌾", "Gossypium"),
            CropItem("তামাক", "🌿", "Nicotiana tabacum"),
            CropItem("ধান", "🌾", "Oryza sativa"),
            CropItem("লঙ্কা", "🌶️", "Capsicum annuum"),
            CropItem("টমেটো", "🍅", "Solanum lycopersicum"),
            CropItem("গম", "🌾", "Triticum"),
            CropItem("বাদাম", "🥜", "Prunus dulcis"),
            CropItem("আপেল", "🍎", "Malus domestica"),
            CropItem("এপ্রিকট", "🍑", "Prunus armeniaca"),
            CropItem("কলা", "🍌", "Musa"),
            CropItem("যব", "🌾", "Hordeum vulgare"),
            CropItem("শিম", "🫘", "Phaseolus vulgaris"),
            CropItem("করলা", "🥒", "Momordica charantia"),
            CropItem("ডাল", "🌱", "Vigna mungo"),
            CropItem("বেগুন", "🍆", "Solanum melongena"),
            CropItem("মটরশুঁটি", "🫛", "Vicia faba"),
            CropItem("বাঁধাকপি", "🥬", "Brassica oleracea"),
            CropItem("সরিষা", "🌼", "Brassica napus"),
            CropItem("গাজর", "🥕", "Daucus carota"),
            CropItem("আখ", "🎋", "Saccharum officinarum"),
            CropItem("চিনাবাদাম", "🥜", "Arachis hypogaea"),
            CropItem("ভুট্টা", "🌽", "Zea mays")
        )
        "gu" -> listOf(
            CropItem("કપાસ", "🌾", "Gossypium"),
            CropItem("તમાકુ", "🌿", "Nicotiana tabacum"),
            CropItem("ડાંગર", "🌾", "Oryza sativa"),
            CropItem("મરચાં", "🌶️", "Capsicum annuum"),
            CropItem("ટામેટા", "🍅", "Solanum lycopersicum"),
            CropItem("ઘઉં", "🌾", "Triticum"),
            CropItem("બદામ", "🥜", "Prunus dulcis"),
            CropItem("સફરજન", "🍎", "Malus domestica"),
            CropItem("જરદાળુ", "🍑", "Prunus armeniaca"),
            CropItem("કેળું", "🍌", "Musa"),
            CropItem("જવ", "🌾", "Hordeum vulgare"),
            CropItem("વાલ", "🫘", "Phaseolus vulgaris"),
            CropItem("કારેલા", "🥒", "Momordica charantia"),
            CropItem("કઠોળ", "🌱", "Vigna mungo"),
            CropItem("રીંગણ", "🍆", "Solanum melongena"),
            CropItem("વાલ પાપડી", "🫛", "Vicia faba"),
            CropItem("કોબીજ", "🥬", "Brassica oleracea"),
            CropItem("રાઈ", "🌼", "Brassica napus"),
            CropItem("ગાજર", "🥕", "Daucus carota"),
            CropItem("શેરડી", "🎋", "Saccharum officinarum"),
            CropItem("મગફળી", "🥜", "Arachis hypogaea"),
            CropItem("મકાઈ", "🌽", "Zea mays")
        )
        "pa" -> listOf(
            CropItem("ਕਪਾਹ", "🌾", "Gossypium"),
            CropItem("ਤੰਬਾਕੂ", "🌿", "Nicotiana tabacum"),
            CropItem("ਝੋਨਾ", "🌾", "Oryza sativa"),
            CropItem("ਮਿਰਚ", "🌶️", "Capsicum annuum"),
            CropItem("ਟਮਾਟਰ", "🍅", "Solanum lycopersicum"),
            CropItem("ਕਣਕ", "🌾", "Triticum"),
            CropItem("ਬਦਾਮ", "🥜", "Prunus dulcis"),
            CropItem("ਸੇਬ", "🍎", "Malus domestica"),
            CropItem("ਖੁਰਮਾਨੀ", "🍑", "Prunus armeniaca"),
            CropItem("ਕੇਲਾ", "🍌", "Musa"),
            CropItem("ਜੌਂ", "🌾", "Hordeum vulgare"),
            CropItem("ਫਲੀਆਂ", "🫘", "Phaseolus vulgaris"),
            CropItem("ਕਰੇਲਾ", "🥒", "Momordica charantia"),
            CropItem("ਦਾਲਾਂ", "🌱", "Vigna mungo"),
            CropItem("ਬੈਂਗਣ", "🍆", "Solanum melongena"),
            CropItem("ਬਾਕਲਾ", "🫛", "Vicia faba"),
            CropItem("ਬੰਦਗੋਭੀ", "🥬", "Brassica oleracea"),
            CropItem("ਸਰ੍ਹੋਂ", "🌼", "Brassica napus"),
            CropItem("ਗਾਜਰ", "🥕", "Daucus carota"),
            CropItem("ਗੰਨਾ", "🎋", "Saccharum officinarum"),
            CropItem("ਮੂੰਗਫਲੀ", "🥜", "Arachis hypogaea"),
            CropItem("ਮੱਕੀ", "🌽", "Zea mays")
        )
        "or" -> listOf(
            CropItem("କପା", "🌾", "Gossypium"),
            CropItem("ଧୂଆଁପତ୍ର", "🌿", "Nicotiana tabacum"),
            CropItem("ଧାନ", "🌾", "Oryza sativa"),
            CropItem("ଲଙ୍କା", "🌶️", "Capsicum annuum"),
            CropItem("ଟମାଟୋ", "🍅", "Solanum lycopersicum"),
            CropItem("ଗହମ", "🌾", "Triticum"),
            CropItem("ବାଦାମ", "🥜", "Prunus dulcis"),
            CropItem("ସେଓ", "🍎", "Malus domestica"),
            CropItem("ଜରଦାଳୁ", "🍑", "Prunus armeniaca"),
            CropItem("କଦଳୀ", "🍌", "Musa"),
            CropItem("ଯବ", "🌾", "Hordeum vulgare"),
            CropItem("ଶିମ୍ବ", "🫘", "Phaseolus vulgaris"),
            CropItem("କଲରା", "🥒", "Momordica charantia"),
            CropItem("ଡାଲି", "🌱", "Vigna mungo"),
            CropItem("ବାଇଗଣ", "🍆", "Solanum melongena"),
            CropItem("ବାକୁଳା", "🫛", "Vicia faba"),
            CropItem("ବନ୍ଧାକୋବି", "🥬", "Brassica oleracea"),
            CropItem("ଶୋରିଷ", "🌼", "Brassica napus"),
            CropItem("ଗାଜର", "🥕", "Daucus carota"),
            CropItem("ଆଖୁ", "🎋", "Saccharum officinarum"),
            CropItem("ଚିନାବାଦାମ", "🥜", "Arachis hypogaea"),
            CropItem("ମକା", "🌽", "Zea mays")
        )
        else -> AllAvailableCrops
    }
}

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
