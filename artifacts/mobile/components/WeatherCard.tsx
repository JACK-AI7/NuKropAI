import { Ionicons } from "@expo/vector-icons";
import { LinearGradient } from "expo-linear-gradient";
import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { useColors } from "@/hooks/useColors";

const WEATHER = {
  temp: 28,
  condition: "Partly Cloudy",
  humidity: 65,
  wind: 12,
  uv: 6,
  recommendation: "Good conditions for spraying. Avoid irrigation after 3 PM.",
};

export function WeatherCard() {
  const colors = useColors();

  return (
    <LinearGradient
      colors={["#0A2D1A", "#0C3820", "#0A2D1A"]}
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
      style={[styles.container, { borderRadius: colors.radius, borderColor: colors.border }]}
    >
      <View style={styles.topRow}>
        <View>
          <Text style={[styles.temp, { color: colors.foreground }]}>{WEATHER.temp}°C</Text>
          <Text style={[styles.condition, { color: colors.mutedForeground }]}>{WEATHER.condition}</Text>
        </View>
        <Ionicons name="partly-sunny" size={52} color={colors.primary} />
      </View>

      <View style={styles.statsRow}>
        <View style={styles.stat}>
          <Ionicons name="water" size={15} color={colors.accent} />
          <Text style={[styles.statValue, { color: colors.foreground }]}>{WEATHER.humidity}%</Text>
          <Text style={[styles.statLabel, { color: colors.mutedForeground }]}>Humidity</Text>
        </View>
        <View style={[styles.divider, { backgroundColor: colors.border }]} />
        <View style={styles.stat}>
          <Ionicons name="speedometer" size={15} color={colors.accent} />
          <Text style={[styles.statValue, { color: colors.foreground }]}>{WEATHER.wind} km/h</Text>
          <Text style={[styles.statLabel, { color: colors.mutedForeground }]}>Wind</Text>
        </View>
        <View style={[styles.divider, { backgroundColor: colors.border }]} />
        <View style={styles.stat}>
          <Ionicons name="sunny" size={15} color="#F59E0B" />
          <Text style={[styles.statValue, { color: colors.foreground }]}>UV {WEATHER.uv}</Text>
          <Text style={[styles.statLabel, { color: colors.mutedForeground }]}>Index</Text>
        </View>
      </View>

      <View
        style={[
          styles.tip,
          { backgroundColor: "rgba(74,222,128,0.08)", borderColor: "rgba(74,222,128,0.2)" },
        ]}
      >
        <Ionicons name="leaf" size={13} color={colors.accent} />
        <Text style={[styles.tipText, { color: colors.accent }]} numberOfLines={2}>
          {WEATHER.recommendation}
        </Text>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    borderWidth: 1,
    marginBottom: 24,
  },
  topRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 20,
  },
  temp: {
    fontSize: 44,
    fontWeight: "700",
    fontFamily: "Inter_700Bold",
    letterSpacing: -1,
  },
  condition: {
    fontSize: 14,
    fontFamily: "Inter_400Regular",
    marginTop: 2,
  },
  statsRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 16,
  },
  stat: {
    flex: 1,
    alignItems: "center",
    gap: 4,
  },
  statValue: {
    fontSize: 14,
    fontWeight: "600",
    fontFamily: "Inter_600SemiBold",
  },
  statLabel: {
    fontSize: 11,
    fontFamily: "Inter_400Regular",
  },
  divider: {
    width: 1,
    height: 40,
    opacity: 0.4,
  },
  tip: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    padding: 10,
    borderRadius: 10,
    borderWidth: 1,
  },
  tipText: {
    fontSize: 12,
    fontFamily: "Inter_400Regular",
    flex: 1,
    lineHeight: 18,
  },
});
