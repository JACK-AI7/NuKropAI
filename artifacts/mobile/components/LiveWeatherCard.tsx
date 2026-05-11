import { Ionicons } from "@expo/vector-icons";
import { LinearGradient } from "expo-linear-gradient";
import React, { useEffect } from "react";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import Animated, {
  useAnimatedStyle,
  useSharedValue,
  withRepeat,
  withSequence,
  withTiming,
} from "react-native-reanimated";
import { useColors } from "@/hooks/useColors";
import type { WeatherData } from "@/hooks/useWeather";
import { PulseIndicator } from "./PulseIndicator";

const ICON_MAP: Record<string, string> = {
  sunny: "sunny",
  "partly-sunny": "partly-sunny",
  cloudy: "cloudy",
  rainy: "rainy",
  thunderstorm: "thunderstorm",
  snow: "snow",
  cloud: "cloud",
};

function WeatherIcon({
  icon,
  size = 52,
  color,
}: {
  icon: string;
  size?: number;
  color: string;
}) {
  const scale = useSharedValue(1);

  useEffect(() => {
    if (icon === "thunderstorm") {
      scale.value = withRepeat(
        withSequence(
          withTiming(1.2, { duration: 220 }),
          withTiming(0.88, { duration: 220 }),
          withTiming(1, { duration: 300 }),
          withTiming(1, { duration: 700 }),
        ),
        -1,
        false,
      );
    } else if (icon === "rainy") {
      scale.value = withRepeat(
        withSequence(
          withTiming(1.09, { duration: 1000 }),
          withTiming(0.96, { duration: 1000 }),
        ),
        -1,
        false,
      );
    } else {
      scale.value = withRepeat(
        withSequence(
          withTiming(1.07, { duration: 2800 }),
          withTiming(1, { duration: 2800 }),
        ),
        -1,
        false,
      );
    }
  }, [icon, scale]);

  const s = useAnimatedStyle(() => ({ transform: [{ scale: scale.value }] }));

  return (
    <Animated.View style={s}>
      <Ionicons
        name={(ICON_MAP[icon] ?? "partly-sunny") as never}
        size={size}
        color={color}
      />
    </Animated.View>
  );
}

function SkeletonBox({
  w,
  h,
  r = 7,
}: {
  w: number | string;
  h: number;
  r?: number;
}) {
  const opacity = useSharedValue(0.3);
  useEffect(() => {
    opacity.value = withRepeat(
      withSequence(
        withTiming(0.65, { duration: 750 }),
        withTiming(0.3, { duration: 750 }),
      ),
      -1,
      false,
    );
  }, [opacity]);
  const s = useAnimatedStyle(() => ({ opacity: opacity.value }));
  return (
    <Animated.View
      style={[
        { height: h, borderRadius: r, backgroundColor: "#ffffff22" },
        w === "100%" ? { width: "100%" } : { width: w as number },
        s,
      ]}
    />
  );
}

function fmt12h(isoStr: string): string {
  if (!isoStr) return "--:--";
  try {
    const d = new Date(isoStr);
    return d.toLocaleTimeString("en-IN", {
      hour: "numeric",
      minute: "2-digit",
      hour12: true,
    });
  } catch {
    return "--:--";
  }
}

function dayLabel(dateStr: string, index: number): string {
  if (index === 0) return "Today";
  if (index === 1) return "Tmrw";
  try {
    return new Date(dateStr).toLocaleDateString("en-IN", { weekday: "short" });
  } catch {
    return "---";
  }
}

export interface LiveWeatherCardProps {
  weather: WeatherData | null;
  loading: boolean;
  error: string | null;
  city: string;
}

