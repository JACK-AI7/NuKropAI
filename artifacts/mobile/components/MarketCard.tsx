import { Ionicons } from "@expo/vector-icons";
import React, { useEffect } from "react";
import {
  ActivityIndicator,
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
  withTiming,
} from "react-native-reanimated";
import { useColors } from "@/hooks/useColors";
import type { MarketCrop, MarketData } from "@/hooks/useMarket";
import { GlassCard } from "./GlassCard";
import { PulseIndicator } from "./PulseIndicator";

function SkeletonRow({ delay }: { delay: number }) {
  const opacity = useSharedValue(0.25);
  useEffect(() => {
    opacity.value = withDelay(
      delay,
      withRepeat(
        withSequence(
          withTiming(0.6, { duration: 700 }),
          withTiming(0.25, { duration: 700 }),
        ),
        -1,
        false,
      ),
    );
  }, [delay, opacity]);
  const s = useAnimatedStyle(() => ({ opacity: opacity.value }));
  return (
    <Animated.View style={[styles.skRow, s]}>
      <View style={[styles.skCell, { width: 30, height: 20, borderRadius: 4 }]} />
      <View style={[styles.skCell, { flex: 1, height: 14, borderRadius: 4 }]} />
      <View style={[styles.skCell, { width: 70, height: 14, borderRadius: 4 }]} />
      <View style={[styles.skCell, { width: 80, height: 14, borderRadius: 4 }]} />
    </Animated.View>
  );
}

function CropRow({ crop, delay }: { crop: MarketCrop; delay: number }) {
  const colors = useColors();
  const opacity = useSharedValue(0);
  const tx = useSharedValue(14);

  useEffect(() => {
    opacity.value = withDelay(delay, withTiming(1, { duration: 380 }));
    tx.value = withDelay(delay, withTiming(0, { duration: 340 }));
  }, [delay, opacity, tx]);

  const s = useAnimatedStyle(() => ({
    opacity: opacity.value,
    transform: [{ translateX: tx.value }],
  }));

  const changeColor =
    crop.trend === "up"
      ? "#22C55E"
      : crop.trend === "down"
        ? "#FF453A"
        : colors.mutedForeground;

  const trendIcon =
    crop.trend === "up"
      ? "trending-up"
      : crop.trend === "down"
        ? "trending-down"
        : "remove";

  const sign = crop.change >= 0 ? "+" : "";

  return (
    <Animated.View
      style={[styles.cropRow, { borderBottomColor: colors.border }, s]}
    >
      <Text style={styles.cropEmoji}>{crop.emoji}</Text>

      <View style={styles.cropName}>
        <Text style={[styles.cropNameText, { color: colors.foreground }]}>
          {crop.name}
        </Text>
        <Text
          style={[styles.cropMarket, { color: colors.mutedForeground }]}
          numberOfLines={1}
        >
          {crop.market}
        </Text>
      </View>

      <Text style={[styles.cropPrice, { color: colors.foreground }]}>
        ₹{crop.price.toLocaleString("en-IN")}
      </Text>

      <View
        style={[styles.changeChip, { backgroundColor: changeColor + "18" }]}
      >
        <Ionicons name={trendIcon as never} size={10} color={changeColor} />
        <Text style={[styles.changeText, { color: changeColor }]}>
          {sign}
          {crop.change} ({sign}
          {crop.changePct.toFixed(2)}%)
        </Text>
      </View>
    </Animated.View>
  );
}

