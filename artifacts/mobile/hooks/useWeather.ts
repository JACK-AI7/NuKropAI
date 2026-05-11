import { useCallback, useEffect, useRef, useState } from "react";

const API_BASE = process.env["EXPO_PUBLIC_DOMAIN"]
  ? `https://${process.env["EXPO_PUBLIC_DOMAIN"]}`
  : "";

const POLL_INTERVAL_MS = 10 * 60 * 1000; // 10 minutes

export interface WeatherCurrent {
  temp: number;
  feelsLike: number;
  humidity: number;
  windSpeed: number;
  uvIndex: number;
  precipitation: number;
  cloudCover: number;
  pressure: number;
  condition: string;
  icon: string;
  rainChance: number;
}

export interface WeatherDay {
  date: string;
  maxTemp: number;
  minTemp: number;
  condition: string;
  icon: string;
  precipitationMm: number;
  precipitationPct: number;
  uvMax: number;
}

export interface HourlyPoint {
  time: string;
  temp: number;
  precipPct: number;
  icon: string;
}

export interface WeatherData {
  latitude: number;
  longitude: number;
  current: WeatherCurrent;
  forecast: WeatherDay[];
  hourly: HourlyPoint[];
  farmingTip: string;
  sunrise: string;
  sunset: string;
  updatedAt: string;
}

export function useWeather(lat: number, lon: number) {
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const mountedRef = useRef(true);

  const load = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/api/weather?lat=${lat.toFixed(4)}&lon=${lon.toFixed(4)}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = (await res.json()) as WeatherData;
      if (mountedRef.current) {
        setWeather(data);
        setError(null);
      }
    } catch (e) {
      if (mountedRef.current) {
        setError("Weather data temporarily unavailable");
      }
    } finally {
      if (mountedRef.current) setLoading(false);
    }
  }, [lat, lon]);

  useEffect(() => {
    mountedRef.current = true;
    setLoading(true);
    load();
    intervalRef.current = setInterval(load, POLL_INTERVAL_MS);
    return () => {
      mountedRef.current = false;
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [load]);

  return { weather, loading, error, refresh: load };
}
