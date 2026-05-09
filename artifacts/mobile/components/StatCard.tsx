import { Ionicons } from "@expo/vector-icons";
import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { useColors } from "@/hooks/useColors";

interface StatCardProps {
  label: string;
  value: string;
  icon: string;
  color?: string;
  subtitle?: string;
}

export function StatCard({ label, value, icon, color, subtitle }: StatCardProps) {
  const colors = useColors();
  const ic = color ?? colors.primary;

  return (
    <View
      style={[
        styles.container,
        { backgroundColor: colors.card, borderRadius: colors.radius, borderColor: colors.border },
      ]}
    >
      <View style={[styles.iconWrap, { backgroundColor: ic + "18" }]}>
        <Ionicons name={icon as never} size={20} color={ic} />
      </View>
      <Text style={[styles.value, { color: colors.foreground }]}>{value}</Text>
      <Text style={[styles.label, { color: colors.mutedForeground }]}>{label}</Text>
      {subtitle && <Text style={[styles.subtitle, { color: ic }]}>{subtitle}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 14,
    borderWidth: 1,
    alignItems: "center",
    gap: 5,
    flex: 1,
  },
  iconWrap: {
    width: 38,
    height: 38,
    borderRadius: 12,
    justifyContent: "center",
    alignItems: "center",
  },
  value: { fontSize: 20, fontWeight: "700", fontFamily: "Inter_700Bold" },
  label: { fontSize: 11, fontFamily: "Inter_400Regular", textAlign: "center" },
  subtitle: { fontSize: 11, fontFamily: "Inter_500Medium" },
});
