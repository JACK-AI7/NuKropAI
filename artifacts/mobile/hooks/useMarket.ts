import { useCallback, useEffect, useRef, useState } from "react";
import { AppState, type AppStateStatus } from "react-native";
import { useNavigation } from "expo-router";
import { request } from "@/utils/api";

const POLL_INTERVAL_MS = 30 * 60 * 1000; // 30 minutes

export interface MarketCrop {
  name: string;
  nameHi: string;
  nameTe: string;
  emoji: string;
  price: number;
  unit: string;
  change: number;
  changePct: number;
  trend: "up" | "down" | "stable";
  weekHigh: number;
  weekLow: number;
  market: string;
}

export interface MarketData {
  crops: MarketCrop[];
  marketSentiment: "bullish" | "bearish" | "neutral";
  topGainer: string;
  topLoser: string;
  region: string;
  updatedAt: string;
}

export function useMarket(region: string) {
  const [market, setMarket] = useState<MarketData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const mountedRef = useRef(true);
  const navigation = useNavigation();
  const [isFocused, setIsFocused] = useState(true);
  const appState = useRef(AppState.currentState);

  const load = useCallback(async (signal?: AbortSignal) => {
    let delay = 2000;
    let attempts = 0;
    const maxAttempts = 3;

    while (attempts < maxAttempts) {
      try {
        const data = await request<MarketData>(
          `/api/market?region=${encodeURIComponent(region)}`,
          { signal }
        );
        if (mountedRef.current) {
          setMarket(data);
          setError(null);
        }
        return; // Success
      } catch (e: any) {
        if (e.name === "AbortError" && signal?.aborted) return;
        attempts++;
        if (attempts >= maxAttempts) {
          if (mountedRef.current) setError(e.message || "Market data temporarily unavailable");
          break;
        }
        // Wait before retry
        await new Promise(resolve => setTimeout(resolve, delay));
        delay *= 2;
      } finally {
        if (mountedRef.current && (attempts >= maxAttempts || attempts === 0)) {
          setLoading(false);
        }
      }
    }
  }, [region]);

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

  return { market, loading, error, refresh: load };
}
