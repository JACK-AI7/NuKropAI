import { FastifyInstance } from 'fastify';
import { processSoilHealthCard, triggerCropLifecycleEngine } from '../controllers/ai.controller';
import { authenticate } from '../middleware/auth';

export default async function aiRoutes(fastify: FastifyInstance) {
  // Routes for AI processing and integrations
  
  // 1. Process Soil Health Card OCR
  fastify.post('/soil-ocr', { preHandler: [authenticate] }, processSoilHealthCard);
  
  // 2. Trigger the Crop Lifecycle Engine manually (usually hit by chron)
  fastify.post('/lifecycle/tick', { preHandler: [authenticate] }, triggerCropLifecycleEngine);
}
