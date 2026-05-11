import { useCallback, useEffect, useRef, useState } from "react";
import type { WeatherData } from "./useWeather";

const API_BASE = process.env["EXPO_PUBLIC_DOMAIN"]
  ? `https://${process.env["EXPO_PUBLIC_DOMAIN"]}`
  : "";

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
  const load = useCallback(async () => {
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
      const res = await fetch(`${API_BASE}/api/alerts?${qs}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = (await res.json()) as { alerts: FarmingAlert[] };
      if (mountedRef.current) {
        setAlerts(data.alerts ?? []);
        setLoading(false);
      }
    } catch (_) {
      if (mountedRef.current) setLoading(false);
    }
  }, []); // intentionally stable — all values come from refs

  // Start polling once weather first becomes available
  const weatherReady = weather !== null;
  useEffect(() => {
    mountedRef.current = true;
    if (!weatherReady) return;

    load();
    const id = setInterval(load, POLL_INTERVAL_MS);
    return () => {
      clearInterval(id);
      mountedRef.current = false;
    };
  }, [weatherReady, load]);

  return { alerts, loading, refresh: load };
}
