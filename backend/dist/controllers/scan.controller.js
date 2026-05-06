"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ScanController = void 0;
const prisma_1 = require("../lib/prisma");
const weather_service_1 = require("../services/weather.service");
const retry_1 = require("../utils/retry");
const logger_1 = require("../utils/logger");
class ScanController {
    static async createScan(req, res) {
        try {
            const userId = req.userId;
            const file = req.file;
            const { label, isSoilAnalysis, latitude, longitude, confidence, 
            // Client-provided analysis fields (if mobile did analysis)
            plantName, diseaseName, cause, severity, treatment, fertilizer, pesticide, soilType, soilHealth, aiModel, modelConfidence, processingTime, pestDetections, weather: weatherJson, matchedDiseaseKey, prevention, chemicalClass, suitableCrops, } = req.body;
            if (!file)
                return res.status(400).json({ error: 'No image uploaded' });
            const lat = parseFloat(latitude ?? req.body.lat);
            const lng = parseFloat(longitude ?? req.body.lng);
            const isSoil = isSoilAnalysis === 'true' || isSoilAnalysis === true;
            // If client already provided full analysis, skip server-side AI
            const clientAnalyzed = plantName != null || soilType != null;
            let analysis = null;
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
            }
            else {
                // Server-side AI path (legacy) — keep for compatibility
                return res.status(501).json({ error: 'Server-side AI is disabled. Use client analysis.' });
            }
            // Parse weather if provided as JSON string
            let weatherSnapshot;
            if (weatherJson) {
                try {
                    weatherSnapshot = typeof weatherJson === 'string' ? JSON.parse(weatherJson) : weatherJson;
                }
                catch (_) { }
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
                    weatherData = await (0, retry_1.retryWithTimeout)(() => weather_service_1.WeatherService.getWeather(lat, lng), 10000, { maxRetries: 2 });
                }
                catch (error) {
                    logger_1.logger.warn('Weather fetch failed, continuing without weather data', {
                        error: error.message,
                        lat,
                        lng,
                    });
                }
            }
            const scan = await prisma_1.prisma.scan.create({
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
            logger_1.logger.info('Scan created successfully', {
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
        }
        catch (error) {
            logger_1.logger.error('Failed to create scan', {
                service: 'scan-controller',
                error: error.message,
                userId: req.userId,
            });
            res.status(500).json({ error: 'Failed to create scan' });
        }
    }
    static async getHistory(req, res) {
        try {
            const userId = req.userId;
            const scans = await prisma_1.prisma.scan.findMany({
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
            logger_1.logger.info('Scan history retrieved', {
                service: 'scan-controller',
                userId,
                count: scans.length,
            });
            res.json(scans);
        }
        catch (error) {
            logger_1.logger.error('Failed to fetch scan history', {
                service: 'scan-controller',
                error: error.message,
                userId: req.userId,
            });
            res.status(500).json({ error: 'Failed to fetch scan history' });
        }
    }
    static async getScanById(req, res) {
        try {
            const userId = req.userId;
            const { id } = req.params;
            const scan = await prisma_1.prisma.scan.findFirst({
                where: {
                    id: id,
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
            logger_1.logger.info('Scan retrieved', {
                service: 'scan-controller',
                scanId: id,
                userId,
            });
            res.json(scan);
        }
        catch (error) {
            logger_1.logger.error('Failed to fetch scan', {
                service: 'scan-controller',
                error: error.message,
                userId: req.userId,
                scanId: req.params.id,
            });
            res.status(500).json({ error: 'Failed to fetch scan' });
        }
    }
}
exports.ScanController = ScanController;
