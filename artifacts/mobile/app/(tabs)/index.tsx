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
import { WeatherCard } from "@/components/WeatherCard";
import { AIInsightCard } from "@/components/AIInsightCard";
import { PulseIndicator } from "@/components/PulseIndicator";
import { StatCard } from "@/components/StatCard";

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
  const translateY = useSharedValue(16);

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
  const glow = useSharedValue(0.4);

  useEffect(() => {
    glow.value = withRepeat(
      withSequence(
        withTiming(0.9, { duration: 2000 }),
        withTiming(0.4, { duration: 2000 })
      ),
      -1,
      false
    );
  }, [glow]);

  const glowStyle = useAnimatedStyle(() => ({
    shadowColor: glowColor,
    shadowOpacity: glow.value,
    shadowRadius: 12,
    shadowOffset: { width: 0, height: 4 },
    elevation: 8,
  }));

  return (
    <Animated.View style={[glowStyle, style]}>
      <TouchableOpacity onPress={onPress} activeOpacity={0.85} style={{ flex: 1 }}>
        {children}
      </TouchableOpacity>
    </Animated.View>
  );
}

export default function HomeScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const { farmerName, insights, scanHistory } = useApp();
  const topPad = Platform.OS === "web" ? 67 : insets.top + 10;
  const todayScans = scanHistory.filter(
    (s) => Date.now() - s.timestamp < 86400000
  ).length;

  const headerOpacity = useSharedValue(0);
  const headerY = useSharedValue(-10);

  useEffect(() => {
    headerOpacity.value = withTiming(1, { duration: 600 });
    headerY.value = withSpring(0, { damping: 18 });
  }, [headerOpacity, headerY]);

  const headerStyle = useAnimatedStyle(() => ({
    opacity: headerOpacity.value,
    transform: [{ translateY: headerY.value }],
  }));

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <ScrollView
        style={{ flex: 1 }}
        contentContainerStyle={[
          styles.scroll,
          { paddingTop: topPad, paddingBottom: Platform.OS === "web" ? 100 : 110 },
        ]}
        showsVerticalScrollIndicator={false}
      >
        <Animated.View style={[styles.header, headerStyle]}>
          <View>
            <Text style={[styles.greeting, { color: colors.mutedForeground }]}>
              {greeting()}
            </Text>
            <Text style={[styles.name, { color: colors.foreground }]}>{farmerName}</Text>
          </View>
          <View style={styles.headerRight}>
            <View style={styles.aiRow}>
              <PulseIndicator size={6} />
              <Text style={[styles.aiLabel, { color: colors.accent }]}>AI Active</Text>
            </View>
            <View
              style={[styles.bell, { backgroundColor: colors.card, borderColor: colors.border }]}
            >
              <Ionicons name="notifications-outline" size={21} color={colors.foreground} />
              <View style={[styles.notifBadge, { backgroundColor: colors.destructive }]} />
            </View>
          </View>
        </Animated.View>

        <EntranceCard delay={80} style={styles.statsRow}>
          <View style={styles.statsInner}>
            <StatCard label="Scans Today" value={String(todayScans)} icon="scan" />
            <StatCard
              label="Health Score"
              value="78%"
              icon="leaf"
              color={colors.accent}
              subtitle="+3% week"
            />
            <StatCard
              label="AI Alerts"
              value={String(insights.length)}
              icon="warning"
              color="#F59E0B"
            />
          </View>
        </EntranceCard>

        <EntranceCard delay={160}>
          <Text style={[styles.sectionTitle, { color: colors.foreground }]}>
            Weather Intelligence
          </Text>
          <WeatherCard />
        </EntranceCard>

        <EntranceCard delay={240}>
          <Text style={[styles.sectionTitle, { color: colors.foreground }]}>Quick Actions</Text>
          <View style={styles.actionsRow}>
            <GlowButton
              onPress={() => router.push("/(tabs)/scanner")}
              glowColor="#22C55E"
              style={[styles.actionBtn, { borderRadius: colors.radius }]}
            >
              <LinearGradient
                colors={["#22C55E", "#15803D"]}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={[styles.actionInner, { borderRadius: colors.radius }]}
              >
                <Ionicons name="scan" size={30} color="#000" />
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
              <View style={[styles.actionInner, { borderRadius: colors.radius }]}>
                <Ionicons name="chatbubble-ellipses" size={30} color={colors.primary} />
                <Text style={[styles.actionTitle, { color: colors.foreground }]}>Ask AI</Text>
                <Text style={[styles.actionSub, { color: colors.mutedForeground }]}>
                  Farming Assistant
                </Text>
              </View>
            </TouchableOpacity>
          </View>
        </EntranceCard>

        <EntranceCard delay={320}>
          <Text style={[styles.sectionTitle, { color: colors.foreground }]}>AI Insights</Text>
          {insights.map((insight) => (
            <AIInsightCard key={insight.id} insight={insight} />
          ))}
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
  headerRight: { flexDirection: "row", alignItems: "center", gap: 12 },
  aiRow: { flexDirection: "row", alignItems: "center", gap: 6 },
  aiLabel: { fontSize: 12, fontFamily: "Inter_500Medium" },
  bell: {
    width: 40, height: 40, borderRadius: 20,
    justifyContent: "center", alignItems: "center", borderWidth: 1,
  },
  notifBadge: {
    position: "absolute", top: 9, right: 9,
    width: 7, height: 7, borderRadius: 3.5,
  },
  statsRow: { marginBottom: 24 },
  statsInner: { flexDirection: "row", gap: 10 },
  sectionTitle: {
    fontSize: 16, fontWeight: "600", fontFamily: "Inter_600SemiBold",
    marginBottom: 12, marginTop: 4,
  },
  actionsRow: { flexDirection: "row", gap: 12, marginBottom: 26 },
  actionBtn: { flex: 1, overflow: "hidden" },
  actionInner: { padding: 20, gap: 6 },
  actionTitle: {
    fontSize: 16, fontWeight: "700", fontFamily: "Inter_700Bold",
    color: "#000", marginTop: 4,
  },
  actionSub: {
    fontSize: 12, fontFamily: "Inter_400Regular", color: "#00000066",
  },
});
