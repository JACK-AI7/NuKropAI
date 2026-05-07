"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AIService = void 0;
const fs_1 = __importDefault(require("fs"));
const dotenv_1 = __importDefault(require("dotenv"));
const logger_1 = require("../utils/logger");
const retry_1 = require("../utils/retry");
dotenv_1.default.config();
const OLLAMA_HOST = process.env.OLLAMA_HOST?.replace(/\/$/, '') || 'http://localhost:11434';
const OLLAMA_VISION_MODEL = process.env.OLLAMA_VISION_MODEL || 'llava:latest';
const CHAT_MODEL = process.env.OLLAMA_CHAT_MODEL || 'phi3:mini';
const MISTRAL_API_URL = 'https://api.mistral.ai/v1/chat/completions';
const MISTRAL_VISION_MODEL = process.env.MISTRAL_VISION_MODEL || 'mistral-small-latest';
const MISTRAL_CHAT_MODEL = process.env.MISTRAL_CHAT_MODEL || 'mistral-small-latest';
const OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions';
const OPENROUTER_MODEL = process.env.OPENROUTER_MODEL || 'deepseek/deepseek-chat-v3-0324';
const CONFIDENCE_THRESHOLDS = {
    HIGH: 0.85,
    MEDIUM: 0.70,
    LOW: 0.50,
};
class AIService {
    static regionHintFromCoordinates(lat, lng) {
        if (lat == null || lng == null || Number.isNaN(lat) || Number.isNaN(lng))
            return undefined;
        if (lat > 28)
            return `Northern / north-western belt (~${lat.toFixed(1)}°N, ${lng.toFixed(1)}°E) — typical of Punjab, Haryana, UP plains, northern hills`;
        if (lat < 15)
            return `Southern / peninsular (~${lat.toFixed(1)}°N, ${lng.toFixed(1)}°E) — typical of Tamil Nadu, Kerala, Karnataka, Andhra coastal / inland`;
        if (lng < 75)
            return `Western (~${lat.toFixed(1)}°N, ${lng.toFixed(1)}°E) — typical of Gujarat, Maharashtra, Rajasthan fringe`;
        if (lng > 85)
            return `Eastern (~${lat.toFixed(1)}°N, ${lng.toFixed(1)}°E) — typical of West Bengal, Odisha, Bihar, Jharkhand`;
        return `Central (~${lat.toFixed(1)}°N, ${lng.toFixed(1)}°E) — typical of Madhya Pradesh, Chhattisgarh, parts of Maharashtra / UP`;
    }
    static buildPrompts(isSoil, weather) {
        const weatherParts = [];
        if (weather?.temp != null)
            weatherParts.push(`Current temperature: ${weather.temp}°C.`);
        if (weather?.humidity != null)
            weatherParts.push(`Current relative humidity: ${weather.humidity}%.`);
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
    static parseJsonFromModelText(text) {
        const cleaned = text.replace(/```json\s*/gi, '').replace(/```/g, '').trim();
        const start = cleaned.indexOf('{');
        const end = cleaned.lastIndexOf('}');
        if (start === -1 || end === -1 || end <= start) {
            throw new Error('No JSON object in model response');
        }
        return JSON.parse(cleaned.slice(start, end + 1));
    }
    static validateCrop(parsed) {
        if (!parsed.plantName || !parsed.diseaseName || !parsed.pesticide) {
            throw new Error('Invalid response: missing required fields');
        }
        if (!parsed.confidence || parsed.confidence < 0 || parsed.confidence > 1) {
            parsed.confidence = 0.5;
        }
    }
    static validateSoil(parsed) {
        if (!parsed.soilType || !parsed.health || !parsed.nutrients) {
            throw new Error('Invalid soil response: missing required fields');
        }
    }
    static mistralMessageContentToString(content) {
        if (typeof content === 'string')
            return content.trim();
        if (Array.isArray(content)) {
            return content
                .map((part) => {
                if (typeof part === 'string')
                    return part;
                if (part?.type === 'text' && part.text)
                    return String(part.text);
                return '';
            })
                .join('')
                .trim();
        }
        return '';
    }
    static async callOpenRouterChat(messages, temperature, maxTokens, jsonObjectMode) {
        const key = process.env.OPENROUTER_API_KEY;
        if (!key)
            throw new Error('OPENROUTER_API_KEY not set');
        const body = {
            model: OPENROUTER_MODEL,
            messages,
            temperature,
            max_tokens: maxTokens,
        };
        if (jsonObjectMode) {
            body.response_format = { type: 'json_object' };
        }
        const res = await fetch(OPENROUTER_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${key}`,
                'HTTP-Referer': 'https://nukropai.com', // Optional but recommended by OpenRouter
                'X-Title': 'NuKropAI', // Optional but recommended
            },
            body: JSON.stringify(body),
        });
        if (!res.ok) {
            const t = await res.text();
            throw new Error(`OpenRouter API ${res.status}: ${t}`);
        }
        const data = (await res.json());
        const raw = data?.choices?.[0]?.message?.content;
        if (!raw)
            throw new Error('OpenRouter returned empty content');
        return String(raw).trim();
    }
    static async callMistralChat(messages, model, temperature, maxTokens, jsonObjectMode) {
        const key = process.env.MISTRAL_API_KEY;
        if (!key)
            throw new Error('MISTRAL_API_KEY not set');
        const body = {
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
        const data = (await res.json());
        const raw = data?.choices?.[0]?.message?.content;
        const text = this.mistralMessageContentToString(raw);
        if (!text)
            throw new Error('Mistral returned empty content');
        return text;
    }
    static async callMistralVision(imagePath, prompt, _isSoil) {
        const imageData = fs_1.default.readFileSync(imagePath);
        const base64 = imageData.toString('base64');
        const mime = imagePath.toLowerCase().endsWith('.png') ? 'image/png' : 'image/jpeg';
        const dataUri = `data:${mime};base64,${base64}`;
        const text = await this.callMistralChat([
            {
                role: 'user',
                content: [
                    { type: 'text', text: prompt },
                    { type: 'image_url', image_url: dataUri },
                ],
            },
        ], MISTRAL_VISION_MODEL, 0.2, 4096, false);
        return this.parseJsonFromModelText(text);
    }
    static async mistralTextJson(prompt) {
        const text = await this.callMistralChat([{ role: 'user', content: prompt }], MISTRAL_CHAT_MODEL, 0.35, 4096, true);
        return this.parseJsonFromModelText(text);
    }
    static async callOllama(endpoint, body, timeout = 60000) {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), timeout);
            const response = await fetch(`${OLLAMA_HOST}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
                signal: controller.signal,
            });
            clearTimeout(timeoutId);
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Ollama API ${response.status}: ${errorText}`);
            }
            return response.json();
        }
        catch (error) {
            if (error.name === 'AbortError' || error.message?.includes('aborted')) {
                throw new Error('Ollama request timed out after 60 seconds');
            }
            if (error.message?.includes('failed to connect') ||
                error.message?.includes('ECONNREFUSED') ||
                error.message?.includes('ENOTFOUND')) {
                throw new Error('Ollama server not running or unreachable');
            }
            throw error;
        }
    }
    static async analyzeWithOllamaEnhanced(imagePath, isSoil, weather) {
        const { soilPrompt, cropPrompt } = this.buildPrompts(isSoil, weather);
        const prompt = isSoil ? soilPrompt : cropPrompt;
        const imageData = fs_1.default.readFileSync(imagePath);
        const base64Image = imageData.toString('base64');
        if (base64Image.length < 100) {
            throw new Error('Image file too small or corrupted');
        }
        const result = await this.callOllama('/api/generate', {
            model: OLLAMA_VISION_MODEL,
            prompt,
            images: [base64Image],
            stream: false,
            options: { num_predict: 1024, temperature: 0.2 },
        });
        const text = result.response?.trim() || '';
        if (!text)
            throw new Error('Ollama returned empty response');
        const parsed = this.parseJsonFromModelText(text);
        if (isSoil)
            this.validateSoil(parsed);
        else
            this.validateCrop(parsed);
        return parsed;
    }
    static async analyzeWithMistralVisionFull(imagePath, isSoil, weather) {
        const { soilPrompt, cropPrompt } = this.buildPrompts(isSoil, weather);
        const prompt = isSoil ? soilPrompt : cropPrompt;
        const parsed = await this.callMistralVision(imagePath, prompt, isSoil);
        if (isSoil)
            this.validateSoil(parsed);
        else
            this.validateCrop(parsed);
        return parsed;
    }
    static async tryFallbackAnalysis(imagePath, isSoil, weather) {
        try {
            return await this.analyzeWithOllamaEnhanced(imagePath, isSoil, weather);
        }
        catch (error) {
            logger_1.logger.warn('Fallback analysis also failed', {
                service: 'ai-inference',
                error: error.message,
            });
            return { confidence: 0, _error: true };
        }
    }
    static async analyzeImage(imagePath, isSoil = false, weather) {
        const startTime = Date.now();
        try {
            if (process.env.MISTRAL_API_KEY) {
                try {
                    logger_1.logger.info('Attempting Mistral vision analysis', { service: 'ai-inference', isSoil });
                    const result = await (0, retry_1.retryWithTimeout)(() => this.analyzeWithMistralVisionFull(imagePath, isSoil, weather), 30000, { maxRetries: 1 });
                    const durationMs = Date.now() - startTime;
                    if (result.confidence < CONFIDENCE_THRESHOLDS.MEDIUM) {
                        logger_1.logger.warn('Low confidence — trying fallback', {
                            service: 'ai-inference',
                            confidence: result.confidence,
                        });
                        const fallbackResult = await this.tryFallbackAnalysis(imagePath, isSoil, weather);
                        if (fallbackResult.confidence > result.confidence) {
                            return { ...fallbackResult, duration_ms: durationMs, used_fallback: true, _source: 'ollama' };
                        }
                    }
                    logger_1.logger.info('Mistral analysis successful', {
                        service: 'ai-inference',
                        confidence: result.confidence,
                        duration_ms: durationMs,
                    });
                    return { ...result, duration_ms: durationMs, used_fallback: false, _source: 'mistral' };
                }
                catch (e) {
                    logger_1.logger.error('Mistral vision failed', { service: 'ai-inference', error: e?.message });
                }
            }
            logger_1.logger.info('Using Ollama for analysis', { service: 'ai-inference', model: OLLAMA_VISION_MODEL });
            const result = await (0, retry_1.retryWithTimeout)(() => this.analyzeWithOllamaEnhanced(imagePath, isSoil, weather), 60000, { maxRetries: 2 });
            const durationMs = Date.now() - startTime;
            logger_1.logger.info('Ollama analysis completed', {
                service: 'ai-inference',
                model: OLLAMA_VISION_MODEL,
                duration_ms: durationMs,
            });
            return { ...result, duration_ms: durationMs, used_fallback: false, _source: 'ollama' };
        }
        catch (error) {
            logger_1.logger.error('Image analysis failed', {
                service: 'ai-inference',
                error: error.message,
                duration_ms: Date.now() - startTime,
            });
            return {
                _error: true,
                message: error.message || 'Vision AI unavailable (set MISTRAL_API_KEY or run Ollama with a vision model)',
            };
        }
    }
    static async chat(message, history) {
        try {
            if (message.includes('data:image') ||
                message.includes('base64')) {
                logger_1.logger.error('Chat received image data — use image scan feature', {
                    service: 'ai-service',
                    message: message.substring(0, 100),
                });
                return 'I can only process text messages. Please use the image scan feature for analyzing photos.';
            }
            const messages = history.map((h) => ({
                role: h.role === 'model' ? 'assistant' : 'user',
                content: h.parts[0].text,
            }));
            messages.push({ role: 'user', content: message });
            if (process.env.OPENROUTER_API_KEY) {
                try {
                    return await this.callOpenRouterChat(messages, 0.7, 4096, false);
                }
                catch (e) {
                    logger_1.logger.warn('OpenRouter chat failed, falling back to Mistral/Ollama', {
                        service: 'ai-service',
                        error: e.message,
                    });
                }
            }
            if (process.env.MISTRAL_API_KEY) {
                try {
                    return await this.callMistralChat(messages, MISTRAL_CHAT_MODEL, 0.7, 4096, false);
                }
                catch (e) {
                    logger_1.logger.warn('Mistral chat failed, falling back to Ollama', {
                        service: 'ai-service',
                        error: e.message,
                    });
                }
            }
            const result = await this.callOllama('/api/chat', {
                model: CHAT_MODEL,
                messages,
                stream: false,
            });
            return result.message?.content || "I couldn't generate a response.";
        }
        catch (error) {
            logger_1.logger.error('AI Chat Error', {
                service: 'ai-service',
                error: error.message,
            });
            return "I'm having trouble. Please try again.";
        }
    }
    static async researchAgProducts(ctx) {
        const weatherLine = ctx.weather && Object.keys(ctx.weather).length
            ? `Live weather snapshot: ${JSON.stringify(ctx.weather)}`
            : 'Weather: not available.';
        const regionBlock = ctx.regionHint || ctx.latitude != null
            ? `Farmer location context:\n- Region hint: ${ctx.regionHint || 'unknown'}\n- GPS: ${ctx.latitude != null && ctx.longitude != null ? `latitude ${ctx.latitude}, longitude ${ctx.longitude}` : 'not provided'}`
            : 'Farmer location: not provided — suggest products commonly available across India.';
        let prompt;
        if (ctx.isSoil) {
            prompt = `You are an agricultural inputs advisor for India. Recommend fertilizer / soil amendment products for:
${regionBlock}
- Soil type: ${ctx.soilType || 'Unknown'}
- Soil health: ${ctx.soilHealth || 'Unknown'}
- Nutrient guidance: ${ctx.nutrients || ctx.fertilizer || 'Not specified'}
${weatherLine}

Return ONLY valid JSON (no markdown):
{
  "researchSummary": "2-4 sentences",
  "suggestions": [
    {
      "productName": "Specific product",
      "productType": "Fertilizer|Soil amendment|Organic|Micronutrient|Other",
      "activeIngredient": "",
      "whyItFits": "1-2 sentences",
      "applicationTip": "practical timing/rate",
      "safetyNote": "over-use, soil test, label disclaimer",
      "regionalAvailability": "availability in this region",
      "purchaseUrl": "Amazon.in or AgriBegri search URL",
      "imageUrl": "product image URL"
    }
  ]
}
Rules: 3-5 suggestions.`;
        }
        else {
            prompt = `You are an agricultural inputs advisor for India. Recommend pesticide/fungicide products for:
${regionBlock}
- Crop: ${ctx.plantName || 'Unknown'}
- Problem: ${ctx.diseaseName || 'Unknown'}
- Treatment outline: ${ctx.treatment || 'Not specified'}
- Technical pesticide guidance: ${ctx.pesticide || 'Not specified'}
${weatherLine}

Return ONLY valid JSON (no markdown):
{
  "researchSummary": "2-4 sentences",
  "suggestions": [
    {
      "productName": "Active ingredient + formulation",
      "productType": "Fungicide|Insecticide|Herbicide|Bio-pesticide|Other",
      "activeIngredient": "",
      "whyItFits": "linked to ${ctx.diseaseName || 'the diagnosis'}",
      "applicationTip": "timing, rotation, spray tips",
      "safetyNote": "PPE, PHI, resistance — always read label",
      "regionalAvailability": "typical availability in this region",
      "purchaseUrl": "Amazon.in or AgriBegri search URL",
      "imageUrl": "product image URL"
    }
  ]
}
Rules: 3-5 suggestions.`;
        }
        let lastErr = null;
        if (process.env.OPENROUTER_API_KEY) {
            try {
                console.log('[AI] Researching products with OpenRouter...');
                const text = await this.callOpenRouterChat([{ role: 'user', content: prompt }], 0.35, 4096, true);
                const parsed = this.parseJsonFromModelText(text);
                this.validateProductResearch(parsed);
                return {
                    researchSummary: String(parsed.researchSummary),
                    suggestions: parsed.suggestions,
                    _source: 'openrouter',
                };
            }
            catch (e) {
                lastErr = e?.message || String(e);
                console.warn('[AI] OpenRouter product research failed:', lastErr);
            }
        }
        if (process.env.MISTRAL_API_KEY) {
            try {
                console.log('[AI] Researching products with Mistral...');
                const parsed = await this.mistralTextJson(prompt);
                this.validateProductResearch(parsed);
                return {
                    researchSummary: String(parsed.researchSummary),
                    suggestions: parsed.suggestions,
                    _source: 'mistral',
                };
            }
            catch (e) {
                lastErr = e?.message || String(e);
                console.error('[AI] Mistral product research failed:', lastErr);
            }
        }
        try {
            console.log('[AI] Researching products with Ollama...');
            const parsed = await this.ollamaChatJson(prompt);
            this.validateProductResearch(parsed);
            return {
                researchSummary: String(parsed.researchSummary),
                suggestions: parsed.suggestions,
                _source: 'ollama',
            };
        }
        catch (e) {
            lastErr = e?.message || String(e);
            console.warn('Ollama product research failed:', lastErr);
        }
        return {
            _error: true,
            message: lastErr || 'Product research unavailable (set OPENROUTER_API_KEY or MISTRAL_API_KEY or run Ollama chat)',
        };
    }
    static validateProductResearch(parsed) {
        if (!parsed || typeof parsed.researchSummary !== 'string' || !Array.isArray(parsed.suggestions)) {
            throw new Error('Invalid product research JSON shape');
        }
        if (parsed.suggestions.length === 0)
            throw new Error('No product suggestions in response');
        for (const s of parsed.suggestions) {
            if (!s || typeof s.productName !== 'string' || !s.productName.trim()) {
                throw new Error('Each suggestion must include productName');
            }
        }
    }
    static async ollamaChatJson(prompt) {
        const result = await this.callOllama('/api/chat', {
            model: CHAT_MODEL,
            messages: [{ role: 'user', content: prompt }],
            stream: false,
        });
        const text = result.message?.content?.trim() || '';
        if (!text)
            throw new Error('Ollama chat returned empty response');
        return this.parseJsonFromModelText(text);
    }
}
exports.AIService = AIService;
