package com.example.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable

private val NuKropColorScheme = darkColorScheme(
    primary = NuKropAccent,
    onPrimary = NuKropDark,
    primaryContainer = NuKropGreen,
    onPrimaryContainer = NuKropText,
    secondary = NuKropGreenLight,
    onSecondary = NuKropDark,
    secondaryContainer = NuKropCardLight,
    onSecondaryContainer = NuKropText,
    tertiary = NuKropBadgeYellow,
    onTertiary = NuKropDark,
    background = NuKropDark,
    onBackground = NuKropText,
    surface = NuKropSurface,
    onSurface = NuKropText,
    surfaceVariant = NuKropCard,
    onSurfaceVariant = NuKropTextMuted,
    error = NuKropError,
    onError = NuKropWhite,
    outline = NuKropTextDim
)

@Composable
fun MyApplicationTheme(
    darkTheme: Boolean = true,
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit,
) {
    MaterialTheme(
        colorScheme = NuKropColorScheme,
        typography = Typography,
        content = content
    )
}
