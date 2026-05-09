import { Ionicons } from "@expo/vector-icons";
import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { useColors } from "@/hooks/useColors";

export interface ScanResult {
  disease: string;
  confidence: number;
  severity: "low" | "medium" | "high";
  affectedArea: number;
  recommendations: string[];
  treatments: string[];
}

const SEVERITY_COLORS: Record<ScanResult["severity"], string> = {
  low: "#22C55E",
  medium: "#F59E0B",
  high: "#FF453A",
};

export function ScanResultCard({ result }: { result: ScanResult }) {
  const colors = useColors();
  const sc = SEVERITY_COLORS[result.severity];

  return (
    <View
      style={[
        styles.container,
        { backgroundColor: colors.card, borderRadius: colors.radius, borderColor: colors.border },
      ]}
    >
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <View style={[styles.badge, { backgroundColor: sc + "20", borderColor: sc + "40" }]}>
            <Text style={[styles.badgeText, { color: sc }]}>{result.severity.toUpperCase()} SEVERITY</Text>
          </View>
          <Text style={[styles.diseaseName, { color: colors.foreground }]}>{result.disease}</Text>
        </View>
        <View style={styles.confidenceBlock}>
          <Text style={[styles.confValue, { color: colors.primary }]}>{result.confidence}%</Text>
          <Text style={[styles.confLabel, { color: colors.mutedForeground }]}>match</Text>
        </View>
      </View>

      {result.affectedArea > 0 && (
        <View style={[styles.areaRow, { borderTopColor: colors.border }]}>
          <Text style={[styles.areaLabel, { color: colors.mutedForeground }]}>Affected Area</Text>
          <View style={[styles.barBg, { backgroundColor: colors.border }]}>
            <View style={[styles.barFill, { width: `${result.affectedArea}%`, backgroundColor: sc }]} />
          </View>
          <Text style={[styles.areaPct, { color: sc }]}>{result.affectedArea}%</Text>
        </View>
      )}

      {result.recommendations.length > 0 && (
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, { color: colors.foreground }]}>Immediate Actions</Text>
          {result.recommendations.map((rec, i) => (
            <View key={i} style={styles.listItem}>
              <Ionicons name="checkmark-circle" size={15} color={colors.primary} />
              <Text style={[styles.listText, { color: colors.mutedForeground }]}>{rec}</Text>
            </View>
          ))}
        </View>
      )}

      {result.treatments.length > 0 && (
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, { color: colors.foreground }]}>Treatments</Text>
          {result.treatments.map((t, i) => (
            <View key={i} style={styles.listItem}>
              <Ionicons name="flask" size={15} color={colors.accent} />
              <Text style={[styles.listText, { color: colors.mutedForeground }]}>{t}</Text>
            </View>
          ))}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16, borderWidth: 1, gap: 14 },
  header: { flexDirection: "row", justifyContent: "space-between", alignItems: "flex-start" },
  headerLeft: { flex: 1, gap: 6 },
  badge: {
    alignSelf: "flex-start",
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
    borderWidth: 1,
  },
  badgeText: { fontSize: 10, fontWeight: "700", fontFamily: "Inter_700Bold", letterSpacing: 0.5 },
  diseaseName: { fontSize: 17, fontWeight: "700", fontFamily: "Inter_700Bold" },
  confidenceBlock: { alignItems: "center", marginLeft: 12 },
  confValue: { fontSize: 30, fontWeight: "700", fontFamily: "Inter_700Bold" },
  confLabel: { fontSize: 11, fontFamily: "Inter_400Regular" },
  areaRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    paddingTop: 12,
    borderTopWidth: 1,
  },
  areaLabel: { fontSize: 13, fontFamily: "Inter_400Regular", width: 95 },
  barBg: { flex: 1, height: 6, borderRadius: 3, overflow: "hidden" },
  barFill: { height: "100%", borderRadius: 3 },
  areaPct: { fontSize: 13, fontWeight: "600", fontFamily: "Inter_600SemiBold", width: 36, textAlign: "right" },
  section: { gap: 8 },
  sectionTitle: { fontSize: 14, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  listItem: { flexDirection: "row", gap: 8, alignItems: "flex-start" },
  listText: { fontSize: 13, fontFamily: "Inter_400Regular", flex: 1, lineHeight: 18 },
});
