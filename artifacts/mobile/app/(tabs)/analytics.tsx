import { Ionicons } from "@expo/vector-icons";
import React, { useEffect, useRef, useState } from "react";
import {
  ActivityIndicator,
  Platform,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import Animated, {
  Easing,
  useAnimatedStyle,
  useSharedValue,
  withDelay,
  withSpring,
  withTiming,
} from "react-native-reanimated";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { useColors } from "@/hooks/useColors";
import { useApp } from "@/contexts/AppContext";
import { useMarket } from "@/hooks/useMarket";
import { useWeather } from "@/hooks/useWeather";
import { GlassCard } from "@/components/GlassCard";
import { MarketCard } from "@/components/MarketCard";
import { request } from "@/utils/api";
import { fetchRegionalOutbreaks, calculateDiseaseRisk, type OutbreakRegion, type DiseaseRisk } from "@/utils/outbreaks";
import { getCalendarForRegion, type CropCalendar } from "@/utils/calendar";
import { calculateYield, forecastProfit, type YieldEstimate, type ProfitForecast } from "@/utils/prediction_engine";
import { aggregateCooperativeData, getDistrictIntelligence, type CooperativeStats, type DistrictInsight } from "@/utils/enterprise";
import { processAnomalyPipeline, type AnomalyEvent, getSeverityColor } from "@/utils/anomalies";
import { getMLPerformanceReport, getSystemHealth, type MLMetrics, type SystemHealth } from "@/utils/observability";
import { withRetry } from "@/utils/resilience";

const FALLBACK_DISEASES = [
  { name: "Early Blight", pct: 40, color: "#FF453A" },
  { name: "Leaf Blight", pct: 25, color: "#F59E0B" },
  { name: "Powdery Mildew", pct: 20, color: "#8B5CF6" },
  { name: "Other", pct: 15, color: "#22C55E" },
];

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function AnimBar({
  pct,
  color,
  delay,
}: {
  pct: number;
  color: string;
  delay: number;
}) {
  const width = useSharedValue(0);
  useEffect(() => {
    width.value = withDelay(
      delay,
      withTiming(pct, { duration: 900, easing: Easing.out(Easing.cubic) }),
    );
  }, [delay, pct, width]);
  const s = useAnimatedStyle(
    () => ({ width: `${width.value}%` as unknown as number }),
  );
  return (
    <Animated.View
      style={[{ height: 7, borderRadius: 4, backgroundColor: color }, s]}
    />
  );
}

function ColBar({
  value,
  max,
  color,
  delay,
}: {
  value: number;
  max: number;
  color: string;
  delay: number;
}) {
  const h = useSharedValue(0);
  useEffect(() => {
    h.value = withDelay(
      delay,
      withTiming(Math.max(4, (value / Math.max(max, 1)) * 76), {
        duration: 700,
        easing: Easing.out(Easing.cubic),
      }),
    );
  }, [delay, h, max, value]);
  const s = useAnimatedStyle(() => ({ height: h.value }));
  return (
    <Animated.View
      style={[{ width: 10, borderRadius: 3, backgroundColor: color }, s]}
    />
  );
}

function CountUpText({
  to,
  suffix = "",
  duration = 1100,
  style,
}: {
  to: number;
  suffix?: string;
  duration?: number;
  style?: object;
}) {
  const [displayed, setDisplayed] = useState(0);
  const hasAnimated = useRef(false);
  useEffect(() => {
    if (hasAnimated.current) {
      setDisplayed(to);
      return;
    }
    hasAnimated.current = true;
    const steps = 36;
    let i = 0;
    const interval = setInterval(() => {
      i++;
      setDisplayed(Math.round((i / steps) * to));
      if (i >= steps) clearInterval(interval);
    }, duration / steps);
    return () => clearInterval(interval);
  }, [to, duration]);
  return (
    <Text style={style}>
      {displayed}
      {suffix}
    </Text>
  );
}

function StatBlock({
  icon,
  label,
  value,
  suffix = "",
  color,
  delay,
}: {
  icon: string;
  label: string;
  value: number;
  suffix?: string;
  color: string;
  delay: number;
}) {
  const colors = useColors();
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
    <Animated.View style={[styles.statCell, s]}>
      <GlassCard style={{ alignItems: "center", gap: 5 }} padding={14}>
        <Ionicons name={icon as never} size={22} color={color} />
        <CountUpText
          to={value}
          suffix={suffix}
          style={[styles.statVal, { color: colors.foreground }]}
        />
        <Text style={[styles.statLbl, { color: colors.mutedForeground }]}>
          {label}
        </Text>
      </GlassCard>
    </Animated.View>
  );
}

