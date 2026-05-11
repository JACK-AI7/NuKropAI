import { Ionicons } from "@expo/vector-icons";
import React from "react";
import { StyleSheet, Text, View, ScrollView } from "react-native";
import { useColors } from "@/hooks/useColors";
import { getTreatmentsForDisease } from "@/utils/treatments";

export interface ScanResult {
  disease: string;
  confidence: number;
  severity: "low" | "medium" | "high";
  affectedArea: number;
  isHealthy?: boolean;
  recommendations: string[];
  treatments: string[];
  explanation?: string;
}

const SEVERITY_COLORS: Record<ScanResult["severity"], string> = {
  low: "#22C55E",
  medium: "#F59E0B",
  high: "#FF453A",
};

export function ScanResultCard({ result }: { result: ScanResult }) {
  const colors = useColors();
  const sc = SEVERITY_COLORS[result.severity];
  const isHealthy = result.isHealthy ?? result.severity === "low";

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
            <Ionicons
              name={isHealthy ? "checkmark-circle" : "warning"}
              size={11}
              color={sc}
            />
            <Text style={[styles.badgeText, { color: sc }]}>
              {isHealthy ? "HEALTHY" : `${result.severity.toUpperCase()} SEVERITY`}
            </Text>
          </View>
          <Text style={[styles.diseaseName, { color: colors.foreground }]}>{result.disease}</Text>
        </View>
        <View style={styles.confidenceBlock}>
          <Text style={[styles.confValue, { color: isHealthy ? colors.accent : colors.primary }]}>
            {result.confidence}%
          </Text>
          <Text style={[styles.confLabel, { color: colors.mutedForeground }]}>match</Text>
        </View>
      </View>

      {result.explanation ? (
        <View style={[styles.explanation, { backgroundColor: colors.background, borderColor: colors.border }]}>
          <Text style={[styles.explanationText, { color: colors.mutedForeground }]}>
            {result.explanation}
          </Text>
        </View>
      ) : null}

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

      {/* Real Product Recommendations */}
      {(() => {
        const productInfo = getTreatmentsForDisease(result.disease);
        if (!productInfo) return null;

        return (
          <View style={styles.section}>
            <Text style={[styles.sectionTitle, { color: colors.foreground }]}>
              Recommended Products
            </Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.productsScroll}>
              {productInfo.products.map((p, i) => (
                <View key={i} style={[styles.productCard, { backgroundColor: colors.background, borderColor: colors.border }]}>
                  <View style={styles.productHeader}>
                    <View style={[styles.typeBadge, { backgroundColor: p.type === "Organic" ? "#22C55E20" : colors.primary + "20" }]}>
                      <Text style={[styles.typeText, { color: p.type === "Organic" ? "#22C55E" : colors.primary }]}>
                        {p.type.toUpperCase()}
                      </Text>
                    </View>
                    <Ionicons name="cart" size={16} color={colors.mutedForeground} />
                  </View>
                  <Text style={[styles.productName, { color: colors.foreground }]}>{p.name}</Text>
                  <Text style={[styles.productActive, { color: colors.mutedForeground }]}>{p.activeIngredient}</Text>
                  
                  <View style={[styles.productDetail, { borderTopColor: colors.border }]}>
                    <Ionicons name="flask-outline" size={12} color={colors.primary} />
                    <Text style={[styles.detailText, { color: colors.foreground }]}>{p.dosage}</Text>
                  </View>
                  <View style={styles.productDetail}>
                    <Ionicons name="time-outline" size={12} color={colors.accent} />
                    <Text style={[styles.detailText, { color: colors.foreground }]}>{p.timing}</Text>
                  </View>
                  <View style={[styles.safetyBox, { backgroundColor: "#FF453A10" }]}>
                    <Ionicons name="shield-checkmark" size={10} color="#FF453A" />
                    <Text style={styles.safetyText}>{p.safety}</Text>
                  </View>
                </View>
              ))}
            </ScrollView>
          </View>
        );
      })()}

      {result.treatments.length > 0 && !getTreatmentsForDisease(result.disease) && (
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, { color: colors.foreground }]}>General Treatments</Text>
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
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
    borderWidth: 1,
  },
  badgeText: { fontSize: 10, fontWeight: "700", fontFamily: "Inter_700Bold", letterSpacing: 0.5 },
  diseaseName: { fontSize: 17, fontWeight: "700", fontFamily: "Inter_700Bold", lineHeight: 22 },
  confidenceBlock: { alignItems: "center", marginLeft: 12 },
  confValue: { fontSize: 30, fontWeight: "700", fontFamily: "Inter_700Bold" },
  confLabel: { fontSize: 11, fontFamily: "Inter_400Regular" },
  explanation: {
    padding: 12,
    borderRadius: 10,
    borderWidth: 1,
  },
  explanationText: { fontSize: 13, fontFamily: "Inter_400Regular", lineHeight: 19 },
  areaRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    paddingTop: 12,
    borderTopWidth: 1,
  },
  areaLabel: { fontSize: 12, fontFamily: "Inter_400Regular", width: 90 },
  barBg: { flex: 1, height: 6, borderRadius: 3, overflow: "hidden" },
  barFill: { height: "100%", borderRadius: 3 },
  areaPct: { fontSize: 13, fontWeight: "600", fontFamily: "Inter_600SemiBold", width: 36, textAlign: "right" },
  section: { gap: 8 },
  sectionTitle: { fontSize: 14, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  listItem: { flexDirection: "row", gap: 8, alignItems: "flex-start" },
  listText: { fontSize: 13, fontFamily: "Inter_400Regular", flex: 1, lineHeight: 18 },
  productsScroll: { gap: 12, paddingRight: 16 },
  productCard: { 
    width: 220, 
    padding: 12, 
    borderRadius: 14, 
    borderWidth: 1,
    gap: 8,
  },
  productHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  typeBadge: { paddingHorizontal: 6, paddingVertical: 2, borderRadius: 4 },
  typeText: { fontSize: 8, fontWeight: "800", fontFamily: "Inter_800ExtraBold" },
  productName: { fontSize: 15, fontWeight: "700", fontFamily: "Inter_700Bold" },
  productActive: { fontSize: 11, fontFamily: "Inter_400Regular", marginTop: -4 },
  productDetail: { flexDirection: "row", alignItems: "center", gap: 6, paddingTop: 8, borderTopWidth: 1 },
  detailText: { fontSize: 12, fontFamily: "Inter_500Medium", flex: 1 },
  safetyBox: { flexDirection: "row", gap: 6, padding: 8, borderRadius: 8 },
  safetyText: { fontSize: 10, fontFamily: "Inter_400Regular", color: "#FF453A", flex: 1 },
});