function timeAgo(isoStr: string): string {
  const ms = Date.now() - new Date(isoStr).getTime();
  const mins = Math.floor(ms / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  return `${Math.floor(mins / 60)}h ago`;
}

export interface MarketCardProps {
  market: MarketData | null;
  loading: boolean;
  error: string | null;
  onRefresh: () => void;
}

export function MarketCard({
  market,
  loading,
  error,
  onRefresh,
}: MarketCardProps) {
  const colors = useColors();

  const sentimentColor =
    market?.marketSentiment === "bullish"
      ? "#22C55E"
      : market?.marketSentiment === "bearish"
        ? "#FF453A"
        : "#F59E0B";

  const sentimentIcon =
    market?.marketSentiment === "bullish"
      ? "trending-up"
      : market?.marketSentiment === "bearish"
        ? "trending-down"
        : "remove";

  return (
    <GlassCard style={styles.card}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <Ionicons name="bar-chart" size={17} color={colors.primary} />
          <Text style={[styles.title, { color: colors.foreground }]}>
            Live Market Prices
          </Text>
          <View style={styles.livePill}>
            <PulseIndicator size={5} />
            <Text style={[styles.liveLabel, { color: colors.primary }]}>
              LIVE
            </Text>
          </View>
        </View>
        <TouchableOpacity
          onPress={onRefresh}
          hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }}
          disabled={loading && !market}
        >
          {loading && market ? (
            <ActivityIndicator size="small" color={colors.mutedForeground} />
          ) : (
            <Ionicons name="refresh" size={17} color={colors.mutedForeground} />
          )}
        </TouchableOpacity>
      </View>

      {/* Sentiment */}
      {market && (
        <View style={styles.sentimentRow}>
          <View
            style={[
              styles.sentimentChip,
              {
                backgroundColor: sentimentColor + "1A",
                borderColor: sentimentColor + "44",
              },
            ]}
          >
            <Ionicons
              name={sentimentIcon as never}
              size={12}
              color={sentimentColor}
            />
            <Text style={[styles.sentimentLabel, { color: sentimentColor }]}>
              {market.marketSentiment.charAt(0).toUpperCase() +
                market.marketSentiment.slice(1)}
            </Text>
          </View>
          <Text
            style={[styles.sentimentDetail, { color: colors.mutedForeground }]}
            numberOfLines={1}
          >
            ↑ {market.topGainer} · ↓ {market.topLoser}
          </Text>
        </View>
      )}

      {/* Divider */}
      <View style={[styles.divider, { backgroundColor: colors.border }]} />

      {/* Column headers */}
      <View style={styles.colHeader}>
        <Text style={[styles.colLbl, { color: colors.mutedForeground, flex: 1, marginLeft: 38 }]}>
          Crop
        </Text>
        <Text style={[styles.colLbl, { color: colors.mutedForeground, width: 86, textAlign: "right" }]}>
          ₹/Quintal
        </Text>
        <Text style={[styles.colLbl, { color: colors.mutedForeground, width: 100, textAlign: "right" }]}>
          Change
        </Text>
      </View>

      {/* Content */}
      {loading && !market ? (
        [0, 1, 2, 3, 4, 5].map((i) => <SkeletonRow key={i} delay={i * 70} />)
      ) : error && !market ? (
        <View style={styles.errorBox}>
          <Ionicons
            name="cloud-offline-outline"
            size={26}
            color={colors.mutedForeground}
          />
          <Text
            style={[styles.errorText, { color: colors.mutedForeground }]}
          >
            Market data temporarily unavailable
          </Text>
          <TouchableOpacity onPress={onRefresh} style={styles.retryBtn}>
            <Text style={[styles.retryText, { color: colors.primary }]}>
              Tap to retry
            </Text>
          </TouchableOpacity>
        </View>
      ) : (
        market?.crops.map((crop, i) => (
          <CropRow key={crop.name} crop={crop} delay={i * 55} />
        ))
      )}

      {/* Nearby Mandis */}
      {market?.nearbyMandis && market.nearbyMandis.length > 0 && (
        <View style={styles.nearbySection}>
          <Text style={[styles.nearbyTitle, { color: colors.foreground }]}>Nearby Markets</Text>
          {market.nearbyMandis.map((m, i) => (
            <View key={i} style={[styles.nearbyRow, { borderBottomColor: colors.border, borderBottomWidth: i < 2 ? 1 : 0 }]}>
              <View style={styles.nearbyInfo}>
                <Text style={[styles.nearbyName, { color: colors.foreground }]}>{m.name}</Text>
                <Text style={[styles.nearbyDist, { color: colors.mutedForeground }]}>{m.distance} km away</Text>
              </View>
              <View style={styles.nearbyPrice}>
                <Text style={[styles.nearbyPriceVal, { color: colors.primary }]}>₹{m.price.toLocaleString("en-IN")}</Text>
                <Text style={[styles.nearbyCrop, { color: colors.mutedForeground }]}>{m.crop}</Text>
              </View>
            </View>
          ))}
          <View style={[styles.sellingTip, { backgroundColor: colors.primary + "10" }]}>
            <Ionicons name="bulb" size={14} color={colors.primary} />
            <Text style={[styles.tipText, { color: colors.foreground }]}>
              Selling at <Text style={{ fontWeight: "700" }}>{market.nearbyMandis[0].name}</Text> could save you 15% in transport costs.
            </Text>
          </View>
        </View>
      )}

      {/* Footer */}
      {market && (
        <View style={styles.footer}>
          <Ionicons name="time-outline" size={11} color={colors.mutedForeground} />
          <Text style={[styles.footerText, { color: colors.mutedForeground }]}>
            Updated {timeAgo(market.updatedAt)} · {market.region} Mandi
          </Text>
        </View>
      )}

      <Text style={[styles.disclaimer, { color: colors.mutedForeground }]}>
        AI-generated estimates based on seasonal Indian mandi patterns.
      </Text>
    </GlassCard>
  );
}

