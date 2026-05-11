import { Ionicons } from "@expo/vector-icons";
import { LinearGradient } from "expo-linear-gradient";
import { router } from "expo-router";
import React, { useEffect } from "react";
import {
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  useWindowDimensions,
} from "react-native";
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withDelay,
  withRepeat,
  withSequence,
  withSpring,
  withTiming,
} from "react-native-reanimated";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { useColors } from "@/hooks/useColors";
import { useApp } from "@/contexts/AppContext";
import { useLocation } from "@/hooks/useLocation";
import { useWeather } from "@/hooks/useWeather";
import { useAlerts } from "@/hooks/useAlerts";
import { useNotifications } from "@/hooks/useNotifications";
import { registerBackgroundFetchAsync } from "@/utils/background";
import { LiveWeatherCard } from "@/components/LiveWeatherCard";
import { AIInsightCard } from "@/components/AIInsightCard";
import { PulseIndicator } from "@/components/PulseIndicator";
import { StatCard } from "@/components/StatCard";
import { ParticleBackground } from "@/components/ParticleBackground";
import { FarmMap } from "@/components/FarmMap";
import type { AIInsight } from "@/contexts/AppContext";

function greeting(): string {
  const h = new Date().getHours();
  if (h < 12) return "Good Morning";
  if (h < 17) return "Good Afternoon";
  return "Good Evening";
}

function EntranceCard({
  children,
  delay,
  style,
}: {
  children: React.ReactNode;
  delay: number;
  style?: object;
}) {
  const opacity = useSharedValue(0);
  const translateY = useSharedValue(18);

  useEffect(() => {
    opacity.value = withDelay(delay, withTiming(1, { duration: 500 }));
    translateY.value = withDelay(delay, withSpring(0, { damping: 16 }));
  }, [delay, opacity, translateY]);

  const s = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [{ translateY: translateY.value }],
  }));

  return <Animated.View style={[s, style]}>{children}</Animated.View>;
}

function GlowButton({
  onPress,
  children,
  glowColor,
  style,
}: {
  onPress: () => void;
  children: React.ReactNode;
  glowColor: string;
  style?: object;
}) {
  const glow = useSharedValue(0.3);
  const isWeb = Platform.OS === "web";

  useEffect(() => {
    glow.value = withRepeat(
      withSequence(
        withTiming(1, { duration: 2200 }),
        withTiming(0.3, { duration: 2200 }),
      ),
      -1,
      false,
    );
  }, [glow]);

  const glowStyle = useAnimatedStyle(() => {
    if (isWeb) return {};
    return {
      shadowColor: glowColor,
      shadowOpacity: glow.value,
      shadowRadius: 14,
      shadowOffset: { width: 0, height: 4 },
      elevation: 8,
    };
  });

  return (
    <Animated.View
      style={[
        glowStyle,
        style,
        isWeb ? { boxShadow: `0 4px 14px ${glowColor}88` } : undefined,
      ]}
    >
      <TouchableOpacity onPress={onPress} activeOpacity={0.85} style={{ flex: 1 }}>
        {children}
      </TouchableOpacity>
    </Animated.View>
  );
}

function LiveStatCard({
  label,
  value,
  icon,
  color,
  subtitle,
  delay,
}: {
  label: string;
  value: string;
  icon: string;
  color?: string;
  subtitle?: string;
  delay: number;
}) {
  const scale = useSharedValue(0.88);
  const opacity = useSharedValue(0);

  useEffect(() => {
    scale.value = withDelay(delay, withSpring(1, { damping: 14 }));
    opacity.value = withDelay(delay, withTiming(1, { duration: 400 }));
  }, [delay, opacity, scale]);

  const s = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [{ scale: scale.value }],
  }));

  return (
    <Animated.View style={[{ flex: 1 }, s]}>
      <StatCard
        label={label}
        value={value}
        icon={icon as never}
        color={color}
        subtitle={subtitle}
      />
    </Animated.View>
  );
}

