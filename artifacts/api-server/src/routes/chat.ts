import type { Request, Response } from "express";
import { Router } from "express";
import { openai } from "@workspace/integrations-openai-ai-server";

const chatRouter = Router();

const SYSTEM_PROMPTS: Record<string, string> = {
  en: `You are NuKropAI, an expert AI farming assistant for Indian farmers. Provide precise, actionable advice about:
- Crop diseases: detection, treatment, prevention with specific product names and dosages
- Pest management and integrated pest management (IPM) strategies
- Soil health, fertilizer recommendations with NPK ratios and quantities per acre
- Weather-based farming decisions (sowing, irrigation, spraying windows)
- Government schemes, subsidies, and PM-KISAN benefits
- Crop calendar, intercropping, and yield optimization

Keep responses concise (under 200 words), practical, farmer-friendly, and specific. Always include product names and quantities when recommending treatments. Respond in English only.`,

  hi: `आप NuKropAI हैं, भारतीय किसानों के लिए विशेषज्ञ AI कृषि सहायक। सटीक, व्यावहारिक सलाह दें:
- फसल रोग, कीट, खरपतवार प्रबंधन
- उर्वरक अनुशंसाएं (मात्रा प्रति एकड़ सहित)
- मौसम-आधारित खेती निर्णय
- सरकारी योजनाएं और PM-KISAN
- फसल कैलेंडर और उपज अनुकूलन
संक्षिप्त (200 शब्दों से कम), व्यावहारिक उत्तर दें। हिन्दी में उत्तर दें।`,

  te: `మీరు NuKropAI, భారతీయ రైతులకు నిపుణ AI వ్యవసాయ సహాయకుడు. ఖచ్చితమైన, ఆచరణీయ సలహాలు ఇవ్వండి:
- పంట వ్యాధులు, చీడలు, కలుపు నిర్వహణ
- ఎరువుల సిఫార్సులు (ఎకరాకు పరిమాణాలతో)
- వాతావరణ ఆధారిత వ్యవసాయ నిర్ణయాలు
- ప్రభుత్వ పథకాలు మరియు PM-KISAN
సంక్షిప్తంగా (200 పదాల కంటే తక్కువ) తెలుగులో సమాధానం ఇవ్వండి.`,
};

chatRouter.post("/chat", async (req: Request, res: Response) => {
  const {
    message,
    language = "en",
    history = [],
    stream: useStream = false,
  } = req.body as {
    message: string;
    language: string;
    history: Array<{ role: "user" | "assistant"; content: string }>;
    stream?: boolean;
  };

  if (!message?.trim()) {
    res.status(400).json({ error: "Message is required" });
    return;
  }

  const systemPrompt = SYSTEM_PROMPTS[language] ?? SYSTEM_PROMPTS["en"]!;
  const messages = [
    { role: "system" as const, content: systemPrompt },
    ...history.slice(-12).map((h) => ({ role: h.role, content: h.content })),
    { role: "user" as const, content: message },
  ];

  try {
    if (useStream) {
      res.setHeader("Content-Type", "text/event-stream");
      res.setHeader("Cache-Control", "no-cache");
      res.setHeader("Connection", "keep-alive");
      res.setHeader("X-Accel-Buffering", "no");

      const stream = await openai.chat.completions.create({
        model: "gpt-5-mini",
        max_completion_tokens: 512,
        messages,
        stream: true,
      });

      for await (const chunk of stream) {
        const content = chunk.choices[0]?.delta?.content;
        if (content) {
          res.write(`data: ${JSON.stringify({ content })}\n\n`);
        }
      }
      res.write(`data: ${JSON.stringify({ done: true })}\n\n`);
      res.end();
    } else {
      const completion = await openai.chat.completions.create({
        model: "gpt-5-mini",
        max_completion_tokens: 512,
        messages,
      });
      const reply =
        completion.choices[0]?.message?.content ??
        "I could not process that. Please try again.";
      res.json({ reply, language });
    }
  } catch (err) {
    req.log.error({ err }, "Chat completion failed");
    if (useStream) {
      res.write(`data: ${JSON.stringify({ error: "AI service unavailable" })}\n\n`);
      res.end();
    } else {
      res.status(500).json({ error: "AI service temporarily unavailable. Please try again." });
    }
  }
});

export default chatRouter;
