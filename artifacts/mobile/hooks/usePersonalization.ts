import { useState, useEffect, useCallback } from "react";
import { useApp } from "@/contexts/AppContext";
import { useAuth } from "@/contexts/AuthContext";
import { request } from "@/utils/api";

export interface PersonalizedInsight {
  id: string;
  type: "recommendation" | "warning" | "tip";
  title: string;
  message: string;
  crop?: string;
  priority: number;
}

export function usePersonalization() {
  const { user } = useAuth();
  const { cropsGrown, farmLocation, scanHistory, language } = useApp();
  const [personalInsights, setPersonalInsights] = useState<PersonalizedInsight[]>([]);
  const [loading, setLoading] = useState(false);

  const generateInsights = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    try {
      // Send context to AI to generate personalized guidance
      const data = await request<PersonalizedInsight[]>("/api/personalize", {
        method: "POST",
        body: JSON.stringify({
          userId: user.uid,
          crops: cropsGrown,
          location: farmLocation,
          history: scanHistory.slice(0, 10), // Send last 10 scans for context
          language,
        }),
      });
      setPersonalInsights(data);
    } catch (error) {
      console.error("Personalization error:", error);
      // Fallback insights
      setPersonalInsights([
        {
          id: "p1",
          type: "recommendation",
          title: `Optimizing ${cropsGrown[0] || "Crop"} Yield`,
          message: `Based on your recent scans in ${farmLocation}, we recommend adjusting nitrogen levels for the upcoming week.`,
          priority: 1,
        }
      ]);
    } finally {
      setLoading(false);
    }
  }, [user, cropsGrown, farmLocation, scanHistory, language]);

  useEffect(() => {
    generateInsights();
  }, [generateInsights]);

  return { personalInsights, loading, refresh: generateInsights };
}
