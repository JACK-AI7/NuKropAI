import type { Request, Response } from "express";
import { Router } from "express";
import { openai } from "@workspace/integrations-openai-ai-server";

const chatRouter = Router();

const SYSTEM_PROMPTS: Record<string, string> = {
  en: `You are NuKropAI, an expert AI farming assistant for Indian farmers. Provide precise, actionable advice about:
- Crop diseases: detection, treatment, and prevention
- Pest management and pesticide recommendations with dosages
- Soil health, fertilizer recommendations with specific quantities
- Weather-based farming decisions
- Government schemes and subsidies for farmers
- Crop calendar, planting, and harvesting timing

Keep responses concise (under 150 words), practical, and farmer-friendly. Always mention specific product names or quantities when recommending treatments. Respond only in English.`,

  hi: `आप NuKropAI हैं, भारतीय किसानों के लिए एक विशेषज्ञ AI कृषि सहायक। निम्नलिखित पर सटीक, व्यावहारिक सलाह दें:
- फसल रोग का पता लगाना, उपचार और रोकथाम
- कीट प्रबंधन और कीटनाशक अनुशंसाएं
- मिट्टी की सेहत और उर्वरक अनुशंसाएं
- मौसम आधारित कृषि निर्णय
- किसानों के लिए सरकारी योजनाएं

उत्तर संक्षिप्त (150 शब्दों से कम), व्यावहारिक रखें। हिन्दी में उत्तर दें।`,

  te: `మీరు NuKropAI, భారతీయ రైతులకు నిపుణ AI వ్యవసాయ సహాయకుడు. ఈ విషయాలపై ఖచ్చితమైన సలహాలు ఇవ్వండి:
- పంట వ్యాధి గుర్తింపు, చికిత్స మరియు నివారణ
- చీడ నిర్వహణ మరియు పురుగుమందుల సిఫార్సులు
- నేల ఆరోగ్యం మరియు ఎరువుల సిఫార్సులు
- వాతావరణ ఆధారిత వ్యవసాయ నిర్ణయాలు

సమాధానాలు సంక్షిప్తంగా (150 పదాల కంటే తక్కువ) ఉంచండి. తెలుగులో సమాధానం ఇవ్వండి।`,
};

chatRouter.post("/chat", async (req: Request, res: Response) => {
  const { message, language = "en", history = [] } = req.body as {
    message: string;
    language: string;
    history: Array<{ role: "user" | "assistant"; content: string }>;
  };

  if (!message?.trim()) {
    res.status(400).json({ error: "Message is required" });
    return;
  }

  const systemPrompt = SYSTEM_PROMPTS[language] ?? SYSTEM_PROMPTS["en"]!;

  const messages = [
    { role: "system" as const, content: systemPrompt },
    ...history.slice(-10).map((h) => ({
      role: h.role as "user" | "assistant",
      content: h.content,
    })),
    { role: "user" as const, content: message },
  ];

  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-5-mini",
      max_completion_tokens: 512,
      messages,
    });

    const reply =
      completion.choices[0]?.message?.content ??
      "I could not process that request. Please try again.";
    res.json({ reply, language });
  } catch (err) {
    req.log.error({ err }, "Chat completion failed");
    res.status(500).json({ error: "AI service temporarily unavailable. Please try again." });
  }
});

export default chatRouter;
