import type { Request, Response } from "express";
import { Router } from "express";
import { openai } from "@workspace/integrations-openai-ai-server";

const scanRouter = Router();

const SYSTEM_PROMPT = `You are an expert agricultural AI system specializing in plant pathology and crop disease detection for Indian farmers. Analyze the provided crop or plant image with high precision.

Return ONLY valid JSON — no markdown fences, no explanation outside the JSON object:
{
  "disease": "string (specific disease name with scientific name in parentheses, or 'Healthy Crop' if no disease found)",
  "confidence": number (0.0 to 1.0 — use 0.85–0.98 for clear signs, 0.60–0.84 for uncertain),
  "severity": "low" | "medium" | "high",
  "affectedArea": number (integer 0–100, estimated % of visible plant affected),
  "isHealthy": boolean,
  "recommendations": ["string", "string", "string"] (3–4 specific, actionable steps),
  "treatments": ["string"] (specific product names with exact dosages for Indian markets — e.g., "Mancozeb 75 WP @ 2.5g/L water every 7 days"; empty array if healthy),
  "explanation": "string (2–3 sentences describing the diagnosis, visible symptoms, and prognosis)"
}

Rules:
- Healthy plant → isHealthy:true, disease:"Healthy Crop", severity:"low", affectedArea:0, treatments:[]
- Not a plant → disease:"No crop detected", confidence:0.1, isHealthy:true, affectedArea:0
- Diagnose specifically: prefer "Early Blight (Alternaria solani)" over just "Blight"
- recommendations always include monitoring, cultural, and chemical options
- treatments always include exact quantities suitable for Indian markets`;

interface ScanAnalysis {
  disease: string;
  confidence: number;
  severity: "low" | "medium" | "high";
  affectedArea: number;
  isHealthy: boolean;
  recommendations: string[];
  treatments: string[];
  explanation: string;
}

scanRouter.post("/scan", async (req: Request, res: Response) => {
  const { imageBase64 } = req.body as { imageBase64?: string };

  if (!imageBase64?.trim()) {
    res.status(400).json({ error: "imageBase64 is required" });
    return;
  }

  const mimeType =
    imageBase64.startsWith("/9j/") || imageBase64.startsWith("_9j_")
      ? "image/jpeg"
      : imageBase64.startsWith("iVBOR")
      ? "image/png"
      : imageBase64.startsWith("UklGR")
      ? "image/webp"
      : "image/jpeg";

  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      max_completion_tokens: 1024,
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        {
          role: "user",
          content: [
            {
              type: "text",
              text: "Analyze this crop/plant image for diseases, pests, or health issues. Return the JSON analysis only.",
            },
            {
              type: "image_url",
              image_url: {
                url: `data:${mimeType};base64,${imageBase64}`,
                detail: "high",
              },
            },
          ],
        },
      ],
    });

    const raw = completion.choices[0]?.message?.content ?? "{}";
    const jsonMatch = raw.match(/\{[\s\S]*\}/);
    if (!jsonMatch) throw new Error("No JSON in AI response");

    const a = JSON.parse(jsonMatch[0]) as ScanAnalysis;

    res.json({
      disease: a.disease ?? "Unknown",
      confidence: Math.min(99, Math.max(1, Math.round((a.confidence ?? 0.5) * 100))),
      severity: (["low", "medium", "high"].includes(a.severity) ? a.severity : "medium") as ScanAnalysis["severity"],
      affectedArea: Math.min(100, Math.max(0, Math.round(a.affectedArea ?? 0))),
      isHealthy: a.isHealthy ?? false,
      recommendations: Array.isArray(a.recommendations) ? a.recommendations.slice(0, 5) : [],
      treatments: Array.isArray(a.treatments) ? a.treatments.slice(0, 4) : [],
      explanation: a.explanation ?? "",
    });
  } catch (err) {
    req.log.error({ err }, "Crop scan analysis failed");
    res.status(500).json({ error: "Analysis failed. Please try again with a clearer photo." });
  }
});

export default scanRouter;
