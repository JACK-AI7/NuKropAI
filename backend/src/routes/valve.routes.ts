import { FastifyInstance } from 'fastify';
import { getValves, toggleValve } from '../controllers/valve.controller';
import { authenticate, requireRole } from '../middleware/auth';

export default async function valveRoutes(fastify: FastifyInstance) {
  // Registered under /irrigation prefix -> /irrigation/valves
  fastify.get('/valves', { preHandler: [authenticate] }, getValves);
  // Registered under /irrigation prefix -> /irrigation/valves/toggle
  fastify.post('/valves/toggle', { preHandler: [authenticate, requireRole(['farmer', 'admin'])] }, toggleValve);
}