export function LiveWeatherCard({
  weather,
  loading,
  error,
  city,
}: LiveWeatherCardProps) {
  const colors = useColors();

  /* ── Loading skeleton ────────────────────────────────────────────── */
  if (loading && !weather) {
    return (
      <LinearGradient
        colors={["#0A2D1A", "#0C3820", "#0A2D1A"]}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
        style={styles.card}
      >
        <View style={styles.skRow}>
          <SkeletonBox w={90} h={12} />
          <SkeletonBox w={48} h={16} r={10} />
        </View>
        <View style={[styles.skRow, { marginTop: 14, alignItems: "flex-start" }]}>
          <View style={{ gap: 8, flex: 1 }}>
            <SkeletonBox w={130} h={44} />
            <SkeletonBox w={100} h={13} />
            <SkeletonBox w={110} h={12} />
          </View>
          <SkeletonBox w={58} h={58} r={29} />
        </View>
        <View style={[styles.statsRow, { marginTop: 20 }]}>
          {[0, 1, 2, 3].map((i) => (
            <View key={i} style={{ flex: 1, alignItems: "center", gap: 6 }}>
              <SkeletonBox w={28} h={12} />
              <SkeletonBox w={36} h={12} />
            </View>
          ))}
        </View>
        <View style={{ marginTop: 16, gap: 6 }}>
          <SkeletonBox w="100%" h={40} />
        </View>
      </LinearGradient>
    );
  }

  /* ── Error state ─────────────────────────────────────────────────── */
  if ((error || !weather) && !loading) {
    return (
      <LinearGradient
        colors={["#0A2D1A", "#0C3820", "#0A2D1A"]}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
        style={[styles.card, styles.centerCol]}
      >
        <Ionicons name="cloud-offline-outline" size={34} color="#ffffff44" />
        <Text style={styles.errText}>
          {error ?? "Weather data unavailable"}
        </Text>
        <Text style={styles.errSub}>Will retry automatically</Text>
      </LinearGradient>
    );
  }

  if (!weather) return null;

  const { current, forecast, hourly, farmingTip, sunrise, sunset } = weather;

  return (
    <LinearGradient
      colors={["#0A2D1A", "#0C3820", "#0A2D1A"]}
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
      style={styles.card}
    >
      {/* Location + LIVE badge */}
      <View style={styles.topRow}>
        <View style={styles.locRow}>
          <Ionicons name="location-sharp" size={11} color="#22C55E99" />
          <Text style={styles.cityText} numberOfLines={1}>
            {city}
          </Text>
        </View>
        <View style={styles.liveBadge}>
          <PulseIndicator size={5} />
          <Text style={styles.liveText}>LIVE</Text>
        </View>
      </View>

      {/* Temperature + icon */}
      <View style={styles.mainRow}>
        <View style={{ flex: 1 }}>
          <Text style={styles.tempText}>{current.temp}°C</Text>
          <Text style={styles.condText}>{current.condition}</Text>
          <Text style={styles.rangeText}>
            ↑{forecast[0]?.maxTemp ?? current.temp}° ↓
            {forecast[0]?.minTemp ?? current.temp}° · Feels{" "}
            {current.feelsLike}°
          </Text>
        </View>
        <WeatherIcon icon={current.icon} size={58} color="#22C55E" />
      </View>

      {/* Stats strip */}
      <View style={styles.statsRow}>
        <View style={styles.stat}>
          <Ionicons name="water" size={13} color="#60A5FA" />
          <Text style={styles.statVal}>{current.humidity}%</Text>
          <Text style={styles.statLbl}>Humidity</Text>
        </View>
        <View style={[styles.stat, styles.statDiv]}>
          <Ionicons name="navigate" size={13} color="#A78BFA" />
          <Text style={styles.statVal}>{current.windSpeed}</Text>
          <Text style={styles.statLbl}>km/h</Text>
        </View>
        <View style={[styles.stat, styles.statDiv]}>
          <Ionicons name="sunny" size={13} color="#FBBF24" />
          <Text style={styles.statVal}>UV {current.uvIndex}</Text>
          <Text style={styles.statLbl}>Index</Text>
        </View>
        <View style={[styles.stat, styles.statDiv]}>
          <Ionicons name="rainy" size={13} color="#60A5FA" />
          <Text style={styles.statVal}>{current.rainChance}%</Text>
          <Text style={styles.statLbl}>Rain</Text>
        </View>
      </View>

      {/* Sunrise / sunset */}
      <View style={styles.sunRow}>
        <Ionicons name="sunny-outline" size={11} color="#FBBF2466" />
        <Text style={styles.sunText}>↑ {fmt12h(sunrise)}</Text>
        <View style={styles.sunDivider} />
        <Ionicons name="moon-outline" size={11} color="#8B5CF666" />
        <Text style={styles.sunText}>↓ {fmt12h(sunset)}</Text>
      </View>

      {/* Hourly strip */}
      {hourly.length > 0 && (
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.hourlyScroll}
          contentContainerStyle={styles.hourlyContent}
        >
          {hourly.map((h, i) => (
            <View key={i} style={styles.hourItem}>
              <Text style={styles.hourTime}>{h.time}</Text>
              <Ionicons
                name={(ICON_MAP[h.icon] ?? "partly-sunny") as never}
                size={14}
                color="#22C55E77"
              />
              <Text style={styles.hourTemp}>{h.temp}°</Text>
              {h.precipPct > 0 && (
                <Text style={styles.hourPrecip}>{h.precipPct}%</Text>
              )}
            </View>
          ))}
        </ScrollView>
      )}

      {/* 5-day forecast pills */}
      {forecast.length > 0 && (
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.forecastScroll}
          contentContainerStyle={styles.forecastContent}
        >
          {forecast.slice(0, 7).map((day, i) => (
            <View key={i} style={styles.forecastPill}>
              <Text style={styles.forecastDay}>{dayLabel(day.date, i)}</Text>
              <Ionicons
                name={(ICON_MAP[day.icon] ?? "partly-sunny") as never}
                size={16}
                color="#22C55E88"
              />
              <Text style={styles.forecastHi}>{day.maxTemp}°</Text>
              <Text style={styles.forecastLo}>{day.minTemp}°</Text>
            </View>
          ))}
        </ScrollView>
      )}

      {/* AI farming tip */}
      <View style={styles.tipBox}>
        <Ionicons name="leaf" size={13} color="#22C55E" />
        <Text style={styles.tipText}>{farmingTip}</Text>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 16,
    padding: 18,
    overflow: "hidden",
    marginBottom: 8,
  },
  centerCol: {
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 44,
    gap: 10,
  },
  errText: {
    color: "#ffffff77",
    fontSize: 13,
    fontFamily: "Inter_400Regular",
    textAlign: "center",
  },
  errSub: {
    color: "#ffffff44",
    fontSize: 11,
    fontFamily: "Inter_400Regular",
  },
  skRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  topRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 14,
  },
  locRow: { flexDirection: "row", alignItems: "center", gap: 4, flex: 1 },
  cityText: {
    fontSize: 12,
    color: "#ffffff77",
    fontFamily: "Inter_400Regular",
  },
  liveBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: 5,
    backgroundColor: "#22C55E1A",
    paddingHorizontal: 9,
    paddingVertical: 4,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "#22C55E44",
  },
  liveText: {
    fontSize: 9,
    color: "#22C55E",
    fontFamily: "Inter_700Bold",
    letterSpacing: 1.2,
  },
  mainRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: 20,
  },
  tempText: {
    fontSize: 46,
    fontWeight: "700",
    fontFamily: "Inter_700Bold",
    color: "#fff",
    lineHeight: 52,
  },
  condText: {
    fontSize: 14,
    color: "#ffffff88",
    fontFamily: "Inter_400Regular",
    marginTop: 3,
  },
  rangeText: {
    fontSize: 11,
    color: "#ffffff55",
    fontFamily: "Inter_400Regular",
    marginTop: 4,
  },
  statsRow: {
    flexDirection: "row",
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderColor: "#ffffff12",
    paddingVertical: 13,
    marginBottom: 12,
  },
  stat: { flex: 1, alignItems: "center", gap: 3 },
  statDiv: { borderLeftWidth: 1, borderColor: "#ffffff12" },
  statVal: {
    fontSize: 12,
    fontWeight: "600",
    fontFamily: "Inter_600SemiBold",
    color: "#fff",
  },
  statLbl: {
    fontSize: 9,
    color: "#ffffff55",
    fontFamily: "Inter_400Regular",
  },
  sunRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    marginBottom: 12,
  },
  sunText: {
    fontSize: 11,
    color: "#ffffff55",
    fontFamily: "Inter_400Regular",
  },
  sunDivider: {
    width: 1,
    height: 10,
    backgroundColor: "#ffffff22",
    marginHorizontal: 4,
  },
  hourlyScroll: { marginBottom: 10 },
  hourlyContent: { gap: 16, paddingVertical: 2 },
  hourItem: { alignItems: "center", gap: 4, minWidth: 44 },
  hourTime: {
    fontSize: 9,
    color: "#ffffff55",
    fontFamily: "Inter_400Regular",
  },
  hourTemp: {
    fontSize: 12,
    fontWeight: "600",
    fontFamily: "Inter_600SemiBold",
    color: "#fff",
  },
  hourPrecip: {
    fontSize: 9,
    color: "#60A5FA88",
    fontFamily: "Inter_400Regular",
  },
  forecastScroll: { marginBottom: 14 },
  forecastContent: { gap: 8, paddingVertical: 2 },
  forecastPill: {
    alignItems: "center",
    gap: 4,
    backgroundColor: "#ffffff09",
    borderRadius: 10,
    paddingVertical: 8,
    paddingHorizontal: 10,
    minWidth: 52,
  },
  forecastDay: {
    fontSize: 9,
    color: "#ffffff66",
    fontFamily: "Inter_500Medium",
  },
  forecastHi: {
    fontSize: 12,
    fontWeight: "600",
    fontFamily: "Inter_600SemiBold",
    color: "#fff",
  },
  forecastLo: {
    fontSize: 10,
    color: "#ffffff55",
    fontFamily: "Inter_400Regular",
  },
  tipBox: {
    flexDirection: "row",
    alignItems: "flex-start",
    gap: 8,
    backgroundColor: "#22C55E12",
    borderRadius: 10,
    padding: 12,
    borderWidth: 1,
    borderColor: "#22C55E2A",
  },
  tipText: {
    fontSize: 12,
    color: "#ffffffcc",
    fontFamily: "Inter_400Regular",
    lineHeight: 18,
    flex: 1,
  },
});
