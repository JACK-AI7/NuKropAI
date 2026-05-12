import { useCallback, useEffect, useRef, useState } from "react";
import { AppState, type AppStateStatus } from "react-native";
import { useNavigation } from "expo-router";
import { request } from "@/utils/api";

const POLL_INTERVAL_MS = 10 * 60 * 1000; // 10 minutes

export interface WeatherCurrent {
  temp: number;
  feelsLike: number;
  humidity: number;
  windSpeed: number;
  uvIndex: number;
  rain: number;
  farmingTip: string;
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
  const navigation = useNavigation();
  const [isFocused, setIsFocused] = useState(true); // Default to true, listener will update
  const appState = useRef(AppState.currentState);

  const load = useCallback(async (signal?: AbortSignal) => {
    let delay = 2000;
    let attempts = 0;
    const maxAttempts = 3;

    while (attempts < maxAttempts) {
      try {
        const data = await request<WeatherData>(
          `/api/weather?lat=${lat.toFixed(4)}&lon=${lon.toFixed(4)}`,
          { signal }
        );
        if (mountedRef.current) {
          setWeather(data);
          setError(null);
        }
        return;
      } catch (e: any) {
        if (e.name === "AbortError" && signal?.aborted) return;
        attempts++;
        if (attempts >= maxAttempts) {
          if (mountedRef.current) {
            setError(e.message || "Weather data temporarily unavailable");
          }
          break;
        }
        await new Promise((resolve) => setTimeout(resolve, delay));
        delay *= 2;
      } finally {
        if (mountedRef.current && (attempts >= maxAttempts || attempts === 0)) {
          setLoading(false);
        }
      }
    }
  }, [lat, lon]);

  useEffect(() => {
    const unsubFocus = navigation.addListener("focus", () => setIsFocused(true));
    const unsubBlur = navigation.addListener("blur", () => setIsFocused(false));
    return () => {
      unsubFocus();
      unsubBlur();
    };
  }, [navigation]);

  useEffect(() => {
    mountedRef.current = true;
    const controller = new AbortController();

    const startPolling = () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
      intervalRef.current = setInterval(() => {
        if (appState.current === "active" && mountedRef.current) {
          load();
        }
      }, POLL_INTERVAL_MS);
    };

    const handleAppStateChange = (nextAppState: AppStateStatus) => {
      appState.current = nextAppState;
      if (nextAppState === "active" && isFocused) {
        load();
      }
    };

    const sub = AppState.addEventListener("change", handleAppStateChange);

    if (isFocused) {
      setLoading(true);
      load(controller.signal);
      startPolling();
    }
    
    return () => {
      mountedRef.current = false;
      controller.abort();
      sub.remove();
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [load, isFocused]);

  return { weather, loading, error, refresh: load };
}