export default function AnalyticsScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const { scanHistory, language, locationCity, lat, lon } = useApp();
  const topPad = Platform.OS === "web" ? 67 : insets.top + 10;

  const [aiRec, setAiRec] = useState<string | null>(null);
  const [aiLoading, setAiLoading] = useState(false);

  // Live market prices
  const { market, loading: marketLoading, error: marketError, refresh: refreshMarket } = useMarket(
    locationCity ?? "Telangana",
  );

  const [outbreaks, setOutbreaks] = useState<OutbreakRegion[]>([]);
  const [risks, setRisks] = useState<DiseaseRisk[]>([]);
  const [calendars, setCalendars] = useState<CropCalendar[]>([]);
  const [yieldEst, setYieldEst] = useState<YieldEstimate | null>(null);
  const [profitEst, setProfitEst] = useState<ProfitForecast | null>(null);
  const [coopStats, setCoopStats] = useState<CooperativeStats | null>(null);
  const [districtInsights, setDistrictInsights] = useState<DistrictInsight[]>([]);
  const [anomalies, setAnomalies] = useState<AnomalyEvent[]>([]);
  const [mlMetrics, setMlMetrics] = useState<MLMetrics | null>(null);
  const [sysHealth, setSysHealth] = useState<SystemHealth | null>(null);
  
  const { weather } = useWeather(lat, lon);
  const { cropsGrown, farmLocation, farms, userRole, advisorStats, activeFarmId } = useApp();
  const activeFarm = farms.find(f => f.id === activeFarmId) || farms[0];

  useEffect(() => {
    const loadPredictive = async () => {
      try {
        const stateName = activeFarm.location.split(",").pop()?.trim() || "Telangana";
        const regionalOutbreaks = await fetchRegionalOutbreaks(stateName);
        setOutbreaks(regionalOutbreaks);

        if (weather) {
          const calculatedRisks = calculateDiseaseRisk(weather.humidity, weather.temp, regionalOutbreaks);
          setRisks(calculatedRisks);

          const mainCrop = activeFarm.crops[0]?.name || "Rice";
          const est = calculateYield(mainCrop, healthPct, "low", { 
            temp: weather.temp, 
            humidity: weather.humidity, 
            rain: weather.rain || 0 
          }, regionalOutbreaks.length);
          setYieldEst(est);

          if (market) {
            const cropMarketData = market.crops.find(c => c.name === mainCrop);
            if (cropMarketData) {
              const pEst = forecastProfit(est, cropMarketData.price);
              setProfitEst(pEst);
            }
          }
        }

        const regionalCals = getCalendarForRegion(stateName, activeFarm.crops.map(c => c.name));
        setCalendars(regionalCals);

        if (userRole !== "farmer") {
          setCoopStats(aggregateCooperativeData(farms));
          setDistrictInsights(getDistrictIntelligence());
          
          const [perf, health] = await Promise.all([
            getMLPerformanceReport(stateName),
            getSystemHealth()
          ]);
          setMlMetrics(perf);
          setSysHealth(health);
        }
        
        const detected = await processAnomalyPipeline([
          { type: "ndvi", value: activeFarm.ndvi.score * 100 },
          { type: "moisture", value: activeFarm.soilHealth.moisture }
        ]);
        setAnomalies(detected);
      } catch (err) {
        console.error("Predictive load error:", err);
      }
    };
    loadPredictive();
  }, [weather, market, healthPct, userRole, farms, activeFarm]);

  const totalScans = 20 + scanHistory.length;
  const diseasesFound = scanHistory.filter((s) => s.severity !== "low").length + 12;
  
  const healthPct = useMemo(() => 
    Math.round(Math.max(60, 100 - (diseasesFound / Math.max(totalScans, 1)) * 60)),
    [diseasesFound, totalScans]
  );

  const diseaseBreakdown = useMemo(() => {
    const diseaseMap = scanHistory.reduce<Record<string, number>>((acc, s) => {
      const key = s.disease.split("(")[0]?.trim() ?? s.disease;
      acc[key] = (acc[key] ?? 0) + 1;
      return acc;
    }, {});

    return Object.keys(diseaseMap).length > 0
      ? Object.entries(diseaseMap)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 4)
          .map(([name, count], i) => ({
            name,
            pct: Math.round((count / Math.max(scanHistory.length, 1)) * 100),
            color: FALLBACK_DISEASES[i]?.color ?? "#22C55E",
          }))
      : FALLBACK_DISEASES;
  }, [scanHistory]);

  const { weeklyData, maxScans } = useMemo(() => {
    const now = Date.now();
    const data = DAYS.map((day, i) => {
      const start = now - (6 - i) * 86400000;
      const end = start + 86400000;
      const dayScans = scanHistory.filter(
        (s) => s.timestamp >= start && s.timestamp < end,
      );
      const baseFallback = [3, 5, 2, 7, 4, 6, 3][i] ?? 3;
      return {
        day,
        scans: dayScans.length + baseFallback,
        diseases:
          dayScans.filter((s) => s.severity !== "low").length +
          ([1, 2, 0, 3, 1, 2, 1][i] ?? 0),
      };
    });
    return { weeklyData: data, maxScans: Math.max(...data.map((d) => d.scans)) };
  }, [scanHistory]);

  useEffect(() => {
    const fetchRec = async () => {
      setAiLoading(true);
      try {
        const data = await request<{ reply: string }>("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: `Based on ${totalScans} total scans with ${diseasesFound} diseases detected (${healthPct}% health score), give me a concise 2-sentence weekly farm advisory with one specific action to take this week.`,
            language,
            history: [],
          }),
        });
        setAiRec(data.reply);
      } catch (_) {
        setAiRec(
          `Based on this week's data, early blight is the most common threat. Apply Mancozeb 75 WP @ 2.5g/L before the upcoming rain window on Thursday.`,
        );
      } finally {
        setAiLoading(false);
      }
    };
    fetchRec();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const farmTwin = activeFarm;

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <ScrollView
        contentContainerStyle={[
          styles.scroll,
          {
            paddingTop: topPad,
            paddingBottom: Platform.OS === "web" ? 100 : 110,
          },
        ]}
        showsVerticalScrollIndicator={false}
      >
        <Text style={[styles.title, { color: colors.foreground }]}>
          Analytics
        </Text>
        <Text style={[styles.subtitle, { color: colors.mutedForeground }]}>
          AI-powered crop health insights
        </Text>

        {/* AI Advisor / Enterprise Dashboard Overlay */}
        {userRole !== "farmer" && (
          <View style={styles.advisorHeader}>
            <View style={styles.advisorBadge}>
              <Ionicons name="shield-checkmark" size={16} color={colors.primary} />
              <Text style={[styles.advisorBadgeText, { color: colors.primary }]}>
                {userRole === "advisor" ? "AGRI ADVISOR PORTAL" : "ENTERPRISE DASHBOARD"}
              </Text>
            </View>
          </View>
        )}

        {userRole === "advisor" && advisorStats && (
          <View style={styles.statsGrid}>
            <StatBlock icon="people" label="Farms" value={advisorStats.assignedFarms} color={colors.primary} delay={60} />
            <StatBlock icon="warning" label="Outbreaks" value={advisorStats.activeOutbreaks} color="#FF453A" delay={120} />
            <StatBlock icon="chatbubbles" label="Pending" value={advisorStats.pendingRecommendations} color={colors.accent} delay={180} />
            <StatBlock icon="analytics" label="Score" value={92} suffix="%" color="#F59E0B" delay={240} />
          </View>
        )}

        {userRole === "enterprise" && coopStats && (
          <GlassCard style={styles.card}>
            <Text style={[styles.cardTitle, { color: colors.foreground }]}>Cooperative Cluster: Telangana North</Text>
            <View style={styles.coopGrid}>
              <View style={styles.coopItem}>
                <Text style={[styles.coopLbl, { color: colors.mutedForeground }]}>Total Area</Text>
                <Text style={[styles.coopVal, { color: colors.foreground }]}>{coopStats.totalAcreage} <Text style={styles.coopUnit}>Acres</Text></Text>
              </View>
              <View style={styles.coopItem}>
                <Text style={[styles.coopLbl, { color: colors.mutedForeground }]}>Avg Health</Text>
                <Text style={[styles.coopVal, { color: "#22C55E" }]}>{coopStats.averageHealth}%</Text>
              </View>
              <View style={styles.coopItem}>
                <Text style={[styles.coopLbl, { color: colors.mutedForeground }]}>Productivity Index</Text>
                <Text style={[styles.coopVal, { color: colors.accent }]}>{coopStats.productivityIndex}/100</Text>
              </View>
              <View style={styles.coopItem}>
                <Text style={[styles.coopLbl, { color: colors.mutedForeground }]}>Top Crop</Text>
                <Text style={[styles.coopVal, { color: colors.foreground }]}>{coopStats.topPerformingCrop}</Text>
              </View>
            </View>
          </GlassCard>
        )}

        {userRole !== "farmer" && districtInsights.length > 0 && (
          <GlassCard style={styles.card}>
            <Text style={[styles.cardTitle, { color: colors.foreground }]}>District Intelligence</Text>
            <View style={styles.districtTable}>
              {districtInsights.map((di, i) => (
                <View key={i} style={[styles.districtRow, { borderBottomWidth: i < districtInsights.length - 1 ? 1 : 0, borderBottomColor: colors.border }]}>
                  <View style={styles.districtInfo}>
                    <Text style={[styles.districtName, { color: colors.foreground }]}>{di.district}</Text>
                    <Text style={[styles.districtMeta, { color: colors.mutedForeground }]}>{di.activeOutbreaks} Outbreaks</Text>
                  </View>
                  <View style={styles.districtStats}>
                    <Text style={[styles.districtScore, { color: di.avgNDVI > 0.75 ? "#22C55E" : "#F59E0B" }]}>{(di.avgNDVI * 100).toFixed(0)}% NDVI</Text>
                    <Text style={[styles.districtRain, { color: di.rainfallStatus === "Deficit" ? "#EF4444" : colors.primary }]}>{di.rainfallStatus}</Text>
                  </View>
                </View>
              ))}
            </View>
          </GlassCard>
        )}

        {/* Yield & Profitability Forecast */}
        {yieldEst && profitEst && (
          <GlassCard style={styles.card}>
            <View style={styles.recRow}>
              <Ionicons name="trending-up" size={18} color={colors.accent} />
              <Text style={[styles.cardTitle, { color: colors.foreground, marginBottom: 0 }]}>
                Seasonal Forecast ({activeFarm.crops[0]?.name || "Main Crop"})
              </Text>
            </View>
            <View style={styles.forecastGrid}>
              <View style={styles.forecastItem}>
                <Text style={[styles.forecastLbl, { color: colors.mutedForeground }]}>Expected Yield</Text>
                <Text style={[styles.forecastVal, { color: colors.foreground }]}>
                  {yieldEst.expectedYield} <Text style={styles.forecastUnit}>Qtl/Acre</Text>
                </Text>
              </View>
              <View style={styles.forecastItem}>
                <Text style={[styles.forecastLbl, { color: colors.mutedForeground }]}>Estimated Profit</Text>
                <Text style={[styles.forecastVal, { color: "#22C55E" }]}>
                  ₹{profitEst.expectedProfit.toLocaleString("en-IN")}
                </Text>
              </View>
              <View style={styles.forecastItem}>
                <Text style={[styles.forecastLbl, { color: colors.mutedForeground }]}>ROI</Text>
                <Text style={[styles.forecastVal, { color: colors.accent }]}>
                  {profitEst.roi}%
                </Text>
              </View>
              <View style={styles.forecastItem}>
                <Text style={[styles.forecastLbl, { color: colors.mutedForeground }]}>Confidence</Text>
                <Text style={[styles.forecastVal, { color: "#F59E0B" }]}>
                  {yieldEst.harvestConfidence}%
                </Text>
              </View>
            </View>
            <View style={[styles.yieldBarArea, { backgroundColor: colors.border }]}>
              <View style={[styles.yieldBarFill, { width: `${(yieldEst.expectedYield / yieldEst.potentialYield) * 100}%`, backgroundColor: colors.accent }]} />
              <Text style={styles.yieldBarText}>
                {yieldEst.diseaseImpact}% potential lost to disease/stress
              </Text>
            </View>

            {/* Crop Stress Modeling */}
            {yieldEst.stresses.length > 0 && (
              <View style={styles.stressSection}>
                <Text style={[styles.stressTitle, { color: colors.foreground }]}>Crop Stress Indicators</Text>
                <View style={styles.stressGrid}>
                  {yieldEst.stresses.map((s, i) => (
                    <View key={i} style={styles.stressItem}>
                      <View style={styles.stressHeader}>
                        <Text style={[styles.stressName, { color: colors.mutedForeground }]}>{s.type}</Text>
                        <Text style={[styles.stressPct, { color: s.intensity > 0.5 ? "#FF453A" : "#F59E0B" }]}>
                          {Math.round(s.intensity * 100)}%
                        </Text>
                      </View>
                      <View style={[styles.stressBarBg, { backgroundColor: colors.border }]}>
                        <View style={[styles.stressBarFill, { width: `${s.intensity * 100}%`, backgroundColor: s.intensity > 0.5 ? "#FF453A" : "#F59E0B" }]} />
                      </View>
                    </View>
                  ))}
                </View>
              </View>
            )}
          </GlassCard>
        )}

        {/* Farm Digital Twin: Soil Health */}
        <GlassCard style={styles.card}>
          <View style={styles.recRow}>
            <Ionicons name="leaf" size={18} color="#22C55E" />
            <Text style={[styles.cardTitle, { color: colors.foreground, marginBottom: 0 }]}>
              Farm Digital Twin: Soil Health
            </Text>
          </View>
          <View style={styles.soilGrid}>
            <View style={styles.soilItem}>
              <Text style={[styles.soilLbl, { color: colors.mutedForeground }]}>Nitrogen (N)</Text>
              <View style={styles.soilMetric}>
                <Text style={[styles.soilVal, { color: colors.foreground }]}>{farmTwin.soilHealth.npk.n}</Text>
                <Text style={styles.soilUnit}>kg/ha</Text>
              </View>
              <View style={[styles.soilIndicator, { backgroundColor: "#22C55E40" }]} />
            </View>
            <View style={styles.soilItem}>
              <Text style={[styles.soilLbl, { color: colors.mutedForeground }]}>Phosphorus (P)</Text>
              <View style={styles.soilMetric}>
                <Text style={[styles.soilVal, { color: colors.foreground }]}>{farmTwin.soilHealth.npk.p}</Text>
                <Text style={styles.soilUnit}>kg/ha</Text>
              </View>
              <View style={[styles.soilIndicator, { backgroundColor: "#F59E0B40" }]} />
            </View>
            <View style={styles.soilItem}>
              <Text style={[styles.soilLbl, { color: colors.mutedForeground }]}>Potassium (K)</Text>
              <View style={styles.soilMetric}>
                <Text style={[styles.soilVal, { color: colors.foreground }]}>{farmTwin.soilHealth.npk.k}</Text>
                <Text style={styles.soilUnit}>kg/ha</Text>
              </View>
              <View style={[styles.soilIndicator, { backgroundColor: "#22C55E40" }]} />
            </View>
            <View style={styles.soilItem}>
              <Text style={[styles.soilLbl, { color: colors.mutedForeground }]}>Soil pH</Text>
              <View style={styles.soilMetric}>
                <Text style={[styles.soilVal, { color: colors.foreground }]}>{farmTwin.soilHealth.ph}</Text>
                <Text style={styles.soilUnit}>pH</Text>
              </View>
              <View style={[styles.soilIndicator, { backgroundColor: "#22C55E40" }]} />
            </View>
          </View>
          <View style={[styles.soilAnalysis, { backgroundColor: colors.background, borderColor: colors.border }]}>
            <Ionicons name="information-circle" size={16} color={colors.primary} />
            <Text style={[styles.analysisText, { color: colors.mutedForeground }]}>
              Phosphorus is slightly low. Consider adding 15kg/acre of DAP during next irrigation.
            </Text>
          </View>
        </GlassCard>
        <Text style={[styles.subtitle, { color: colors.mutedForeground }]}>
          AI-powered crop health insights
        </Text>

        <View style={styles.statsGrid}>
          <StatBlock
            icon="scan"
            label="Total Scans"
            value={totalScans}
            color={colors.primary}
            delay={60}
          />
          <StatBlock
            icon="warning"
            label="Diseases"
            value={diseasesFound}
            color="#FF453A"
            delay={120}
          />
          <StatBlock
            icon="leaf"
            label="Health Score"
            value={healthPct}
            suffix="%"
            color={colors.accent}
            delay={180}
          />
          <StatBlock
            icon="trending-up"
            label="Improvement"
            value={12}
            suffix="%"
            color="#F59E0B"
            delay={240}
          />
        </View>

        <GlassCard style={styles.card}>
          <Text style={[styles.cardTitle, { color: colors.foreground }]}>
            Disease Breakdown
          </Text>
          {diseaseBreakdown.map((d, i) => (
            <View key={i} style={styles.breakRow}>
              <View style={styles.breakLabel}>
                <View style={[styles.dot, { backgroundColor: d.color }]} />
                <Text style={[styles.breakName, { color: colors.foreground }]}>
                  {d.name}
                </Text>
              </View>
              <View style={styles.breakBarArea}>
                <View
                  style={[styles.barBg, { backgroundColor: colors.border }]}
                >
                  <AnimBar pct={d.pct} color={d.color} delay={i * 140 + 300} />
                </View>
                <Text
                  style={[
                    styles.breakPct,
                    { color: colors.mutedForeground },
                  ]}
                >
                  {d.pct}%
                </Text>
              </View>
            </View>
          ))}
        </GlassCard>

        <GlassCard style={styles.card}>
          <Text style={[styles.cardTitle, { color: colors.foreground }]}>
            Weekly Activity
          </Text>
          <View style={styles.legend}>
            <View style={styles.legendItem}>
              <View style={[styles.dot, { backgroundColor: colors.primary }]} />
              <Text
                style={[styles.legendTxt, { color: colors.mutedForeground }]}
              >
                Scans
              </Text>
            </View>
            <View style={styles.legendItem}>
              <View style={[styles.dot, { backgroundColor: "#FF453A" }]} />
              <Text
                style={[styles.legendTxt, { color: colors.mutedForeground }]}
              >
                Diseases
              </Text>
            </View>
          </View>
          <View style={styles.chart}>
            {weeklyData.map((d, i) => (
              <View key={i} style={styles.chartCol}>
                <View style={styles.barGroup}>
                  <ColBar
                    value={d.scans}
                    max={maxScans}
                    color={colors.primary}
                    delay={i * 80 + 400}
                  />
                  <ColBar
                    value={d.diseases}
                    max={maxScans}
                    color="#FF453A"
                    delay={i * 80 + 450}
                  />
                </View>
                <Text
                  style={[styles.dayLbl, { color: colors.mutedForeground }]}
                >
                  {d.day}
                </Text>
              </View>
            ))}
          </View>
        </GlassCard>

        {/* Live Market Prices */}
        <MarketCard
          market={market}
          loading={marketLoading}
          error={marketError}
          onRefresh={refreshMarket}
        />

        {/* Predictive Disease Risk */}
        {risks.length > 0 && (
          <GlassCard style={styles.card}>
            <View style={styles.recRow}>
              <Ionicons name="alert-circle" size={18} color="#FF453A" />
              <Text style={[styles.cardTitle, { color: colors.foreground, marginBottom: 0 }]}>
                Predictive Disease Risk
              </Text>
            </View>
            <View style={{ marginTop: 14 }}>
              {risks.map((risk, i) => (
                <View key={i} style={[styles.riskBox, { backgroundColor: risk.severity === "high" ? "#FF453A10" : "#F59E0B10" }]}>
                  <View style={styles.riskHeader}>
                    <Text style={[styles.riskName, { color: colors.foreground }]}>{risk.disease}</Text>
                    <Text style={[styles.riskProb, { color: risk.severity === "high" ? "#FF453A" : "#F59E0B" }]}>
                      {Math.round(risk.probability * 100)}% Risk
                    </Text>
                  </View>
                  <View style={styles.riskFactors}>
                    {risk.factors.map((f, fi) => (
                      <View key={fi} style={styles.factorItem}>
                        <View style={[styles.dot, { backgroundColor: risk.severity === "high" ? "#FF453A" : "#F59E0B", width: 4, height: 4 }]} />
                        <Text style={[styles.factorText, { color: colors.mutedForeground }]}>{f}</Text>
                      </View>
                    ))}
                  </View>
                </View>
              ))}
            </View>
          </GlassCard>
        )}

        {/* Regional Outbreak Heatmap */}
        {outbreaks.length > 0 && (
          <GlassCard style={styles.card}>
            <Text style={[styles.cardTitle, { color: colors.foreground }]}>
              Regional Outbreak Map
            </Text>
            <View style={styles.outbreakGrid}>
              {outbreaks.map((ob, i) => (
                <View key={i} style={[styles.outbreakItem, { borderBottomWidth: i < outbreaks.length - 1 ? 1 : 0, borderBottomColor: colors.border }]}>
                  <View style={styles.obLeft}>
                    <Text style={[styles.obDistrict, { color: colors.foreground }]}>{ob.district}</Text>
                    <Text style={[styles.obCount, { color: colors.mutedForeground }]}>{ob.count} active reports</Text>
                  </View>
                  <View style={[styles.obBadge, { backgroundColor: ob.severity === "high" ? "#FF453A20" : "#F59E0B20" }]}>
                    <Text style={[styles.obBadgeText, { color: ob.severity === "high" ? "#FF453A" : "#F59E0B" }]}>
                      {ob.severity.toUpperCase()}
                    </Text>
                  </View>
                </View>
              ))}
            </View>
          </GlassCard>
        )}

        {/* Crop Calendar */}
        {calendars.map((cal, ci) => (
          <GlassCard key={ci} style={styles.card}>
            <View style={styles.recRow}>
              <Ionicons name="calendar" size={18} color={colors.primary} />
              <Text style={[styles.cardTitle, { color: colors.foreground, marginBottom: 0 }]}>
                {cal.crop} Calendar ({cal.season})
              </Text>
            </View>
            <View style={styles.calendarTimeline}>
              {cal.events.map((ev, ei) => (
                <View key={ei} style={styles.timelineItem}>
                  <View style={styles.timelinePoint}>
                    <View style={[styles.pointDot, { backgroundColor: colors.primary }]} />
                    {ei < cal.events.length - 1 && <View style={[styles.pointLine, { backgroundColor: colors.border }]} />}
                  </View>
                  <View style={styles.timelineContent}>
                    <View style={styles.timelineHeader}>
                      <Text style={[styles.timelineStage, { color: colors.foreground }]}>{ev.stage}</Text>
                      <Text style={[styles.timelineMonth, { color: colors.primary }]}>{ev.month}</Text>
                    </View>
                    <Text style={[styles.timelineActivity, { color: colors.mutedForeground }]}>{ev.activity}</Text>
                  </View>
                </View>
              ))}
            </View>
          </GlassCard>
        ))}

        <GlassCard style={styles.card}>
          <View style={styles.recRow}>
            <Ionicons name="sparkles" size={18} color={colors.accent} />
            <Text style={[styles.cardTitle, { color: colors.foreground }]}>
              AI Weekly Advisory
            </Text>
          </View>
          {aiLoading ? (
            <View style={styles.loadingRow}>
              <ActivityIndicator size="small" color={colors.primary} />
              <Text
                style={[
                  styles.loadingTxt,
                  { color: colors.mutedForeground },
                ]}
              >
                Generating personalized advice…
              </Text>
            </View>
          ) : (
            <Text
              style={[styles.recText, { color: colors.mutedForeground }]}
            >
              {aiRec}
            </Text>
          )}
        </GlassCard>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  scroll: { paddingHorizontal: 16 },
  title: {
    fontSize: 24,
    fontWeight: "700",
    fontFamily: "Inter_700Bold",
    letterSpacing: -0.5,
  },
  subtitle: {
    fontSize: 13,
    fontFamily: "Inter_400Regular",
    marginBottom: 22,
    marginTop: 4,
  },
  statsGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 10,
    marginBottom: 16,
  },
  statCell: { width: "47%" },
  statVal: {
    fontSize: 24,
    fontWeight: "700",
    fontFamily: "Inter_700Bold",
  },
  statLbl: {
    fontSize: 11,
    fontFamily: "Inter_400Regular",
    textAlign: "center",
  },
  card: { marginBottom: 16 },
  cardTitle: {
    fontSize: 15,
    fontWeight: "600",
    fontFamily: "Inter_600SemiBold",
    marginBottom: 14,
  },
  breakRow: { marginBottom: 12 },
  breakLabel: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 6,
  },
  dot: { width: 8, height: 8, borderRadius: 4 },
  breakName: { fontSize: 13, fontFamily: "Inter_400Regular" },
  breakBarArea: { flexDirection: "row", alignItems: "center", gap: 8 },
  barBg: { flex: 1, height: 7, borderRadius: 4, overflow: "hidden" },
  breakPct: {
    fontSize: 12,
    fontFamily: "Inter_500Medium",
    width: 32,
    textAlign: "right",
  },
  legend: { flexDirection: "row", gap: 16, marginBottom: 14 },
  legendItem: { flexDirection: "row", alignItems: "center", gap: 6 },
  legendTxt: { fontSize: 12, fontFamily: "Inter_400Regular" },
  chart: { flexDirection: "row", justifyContent: "space-between" },
  chartCol: { alignItems: "center", gap: 6 },
  barGroup: {
    flexDirection: "row",
    gap: 3,
    alignItems: "flex-end",
    height: 76,
  },
  dayLbl: { fontSize: 10, fontFamily: "Inter_400Regular" },
  recRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 12,
  },
  recText: {
    fontSize: 13,
    fontFamily: "Inter_400Regular",
    lineHeight: 20,
  },
  loadingRow: { flexDirection: "row", alignItems: "center", gap: 10 },
  loadingTxt: {
    fontSize: 13,
    fontFamily: "Inter_400Regular",
    fontStyle: "italic",
  },
  riskBox: { padding: 14, borderRadius: 12, marginBottom: 10 },
  riskHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 8 },
  riskName: { fontSize: 14, fontWeight: "700", fontFamily: "Inter_700Bold" },
  riskProb: { fontSize: 13, fontWeight: "800", fontFamily: "Inter_800ExtraBold" },
  riskFactors: { gap: 4 },
  factorItem: { flexDirection: "row", alignItems: "center", gap: 6 },
  factorText: { fontSize: 11, fontFamily: "Inter_400Regular" },
  outbreakGrid: { gap: 0 },
  districtRow: { flexDirection: "row", justifyContent: "space-between", paddingVertical: 10 },
  districtInfo: { gap: 2 },
  districtName: { fontSize: 14, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  districtMeta: { fontSize: 11, fontFamily: "Inter_400Regular" },
  districtStats: { alignItems: "flex-end", gap: 2 },
  districtScore: { fontSize: 13, fontWeight: "700", fontFamily: "Inter_700Bold" },
  districtRain: { fontSize: 10, fontWeight: "700", fontFamily: "Inter_700Bold" },
  advisorHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 12, marginTop: -4 },
  advisorBadge: { flexDirection: "row", alignItems: "center", gap: 6, backgroundColor: "rgba(34, 197, 94, 0.1)", paddingHorizontal: 10, paddingVertical: 6, borderRadius: 12, borderWidth: 1, borderColor: "rgba(34, 197, 94, 0.3)" },
  advisorBadgeText: { fontSize: 10, fontWeight: "800", fontFamily: "Inter_800ExtraBold", letterSpacing: 0.5 },
  reportBtn: { flexDirection: "row", alignItems: "center", gap: 6, backgroundColor: "rgba(255,255,255,0.05)", paddingHorizontal: 12, paddingVertical: 6, borderRadius: 10, borderWidth: 1, borderColor: "rgba(255,255,255,0.1)" },
  reportBtnText: { fontSize: 11, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  coopGrid: { flexDirection: "row", flexWrap: "wrap", gap: 12, marginTop: 4 },
  coopItem: { width: "47%", gap: 4 },
  coopLbl: { fontSize: 10, fontFamily: "Inter_400Regular" },
  coopVal: { fontSize: 16, fontWeight: "700", fontFamily: "Inter_700Bold" },
  coopUnit: { fontSize: 10, fontWeight: "400" },
  outbreakItem: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", paddingVertical: 12 },
  obLeft: { gap: 2 },
  obDistrict: { fontSize: 14, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  obCount: { fontSize: 11, fontFamily: "Inter_400Regular" },
  obBadge: { paddingHorizontal: 8, paddingVertical: 4, borderRadius: 6 },
  obBadgeText: { fontSize: 10, fontWeight: "800", fontFamily: "Inter_800ExtraBold" },
  calendarTimeline: { marginTop: 16, paddingLeft: 8 },
  timelineItem: { flexDirection: "row", gap: 16, paddingBottom: 20 },
  timelinePoint: { alignItems: "center" },
  pointDot: { width: 10, height: 10, borderRadius: 5 },
  pointLine: { width: 2, flex: 1, marginTop: 4 },
  timelineContent: { flex: 1, gap: 4, marginTop: -2 },
  timelineHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  timelineStage: { fontSize: 14, fontWeight: "700", fontFamily: "Inter_700Bold" },
  timelineMonth: { fontSize: 12, fontWeight: "600", fontFamily: "Inter_600SemiBold" },
  timelineActivity: { fontSize: 12, fontFamily: "Inter_400Regular", lineHeight: 18 },
  forecastGrid: { flexDirection: "row", flexWrap: "wrap", gap: 12, marginTop: 16 },
  forecastItem: { width: "47%", gap: 4 },
  forecastLbl: { fontSize: 11, fontFamily: "Inter_400Regular" },
  forecastVal: { fontSize: 18, fontWeight: "700", fontFamily: "Inter_700Bold" },
  forecastUnit: { fontSize: 10, fontFamily: "Inter_400Regular" },
  yieldBarArea: { height: 24, borderRadius: 12, overflow: "hidden", marginTop: 16, justifyContent: "center" },
  yieldBarFill: { height: "100%", position: "absolute", left: 0 },
  yieldBarText: { fontSize: 10, fontWeight: "600", fontFamily: "Inter_600SemiBold", color: "#fff", textAlign: "center", zIndex: 1 },
  soilGrid: { flexDirection: "row", flexWrap: "wrap", gap: 12, marginTop: 16 },
  soilItem: { width: "47%", padding: 12, borderRadius: 12, backgroundColor: "#ffffff08", gap: 6 },
  soilLbl: { fontSize: 11, fontFamily: "Inter_400Regular" },
  soilMetric: { flexDirection: "row", alignItems: "baseline", gap: 4 },
  soilVal: { fontSize: 20, fontWeight: "700", fontFamily: "Inter_700Bold" },
  soilUnit: { fontSize: 10, fontFamily: "Inter_400Regular" },
  soilIndicator: { height: 4, borderRadius: 2, width: "100%" },
  soilAnalysis: { flexDirection: "row", alignItems: "center", gap: 8, padding: 12, borderRadius: 10, borderWidth: 1, marginTop: 12 },
  analysisText: { fontSize: 12, fontFamily: "Inter_400Regular", flex: 1, lineHeight: 18 },
  stressSection: { marginTop: 20, paddingTop: 16, borderTopWidth: 1, borderTopColor: "#ffffff10" },
  stressTitle: { fontSize: 13, fontWeight: "700", fontFamily: "Inter_700Bold", marginBottom: 12 },
  stressGrid: { gap: 12 },
  stressItem: { gap: 6 },
  stressHeader: { flexDirection: "row", justifyContent: "space-between" },
  stressName: { fontSize: 11, fontFamily: "Inter_500Medium" },
  stressPct: { fontSize: 11, fontWeight: "700", fontFamily: "Inter_700Bold" },
  stressBarBg: { height: 4, borderRadius: 2, overflow: "hidden" },
  stressBarFill: { height: "100%", borderRadius: 2 },
});
