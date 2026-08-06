import { otelSdk } from './tracing';
// Start OpenTelemetry SDK before loading Fastify
otelSdk.start();

import Fastify from 'fastify';
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import rateLimit from '@fastify/rate-limit';
import * as dotenv from 'dotenv';
import { pool } from './config/db';
import apiRoutes from './routes';
import client from 'prom-client';
import pino from 'pino';
import fastifyStatic from '@fastify/static';
import path from 'path';


dotenv.config();

// Initialize structured logging for Loki
const logger = pino({
  level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
  transport: process.env.NODE_ENV !== 'production' ? { target: 'pino-pretty' } : undefined
});

const fastify = Fastify({ logger });

// Serve APKs directly from the user's Downloads folder
fastify.register(fastifyStatic, {
  root: 'C:\\Users\\bjasw\\Downloads',
  prefix: '/downloads/', 
});


// Initialize Prometheus Metrics
const collectDefaultMetrics = client.collectDefaultMetrics;
collectDefaultMetrics({ prefix: 'nukrop_' });

// Custom SRE Metrics
export const iotCommandCounter = new client.Counter({
  name: 'nukrop_iot_commands_total',
  help: 'Total IoT commands dispatched',
  labelNames: ['provider', 'command', 'status']
});

export const iotTelemetryLatency = new client.Histogram({
  name: 'nukrop_iot_telemetry_latency_seconds',
  help: 'Latency between command dispatch and async hardware verification',
  buckets: [0.5, 1, 2, 5, 10, 15] // SRE timeout is 15s
});

fastify.get('/metrics', async (request, reply) => {
  reply.header('Content-Type', client.register.contentType);
  return client.register.metrics();
});


// Register Helmet Security Headers
fastify.register(helmet, {
  global: true,
  contentSecurityPolicy: false, // Turn off CSP if index.html is hosted separately or proxying
});

// Register CORS
fastify.register(cors, {
  origin: true,
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
});

// Register WebSocket Support for IoT Telemetry
fastify.register(require('@fastify/websocket'));

// Register Rate Limiter (Max 100 requests per minute per IP)
fastify.register(rateLimit, {
  max: 100,
  timeWindow: '1 minute',
  errorResponseBuilder: (request, context) => {
    return {
      statusCode: 429,
      error: 'Too Many Requests',
      message: `Rate limit exceeded. Try again in ${context.after}.`
    };
  }
});

// Public Health Check
fastify.get('/health', async (request, reply) => {
  try {
    const client = await pool.connect();
    client.release();
    return { status: 'ok', db: 'connected', timestamp: new Date().toISOString() };
  } catch (err) {
    fastify.log.error(err);
    return reply.status(500).send({ status: 'error', db: 'disconnected', error: (err as Error).message });
  }
});

// Register API Route Hub
fastify.register(apiRoutes, { prefix: '/api/v1' });

// Global Error Handler
fastify.setErrorHandler((error, request, reply) => {
  fastify.log.error(error);
  
  if (error.statusCode) {
    return reply.status(error.statusCode).send({
      error: error.name,
      message: error.message
    });
  }

  return reply.status(500).send({
    error: 'InternalServerError',
    message: 'An unexpected database or processing error occurred'
  });
});

const start = async () => {
  try {
    const port = process.env.PORT ? parseInt(process.env.PORT) : 3000;
    await fastify.listen({ port, host: '0.0.0.0' });
    console.log(`NuKropAI Core Server listening on port ${port}`);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
