import { useCallback, useEffect, useRef, useState } from "react";

const API_BASE = process.env["EXPO_PUBLIC_DOMAIN"]
  ? `https://${process.env["EXPO_PUBLIC_DOMAIN"]}`
  : "";

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

  const load = useCallback(async () => {
    try {
      const res = await fetch(
        `${API_BASE}/api/market?region=${encodeURIComponent(region)}`,
      );
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = (await res.json()) as MarketData;
      if (mountedRef.current) {
        setMarket(data);
        setError(null);
      }
    } catch (_) {
      if (mountedRef.current) setError("Market data temporarily unavailable");
    } finally {
      if (mountedRef.current) setLoading(false);
    }
  }, [region]);

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

  return { market, loading, error, refresh: load };
}
