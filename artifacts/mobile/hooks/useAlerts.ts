import { useCallback, useEffect, useRef, useState } from "react";
import { AppState, type AppStateStatus } from "react-native";
import { useNavigation } from "expo-router";
import { request } from "@/utils/api";
import type { WeatherData } from "./useWeather";

const POLL_INTERVAL_MS = 30 * 60 * 1000; // 30 minutes

export interface FarmingAlert {
  id: string;
  type: "warning" | "danger" | "tip" | "success";
  title: string;
  message: string;
  crop: string | null;
  urgency: "high" | "medium" | "low";
  icon: string;
}

export function useAlerts(
  lat: number,
  lon: number,
  locationCity: string,
  weather: WeatherData | null,
) {
  const [alerts, setAlerts] = useState<FarmingAlert[]>([]);
  const [loading, setLoading] = useState(true);
  const mountedRef = useRef(true);
  const navigation = useNavigation();
  const [isFocused, setIsFocused] = useState(true);
  const appState = useRef(AppState.currentState);

  // Keep latest values in refs so the stable load callback always reads fresh data
  const latRef = useRef(lat);
  const lonRef = useRef(lon);
  const cityRef = useRef(locationCity);
  const weatherRef = useRef<WeatherData | null>(weather);
  latRef.current = lat;
  lonRef.current = lon;
  cityRef.current = locationCity;
  weatherRef.current = weather;

  // Stable callback — reads all live values from refs
  const load = useCallback(async (signal?: AbortSignal) => {
    const w = weatherRef.current;
    const params: Record<string, string> = {
      lat: latRef.current.toFixed(4),
      lon: lonRef.current.toFixed(4),
      city: cityRef.current,
    };
    if (w?.current) {
      params["condition"] = w.current.condition;
      params["temp"] = w.current.temp.toString();
      params["humidity"] = w.current.humidity.toString();
      params["rainChance"] = w.current.rainChance.toString();
      params["windSpeed"] = w.current.windSpeed.toString();
      params["uv"] = w.current.uvIndex.toString();
    }

    try {
      const qs = new URLSearchParams(params).toString();
      const data = await request<{ alerts: FarmingAlert[] }>(`/api/alerts?${qs}`, { signal });
      if (mountedRef.current) {
        setAlerts(data.alerts ?? []);
        setLoading(false);
      }
    } catch (e: any) {
      if (e.name === "AbortError" && signal?.aborted) return;
      if (mountedRef.current) setLoading(false);
    }
  }, []); // intentionally stable — all values come from refs

  useEffect(() => {
    const unsubFocus = navigation.addListener("focus", () => setIsFocused(true));
    const unsubBlur = navigation.addListener("blur", () => setIsFocused(false));
    return () => {
      unsubFocus();
      unsubBlur();
    };
  }, [navigation]);

  // Start polling once weather first becomes available
  const weatherReady = weather !== null;
  useEffect(() => {
    mountedRef.current = true;
    if (!weatherReady) return;

    const controller = new AbortController();

    const startPolling = () => {
      const id = setInterval(() => {
        if (appState.current === "active" && mountedRef.current) {
          load();
        }
      }, POLL_INTERVAL_MS);
      return id;
    };

    const handleAppStateChange = (nextAppState: AppStateStatus) => {
      appState.current = nextAppState;
      if (nextAppState === "active" && isFocused) {
        load();
      }
    };

    const sub = AppState.addEventListener("change", handleAppStateChange);

    let intervalId: ReturnType<typeof setInterval> | null = null;
    if (isFocused) {
      load(controller.signal);
      intervalId = startPolling();
    }

    return () => {
      controller.abort();
      if (intervalId) clearInterval(intervalId);
      sub.remove();
      mountedRef.current = false;
    };
  }, [weatherReady, load, isFocused]);

  return { alerts, loading, refresh: load };
}
