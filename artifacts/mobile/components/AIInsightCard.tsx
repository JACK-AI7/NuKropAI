import { Ionicons } from "@expo/vector-icons";
import React from "react";
import { StyleSheet, Text, View, TouchableOpacity } from "react-native";
import { router } from "expo-router";
import { useColors } from "@/hooks/useColors";
import type { AIInsight } from "@/contexts/AppContext";

function getStyle(type: AIInsight["type"]) {
  switch (type) {
    case "danger":
      return { icon: "warning" as const, color: "#FF453A", bg: "rgba(255,69,58,0.08)" };
    case "warning":
      return { icon: "alert-circle" as const, color: "#F59E0B", bg: "rgba(245,158,11,0.08)" };
    case "success":
      return { icon: "checkmark-circle" as const, color: "#4ADE80", bg: "rgba(74,222,128,0.08)" };
    default:
      return { icon: "bulb" as const, color: "#22C55E", bg: "rgba(34,197,94,0.08)" };
  }
}

function timeAgo(ts: number): string {
  const diff = Date.now() - ts;
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

export function AIInsightCard({ insight }: { insight: AIInsight }) {
  const colors = useColors();
  const s = getStyle(insight.type);

  return (
    <View
      style={[
        styles.container,
        { backgroundColor: colors.card, borderColor: colors.border, borderRadius: colors.radius },
      ]}
    >
      <View style={[styles.icon, { backgroundColor: s.bg }]}>
        <Ionicons name={s.icon} size={20} color={s.color} />
      </View>
      <View style={styles.content}>
        <View style={styles.row}>
          <Text style={[styles.title, { color: colors.foreground }]}>{insight.title}</Text>
          <Text style={[styles.time, { color: colors.mutedForeground }]}>{timeAgo(insight.timestamp)}</Text>
        </View>
        <Text style={[styles.message, { color: colors.mutedForeground }]} numberOfLines={2}>
          {insight.message}
        </Text>
        {insight.crop && (
          <View style={styles.tag}>
            <Text style={[styles.tagText, { color: colors.primary }]}>{insight.crop}</Text>
          </View>
        )}
        {(insight.type === "danger" || insight.type === "warning") && (
          <TouchableOpacity 
            style={[styles.actionBtn, { backgroundColor: s.color + "15", borderColor: s.color + "30" }]}
            onPress={() => router.push("/(tabs)/chat")}
          >
            <Text style={[styles.actionBtnText, { color: s.color }]}>Consult AI Advisor</Text>
            <Ionicons name="arrow-forward" size={12} color={s.color} />
          </TouchableOpacity>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    padding: 14,
    gap: 12,
    borderWidth: 1,
    marginBottom: 10,
  },
  icon: {
    width: 40,
    height: 40,
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
  },
  content: { flex: 1, gap: 4 },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  title: {
    fontSize: 14,
    fontWeight: "600",
    fontFamily: "Inter_600SemiBold",
    flex: 1,
  },
  time: {
    fontSize: 11,
    fontFamily: "Inter_400Regular",
    marginLeft: 8,
  },
  message: {
    fontSize: 13,
    fontFamily: "Inter_400Regular",
    lineHeight: 18,
  },
  tag: {
    alignSelf: "flex-start",
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 6,
    backgroundColor: "rgba(34,197,94,0.1)",
    marginTop: 4,
  },
  tagText: {
    fontSize: 11,
    fontFamily: "Inter_500Medium",
  },
  actionBtn: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    borderWidth: 1,
    marginTop: 10,
  },
  actionBtnText: {
    fontSize: 12,
    fontWeight: "700",
    fontFamily: "Inter_700Bold",
  },
});