const styles = StyleSheet.create({
  card: { marginBottom: 16 },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 10,
  },
  headerLeft: { flexDirection: "row", alignItems: "center", gap: 8 },
  title: {
    fontSize: 15,
    fontWeight: "600",
    fontFamily: "Inter_600SemiBold",
  },
  livePill: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    backgroundColor: "#22C55E18",
    paddingHorizontal: 7,
    paddingVertical: 2,
    borderRadius: 8,
  },
  liveLabel: { fontSize: 9, fontFamily: "Inter_700Bold", letterSpacing: 1 },
  sentimentRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 12,
    flexWrap: "wrap",
  },
  sentimentChip: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 8,
    borderWidth: 1,
  },
  sentimentLabel: { fontSize: 11, fontFamily: "Inter_500Medium" },
  sentimentDetail: {
    fontSize: 11,
    fontFamily: "Inter_400Regular",
    flex: 1,
  },
  divider: { height: 1, marginBottom: 8 },
  colHeader: {
    flexDirection: "row",
    paddingBottom: 7,
    marginBottom: 2,
  },
  colLbl: {
    fontSize: 9,
    fontFamily: "Inter_500Medium",
    textTransform: "uppercase",
    letterSpacing: 0.6,
  },
  skRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    paddingVertical: 11,
  },
  skCell: { backgroundColor: "#ffffff16" },
  cropRow: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 10,
    borderBottomWidth: 1,
    gap: 8,
  },
  cropEmoji: { fontSize: 20, width: 28, textAlign: "center" },
  cropName: { flex: 1 },
  cropNameText: {
    fontSize: 13,
    fontWeight: "500",
    fontFamily: "Inter_500Medium",
  },
  cropMarket: {
    fontSize: 10,
    fontFamily: "Inter_400Regular",
    marginTop: 1,
  },
  cropPrice: {
    fontSize: 13,
    fontWeight: "700",
    fontFamily: "Inter_700Bold",
    width: 80,
    textAlign: "right",
  },
  changeChip: {
    flexDirection: "row",
    alignItems: "center",
    gap: 3,
    paddingHorizontal: 6,
    paddingVertical: 3,
    borderRadius: 6,
    width: 96,
    justifyContent: "flex-end",
  },
  changeText: { fontSize: 9, fontFamily: "Inter_500Medium" },
  errorBox: {
    alignItems: "center",
    paddingVertical: 28,
    gap: 8,
  },
  errorText: {
    fontSize: 13,
    fontFamily: "Inter_400Regular",
    textAlign: "center",
  },
  retryBtn: { paddingVertical: 6 },
  retryText: { fontSize: 13, fontFamily: "Inter_500Medium" },
  footer: {
    flexDirection: "row",
    alignItems: "center",
    gap: 5,
    marginTop: 10,
    marginBottom: 4,
  },
  footerText: { fontSize: 11, fontFamily: "Inter_400Regular" },
  disclaimer: {
    fontSize: 10,
    fontFamily: "Inter_400Regular",
    fontStyle: "italic",
    marginTop: 4,
  },
  nearbySection: { marginTop: 16, paddingTop: 16, borderTopWidth: 1, borderTopColor: "#ffffff10" },
  nearbyTitle: { fontSize: 13, fontWeight: "700", fontFamily: "Inter_700Bold", marginBottom: 12 },
  nearbyRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", paddingVertical: 10 },
  nearbyInfo: { gap: 2 },
  nearbyName: { fontSize: 13, fontWeight: "500", fontFamily: "Inter_500Medium" },
  nearbyDist: { fontSize: 10, fontFamily: "Inter_400Regular" },
  nearbyPrice: { alignItems: "flex-end", gap: 2 },
  nearbyPriceVal: { fontSize: 14, fontWeight: "700", fontFamily: "Inter_700Bold" },
  nearbyCrop: { fontSize: 10, fontFamily: "Inter_500Medium" },
  sellingTip: { flexDirection: "row", alignItems: "center", gap: 8, marginTop: 12, padding: 10, borderRadius: 10 },
  tipText: { fontSize: 11, fontFamily: "Inter_400Regular", flex: 1, lineHeight: 16 },
});
