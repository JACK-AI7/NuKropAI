import { FastifyRequest, FastifyReply } from 'fastify';
import * as jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET || 'SUPER_SECURE_JWT_SECRET_KEY_12345';

export interface AuthenticatedUser {
  id: string;
  email: string;
  role: 'farmer' | 'buyer' | 'admin';
}

declare module 'fastify' {
  interface FastifyRequest {
    user?: AuthenticatedUser;
  }
}

export const authenticate = async (request: FastifyRequest, reply: FastifyReply) => {
  try {
    const authHeader = request.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      reply.status(401).send({ error: 'Unauthorized: Missing or invalid authorization header format' });
      return;
    }

    const token = authHeader.substring(7);
    const decoded = jwt.verify(token, JWT_SECRET) as AuthenticatedUser;
    request.user = decoded;
  } catch (err) {
    reply.status(401).send({ error: 'Unauthorized: Access token has expired or is invalid' });
  }
};

export const requireRole = (allowedRoles: ('farmer' | 'buyer' | 'admin')[]) => {
  return async (request: FastifyRequest, reply: FastifyReply) => {
    if (!request.user) {
      reply.status(401).send({ error: 'Unauthorized: User authentication required' });
      return;
    }

    if (!allowedRoles.includes(request.user.role)) {
      reply.status(403).send({ error: 'Forbidden: You do not have permission to access this resource' });
      return;
    }
  };
};