function AIActivityDot({ index }: { index: number }) {
  const colors = useColors();
  const opacity = useSharedValue(0.2);

  useEffect(() => {
    opacity.value = withDelay(
      index * 200,
      withRepeat(
        withSequence(
          withTiming(1, { duration: 400 }),
          withTiming(0.2, { duration: 400 }),
          withTiming(0.2, { duration: 300 }),
        ),
        -1,
        false,
      ),
    );
  }, [index, opacity]);

  const s = useAnimatedStyle(() => ({ opacity: opacity.value }));

  return (
    <Animated.View
      style={[
        {
          width: 5,
          height: 5,
          borderRadius: 2.5,
          backgroundColor: colors.accent,
        },
        s,
      ]}
    />
  );
}

export default function HomeScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const { farmerName, insights, scanHistory, farms, activeFarmId, setActiveFarmId } = useApp();
  const activeFarm = useMemo(() => farms.find(f => f.id === activeFarmId) || farms[0], [farms, activeFarmId]);
  const topPad = Platform.OS === "web" ? 67 : insets.top + 10;
  const { lat, lon, locationCity } = useMemo(() => ({
    lat: activeFarm.lat,
    lon: activeFarm.lon,
    locationCity: activeFarm.location.split(",")[0].trim()
  }), [activeFarm]);

  // Initialise GPS location
  useLocation();
  useNotifications();

  useEffect(() => {
    registerBackgroundFetchAsync().catch(console.error);
  }, []);

  // Live data hooks
  const { weather, loading: weatherLoading, error: weatherError } = useWeather(lat, lon);
  const { alerts, loading: alertsLoading } = useAlerts(lat, lon, locationCity, weather);

  const todayScans = useMemo(() => scanHistory.filter(
    (s) => Date.now() - s.timestamp < 86400000,
  ).length, [scanHistory]);
  
  const { width: winWidth, height: winHeight } = useWindowDimensions();

  const headerOpacity = useSharedValue(0);
  const headerY = useSharedValue(-12);

  useEffect(() => {
    headerOpacity.value = withTiming(1, { duration: 700 });
    headerY.value = withSpring(0, { damping: 16 });
  }, [headerOpacity, headerY]);

  const headerStyle = useAnimatedStyle(() => ({
    opacity: headerOpacity.value,
    transform: [{ translateY: headerY.value }],
  }));

  // Convert live alerts to AIInsight format for the card, with fallback to static insights
  const displayInsights: AIInsight[] = useMemo(() => 
    alerts.length > 0
      ? alerts.map((a) => ({
          id: a.id,
          type: a.type,
          title: a.title,
          message: a.message,
          timestamp: Date.now(),
          crop: a.crop ?? undefined,
        }))
      : alertsLoading
        ? []
        : insights,
    [alerts, alertsLoading, insights]
  );

  const [overlayType, setOverlayType] = useState<"none" | "ndvi" | "outbreak" | "rainfall">("none");

  const alertCount = useMemo(() => alerts.length > 0 ? alerts.length : insights.length, [alerts, insights]);

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <ParticleBackground
        color={colors.primary}
        count={14}
        width={winWidth}
        height={winHeight}
      />

      <ScrollView
        style={{ flex: 1 }}
        contentContainerStyle={[
          styles.scroll,
          {
            paddingTop: topPad,
            paddingBottom: Platform.OS === "web" ? 100 : 110,
          },
        ]}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <Animated.View style={[styles.header, headerStyle]}>
          <View>
            <Text style={[styles.greeting, { color: colors.mutedForeground }]}>
              {greeting()}
            </Text>
            <Text style={[styles.name, { color: colors.foreground }]}>
              {farmerName}
            </Text>
          </View>
          <View style={styles.headerRight}>
            <View
              style={[
                styles.aiChip,
                {
                  backgroundColor: colors.primary + "18",
                  borderColor: colors.primary + "40",
                },
              ]}
            >
              <PulseIndicator size={6} />
              <Text style={[styles.aiLabel, { color: colors.primary }]}>
                AI Active
              </Text>
              <View style={styles.aiDots}>
                {[0, 1, 2].map((i) => (
                  <AIActivityDot key={i} index={i} />
                ))}
              </View>
            </View>
          </View>
        </Animated.View>

        {/* Multi-Farm Switcher */}
        <View style={styles.farmSwitcher}>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.farmScroll}>
            {farms.map((f) => (
              <TouchableOpacity
                key={f.id}
                onPress={() => setActiveFarmId(f.id)}
                style={[
                  styles.farmChip,
                  { 
                    backgroundColor: activeFarmId === f.id ? colors.primary : colors.card,
                    borderColor: activeFarmId === f.id ? colors.primary : colors.border
                  }
                ]}
              >
                <Ionicons name="location" size={14} color={activeFarmId === f.id ? "#000" : colors.mutedForeground} />
                <Text style={[styles.farmChipText, { color: activeFarmId === f.id ? "#000" : colors.foreground }]}>
                  {f.name}
                </Text>
              </TouchableOpacity>
            ))}
            <TouchableOpacity style={[styles.farmChip, { borderStyle: "dashed", borderColor: colors.mutedForeground }]}>
              <Ionicons name="add" size={14} color={colors.mutedForeground} />
              <Text style={[styles.farmChipText, { color: colors.mutedForeground }]}>Add Farm</Text>
            </TouchableOpacity>
          </ScrollView>
        </View>

        {/* Satellite NDVI Intelligence */}
        <EntranceCard delay={120}>
          <View style={[styles.ndviCard, { backgroundColor: colors.card, borderColor: colors.border }]}>
            <View style={styles.ndviHeader}>
              <View style={styles.ndviLeft}>
                <View style={[styles.ndviIcon, { backgroundColor: "#22C55E20" }]}>
                  <Ionicons name="globe-outline" size={20} color="#22C55E" />
                </View>
                <View>
                  <Text style={[styles.ndviTitle, { color: colors.foreground }]}>Satellite Intelligence</Text>
                  <Text style={[styles.ndviSub, { color: colors.mutedForeground }]}>Vegetation Health (NDVI)</Text>
                </View>
              </View>
              <View style={[styles.ndviTrend, { backgroundColor: activeFarm.ndvi.trend === "up" ? "#22C55E20" : "#F59E0B20" }]}>
                <Ionicons name={activeFarm.ndvi.trend === "up" ? "trending-up" : "trending-down"} size={14} color={activeFarm.ndvi.trend === "up" ? "#22C55E" : "#F59E0B"} />
                <Text style={[styles.ndviTrendText, { color: activeFarm.ndvi.trend === "up" ? "#22C55E" : "#F59E0B" }]}>
                  {activeFarm.ndvi.trend === "up" ? "+4%" : "-2%"}
                </Text>
              </View>
            </View>
            <View style={styles.ndviBody}>
              <View style={styles.ndviMetric}>
                <Text style={[styles.ndviScore, { color: colors.foreground }]}>{activeFarm.ndvi.score.toFixed(2)}</Text>
                <Text style={[styles.ndviHealth, { color: "#22C55E" }]}>Excellent</Text>
              </View>
              <View style={styles.ndviVisual}>
                <View style={[styles.ndviBarBg, { backgroundColor: colors.border }]}>
                  <View style={[styles.ndviBarFill, { width: `${activeFarm.ndvi.score * 100}%`, backgroundColor: "#22C55E" }]} />
                </View>
                <View style={styles.ndviLegend}>
                  <Text style={[styles.ndviLegendText, { color: colors.mutedForeground }]}>Poor</Text>
                  <Text style={[styles.ndviLegendText, { color: colors.mutedForeground }]}>Average</Text>
                  <Text style={[styles.ndviLegendText, { color: colors.mutedForeground }]}>High</Text>
                </View>
              </View>
            </View>
          </View>
        </EntranceCard>

        {/* Stats row */}
        <View style={styles.statsRow}>
          <LiveStatCard
            label="Scans Today"
            value={String(todayScans)}
            icon="scan"
            delay={80}
          />
          <LiveStatCard
            label="Health Score"
            value="78%"
            icon="leaf"
            color={colors.accent}
            subtitle="+3% week"
            delay={160}
          />
          <LiveStatCard
            label="AI Alerts"
            value={String(alertCount)}
            icon="warning"
            color="#F59E0B"
            delay={240}
          />
        </View>

        {/* Map Intelligence */}
        <EntranceCard delay={180}>
          <Text style={[styles.sectionTitle, { color: colors.foreground }]}>
            Map Intelligence
          </Text>
          <View style={[styles.mapContainer, { backgroundColor: colors.card, borderColor: colors.border }]}>
            <FarmMap farm={activeFarm} overlayType={overlayType} />
            <View style={styles.mapControls}>
              <TouchableOpacity 
                onPress={() => setOverlayType(overlayType === "ndvi" ? "none" : "ndvi")}
                style={[styles.mapBtn, { backgroundColor: overlayType === "ndvi" ? colors.primary : colors.background }]}
              >
                <Text style={[styles.mapBtnText, { color: overlayType === "ndvi" ? "#000" : colors.mutedForeground }]}>NDVI</Text>
              </TouchableOpacity>
              <TouchableOpacity 
                onPress={() => setOverlayType(overlayType === "outbreak" ? "none" : "outbreak")}
                style={[styles.mapBtn, { backgroundColor: overlayType === "outbreak" ? "#EF4444" : colors.background }]}
              >
                <Text style={[styles.mapBtnText, { color: overlayType === "outbreak" ? "#fff" : colors.mutedForeground }]}>Outbreaks</Text>
              </TouchableOpacity>
              <TouchableOpacity 
                onPress={() => setOverlayType(overlayType === "rainfall" ? "none" : "rainfall")}
                style={[styles.mapBtn, { backgroundColor: overlayType === "rainfall" ? colors.accent : colors.background }]}
              >
                <Text style={[styles.mapBtnText, { color: overlayType === "rainfall" ? "#000" : colors.mutedForeground }]}>Rainfall</Text>
              </TouchableOpacity>
            </View>
          </View>
        </EntranceCard>

        {/* Live Weather */}
        <EntranceCard delay={200}>
          <Text style={[styles.sectionTitle, { color: colors.foreground }]}>
            Weather Intelligence
          </Text>
          <LiveWeatherCard
            weather={weather}
            loading={weatherLoading}
            error={weatherError}
            city={locationCity}
          />
        </EntranceCard>

        {/* Quick Actions */}
        <EntranceCard delay={280}>
          <Text style={[styles.sectionTitle, { color: colors.foreground }]}>
            Quick Actions
          </Text>
          <View style={styles.actionsRow}>
            <GlowButton
              onPress={() => router.push("/(tabs)/scanner")}
              glowColor="#22C55E"
              style={[styles.actionBtn, { borderRadius: colors.radius }]}
            >
              <LinearGradient
                colors={["#22C55E", "#16A34A"]}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={[styles.actionInner, { borderRadius: colors.radius }]}
              >
                <View
                  style={[
                    styles.actionIcon,
                    { backgroundColor: "rgba(0,0,0,0.15)" },
                  ]}
                >
                  <Ionicons name="scan" size={24} color="#000" />
                </View>
                <Text style={styles.actionTitle}>Scan Crop</Text>
                <Text style={styles.actionSub}>AI Disease Detection</Text>
              </LinearGradient>
            </GlowButton>

            <TouchableOpacity
              style={[
                styles.actionBtn,
                {
                  backgroundColor: colors.card,
                  borderColor: colors.border,
                  borderWidth: 1,
                  borderRadius: colors.radius,
                },
              ]}
              onPress={() => router.push("/(tabs)/chat")}
              activeOpacity={0.85}
            >
              <View
                style={[styles.actionInner, { borderRadius: colors.radius }]}
              >
                <View
                  style={[
                    styles.actionIcon,
                    { backgroundColor: colors.primary + "18" },
                  ]}
                >
                  <Ionicons
                    name="chatbubble-ellipses"
                    size={24}
                    color={colors.primary}
                  />
                </View>
                <Text style={[styles.actionTitle, { color: colors.foreground }]}>
                  Ask AI
                </Text>
                <Text
                  style={[
                    styles.actionSub,
                    { color: colors.mutedForeground },
                  ]}
                >
                  Farming Assistant
                </Text>
              </View>
            </TouchableOpacity>
          </View>
        </EntranceCard>

        {/* Recent Scans */}
        <EntranceCard delay={320}>
          <View style={styles.sectionHeader}>
            <Text style={[styles.sectionTitle, { color: colors.foreground, marginBottom: 0 }]}>
              Recent Scans
            </Text>
            {scanHistory.length > 0 && (
              <TouchableOpacity onPress={() => router.push("/(tabs)/analytics")}>
                <Text style={[styles.viewAll, { color: colors.primary }]}>View History</Text>
              </TouchableOpacity>
            )}
          </View>
          <View style={{ marginTop: 12 }}>
            {scanHistory.length === 0 ? (
              <View style={[styles.emptyScans, { backgroundColor: colors.card, borderColor: colors.border }]}>
                <Ionicons name="camera-outline" size={32} color={colors.mutedForeground} />
                <Text style={[styles.emptyText, { color: colors.mutedForeground }]}>
                  No scans yet. Start your first crop diagnosis!
                </Text>
                <TouchableOpacity 
                  style={[styles.emptyBtn, { backgroundColor: colors.primary }]}
                  onPress={() => router.push("/(tabs)/scanner")}
                >
                  <Text style={styles.emptyBtnText}>Start Scan</Text>
                </TouchableOpacity>
              </View>
            ) : (
              scanHistory.slice(0, 3).map((scan) => (
                <View 
                  key={scan.id} 
                  style={[styles.historyItem, { backgroundColor: colors.card, borderColor: colors.border }]}
                >
                  <View style={[styles.historyIcon, { backgroundColor: scan.severity === "high" ? "#EF444420" : "#22C55E20" }]}>
                    <Ionicons 
                      name={scan.severity === "high" ? "warning" : "checkmark-circle"} 
                      size={18} 
                      color={scan.severity === "high" ? "#EF4444" : "#22C55E"} 
                    />
                  </View>
                  <View style={{ flex: 1 }}>
                    <Text style={[styles.historyTitle, { color: colors.foreground }]}>{scan.disease}</Text>
                    <Text style={[styles.historySub, { color: colors.mutedForeground }]}>
                      {new Date(scan.timestamp).toLocaleDateString()} • {scan.confidence}% Confidence
                    </Text>
                  </View>
                  <Ionicons name="chevron-forward" size={16} color={colors.mutedForeground} />
                </View>
              ))
            )}
          </View>
        </EntranceCard>

        {/* AI Insights (live alerts or static fallback) */}
        <EntranceCard delay={360}>
          <View style={styles.insightsHeader}>
            <Text style={[styles.sectionTitle, { color: colors.foreground, marginBottom: 0 }]}>
              AI Insights
            </Text>
            {alerts.length > 0 && (
              <View style={styles.insightsLiveBadge}>
                <PulseIndicator size={5} />
                <Text style={[styles.insightsLiveText, { color: colors.primary }]}>
                  LIVE
                </Text>
              </View>
            )}
          </View>
          <View style={{ marginTop: 12 }}>
            {displayInsights.length === 0 && alertsLoading ? (
              <View style={styles.alertsLoading}>
                <PulseIndicator size={8} />
                <Text
                  style={[
                    styles.alertsLoadingText,
                    { color: colors.mutedForeground },
                  ]}
                >
                  Generating AI insights…
                </Text>
              </View>
            ) : (
              displayInsights.map((insight) => (
                <AIInsightCard key={insight.id} insight={insight} />
              ))
            )}
          </View>
        </EntranceCard>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  scroll: { paddingHorizontal: 16 },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: 22,
  },
  greeting: { fontSize: 13, fontFamily: "Inter_400Regular" },
  name: {
    fontSize: 22,
    fontWeight: "700",
    fontFamily: "Inter_700Bold",
    letterSpacing: -0.5,
    marginTop: 2,
  },
  headerRight: { flexDirection: "row", alignItems: "center", gap: 10 },
  aiChip: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 20,
    borderWidth: 1,
  },
  aiLabel: { fontSize: 11, fontFamily: "Inter_500Medium" },
  aiDots: { flexDirection: "row", gap: 2 },
  bell: {
    width: 38,
    height: 38,
    borderRadius: 19,
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 1,
  },
  notifBadge: {
    position: "absolute",
    top: 9,
    right: 9,
    width: 7,
    height: 7,
    borderRadius: 3.5,
  },
  statsRow: {
    flexDirection: "row",
    gap: 10,
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: "600",
    fontFamily: "Inter_600SemiBold",
    marginBottom: 12,
    marginTop: 4,
  },
  actionsRow: { flexDirection: "row", gap: 12, marginBottom: 26 },
  actionBtn: { flex: 1, overflow: "hidden" },
  actionInner: { padding: 18, gap: 6 },
  actionIcon: {
    width: 44,
    height: 44,
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 4,
  },
  actionTitle: {
    fontSize: 15,
    fontWeight: "700",
    fontFamily: "Inter_700Bold",
    color: "#000",
  },
  actionSub: {
    fontSize: 11,
    fontFamily: "Inter_400Regular",
    color: "#00000066",
  },
  insightsHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    marginTop: 4,
    marginBottom: 0,
  },
  insightsLiveBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    backgroundColor: "#22C55E18",
    paddingHorizontal: 7,
    paddingVertical: 3,
    borderRadius: 8,
  },
  insightsLiveText: { fontSize: 9, fontFamily: "Inter_700Bold", letterSpacing: 1 },
  alertsLoading: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    paddingVertical: 20,
    paddingHorizontal: 4,
  },
  alertsLoadingText: { fontSize: 13, fontFamily: "Inter_400Regular", fontStyle: "italic" },
  farmSwitcher: { marginBottom: 16, marginTop: -4 },
  farmScroll: { gap: 8 },
  farmChip: { flexDirection: "row", alignItems: "center", gap: 6, paddingHorizontal: 12, paddingVertical: 8, borderRadius: 20, borderWidth: 1 },
  farmChipText: { fontSize: 12, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  ndviCard: { padding: 16, borderRadius: 16, borderWidth: 1, marginBottom: 24 },
  ndviHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16 },
  ndviLeft: { flexDirection: "row", gap: 12, alignItems: "center" },
  ndviIcon: { width: 40, height: 40, borderRadius: 12, justifyContent: "center", alignItems: "center" },
  ndviTitle: { fontSize: 15, fontWeight: "700", fontFamily: "Inter_700Bold" },
  ndviSub: { fontSize: 11, fontFamily: "Inter_400Regular" },
  ndviTrend: { flexDirection: "row", alignItems: "center", gap: 4, paddingHorizontal: 8, paddingVertical: 4, borderRadius: 8 },
  ndviTrendText: { fontSize: 11, fontWeight: "700", fontFamily: "Inter_700Bold" },
  ndviBody: { flexDirection: "row", alignItems: "center", gap: 20 },
  ndviMetric: { alignItems: "center", gap: 2 },
  ndviScore: { fontSize: 24, fontWeight: "800", fontFamily: "Inter_800ExtraBold" },
  ndviHealth: { fontSize: 11, fontWeight: "700", fontFamily: "Inter_700Bold" },
  ndviVisual: { flex: 1, gap: 8 },
  ndviBarBg: { height: 8, borderRadius: 4, overflow: "hidden" },
  ndviBarFill: { height: "100%", borderRadius: 4 },
  ndviLegend: { flexDirection: "row", justifyContent: "space-between" },
  ndviLegendText: { fontSize: 10, fontFamily: "Inter_400Regular" },
  mapContainer: { borderRadius: 20, borderWidth: 1, padding: 10, marginBottom: 20 },
  mapControls: { flexDirection: "row", gap: 8, marginTop: 12 },
  mapBtn: { flex: 1, paddingVertical: 8, borderRadius: 10, alignItems: "center", justifyContent: "center" },
  mapBtnText: { fontSize: 11, fontWeight: "700", fontFamily: "Inter_700Bold" },
  sectionHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 12 },
  viewAll: { fontSize: 13, fontFamily: "Inter_600SemiBold" },
  emptyScans: { padding: 24, borderRadius: 16, borderWidth: 1, alignItems: "center", gap: 10 },
  emptyText: { fontSize: 13, fontFamily: "Inter_400Regular", textAlign: "center", paddingHorizontal: 20 },
  emptyBtn: { paddingHorizontal: 20, paddingVertical: 10, borderRadius: 20, marginTop: 4 },
  emptyBtnText: { fontSize: 13, fontWeight: "700", fontFamily: "Inter_700Bold", color: "#000" },
  historyItem: { flexDirection: "row", alignItems: "center", gap: 12, padding: 14, borderRadius: 14, borderWidth: 1, marginBottom: 8 },
  historyIcon: { width: 36, height: 36, borderRadius: 10, justifyContent: "center", alignItems: "center" },
  historyTitle: { fontSize: 14, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  historySub: { fontSize: 11, fontFamily: "Inter_400Regular", marginTop: 2 },
});
