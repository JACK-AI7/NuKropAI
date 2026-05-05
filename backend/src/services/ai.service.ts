import fs from 'fs';
import dotenv from 'dotenv';

dotenv.config();

const OLLAMA_HOST = process.env.OLLAMA_HOST?.replace(/\/$/, '') || 'http://localhost:11434';
const OLLAMA_VISION_MODEL = process.env.OLLAMA_VISION_MODEL || 'llava:latest';
const CHAT_MODEL = process.env.OLLAMA_CHAT_MODEL || 'phi3:mini';

/** Mistral Chat Completions API — vision + text (see https://docs.mistral.ai/capabilities/vision/) */
const MISTRAL_API_URL = 'https://api.mistral.ai/v1/chat/completions';
const MISTRAL_VISION_MODEL = process.env.MISTRAL_VISION_MODEL || 'mistral-small-latest';
const MISTRAL_CHAT_MODEL = process.env.MISTRAL_CHAT_MODEL || 'mistral-small-latest';

export type WeatherContext = { temp?: number; humidity?: number | null };

export type ProductResearchContext = {
  isSoil: boolean;
  plantName?: string;
  diseaseName?: string;
  treatment?: string;
  pesticide?: string | null;
  fertilizer?: string;
  soilType?: string | null;
  soilHealth?: string | null;
  nutrients?: string;
  weather?: Record<string, unknown>;
  /** Coarse India region from GPS for retail / availability hints */
  regionHint?: string;
  latitude?: number;
  longitude?: number;
};

export type ProductSuggestion = {
  productName: string;
  productType?: string;
  activeIngredient?: string;
  whyItFits?: string;
  applicationTip?: string;
  safetyNote?: string;
  /** How / where this class of product is typically found in the farmer's region */
  regionalAvailability?: string;
  /** Direct search or purchase link (Amazon.in or AgriBegri) */
  purchaseUrl?: string;
  /** Representative high-quality image URL for the product */
  imageUrl?: string;
};

export type ProductResearchOk = {
  researchSummary: string;
  suggestions: ProductSuggestion[];
  _source: 'mistral' | 'ollama';
};

export class AIService {
  /** Rough geographic zone in India from lat/lon (agronomy / retail availability context). */
  static regionHintFromCoordinates(lat?: number, lng?: number): string | undefined {
    if (lat == null || lng == null || Number.isNaN(lat) || Number.isNaN(lng)) return undefined;
    if (lat > 28) {
      return `Northern / north-western belt (~${lat.toFixed(1)}°N, ${lng.toFixed(1)}°E) — typical of Punjab, Haryana, UP plains, northern hills`;
    }
    if (lat < 15) {
      return `Southern / peninsular (~${lat.toFixed(1)}°N, ${lng.toFixed(1)}°E) — typical of Tamil Nadu, Kerala, Karnataka, Andhra coastal / inland`;
    }
    if (lng < 75) {
      return `Western (~${lat.toFixed(1)}°N, ${lng.toFixed(1)}°E) — typical of Gujarat, Maharashtra, Rajasthan fringe`;
    }
    if (lng > 85) {
      return `Eastern (~${lat.toFixed(1)}°N, ${lng.toFixed(1)}°E) — typical of West Bengal, Odisha, Bihar, Jharkhand`;
    }
    return `Central (~${lat.toFixed(1)}°N, ${lng.toFixed(1)}°E) — typical of Madhya Pradesh, Chhattisgarh, parts of Maharashtra / UP`;
  }

