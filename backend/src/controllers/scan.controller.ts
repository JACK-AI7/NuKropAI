import { Request, Response } from 'express';
import { prisma } from '../lib/prisma';
import { WeatherService } from '../services/weather.service';
import { retryWithTimeout } from '../utils/retry';
import { logger } from '../utils/logger';

export class ScanController {
  static async createScan(req: Request, res: Response) {
    try {
      const userId = (req as any).userId;
      const file = req.file;
      const {
        label,
        isSoilAnalysis,
        latitude,
        longitude,
        confidence,
        // Client-provided analysis fields (if mobile did analysis)
        plantName,
        diseaseName,
        cause,
        severity,
        treatment,
        fertilizer,
        pesticide,
        soilType,
        soilHealth,
        aiModel,
        modelConfidence,
        processingTime,
        pestDetections,
        weather: weatherJson,
        matchedDiseaseKey,
        prevention,
        chemicalClass,
        suitableCrops,
      } = req.body;

      if (!file) return res.status(400).json({ error: 'No image uploaded' });

      const lat = parseFloat(latitude ?? req.body.lat);
      const lng = parseFloat(longitude ?? req.body.lng);
      const isSoil = isSoilAnalysis === 'true' || isSoilAnalysis === true;

      // If client already provided full analysis, skip server-side AI
      const clientAnalyzed = plantName != null || soilType != null;
      let analysis: any = null;

      if (clientAnalyzed) {
        analysis = {
          plantName: isSoil ? 'Soil' : plantName,
          diseaseName: isSoil ? 'N/A' : diseaseName,
          cause,
          severity: severity || (isSoil ? 'Low' : 'Medium'),
          confidence: confidence ? parseFloat(confidence) : 0.75,
          treatment: treatment || '',
          fertilizer,
          pesticide,
          soilType,
          soilHealth,
          npk: null,
          matchedDiseaseKey,
          prevention,
          chemicalClass,
          suitableCrops: suitableCrops ? (Array.isArray(suitableCrops) ? suitableCrops : [suitableCrops]) : undefined,
        };
      } else {
        // Server-side AI path (legacy) — keep for compatibility
        return res.status(501).json({ error: 'Server-side AI is disabled. Use client analysis.' });
      }

      // Parse weather if provided as JSON string
      let weatherSnapshot: Record<string, unknown> | undefined;
      if (weatherJson) {
        try {
          weatherSnapshot = typeof weatherJson === 'string' ? JSON.parse(weatherJson) : weatherJson;
        } catch (_) {}
      }

      const finalPlantName = isSoil ? 'Soil' : analysis.plantName;
      const finalDiseaseName = isSoil ? 'N/A' : analysis.diseaseName;
      const finalSeverity = analysis.severity;
      const finalConfidence = analysis.confidence;
      const finalTreatment = analysis.treatment;
      const finalFertilizer = fertilizer || analysis.fertilizer || '';
      const finalPesticide = pesticide || analysis.pesticide || null;
      const finalSoilType = soilType || analysis.soilType || null;
      const finalSoilHealth = soilHealth || analysis.soilHealth || null;
      const finalNpk = analysis.npk;

      // Get weather data with retry
      let weatherData = null;
      if (lat && lng && !weatherSnapshot) {
        try {
          weatherData = await retryWithTimeout(
            () => WeatherService.getWeather(lat, lng),
            10000,
            { maxRetries: 2 }
          );
        } catch (error) {
          logger.warn('Weather fetch failed, continuing without weather data', {
            error: (error as Error).message,
            lat,
            lng,
          });
        }
      }

      const scan = await prisma.scan.create({
        data: {
          userId,
          imageUrl: `/uploads/${file.filename}`,
          plantName: finalPlantName,
          diseaseName: finalDiseaseName,
          cause: analysis.cause || null,
          severity: finalSeverity,
          confidence: finalConfidence,
          treatment: finalTreatment,
          fertilizer: finalFertilizer,
          pesticide: finalPesticide,
          soilType: finalSoilType,
          soilHealth: finalSoilHealth,
          npk: finalNpk,
          isSoilAnalysis: isSoil,
          latitude: lat,
          longitude: lng,
          aiModel: aiModel || (clientAnalyzed ? 'mobile-client' : 'server-ai'),
          modelConfidence: modelConfidence || finalConfidence,
          processingTime: processingTime ? parseFloat(processingTime) : null,
          pestDetections: pestDetections ? JSON.stringify(pestDetections) : null,
          weather: weatherData ? JSON.stringify(weatherData) : (weatherSnapshot ? JSON.stringify(weatherSnapshot) : null),
          matchedDiseaseKey,
        },
        include: {
          user: {
            select: {
              email: true,
              name: true,
            },
          },
        },
      });

      logger.info('Scan created successfully', {
        service: 'scan-controller',
        scanId: scan.id,
        userId,
        plantName: scan.plantName,
        confidence: scan.confidence,
      });

      res.status(201).json({
        message: 'Scan created successfully',
        scan: {
          id: scan.id,
          imageUrl: scan.imageUrl,
          plantName: scan.plantName,
          diseaseName: scan.diseaseName,
          confidence: scan.confidence,
          treatment: scan.treatment,
          createdAt: scan.createdAt,
        },
      });
    } catch (error) {
      logger.error('Failed to create scan', {
        service: 'scan-controller',
        error: (error as Error).message,
        userId: (req as any).userId,
      });
      res.status(500).json({ error: 'Failed to create scan' });
    }
  }

