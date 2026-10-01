package com.example.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
        // Base docked light dock with curved cutout silhouette
        Surface(
            modifier = Modifier
                .fillMaxWidth()
                .height(66.dp)
                .shadow(10.dp, RoundedCornerShape(32.dp), spotColor = Color(0x33000000)),
            shape = RoundedCornerShape(32.dp),
            color = Color(0xFFEBEBEB),
            tonalElevation = 4.dp
        ) {
            Row(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(horizontal = 8.dp),
                horizontalArrangement = Arrangement.SpaceAround,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Tab 1: Home
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
                        contentDescription = "Home",
                        tint = if (isHome) Color(0xFF1B5E20) else Color(0xFF666666),
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        "Home",
                        fontSize = 11.sp,
                        fontWeight = if (isHome) FontWeight.Bold else FontWeight.Medium,
                        color = if (isHome) Color(0xFF1B5E20) else Color(0xFF666666)
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
                        tint = if (isCommunity) Color(0xFF1B5E20) else Color(0xFF666666),
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        "Community",
                        fontSize = 11.sp,
                        fontWeight = if (isCommunity) FontWeight.Bold else FontWeight.Medium,
                        color = if (isCommunity) Color(0xFF1B5E20) else Color(0xFF666666)
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
                        tint = if (isMarket) Color(0xFF1B5E20) else Color(0xFF666666),
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        "Market",
                        fontSize = 11.sp,
                        fontWeight = if (isMarket) FontWeight.Bold else FontWeight.Medium,
                        color = if (isMarket) Color(0xFF1B5E20) else Color(0xFF666666)
                    )
                }

                // Tab 5: Profile
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
                        contentDescription = "Profile",
                        tint = if (isProfile) Color(0xFF1B5E20) else Color(0xFF666666),
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(Modifier.height(2.dp))
                    Text(
                        "Profile",
                        fontSize = 11.sp,
                        fontWeight = if (isProfile) FontWeight.Bold else FontWeight.Medium,
                        color = if (isProfile) Color(0xFF1B5E20) else Color(0xFF666666)
                    )
                }
            }
        }

        // Center Elevated Green FAB for Scanner matching reference image
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.offset(y = (-20).dp)
        ) {
            Box(
                modifier = Modifier
                    .size(60.dp)
                    .shadow(8.dp, CircleShape, spotColor = Color(0xFF1B5E20))
                    .clip(CircleShape)
                    .background(
                        Brush.radialGradient(
                            listOf(
                                Color(0xFF4CAF50),
                                Color(0xFF2E7D32),
                                Color(0xFF1B5E20)
                            )
                        )
                    )
                    .border(3.dp, Color(0xFFEBEBEB), CircleShape)
                    .clickable { onScannerClick() },
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    Icons.Filled.Eco,
                    contentDescription = "Scanner",
                    tint = Color.White,
                    modifier = Modifier.size(30.dp)
                )
            }
            Spacer(Modifier.height(2.dp))
            Text(
                "Scanner",
                fontSize = 10.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF555555)
            )
        }
    }
}