  private static buildPrompts(isSoil: boolean, weather?: WeatherContext) {
    const weatherParts: string[] = [];
    if (weather?.temp != null) weatherParts.push(`Current temperature: ${weather.temp}°C.`);
    if (weather?.humidity != null) weatherParts.push(`Current relative humidity: ${weather.humidity}%.`);
    const weatherContext = weatherParts.length ? `\n${weatherParts.join(' ')}` : '';

    const soilPrompt = `You are an expert Indian agronomist. Analyze this soil image and provide ONLY valid JSON (no markdown):
{
  "soilType": "One of: Alluvial, Black, Red, Laterite, Desert, Mountain, Marshy",
  "health": "Soil health description",
  "suitableCrops": ["Rice", "Wheat"],
  "nutrients": "Fertilizer recommendations with Indian product examples where relevant",
  "npk": [40, 20, 10],
  "regionAdvice": "Region-specific tips"
}${weatherContext}`;

    const cropPrompt = `You are a crop disease specialist for Indian farmers. Analyze this plant image and provide ONLY valid JSON (no markdown):
{
  "plantName": "Common crop name",
  "diseaseName": "Specific disease or pest name",
  "cause": "The specific pathogen (bacteria/fungi), insect, or environmental factor causing the damage",
  "severity": "Low or Medium or High",
  "confidence": 0.95,
  "treatment": "Detailed treatment steps",
  "fertilizer": "NPK recommendations with Indian fertilizer names",
  "pesticide": "Registered-appropriate active ingredients / formulations for India with dose per litre or per kg where applicable",
  "npk": [20, 20, 20],
  "chemicalClass": "Fungicide or Insecticide or Herbicide or Other",
  "prevention": "Preventive measures"
}${weatherContext}`;

    return { soilPrompt, cropPrompt, weatherContext };
  }

  private static parseJsonFromModelText(text: string): any {
    const cleaned = text.replace(/```json\s*/gi, '').replace(/```/g, '').trim();
    const start = cleaned.indexOf('{');
    const end = cleaned.lastIndexOf('}');
    if (start === -1 || end === -1 || end <= start) {
      throw new Error('No JSON object in model response');
    }
    return JSON.parse(cleaned.slice(start, end + 1));
  }

  private static validateCrop(parsed: any) {
    if (!parsed.plantName || !parsed.diseaseName || !parsed.pesticide) {
      throw new Error('Invalid response: missing required fields');
    }
  }

  private static validateSoil(parsed: any) {
    if (!parsed.soilType || !parsed.health || !parsed.nutrients) {
      throw new Error('Invalid soil response: missing required fields');
    }
  }

  private static mistralMessageContentToString(content: unknown): string {
    if (typeof content === 'string') return content.trim();
    if (Array.isArray(content)) {
      return content
        .map((part: any) => {
          if (typeof part === 'string') return part;
          if (part?.type === 'text' && part.text) return String(part.text);
          return '';
        })
        .join('')
        .trim();
    }
    return '';
  }