  static async getHistory(req: Request, res: Response) {
    try {
      const userId = (req as any).userId;
      const scans = await prisma.scan.findMany({
        where: { userId },
        orderBy: { createdAt: 'desc' },
        take: 50,
        include: {
          user: {
            select: {
              email: true,
              name: true,
            },
          },
        },
      });

      logger.info('Scan history retrieved', {
        service: 'scan-controller',
        userId,
        count: scans.length,
      });

      res.json(scans);
    } catch (error) {
      logger.error('Failed to fetch scan history', {
        service: 'scan-controller',
        error: (error as Error).message,
        userId: (req as any).userId,
      });
      res.status(500).json({ error: 'Failed to fetch scan history' });
    }
  }

  static async getScanById(req: Request, res: Response) {
    try {
      const userId = (req as any).userId;
      const { id } = req.params;

      const scan = await prisma.scan.findFirst({
        where: {
          id,
          userId,
        },
        include: {
          user: {
            select: {
              email: true,
              name: true,
            },
          },
        },
      });

      if (!scan) {
        return res.status(404).json({ error: 'Scan not found' });
      }

      logger.info('Scan retrieved', {
        service: 'scan-controller',
        scanId: id,
        userId,
      });

      res.json(scan);
    } catch (error) {
      logger.error('Failed to fetch scan', {
        service: 'scan-controller',
        error: (error as Error).message,
        userId: (req as any).userId,
        scanId: req.params.id,
      });
      res.status(500).json({ error: 'Failed to fetch scan' });
    }
  }
}


      // Parse weather if provided as JSON string
      let weatherSnapshot: Record<string, unknown> | undefined;
      if (weatherJson) {
        try {
          weatherSnapshot = typeof weatherJson === 'string' ? JSON.parse(weatherJson) : weatherJson;
        } catch (_) {}
      }

      const finalPlantName = isSoil ? 'Soil' : analysis.plantName;
      const finalDiseaseName = isSoil ? 'N/A' : analysis.diseaseName;
      const finalSeverity = analysis.severity;
      const finalConfidence = analysis.confidence;
      const finalTreatment = analysis.treatment;
      const finalFertilizer = fertilizer || analysis.fertilizer || '';
      const finalPesticide = pesticide || analysis.pesticide || null;
      const finalSoilType = soilType || analysis.soilType || null;
      const finalSoilHealth = soilHealth || analysis.soilHealth || null;
      const finalNpk = analysis.npk;

      const scan = await prisma.scan.create({
        data: {
          userId,
          imageUrl: `/uploads/${file.filename}`,
          plantName: finalPlantName,
          diseaseName: finalDiseaseName,
          cause: analysis.cause || null,
          severity: finalSeverity,
          confidence: finalConfidence,
          treatment: finalTreatment,
          fertilizer: finalFertilizer,
          pesticide: finalPesticide,
          soilType: finalSoilType,
          soilHealth: finalSoilHealth,
          isSoilAnalysis: isSoil,
          latitude: isNaN(lat) ? null : lat,
          longitude: isNaN(lng) ? null : lng,
          weather: weatherSnapshot ? JSON.stringify(weatherSnapshot) : null,
          aiModel: aiModel || 'client',
          modelVersion: aiModel ? `client-${aiModel}` : undefined,
          pestDetections: pestDetections ? (Array.isArray(pestDetections) ? JSON.stringify(pestDetections) : pestDetections) : null,
          modelConfidence: modelConfidence ? parseFloat(String(modelConfidence)) : null,
          processingTime: processingTime ? parseFloat(String(processingTime)) : null,
        },
      });

      // Minimal product research can be added here later; for now just return scan
      const responseData: Record<string, unknown> = {
        ...scan,
        aiSource: aiModel || 'client',
        weather: weatherSnapshot,
        npk: finalNpk,
        productResearch: null,
        productResearchSource: null,
        productResearchError: null,
        prevention: analysis.prevention,
        chemicalClass: analysis.chemicalClass,
        suitableCrops: analysis.suitableCrops,
        matchedDiseaseKey: analysis.matchedDiseaseKey,
        regionHint: null,
      };

      res.status(201).json(responseData);
    } catch (error: any) {
      console.error('Scan Error:', error);
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
