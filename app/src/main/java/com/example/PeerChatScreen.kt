package com.example

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.filled.Phone
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

data class PeerMessage(
    val id: String,
    val text: String,
    val isFromMe: Boolean,
    val timestamp: String
)

@Composable
fun PeerChatScreen(
    recipientName: String,
    recipientInfo: String,
    recipientPhone: String = "9876543210",
    onNavigateBack: () -> Unit
) {
    val context = LocalContext.current
    var input by remember { mutableStateOf("") }
    val listState = rememberLazyListState()

    var messages by remember {
        mutableStateOf(
            listOf(
                PeerMessage("1", "Hello! Is your farming equipment available for rent this week?", true, "10:15 AM"),
                PeerMessage("2", "Yes brother, Mahindra Tractor & Drip Pump are ready in Pune.", false, "10:17 AM"),
                PeerMessage("3", "Great! What is the hourly rate and pickup location?", true, "10:20 AM")
            )
        )
    }

    LaunchedEffect(messages.size) {
        if (messages.isNotEmpty()) {
            listState.animateScrollToItem(messages.size - 1)
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Brush.verticalGradient(listOf(Color(0xFF0D1208), NuKropDark)))
    ) {
        // Header Bar
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
                Box(
                    modifier = Modifier
                        .size(40.dp)
                        .clip(CircleShape)
                        .background(NuKropAccent.copy(alpha = 0.2f)),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        recipientName.take(1).uppercase(),
                        color = NuKropAccent,
                        fontWeight = FontWeight.Bold,
                        fontSize = 18.sp
                    )
                }
                Spacer(Modifier.width(10.dp))
                Column {
                    Text(recipientName, fontSize = 16.sp, fontWeight = FontWeight.Bold, color = NuKropText)
                    Text(recipientInfo, fontSize = 11.sp, color = NuKropBadgeGreen)
                }
            }

            IconButton(onClick = {
                try {
                    val intent = Intent(Intent.ACTION_DIAL, Uri.parse("tel:$recipientPhone"))
                    context.startActivity(intent)
                } catch (_: Exception) {}
            }) {
                Icon(Icons.Default.Phone, contentDescription = "Call", tint = NuKropAccent)
            }
        }

        // Messages List
        LazyColumn(
            state = listState,
            modifier = Modifier.weight(1f),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            items(messages) { msg ->
                PeerMessageBubble(msg)
            }
        }

        // Input Bar
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xEE141A0A))
                .navigationBarsPadding()
                .padding(horizontal = 12.dp, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            OutlinedTextField(
                value = input,
                onValueChange = { input = it },
                placeholder = { Text("Type message to $recipientName...", fontSize = 13.sp, color = NuKropTextDim) },
                modifier = Modifier.weight(1f),
                shape = RoundedCornerShape(24.dp),
                colors = OutlinedTextFieldDefaults.colors(
                    focusedContainerColor = NuKropCard,
                    unfocusedContainerColor = NuKropCard,
                    focusedBorderColor = NuKropAccent,
                    unfocusedBorderColor = Color(0x30FFFFFF),
                    focusedTextColor = NuKropText,
                    unfocusedTextColor = NuKropText
                ),
                maxLines = 3
            )

            IconButton(
                onClick = {
                    if (input.isNotBlank()) {
                        val timeStr = java.text.SimpleDateFormat("hh:mm a", java.util.Locale.getDefault()).format(java.util.Date())
                        messages = messages + PeerMessage(System.currentTimeMillis().toString(), input.trim(), true, timeStr)
                        input = ""
                    }
                },
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
                    .background(if (input.isNotBlank()) NuKropAccent else Color.Gray.copy(alpha = 0.3f))
            ) {
                Icon(Icons.AutoMirrored.Filled.Send, contentDescription = "Send", tint = NuKropDark)
            }
        }
    }
}

@Composable
fun PeerMessageBubble(msg: PeerMessage) {
    Box(
        modifier = Modifier.fillMaxWidth(),
        contentAlignment = if (msg.isFromMe) Alignment.CenterEnd else Alignment.CenterStart
    ) {
        Box(
            modifier = Modifier
                .widthIn(max = 280.dp)
                .clip(
                    RoundedCornerShape(
                        topStart = 16.dp,
                        topEnd = 16.dp,
                        bottomStart = if (msg.isFromMe) 16.dp else 4.dp,
                        bottomEnd = if (msg.isFromMe) 4.dp else 16.dp
                    )
                )
                .background(if (msg.isFromMe) NuKropAccent.copy(alpha = 0.22f) else NuKropCard)
                .border(1.dp, if (msg.isFromMe) NuKropAccent.copy(alpha = 0.4f) else Color.White.copy(alpha = 0.08f), RoundedCornerShape(16.dp))
                .padding(horizontal = 14.dp, vertical = 10.dp)
        ) {
            Column {
                Text(msg.text, color = NuKropText, fontSize = 14.sp, lineHeight = 19.sp)
                Spacer(Modifier.height(4.dp))
                Text(
                    msg.timestamp,
                    color = NuKropTextMuted,
                    fontSize = 10.sp,
                    modifier = Modifier.align(Alignment.End)
                )
            }
        }
    }
}
