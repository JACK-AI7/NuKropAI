"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.PestDetectionService = void 0;
const fs_1 = __importDefault(require("fs"));
const axios_1 = __importDefault(require("axios"));
/**
 * Service for communicating with the Python YOLO pest detection microservice.
 *
 * The ML service should be running separately (see ml-service/).
 * Configure its URL via ML_SERVICE_URL environment variable (default: http://localhost:8000).
 */
class PestDetectionService {
    /**
     * Detect pests in an image using YOLO.
     * Sends image as base64 JSON to the ML service.
     *
     * @param imagePath Path to the image file on disk
     * @returns Detection results with species, confidences, and bounding boxes
     * @throws Error if ML service is unreachable or returns an error
     */
    static async detect(imagePath) {
        if (!fs_1.default.existsSync(imagePath)) {
            throw new Error(`Image file not found: ${imagePath}`);
        }
        const imageBuffer = fs_1.default.readFileSync(imagePath);
        const base64 = imageBuffer.toString('base64');
        try {
            const response = await axios_1.default.post(`${this.serviceUrl}/detect`, {
                image_base64: base64,
                filename: 'image.jpg',
            }, {
                timeout: 30000,
                headers: { 'Content-Type': 'application/json' },
            });
            return response.data;
        }
        catch (error) {
            const msg = error?.response?.data?.detail || error.message;
            console.error('Pest detection service error:', msg);
            throw new Error(`ML service error: ${msg}`);
        }
    }
    /**
     * Transform YOLO detection into a unified analysis format compatible with existing Scan fields.
     *
     * For pest detection we may have multiple pests; we pick the top confidence as primary.
     *
     * @param yoloResult Raw detection result from YOLO service
     * @param isSoil Flag - ignored for YOLO (always pest)
     * @returns Object with fields matching the crop disease analysis schema
     */
    static mapToAnalysis(yoloResult, _isSoil) {
        const primary = yoloResult.detections[0];
        if (!primary) {
            throw new Error('No pests detected in the image by YOLO');
        }
        // Determine severity based on confidence
        let severity = 'Low';
        if (primary.confidence >= 0.8)
            severity = 'High';
        else if (primary.confidence >= 0.6)
            severity = 'Medium';
        // Format pest detections array for JSON storage
        const pestDetections = yoloResult.detections.map(d => ({
            species: d.species,
            confidence: d.confidence,
            bbox: d.bbox,
        }));
        return {
            plantName: 'Crop (pest-infested)', // generic crop; actual species determined by pest
            diseaseName: primary.species, // pest name used as "disease" for compatibility
            cause: 'Insect or mite pest',
            severity,
            confidence: primary.confidence,
            treatment: '', // LLM product research will fill this
            fertilizer: null,
            pesticide: null,
            npk: null,
            matchedDiseaseKey: null,
            // Extra fields stored separately in DB
            _pestDetections: pestDetections,
            _modelConfidence: yoloResult.top_confidence,
            _processingTime: yoloResult.processing_time,
            _aiSource: 'yolo',
        };
    }
    /**
     * Health check for the ML service.
     */
    static async health() {
        try {
            const response = await axios_1.default.get(`${this.serviceUrl}/health`, { timeout: 5000 });
            return response.data;
        }
        catch (e) {
            console.error('ML service health check failed:', e.message);
            return { status: 'unreachable', model_loaded: false };
        }
    }
}
exports.PestDetectionService = PestDetectionService;
PestDetectionService.serviceUrl = (process.env.ML_SERVICE_URL || process.env.YOLO_SERVICE_URL || 'http://localhost:8000').replace(/\/$/, '');
