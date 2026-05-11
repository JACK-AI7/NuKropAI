import { Ionicons } from "@expo/vector-icons";
import { router } from "expo-router";
import React, { useEffect, useState } from "react";
import {
  ActivityIndicator,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useColors } from "@/hooks/useColors";
import { useAuth } from "@/contexts/AuthContext";
import { GlassCard } from "@/components/GlassCard";
import { fetchPlatformMetrics, type PlatformMetrics } from "@/utils/admin";

export default function AdminScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const { isAdmin } = useAuth();
  const [metrics, setMetrics] = useState<PlatformMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAdmin) {
      router.replace("/(tabs)");
      return;
    }
    fetchPlatformMetrics().then((m) => {
      setMetrics(m);
      setLoading(false);
    });
  }, [isAdmin]);

  if (loading) {
    return (
      <View style={[styles.container, { backgroundColor: colors.background, justifyContent: "center" }]}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <View style={[styles.header, { paddingTop: insets.top + 10 }]}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="chevron-back" size={24} color={colors.foreground} />
        </TouchableOpacity>
        <Text style={[styles.title, { color: colors.foreground }]}>Platform Admin</Text>
      </View>

      <ScrollView contentContainerStyle={styles.scroll}>
        <View style={styles.metricsRow}>
          <GlassCard style={styles.metricCard}>
            <Text style={[styles.metricVal, { color: colors.primary }]}>{metrics?.totalScans}</Text>
            <Text style={[styles.metricLbl, { color: colors.mutedForeground }]}>Total Scans</Text>
          </GlassCard>
          <GlassCard style={styles.metricCard}>
            <Text style={[styles.metricVal, { color: colors.accent }]}>{metrics?.activeUsers}</Text>
            <Text style={[styles.metricLbl, { color: colors.mutedForeground }]}>Active Users</Text>
          </GlassCard>
        </View>

        <Text style={[styles.sectionTitle, { color: colors.foreground }]}>Top Disease Outbreaks</Text>
        <GlassCard padding={0}>
          {metrics?.topDiseases.map((d, i) => (
            <View 
              key={i} 
              style={[
                styles.diseaseRow, 
                { borderBottomWidth: i < metrics.topDiseases.length - 1 ? 1 : 0, borderBottomColor: colors.border }
              ]}
            >
              <Text style={[styles.diseaseName, { color: colors.foreground }]}>{d.name}</Text>
              <View style={[styles.countBadge, { backgroundColor: colors.primary + "18" }]}>
                <Text style={[styles.countText, { color: colors.primary }]}>{d.count} reports</Text>
              </View>
            </View>
          ))}
        </GlassCard>

        <Text style={[styles.sectionTitle, { color: colors.foreground, marginTop: 24 }]}>System Status</Text>
        <GlassCard>
          <View style={styles.statusRow}>
            <View style={[styles.statusDot, { backgroundColor: "#22C55E" }]} />
            <Text style={[styles.statusText, { color: colors.foreground }]}>AI Inference API: Online</Text>
          </View>
          <View style={styles.statusRow}>
            <View style={[styles.statusDot, { backgroundColor: "#22C55E" }]} />
            <Text style={[styles.statusText, { color: colors.foreground }]}>Firestore Realtime: Healthy</Text>
          </View>
          <View style={styles.statusRow}>
            <View style={[styles.statusDot, { backgroundColor: "#22C55E" }]} />
            <Text style={[styles.statusText, { color: colors.foreground }]}>Push Notification Node: Active</Text>
          </View>
        </GlassCard>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  header: { flexDirection: "row", alignItems: "center", paddingHorizontal: 16, paddingBottom: 16, gap: 12 },
  backBtn: { width: 40, height: 40, justifyContent: "center" },
  title: { fontSize: 20, fontWeight: "700", fontFamily: "Inter_700Bold" },
  scroll: { padding: 16, paddingBottom: 40 },
  metricsRow: { flexDirection: "row", gap: 12, marginBottom: 24 },
  metricCard: { flex: 1, alignItems: "center", gap: 4 },
  metricVal: { fontSize: 24, fontWeight: "800", fontFamily: "Inter_800ExtraBold" },
  metricLbl: { fontSize: 12, fontFamily: "Inter_500Medium" },
  sectionTitle: { fontSize: 16, fontWeight: "600", fontFamily: "Inter_600SemiBold", marginBottom: 12 },
  diseaseRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", padding: 16 },
  diseaseName: { fontSize: 14, fontFamily: "Inter_500Medium", flex: 1 },
  countBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  countText: { fontSize: 11, fontWeight: "700", fontFamily: "Inter_700Bold" },
  statusRow: { flexDirection: "row", alignItems: "center", gap: 10, marginBottom: 12 },
  statusDot: { width: 8, height: 8, borderRadius: 4 },
  statusText: { fontSize: 14, fontFamily: "Inter_400Regular" },
});
