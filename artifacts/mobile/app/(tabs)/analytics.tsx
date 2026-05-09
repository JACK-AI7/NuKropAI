import { Ionicons } from "@expo/vector-icons";
import React, { useEffect } from "react";
import { Platform, ScrollView, StyleSheet, Text, View } from "react-native";
import Animated, {
  Easing,
  useAnimatedStyle,
  useSharedValue,
  withDelay,
  withTiming,
} from "react-native-reanimated";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useColors } from "@/hooks/useColors";
import { useApp } from "@/contexts/AppContext";
import { GlassCard } from "@/components/GlassCard";

const DISEASES = [
  { name: "Early Blight", pct: 40, color: "#FF453A" },
  { name: "Leaf Blight", pct: 25, color: "#F59E0B" },
  { name: "Powdery Mildew", pct: 20, color: "#8B5CF6" },
  { name: "Other", pct: 15, color: "#22C55E" },
];

const WEEKLY = [
  { day: "Mon", scans: 3, diseases: 1 },
  { day: "Tue", scans: 5, diseases: 2 },
  { day: "Wed", scans: 2, diseases: 0 },
  { day: "Thu", scans: 7, diseases: 3 },
  { day: "Fri", scans: 4, diseases: 1 },
  { day: "Sat", scans: 6, diseases: 2 },
  { day: "Sun", scans: 3, diseases: 1 },
];

function AnimBar({ pct, color, delay }: { pct: number; color: string; delay: number }) {
  const width = useSharedValue(0);
  useEffect(() => {
    width.value = withDelay(
      delay,
      withTiming(pct, { duration: 800, easing: Easing.out(Easing.cubic) })
    );
  }, [delay, pct, width]);
  const s = useAnimatedStyle(() => ({ width: `${width.value}%` as unknown as number }));
  return <Animated.View style={[{ height: 7, borderRadius: 4, backgroundColor: color }, s]} />;
}

function ColBar({
  value,
  max,
  color,
  delay,
}: {
  value: number;
  max: number;
  color: string;
  delay: number;
}) {
  const h = useSharedValue(0);
  useEffect(() => {
    h.value = withDelay(
      delay,
      withTiming((value / max) * 72, { duration: 600, easing: Easing.out(Easing.cubic) })
    );
  }, [delay, h, max, value]);
  const s = useAnimatedStyle(() => ({ height: h.value }));
  return <Animated.View style={[{ width: 10, borderRadius: 3, backgroundColor: color }, s]} />;
}

