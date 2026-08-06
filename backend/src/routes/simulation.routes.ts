import { FastifyInstance } from 'fastify';
import { runSimulation, getSimulations } from '../controllers/simulation.controller';
import { authenticate } from '../middleware/auth';

export default async function simulationRoutes(fastify: FastifyInstance) {
  fastify.post('/run', { preHandler: [authenticate] }, runSimulation);
  fastify.get('/', { preHandler: [authenticate] }, getSimulations);
}
