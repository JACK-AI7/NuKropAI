import type { Request, Response } from "express";
import { Router } from "express";
import { openai } from "@workspace/integrations-openai-ai-server";

const marketRouter = Router();

interface MarketCrop {
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

interface MarketResponse {
  crops: MarketCrop[];
  marketSentiment: "bullish" | "bearish" | "neutral";
  topGainer: string;
  topLoser: string;
}

// Realistic fallback prices for Telangana/AP region (May — pre-Kharif season)
const FALLBACK: MarketResponse = {
  crops: [
    { name: "Rice", nameHi: "चावल", nameTe: "వరి", emoji: "🌾", price: 2285, unit: "per quintal", change: 35, changePct: 1.56, trend: "up", weekHigh: 2310, weekLow: 2245, market: "Kurnool, AP" },
    { name: "Wheat", nameHi: "गेहूं", nameTe: "గోధుమ", emoji: "🌾", price: 2215, unit: "per quintal", change: -15, changePct: -0.67, trend: "down", weekHigh: 2240, weekLow: 2195, market: "Hyderabad, TS" },
    { name: "Cotton", nameHi: "कपास", nameTe: "పత్తి", emoji: "🌿", price: 7650, unit: "per quintal", change: 120, changePct: 1.59, trend: "up", weekHigh: 7700, weekLow: 7480, market: "Warangal, TS" },
    { name: "Maize", nameHi: "मक्का", nameTe: "మొక్కజొన్న", emoji: "🌽", price: 2090, unit: "per quintal", change: 0, changePct: 0.0, trend: "stable", weekHigh: 2110, weekLow: 2060, market: "Nizamabad, TS" },
    { name: "Tomato", nameHi: "टमाटर", nameTe: "టమాటో", emoji: "🍅", price: 1450, unit: "per quintal", change: 210, changePct: 16.93, trend: "up", weekHigh: 1500, weekLow: 1100, market: "Kurnool, AP" },
    { name: "Onion", nameHi: "प्याज", nameTe: "ఉల్లిపాయ", emoji: "🧅", price: 1080, unit: "per quintal", change: -65, changePct: -5.68, trend: "down", weekHigh: 1180, weekLow: 1020, market: "Kurnool, AP" },
    { name: "Chilli", nameHi: "मिर्च", nameTe: "మిరప", emoji: "🌶️", price: 12400, unit: "per quintal", change: 350, changePct: 2.9, trend: "up", weekHigh: 12500, weekLow: 11800, market: "Guntur, AP" },
    { name: "Sunflower", nameHi: "सूरजमुखी", nameTe: "పొద్దుతిరుగుడు", emoji: "🌻", price: 6250, unit: "per quintal", change: -80, changePct: -1.26, trend: "down", weekHigh: 6380, weekLow: 6150, market: "Adilabad, TS" },
    { name: "Sugarcane", nameHi: "गन्ना", nameTe: "చెరకు", emoji: "🎋", price: 315, unit: "per quintal", change: 0, changePct: 0.0, trend: "stable", weekHigh: 315, weekLow: 315, market: "Nizamabad, TS" },
    { name: "Soybean", nameHi: "सोयाबीन", nameTe: "సోయాబీన్", emoji: "🫘", price: 4780, unit: "per quintal", change: 95, changePct: 2.03, trend: "up", weekHigh: 4820, weekLow: 4650, market: "Hyderabad, TS" },
  ],
  marketSentiment: "bullish",
  topGainer: "Tomato",
  topLoser: "Onion",
};

function parseCrops(raw: string): MarketResponse | null {
  try {
    const objMatch = raw.match(/\{[\s\S]*\}/);
    if (!objMatch) return null;
    const data = JSON.parse(objMatch[0]) as MarketResponse;
    if (!Array.isArray(data.crops) || data.crops.length === 0) return null;
    return data;
  } catch {
    return null;
  }
}

marketRouter.get("/market", async (req: Request, res: Response) => {
  const region = (req.query["region"] as string | undefined) ?? "Telangana";
  const month = new Date().toLocaleString("en-IN", { month: "long" });
  const today = new Date().toISOString().split("T")[0];

  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      max_completion_tokens: 1400,
      messages: [
        {
          role: "system",
          content: `You are an Indian agricultural market data system. Generate realistic Indian mandi crop prices as JSON.

Return ONLY this JSON object (no markdown, no explanation):
{"crops":[{"name":"Rice","nameHi":"चावल","nameTe":"వరి","emoji":"🌾","price":2285,"unit":"per quintal","change":35,"changePct":1.56,"trend":"up","weekHigh":2310,"weekLow":2245,"market":"Kurnool, AP"},...],"marketSentiment":"bullish","topGainer":"Rice","topLoser":"Onion"}

Include all 10 crops: Rice, Wheat, Cotton, Maize, Tomato, Onion, Chilli, Sunflower, Sugarcane, Soybean.
Price ranges: Rice 2000-3500, Wheat 2000-2700, Cotton 6000-9500, Maize 1800-2500, Tomato 500-3500, Onion 800-3500, Chilli 8000-18000, Sunflower 5500-7500, Sugarcane 290-370, Soybean 3800-5800. All per quintal in INR.`,
        },
        {
          role: "user",
          content: `Market prices for ${region}, ${today} (${month}). Return JSON only.`,
        },
      ],
    });

    const raw = completion.choices[0]?.message?.content ?? "";
    const parsed = parseCrops(raw);

    if (!parsed) {
      req.log.warn({ raw: raw.slice(0, 200) }, "Market AI response not parseable, using fallback");
      res.json({ ...FALLBACK, region, updatedAt: new Date().toISOString(), isFallback: true });
      return;
    }

    const crops = parsed.crops.map((c) => ({
      name: c.name ?? "Unknown",
      nameHi: c.nameHi ?? "",
      nameTe: c.nameTe ?? "",
      emoji: c.emoji ?? "🌾",
      price: Number(c.price) || 0,
      unit: "per quintal",
      change: Number(c.change) || 0,
      changePct: parseFloat(Number(c.changePct).toFixed(2)),
      trend: (["up", "down", "stable"].includes(c.trend) ? c.trend : "stable") as MarketCrop["trend"],
      weekHigh: Number(c.weekHigh) || Number(c.price) || 0,
      weekLow: Number(c.weekLow) || Number(c.price) || 0,
      market: c.market ?? `${region} Mandi`,
    }));

    res.json({
      crops,
      marketSentiment: parsed.marketSentiment ?? "neutral",
      topGainer: parsed.topGainer ?? "",
      topLoser: parsed.topLoser ?? "",
      region,
      updatedAt: new Date().toISOString(),
    });
  } catch (err) {
    req.log.error({ err }, "Market data generation failed, using fallback");
    res.json({ ...FALLBACK, region, updatedAt: new Date().toISOString(), isFallback: true });
  }
});

export default marketRouter;
