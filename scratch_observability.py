import re

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\backend\src\server.ts", "r", encoding="utf-8") as f:
    content = f.read()

imports = """import Fastify from 'fastify';
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import rateLimit from '@fastify/rate-limit';
import * as dotenv from 'dotenv';
import { pool } from './config/db';
import apiRoutes from './routes';
import client from 'prom-client';
import pino from 'pino';
"""

content = re.sub(r'import Fastify.*import apiRoutes from \'\./routes\';', imports, content, flags=re.DOTALL)

logger_config = """// Initialize structured logging for Loki
const logger = pino({
  level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
  transport: process.env.NODE_ENV !== 'production' ? { target: 'pino-pretty' } : undefined
});

const fastify = Fastify({ logger });

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
"""

content = re.sub(r'const fastify = Fastify.*?\}\);', logger_config, content, flags=re.DOTALL)

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\backend\src\server.ts", "w", encoding="utf-8") as f:
    f.write(content)
