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
import { LiveWeatherCard } from "@/components/LiveWeatherCard";
import { AIInsightCard } from "@/components/AIInsightCard";
import { PulseIndicator } from "@/components/PulseIndicator";
import { StatCard } from "@/components/StatCard";
import { ParticleBackground } from "@/components/ParticleBackground";
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
  const { farmerName, insights, scanHistory, lat, lon, locationCity } = useApp();
  const topPad = Platform.OS === "web" ? 67 : insets.top + 10;

  // Initialise GPS location (updates AppContext once permission granted)
  useLocation();

  // Live data hooks
  const { weather, loading: weatherLoading, error: weatherError } = useWeather(lat, lon);
  const { alerts, loading: alertsLoading } = useAlerts(lat, lon, locationCity, weather);

  const todayScans = scanHistory.filter(
    (s) => Date.now() - s.timestamp < 86400000,
  ).length;
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
  const displayInsights: AIInsight[] =
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
        : insights;

  const alertCount = alerts.length > 0 ? alerts.length : insights.length;

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
            <View
              style={[
                styles.bell,
                {
                  backgroundColor: colors.card,
                  borderColor: colors.border,
                },
              ]}
            >
              <Ionicons
                name="notifications-outline"
                size={21}
                color={colors.foreground}
              />
              {alertCount > 0 && (
                <View
                  style={[
                    styles.notifBadge,
                    { backgroundColor: colors.destructive },
                  ]}
                />
              )}
            </View>
          </View>
        </Animated.View>

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
});