  private static async callMistralChat(
    messages: Array<{
      role: string;
      content: string | Array<{ type: string; text?: string; image_url?: string }>;
    }>,
    model: string,
    temperature: number,
    maxTokens: number,
    jsonObjectMode?: boolean
  ): Promise<string> {
    const key = process.env.MISTRAL_API_KEY;
    if (!key) throw new Error('MISTRAL_API_KEY not set');

    const body: Record<string, unknown> = {
      model,
      messages,
      temperature,
      max_tokens: maxTokens,
    };
    if (jsonObjectMode) {
      body.response_format = { type: 'json_object' };
    }

    const res = await fetch(MISTRAL_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${key}`,
      },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const t = await res.text();
      throw new Error(`Mistral API ${res.status}: ${t}`);
    }

    const data = (await res.json()) as any;
    const raw = data?.choices?.[0]?.message?.content;
    const text = this.mistralMessageContentToString(raw);
    if (!text) throw new Error('Mistral returned empty content');
    return text;
  }

  private static async analyzeWithMistralVision(
    imagePath: string,
    prompt: string,
    isSoil: boolean
  ): Promise<any> {
    const imageData = fs.readFileSync(imagePath);
    const base64 = imageData.toString('base64');
    const mime = imagePath.toLowerCase().endsWith('.png') ? 'image/png' : 'image/jpeg';
    const dataUri = `data:${mime};base64,${base64}`;

    const text = await this.callMistralChat(
      [
        {
          role: 'user',
          content: [
            { type: 'text', text: prompt },
            { type: 'image_url', image_url: dataUri },
          ],
        },
      ],
      MISTRAL_VISION_MODEL,
      0.2,
      4096,
      false
    );

    const parsed = this.parseJsonFromModelText(text);
    if (isSoil) this.validateSoil(parsed);
    else this.validateCrop(parsed);
    return parsed;
  }

  private static async mistralTextJson(prompt: string): Promise<any> {
    const text = await this.callMistralChat(
      [{ role: 'user', content: prompt }],
      MISTRAL_CHAT_MODEL,
      0.35,
      4096,
      true
    );
    return this.parseJsonFromModelText(text);
  }

  static async analyzeImage(imagePath: string, isSoil: boolean = false, weather?: WeatherContext) {
    const { soilPrompt, cropPrompt } = this.buildPrompts(isSoil, weather);
    const prompt = isSoil ? soilPrompt : cropPrompt;

    try {
      const imageData = fs.readFileSync(imagePath);
      const base64Image = imageData.toString('base64');
      if (base64Image.length < 100) {
        throw new Error('Image file too small or corrupted');
      }

      let lastErr: string | null = null;

      if (process.env.MISTRAL_API_KEY) {
        try {
          console.log('[AI] Attempting Mistral vision analysis...');
          const parsed = await this.analyzeWithMistralVision(imagePath, prompt, isSoil);
          console.log('[AI] Mistral vision success');
          return { ...parsed, _source: 'mistral' as const };
        } catch (e: any) {
          lastErr = e?.message || String(e);
          console.error('[AI] Mistral vision failed:', lastErr);
        }
      } else {
        console.warn('[AI] Mistral API key missing - skipping Mistral vision');
      }

      try {
        console.log('[AI] Attempting Ollama vision analysis...');
        const parsed = await this.analyzeWithOllama(prompt, base64Image, isSoil);
        console.log('[AI] Ollama vision success');
        return { ...parsed, _source: 'ollama' as const };
      } catch (e: any) {
        lastErr = e?.message || String(e);
        console.error('[AI] Ollama vision failed:', lastErr);
      }

      return {
        _error: true,
        message: lastErr || 'Vision AI unavailable (set MISTRAL_API_KEY or run Ollama with a vision model)',
      };
    } catch (error: any) {
      console.error('AI Analysis Error:', error.message);
      return { _error: true, message: error.message };
    }
  }

  private static async analyzeWithOllama(prompt: string, base64Image: string, isSoil: boolean): Promise<any> {
    const result = await this.callOllama('/api/generate', {
      model: OLLAMA_VISION_MODEL,
      prompt,
      images: [base64Image],
      stream: false,
      options: { num_predict: 1024, temperature: 0.2 },
    });

    let text = result.response?.trim() || '';
    if (!text) throw new Error('Ollama returned empty response');

    const parsed = this.parseJsonFromModelText(text);
    if (isSoil) this.validateSoil(parsed);
    else this.validateCrop(parsed);
    return parsed;
  }

  /**
   * After identification: Mistral (or Ollama) synthesizes product ideas for the farmer's region.
   */
  static async researchAgProducts(
    ctx: ProductResearchContext
  ): Promise<ProductResearchOk | { _error: true; message: string }> {
    const weatherLine =
      ctx.weather && Object.keys(ctx.weather).length
        ? `Live weather snapshot: ${JSON.stringify(ctx.weather)}`
        : 'Weather: not available.';

    const regionBlock =
      ctx.regionHint || ctx.latitude != null
        ? `Farmer location context (use to tailor which product TYPES and formulations are commonly sold in agri-retail in this part of India; do not invent specific shop names):
- Region hint: ${ctx.regionHint || 'unknown — suggest widely stocked national/generic lines'}
- GPS: ${ctx.latitude != null && ctx.longitude != null ? `latitude ${ctx.latitude}, longitude ${ctx.longitude}` : 'not provided'}`
        : 'Farmer location: not provided — suggest products commonly available across India.';

    let prompt: string;
    if (ctx.isSoil) {
      prompt = `You are an agricultural inputs advisor for India. The soil was already assessed from a scan. Your task is to RESEARCH and recommend concrete fertilizer / soil amendment / micronutrient products that fit this assessment AND are realistically available in agri-input shops in the farmer's region.

${regionBlock}

Assessment:
- Soil type: ${ctx.soilType || 'Unknown'}
- Soil health: ${ctx.soilHealth || 'Unknown'}
- Nutrient guidance: ${ctx.nutrients || ctx.fertilizer || 'Not specified'}
${weatherLine}

Return ONLY valid JSON (no markdown):
{
  "researchSummary": "2-4 sentences: issue type (soil/nutrient focus) and regional product strategy",
  "suggestions": [
    {
      "productName": "Specific example: generic formulation or widely known product line in India",
      "productType": "Fertilizer|Soil amendment|Organic|Micronutrient|Other",
      "activeIngredient": "nutrient focus or blank",
      "whyItFits": "1-2 sentences",
      "applicationTip": "practical timing/rate hints",
      "safetyNote": "over-use, soil test, label disclaimer",
      "regionalAvailability": "1-2 sentences: how these are typically found in THIS region's market (e.g. cooperative stores, common brand tiers) — no fake addresses",
      "purchaseUrl": "A search link on Amazon.in or AgriBegri.com for this specific product",
      "imageUrl": "Use a representative high-quality agricultural image URL. Examples: https://m.media-amazon.com/images/I/71WzY6I+08L._SL1500_.jpg (for NPK/Fertilizers), https://m.media-amazon.com/images/I/61r5a0w7lEL._SL1500_.jpg (for Organic/Neem)"
    }
  ]
}
Rules: 3-5 suggestions. No fake registration numbers. If uncertain, say so in safetyNote. Provide real-world URLs for purchase and images where possible.`;
    } else {
      prompt = `You are an agricultural inputs advisor for India. A crop problem was ALREADY identified from an image scan. First acknowledge the issue type clearly, then RESEARCH pesticide/fungicide/bio-control options that match standard practice AND are commonly available in the farmer's REGION.

${regionBlock}

Diagnosis context:
- Crop: ${ctx.plantName || 'Unknown'}
- Problem (disease/pests): ${ctx.diseaseName || 'Unknown'}
- Treatment outline: ${ctx.treatment || 'Not specified'}
- Technical pesticide guidance (follow closely): ${ctx.pesticide || 'Not specified'}
- Fertilizer note: ${ctx.fertilizer || 'Not specified'}
${weatherLine}

Return ONLY valid JSON (no markdown):
{
  "researchSummary": "2-4 sentences: what issue type this is (e.g. fungal foliar, sucking pest, viral vector) and why the suggested product classes fit this region's cropping system",
  "suggestions": [
    {
      "productName": "Example: active ingredient + formulation (WP/SC/SL) common in Indian trade",
      "productType": "Fungicide|Insecticide|Herbicide|Bio-pesticide|Other",
      "activeIngredient": "",
      "whyItFits": "linked to ${ctx.diseaseName || 'the diagnosis'}",
      "applicationTip": "timing, rotation, spray tips",
      "safetyNote": "PPE, PHI, resistance — always read label",
      "regionalAvailability": "typical availability in this region (generic vs branded lines); no invented shop names",
      "purchaseUrl": "A search link on Amazon.in or AgriBegri.com for this specific product",
      "imageUrl": "Use a representative high-quality agricultural image URL. Examples: https://m.media-amazon.com/images/I/71e-f-3vQ3L._SL1500_.jpg (for Insecticides), https://m.media-amazon.com/images/I/61mO-p-T6FL._SL1000_.jpg (for Fungicides)"
    }
  ]
}
Rules: 3-5 suggestions. Align with the technical guidance above. No fabricated registration IDs. Provide real-world URLs for purchase and images where possible.`;
    }

    let lastErr: string | null = null;

    if (process.env.MISTRAL_API_KEY) {
      try {
        console.log('[AI] Researching products with Mistral...');
        const parsed = await this.mistralTextJson(prompt);
        console.log('[AI] Mistral research success');
        this.validateProductResearch(parsed);
        return {
          researchSummary: String(parsed.researchSummary),
          suggestions: parsed.suggestions as ProductSuggestion[],
          _source: 'mistral',
        };
      } catch (e: any) {
        lastErr = e?.message || String(e);
        console.error('[AI] Mistral product research failed:', lastErr);
      }
    }

    try {
      console.log('[AI] Researching products with Ollama...');
      const parsed = await this.ollamaChatJson(prompt);
      console.log('[AI] Ollama research success');
      this.validateProductResearch(parsed);
      return {
        researchSummary: String(parsed.researchSummary),
        suggestions: parsed.suggestions as ProductSuggestion[],
        _source: 'ollama',
      };
    } catch (e: any) {
      lastErr = e?.message || String(e);
      console.warn('Ollama product research failed:', lastErr);
    }

    return {
      _error: true,
      message: lastErr || 'Product research unavailable (set MISTRAL_API_KEY or run Ollama chat)',
    };
  }

  private static validateProductResearch(parsed: any) {
    if (!parsed || typeof parsed.researchSummary !== 'string' || !Array.isArray(parsed.suggestions)) {
      throw new Error('Invalid product research JSON shape');
    }
    if (parsed.suggestions.length === 0) throw new Error('No product suggestions in response');
    for (const s of parsed.suggestions) {
      if (!s || typeof s.productName !== 'string' || !s.productName.trim()) {
        throw new Error('Each suggestion must include productName');
      }
    }
  }

  private static async ollamaChatJson(prompt: string): Promise<any> {
    const result = await this.callOllama('/api/chat', {
      model: CHAT_MODEL,
      messages: [{ role: 'user', content: prompt }],
      stream: false,
    });
    const text = result.message?.content?.trim() || '';
    if (!text) throw new Error('Ollama chat returned empty response');
    return this.parseJsonFromModelText(text);
  }

  static async chat(message: string, history: { role: string; parts: { text: string }[] }[]) {
    try {
      const messages = history.map(h => ({
        role: h.role === 'model' ? 'assistant' : 'user',
        content: h.parts[0].text
      }));
      messages.push({ role: 'user', content: message });

      if (process.env.MISTRAL_API_KEY) {
        try {
          return await this.callMistralChat(messages, MISTRAL_CHAT_MODEL, 0.7, 4096, false);
        } catch (e) {
          console.warn('Mistral chat failed, falling back to Ollama:', e);
        }
      }

      const result = await this.callOllama('/api/chat', { model: CHAT_MODEL, messages, stream: false });
      return result.message?.content || "I couldn't generate a response.";
    } catch (error: any) {
      console.error('AI Chat Error:', error.message);
      return "I'm having trouble. Please try again.";
    }
  }

  private static async callOllama(path: string, body: any, timeout = 60000): Promise<any> {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);
      
      const response = await fetch(`${OLLAMA_HOST}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Ollama error ${response.status}: ${errorText}`);
      }
      return response.json();
    } catch (error: any) {
      if (error.name === 'AbortError' || error.message.includes('aborted')) {
        throw new Error('Ollama request timed out after 60 seconds');
      }
      if (error.message.includes('failed to connect') || error.message.includes('ECONNREFUSED') || error.message.includes('ENOTFOUND')) {
        throw new Error('Ollama server not running or unreachable');
      }
      throw error;
    }
  }
}
