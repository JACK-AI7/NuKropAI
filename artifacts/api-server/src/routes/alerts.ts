import type { Request, Response } from "express";
import { Router } from "express";
import { openai } from "@workspace/integrations-openai-ai-server";

const alertsRouter = Router();

interface FarmingAlert {
  id: string;
  type: "warning" | "danger" | "tip" | "success";
  title: string;
  message: string;
  crop: string | null;
  urgency: "high" | "medium" | "low";
  icon: string;
}

// Seasonal fallback alerts — May, pre-Kharif, hot/dry conditions in India
const FALLBACK_ALERTS: FarmingAlert[] = [
  {
    id: "fa1",
    type: "warning",
    title: "Heat Stress Alert",
    message: "Temperatures expected above 38°C. Irrigate cotton and chilli crops daily before 8 AM to prevent wilting and boll drop.",
    crop: "Cotton",
    urgency: "high",
    icon: "thermometer",
  },
  {
    id: "fa2",
    type: "tip",
    title: "Pre-Kharif Soil Prep",
    message: "Ideal window for deep ploughing and FYM incorporation before Kharif sowing. Apply 5 tonnes farmyard manure per acre.",
    crop: null,
    urgency: "medium",
    icon: "leaf",
  },
  {
    id: "fa3",
    type: "success",
    title: "Cotton Sowing Window",
    message: "Late May is optimal for cotton sowing in Telangana. Bunny BG-II hybrid recommended — 1.5 kg seed per acre with 30×60 cm spacing.",
    crop: "Cotton",
    urgency: "medium",
    icon: "sunny",
  },
  {
    id: "fa4",
    type: "warning",
    title: "Irrigation System Check",
    message: "Dry conditions ahead. Inspect drip and sprinkler systems now — repair any leaks before Kharif season starts next month.",
    crop: null,
    urgency: "medium",
    icon: "water",
  },
];

function parseAlerts(raw: string): FarmingAlert[] | null {
  try {
    // Try JSON object first
    const objMatch = raw.match(/\{[\s\S]*\}/);
    if (objMatch) {
      const data = JSON.parse(objMatch[0]) as { alerts?: FarmingAlert[] };
      if (Array.isArray(data.alerts) && data.alerts.length > 0) return data.alerts;
    }
    // Try JSON array
    const arrMatch = raw.match(/\[[\s\S]*\]/);
    if (arrMatch) {
      const arr = JSON.parse(arrMatch[0]) as FarmingAlert[];
      if (Array.isArray(arr) && arr.length > 0) return arr;
    }
    return null;
  } catch {
    return null;
  }
}

alertsRouter.get("/alerts", async (req: Request, res: Response) => {
  const {
    condition,
    temp,
    humidity,
    rainChance,
    windSpeed,
    uv,
    city,
    lat,
    lon,
  } = req.query as Record<string, string | undefined>;

  const month = new Date().toLocaleString("en-IN", { month: "long" });
  const day = new Date().toLocaleDateString("en-IN", { weekday: "long", day: "numeric" });

  const weatherLine = condition
    ? `Weather: ${condition}, ${temp}°C, humidity ${humidity}%, rain ${rainChance}%, wind ${windSpeed} km/h, UV ${uv}.`
    : `Location: ${city ?? "India"} (${lat ?? "17.38"}N, ${lon ?? "78.49"}E).`;

  const userMsg = `${weatherLine} Location: ${city ?? "Telangana, India"}. Date: ${day} ${month}. Generate 3-4 farming alerts for Indian farmers. Return JSON only.`;

  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-5-mini",
      max_completion_tokens: 900,
      messages: [
        {
          role: "system",
          content: `Generate farming alerts for Indian farmers as a JSON object. Return ONLY this structure (no markdown):
{"alerts":[{"id":"a1","type":"warning","title":"Short title","message":"Specific actionable message for farmers.","crop":"CropName or null","urgency":"high","icon":"thermometer"},{"id":"a2","type":"tip","title":"Short title","message":"Specific advice.","crop":null,"urgency":"medium","icon":"leaf"},{"id":"a3","type":"success","title":"Short title","message":"Positive news.","crop":null,"urgency":"low","icon":"sunny"}]}

type values: "warning" "danger" "tip" "success". icon values: "warning" "rainy" "leaf" "thermometer" "bug" "water" "sunny" "alert-circle" "trending-up". Always generate 3-4 alerts.`,
        },
        { role: "user", content: userMsg },
      ],
    });

    const raw = completion.choices[0]?.message?.content ?? "";
    const alerts = parseAlerts(raw);

    if (!alerts) {
      req.log.warn({ raw: raw.slice(0, 300) }, "Alerts AI response not parseable, using fallback");
      res.json({ alerts: FALLBACK_ALERTS, updatedAt: new Date().toISOString(), isFallback: true });
      return;
    }

    const validated = alerts.slice(0, 5).map((a, i) => ({
      id: a.id ?? `alert-${i + 1}`,
      type: (["warning", "danger", "tip", "success"].includes(a.type) ? a.type : "tip") as FarmingAlert["type"],
      title: a.title ?? "Farm Alert",
      message: a.message ?? "",
      crop: a.crop ?? null,
      urgency: (["high", "medium", "low"].includes(a.urgency) ? a.urgency : "medium") as FarmingAlert["urgency"],
      icon: a.icon ?? "leaf",
    }));

    res.json({ alerts: validated, updatedAt: new Date().toISOString() });
  } catch (err) {
    req.log.error({ err }, "Alert generation failed, using fallback");
    res.json({ alerts: FALLBACK_ALERTS, updatedAt: new Date().toISOString(), isFallback: true });
  }
});

export default alertsRouter;
