import { FastifyInstance } from 'fastify';
import { reportOutbreak, getAlerts } from '../controllers/pest.controller';
import { authenticate } from '../middleware/auth';

export default async function pestRoutes(fastify: FastifyInstance) {
  fastify.post('/report', { preHandler: [authenticate] }, reportOutbreak);
  fastify.get('/alerts', { preHandler: [authenticate] }, getAlerts);
}
