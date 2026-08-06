import { FastifyInstance } from 'fastify';
import { logTelemetry, getLatestTelemetry } from '../controllers/soil.controller';
import { authenticate } from '../middleware/auth';

export default async function soilRoutes(fastify: FastifyInstance) {
  fastify.post('/telemetry', { preHandler: [authenticate] }, logTelemetry);
  fastify.get('/telemetry/latest', { preHandler: [authenticate] }, getLatestTelemetry);
}
