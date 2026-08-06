import { FastifyInstance } from 'fastify';
import { getContracts, createContract, verifyQr } from '../controllers/contract.controller';
import { authenticate, requireRole } from '../middleware/auth';

export default async function contractRoutes(fastify: FastifyInstance) {
  fastify.get('/', { preHandler: [authenticate] }, getContracts);
  fastify.post('/create', { preHandler: [authenticate, requireRole(['buyer', 'admin'])] }, createContract);
  fastify.post('/verify-qr', { preHandler: [authenticate, requireRole(['farmer', 'admin'])] }, verifyQr);
}
