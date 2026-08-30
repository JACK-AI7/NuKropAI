package com.example.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.Tab
import com.example.ui.theme.*

@Composable
fun PlantixBottomBar(
    currentTab: Tab,
    onTabSelected: (Tab) -> Unit,
    onScannerClick: () -> Unit
) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .navigationBarsPadding()
            .padding(horizontal = 16.dp, vertical = 8.dp),
        contentAlignment = Alignment.BottomCenter
    ) {
        // Base docked white card with curved cutout silhouette
        Surface(
            modifier = Modifier
                .fillMaxWidth()
                .height(68.dp)
                .shadow(12.dp, RoundedCornerShape(32.dp), spotColor = Color(0x33000000)),
            shape = RoundedCornerShape(32.dp),
            color = Color.White,
            tonalElevation = 6.dp
        ) {
            Row(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 8.dp),
                horizontalArrangement = Arrangement.SpaceAround,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Tab 1: Your crops (Home)
                val isHome = currentTab is Tab.Home
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier
                        .clip(RoundedCornerShape(16.dp))
                        .clickable { onTabSelected(Tab.Home) }
                        .padding(horizontal = 10.dp, vertical = 4.dp)
                ) {
                    Icon(
                        Icons.Filled.Home,
                        contentDescription = "Your crops",
                        tint = if (isHome) PlantixPrimary else PlantixTextMuted,
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        "Your crops",
                        fontSize = 11.sp,
                        fontWeight = if (isHome) FontWeight.Bold else FontWeight.Medium,
                        color = if (isHome) PlantixPrimary else PlantixTextMuted
                    )
                }

                // Tab 2: Community
                val isCommunity = currentTab is Tab.Community
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier
                        .clip(RoundedCornerShape(16.dp))
                        .clickable { onTabSelected(Tab.Community) }
                        .padding(horizontal = 10.dp, vertical = 4.dp)
                ) {
                    Icon(
                        Icons.Filled.PeopleAlt,
                        contentDescription = "Community",
                        tint = if (isCommunity) PlantixPrimary else PlantixTextMuted,
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        "Community",
                        fontSize = 11.sp,
                        fontWeight = if (isCommunity) FontWeight.Bold else FontWeight.Medium,
                        color = if (isCommunity) PlantixPrimary else PlantixTextMuted
                    )
                }

                // Placeholder space for center elevated FAB
                Spacer(modifier = Modifier.width(64.dp))

                // Tab 4: Market
                val isMarket = currentTab is Tab.Market
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier
                        .clip(RoundedCornerShape(16.dp))
                        .clickable { onTabSelected(Tab.Market) }
                        .padding(horizontal = 10.dp, vertical = 4.dp)
                ) {
                    Icon(
                        Icons.Filled.ShoppingCart,
                        contentDescription = "Market",
                        tint = if (isMarket) PlantixPrimary else PlantixTextMuted,
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        "Market",
                        fontSize = 11.sp,
                        fontWeight = if (isMarket) FontWeight.Bold else FontWeight.Medium,
                        color = if (isMarket) PlantixPrimary else PlantixTextMuted
                    )
                }

                // Tab 5: Profile / You
                val isProfile = currentTab is Tab.Profile
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier
                        .clip(RoundedCornerShape(16.dp))
                        .clickable { onTabSelected(Tab.Profile) }
                        .padding(horizontal = 10.dp, vertical = 4.dp)
                ) {
                    Icon(
                        Icons.Filled.Person,
                        contentDescription = "You",
                        tint = if (isProfile) PlantixPrimary else PlantixTextMuted,
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        "Profile",
                        fontSize = 11.sp,
                        fontWeight = if (isProfile) FontWeight.Bold else FontWeight.Medium,
                        color = if (isProfile) PlantixPrimary else PlantixTextMuted
                    )
                }
            }
        }

        // Center Elevated Green FAB for Scanner
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.offset(y = (-18).dp)
        ) {
            Box(
                modifier = Modifier
                    .size(62.dp)
                    .shadow(10.dp, CircleShape, spotColor = PlantixPrimary)
                    .clip(CircleShape)
                    .background(
                        Brush.radialGradient(
                            listOf(
                                PlantixPrimary,
                                PlantixPrimaryDark
                            )
                        )
                    )
                    .clickable { onScannerClick() },
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    Icons.Filled.CenterFocusStrong,
                    contentDescription = "Scanner",
                    tint = Color.White,
                    modifier = Modifier.size(32.dp)
                )
            }
            Spacer(Modifier.height(4.dp))
            Text(
                "Scanner",
                fontSize = 11.sp,
                fontWeight = FontWeight.Bold,
                color = PlantixPrimaryDark
            )
        }
    }
}
