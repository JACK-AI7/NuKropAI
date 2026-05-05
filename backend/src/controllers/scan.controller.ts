import { Request, Response } from 'express';
import { prisma } from '../lib/prisma';
import { RecommendationService } from '../services/recommendation.service';
import { AIService, WeatherContext, ProductResearchOk } from '../services/ai.service';
import { WeatherService } from '../services/weather.service';
import { PestDetectionService } from '../services/pest-detection.service';

export class ScanController {
  static async createScan(req: Request, res: Response) {
    try {
      const userId = (req as any).userId;
      const file = req.file;
      const { label, isSoilAnalysis, latitude, longitude, confidence } = req.body;

      if (!file) return res.status(400).json({ error: 'No image uploaded' });

      const lat = parseFloat(latitude ?? req.body.lat);
      const lng = parseFloat(longitude ?? req.body.lng);
      const isSoil = isSoilAnalysis === 'true' || isSoilAnalysis === true;

      let weatherSnapshot: Record<string, unknown> | undefined;
      const weatherForAi: WeatherContext = {};

      if (!isNaN(lat) && !isNaN(lng)) {
        try {
          const w = await WeatherService.getWeather(lat, lng);
          weatherSnapshot = {
            temp: w.temp,
            humidity: w.humidity,
            windSpeed: w.windSpeed,
            weatherCode: w.weatherCode,
            time: w.time,
            unit: w.unit,
          };
          weatherForAi.temp = w.temp;
          weatherForAi.humidity = w.humidity;
        } catch (weatherErr) {
          console.warn('Weather fetch failed, continuing without:', weatherErr);
        }
      }

      let aiSource: 'ollama' | 'mistral' | 'yolo' | 'database' = 'database';
      let aiError: string | null = null;
      let analysis: any = null;
      let processingTimeMs: number | undefined = undefined;
      let pestDetectionsJson: string | undefined = undefined;
      let modelConfidence: number | undefined = undefined;

      // Determine model selection
      const modelType = (req.body.modelType || 'auto') as string;

      // For pest scans (not soil), try YOLO first unless explicitly 'general'
      const shouldTryYolo = !isSoil && modelType !== 'general';
      let yoloAttempted = false;

      if (shouldTryYolo) {
        yoloAttempted = true;
        try {
          console.log('[Scan] Attempting YOLO pest detection...');
          const yoloResult = await PestDetectionService.detect(file.path);
          if (yoloResult.detections && yoloResult.detections.length > 0) {
            const mapped = PestDetectionService.mapToAnalysis(yoloResult, isSoil);
            analysis = mapped;
            aiSource = 'yolo';
            processingTimeMs = Math.round(yoloResult.processing_time * 1000);
            pestDetectionsJson = JSON.stringify(mapped._pestDetections);
            modelConfidence = mapped._modelConfidence;
            delete analysis._pestDetections;
            delete analysis._modelConfidence;
            delete analysis._processingTime;
            delete analysis._aiSource;
            console.log(`[Scan] YOLO success: detected ${yoloResult.detections.length} pest(s)`);
          } else {
            aiError = 'YOLO: no pests detected';
            console.log('[Scan] YOLO returned no detections, falling back');
          }
        } catch (e: any) {
          aiError = e?.message || String(e);
          console.error('[Scan] YOLO detection failed:', aiError);
        }
      }

      // If YOLO didn't yield analysis, fall back to vision+text AI or database
      if (!analysis) {
        const aiResult = await AIService.analyzeImage(file.path, isSoil, weatherForAi);
        if (aiResult && !aiResult._error) {
          analysis = aiResult;
          aiSource = aiResult._source === 'mistral' ? 'mistral' : 'ollama';
          delete analysis._source;
        } else if (aiResult?._error) {
          aiError = aiResult.message || 'AI analysis failed';
        }
      }

      const weatherForRec =
        weatherSnapshot && weatherSnapshot.temp != null
          ? {
              temp: Number(weatherSnapshot.temp),
              humidity: weatherSnapshot.humidity != null ? Number(weatherSnapshot.humidity) : undefined,
            }
          : undefined;

      if (analysis && isSoil && analysis.soilType) {
        try {
          const dbSoil = RecommendationService.getSoilInsights(analysis.soilType, lat, lng);
          analysis = {
            ...analysis,
            nutrients: analysis.nutrients || dbSoil.nutrients,
            npk: analysis.npk || dbSoil.npk,
            health: analysis.health || dbSoil.health,
            suitableCrops: analysis.suitableCrops || dbSoil.crops,
          };
        } catch {
          /* curated soil type may not exist; keep model output */
        }
      }

      if (analysis && !isSoil && analysis.plantName && analysis.diseaseName) {
        const key = RecommendationService.findMatchingDiseaseKey(analysis.plantName, analysis.diseaseName);
        if (key) {
          try {
            const dbRec = RecommendationService.getRecommendation(key, lat, lng, weatherForRec);
            analysis = {
              ...analysis,
              treatment: dbRec.treatment || analysis.treatment,
              fertilizer: dbRec.fertilizer || analysis.fertilizer,
              pesticide: dbRec.pesticide || analysis.pesticide,
              npk: dbRec.npk || analysis.npk,
              matchedDiseaseKey: key,
            };
          } catch {
            /* ignore */
          }
        }
      }

      if (!analysis) {
        try {
          if (isSoil) {
            if (!label || label === 'Soil_Sample' || String(label).includes('Unknown')) {
              throw new Error('No soil insight data found for label: Soil_Sample');
            }
            analysis = RecommendationService.getSoilInsights(label, lat, lng);
          } else {
            analysis = RecommendationService.getRecommendation(label, lat, lng, weatherForRec);
          }
          aiSource = 'database';
        } catch (e: any) {
          const msg = e?.message || 'No database match';
          return res.status(503).json({
            error:
              'Vision AI is unavailable or failed, and no curated database entry matches this scan. Set MISTRAL_API_KEY (Mistral) or run Ollama with a vision model, or use a known disease label.',
            details: aiError || msg,
          });
        }
      }

      let plantName: string;
      let diseaseName: string;
      let severity: string;
      let conf: number;
      let treatment: string;
      let fertilizer: string;
      let pesticide: string | null;
      let soilType: string | null;
      let soilHealth: string | null;
      let npkForResponse: unknown = null;

      if (isSoil) {
        plantName = 'Soil';
        diseaseName = 'N/A';
        severity = 'Low';
        conf = analysis.confidence != null ? Number(analysis.confidence) : 0.75;
        soilType = analysis.soilType || label || null;
        const healthText = String(analysis.health ?? analysis.soilHealth ?? '').trim();
        soilHealth = healthText || null;
        treatment =
          [analysis.regionAdvice, analysis.treatment].filter(Boolean).join(' ').trim() ||
          healthText ||
          'See fertilizer and nutrient recommendations below.';
        fertilizer = String(analysis.nutrients ?? analysis.fertilizer ?? '').trim();
        pesticide = analysis.pesticide != null ? String(analysis.pesticide) : null;
        npkForResponse = analysis.npk;
      } else {
        plantName = analysis.plantName || String(label || 'Unknown').split('_')[0] || 'Unknown';
        diseaseName = analysis.diseaseName || analysis.name || String(label || '').split('_').slice(1).join(' ') || 'Unknown';
        severity = (analysis.severity || 'Medium').toString();
        conf = analysis.confidence != null ? Number(analysis.confidence) : (confidence ? parseFloat(confidence) : 0.75);
        treatment = analysis.treatment || '';
        fertilizer = analysis.fertilizer || analysis.nutrients || '';
        pesticide = analysis.pesticide || null;
        soilType = null;
        soilHealth = null;
        npkForResponse = analysis.npk;
        if (label?.includes('Healthy')) severity = 'Low';
      }

      const scan = await prisma.scan.create({
        data: {
          userId,
          imageUrl: `/uploads/${file.filename}`,
          plantName,
          diseaseName,
          cause: analysis?.cause || null,
          severity,
          confidence: confidence ? parseFloat(confidence) : conf,
          treatment,
          fertilizer,
          pesticide,
          soilType,
          soilHealth,
          isSoilAnalysis: isSoil,
          latitude: isNaN(lat) ? null : lat,
          longitude: isNaN(lng) ? null : lng,
          weather: weatherSnapshot ? JSON.stringify(weatherSnapshot) : null,
          aiModel: aiSource,
          modelVersion: process.env.YOLO_MODEL_VERSION || (aiSource === 'yolo' ? 'yolo11s-pest-detection-v1' : undefined),
          pestDetections: pestDetectionsJson,
          modelConfidence,
          processingTime: processingTimeMs,
        },
      });

      const regionHint = AIService.regionHintFromCoordinates(
        !isNaN(lat) ? lat : undefined,
        !isNaN(lng) ? lng : undefined
      );

      const research = await AIService.researchAgProducts({
        isSoil,
        plantName,
        diseaseName,
        treatment,
        pesticide,
        fertilizer: isSoil ? undefined : fertilizer,
        nutrients: isSoil ? fertilizer : String(analysis.nutrients ?? '').trim() || undefined,
        soilType,
        soilHealth,
        weather: weatherSnapshot,
        regionHint,
        latitude: !isNaN(lat) ? lat : undefined,
        longitude: !isNaN(lng) ? lng : undefined,
      });

      let productResearch: { researchSummary: string; suggestions: unknown[] } | null = null;
      let productResearchSource: string | null = null;
      let productResearchError: string | null = null;

      if (research && '_error' in research && research._error) {
        productResearchError = research.message;
      } else if (research) {
        const ok = research as ProductResearchOk;
        productResearch = {
          researchSummary: ok.researchSummary,
          suggestions: ok.suggestions,
        };
        productResearchSource = ok._source;
      }

      const responseData: Record<string, unknown> = {
        ...scan,
        aiSource,
        weather: weatherSnapshot,
        npk: npkForResponse,
        productResearch,
        productResearchSource,
        productResearchError,
        prevention: analysis.prevention,
        chemicalClass: analysis.chemicalClass,
        suitableCrops: analysis.suitableCrops,
        matchedDiseaseKey: analysis.matchedDiseaseKey,
        regionHint,
      };

      if (aiError && aiSource !== 'database') {
        responseData._aiWarning = true;
        responseData._aiWarningMessage = aiError;
      }

      res.status(201).json(responseData);
    } catch (error: any) {
      console.error('Scan Error:', error);
      const message = error?.message || 'Failed to process scan';
      if (message.includes('No recommendation data found') || message.includes('No soil insight data found')) {
        return res.status(422).json({ error: message });
      }
      res.status(500).json({ error: 'Failed to process scan' });
    }
  }

  static async getHistory(req: Request, res: Response) {
    try {
      const userId = (req as any).userId;
      const scans = await prisma.scan.findMany({
        where: { userId },
        orderBy: { createdAt: 'desc' },
      });
      res.json(scans);
    } catch (error) {
      res.status(500).json({ error: 'Failed to fetch history' });
    }
  }

  static async getScanById(req: Request, res: Response) {
    try {
      const id = req.params.id as string;
      const scan = await prisma.scan.findUnique({ where: { id } });
      if (!scan) return res.status(404).json({ error: 'Scan not found' });
      res.json(scan);
    } catch (error) {
      res.status(500).json({ error: 'Failed to fetch scan' });
    }
  }
}