export default function AnalyticsScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const { scanHistory } = useApp();
  const topPad = Platform.OS === "web" ? 67 : insets.top + 10;
  const maxScans = Math.max(...WEEKLY.map((d) => d.scans));

  const KEY_STATS = [
    { icon: "scan", label: "Total Scans", value: String(20 + scanHistory.length), color: colors.primary },
    { icon: "warning", label: "Diseases Found", value: "12", color: "#FF453A" },
    { icon: "checkmark-circle", label: "Healthy Crops", value: "85%", color: colors.accent },
    { icon: "trending-up", label: "Improvement", value: "+12%", color: "#F59E0B" },
  ];

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <ScrollView
        contentContainerStyle={[
          styles.scroll,
          { paddingTop: topPad, paddingBottom: Platform.OS === "web" ? 100 : 110 },
        ]}
        showsVerticalScrollIndicator={false}
      >
        <Text style={[styles.title, { color: colors.foreground }]}>Analytics</Text>
        <Text style={[styles.subtitle, { color: colors.mutedForeground }]}>
          AI-powered crop health insights
        </Text>

        <View style={styles.statsGrid}>
          {KEY_STATS.map((stat, i) => (
            <GlassCard key={i} style={styles.statCell} padding={14}>
              <Ionicons name={stat.icon as never} size={22} color={stat.color} />
              <Text style={[styles.statVal, { color: colors.foreground }]}>{stat.value}</Text>
              <Text style={[styles.statLbl, { color: colors.mutedForeground }]}>{stat.label}</Text>
            </GlassCard>
          ))}
        </View>

        <GlassCard style={styles.card}>
          <Text style={[styles.cardTitle, { color: colors.foreground }]}>Disease Breakdown</Text>
          {DISEASES.map((d, i) => (
            <View key={i} style={styles.breakRow}>
              <View style={styles.breakLabel}>
                <View style={[styles.dot, { backgroundColor: d.color }]} />
                <Text style={[styles.breakName, { color: colors.foreground }]}>{d.name}</Text>
              </View>
              <View style={styles.breakBarArea}>
                <View style={[styles.barBg, { backgroundColor: colors.border }]}>
                  <AnimBar pct={d.pct} color={d.color} delay={i * 160} />
                </View>
                <Text style={[styles.breakPct, { color: colors.mutedForeground }]}>{d.pct}%</Text>
              </View>
            </View>
          ))}
        </GlassCard>

        <GlassCard style={styles.card}>
          <Text style={[styles.cardTitle, { color: colors.foreground }]}>Weekly Scans</Text>
          <View style={styles.legend}>
            <View style={styles.legendItem}>
              <View style={[styles.dot, { backgroundColor: colors.primary }]} />
              <Text style={[styles.legendTxt, { color: colors.mutedForeground }]}>Scans</Text>
            </View>
            <View style={styles.legendItem}>
              <View style={[styles.dot, { backgroundColor: "#FF453A" }]} />
              <Text style={[styles.legendTxt, { color: colors.mutedForeground }]}>Diseases</Text>
            </View>
          </View>
          <View style={styles.chart}>
            {WEEKLY.map((d, i) => (
              <View key={i} style={styles.chartCol}>
                <View style={styles.barGroup}>
                  <ColBar value={d.scans} max={maxScans} color={colors.primary} delay={i * 90} />
                  <ColBar value={d.diseases} max={maxScans} color="#FF453A" delay={i * 90 + 45} />
                </View>
                <Text style={[styles.dayLbl, { color: colors.mutedForeground }]}>{d.day}</Text>
              </View>
            ))}
          </View>
        </GlassCard>

        <GlassCard style={styles.card}>
          <View style={styles.recRow}>
            <Ionicons name="sparkles" size={18} color={colors.accent} />
            <Text style={[styles.cardTitle, { color: colors.foreground }]}>AI Recommendation</Text>
          </View>
          <Text style={[styles.recText, { color: colors.mutedForeground }]}>
            Based on this week's data, early blight is the most common threat. Consider preventive
            copper fungicide application before the upcoming rain. Crop health improved +3% vs last
            week.
          </Text>
        </GlassCard>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  scroll: { paddingHorizontal: 16 },
  title: { fontSize: 24, fontWeight: "700", fontFamily: "Inter_700Bold", letterSpacing: -0.5 },
  subtitle: { fontSize: 13, fontFamily: "Inter_400Regular", marginBottom: 22, marginTop: 4 },
  statsGrid: { flexDirection: "row", flexWrap: "wrap", gap: 10, marginBottom: 16 },
  statCell: { width: "47%", alignItems: "center", gap: 5 },
  statVal: { fontSize: 22, fontWeight: "700", fontFamily: "Inter_700Bold" },
  statLbl: { fontSize: 11, fontFamily: "Inter_400Regular", textAlign: "center" },
  card: { marginBottom: 16 },
  cardTitle: { fontSize: 15, fontWeight: "600", fontFamily: "Inter_600SemiBold", marginBottom: 14 },
  breakRow: { marginBottom: 12 },
  breakLabel: { flexDirection: "row", alignItems: "center", gap: 8, marginBottom: 6 },
  dot: { width: 8, height: 8, borderRadius: 4 },
  breakName: { fontSize: 13, fontFamily: "Inter_400Regular" },
  breakBarArea: { flexDirection: "row", alignItems: "center", gap: 8 },
  barBg: { flex: 1, height: 7, borderRadius: 4, overflow: "hidden" },
  breakPct: { fontSize: 12, fontFamily: "Inter_500Medium", width: 32, textAlign: "right" },
  legend: { flexDirection: "row", gap: 16, marginBottom: 14 },
  legendItem: { flexDirection: "row", alignItems: "center", gap: 6 },
  legendTxt: { fontSize: 12, fontFamily: "Inter_400Regular" },
  chart: { flexDirection: "row", justifyContent: "space-between" },
  chartCol: { alignItems: "center", gap: 6 },
  barGroup: { flexDirection: "row", gap: 3, alignItems: "flex-end", height: 72 },
  dayLbl: { fontSize: 10, fontFamily: "Inter_400Regular" },
  recRow: { flexDirection: "row", alignItems: "center", gap: 8, marginBottom: 10 },
  recText: { fontSize: 13, fontFamily: "Inter_400Regular", lineHeight: 20 },
});
