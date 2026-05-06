import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import path from 'path';
import fs from 'fs';
import { prisma } from './lib/prisma';
import { logger, logRequest, logError } from './utils/logger';
import { HealthMonitor } from './utils/health';
import { ModelWarmup } from './utils/warmup';
import { firebaseAuth, optionalFirebaseAuth } from './middleware/firebaseAuth';
import { rateLimit, limitScans, limitAI, limitWebsocket } from './middleware/rateLimiter';
import { validateImageUpload, upload } from './middleware/imageValidation';
import { requestLogger, errorLogger, performanceMonitor } from './middleware/logging';

// Routes
import authRoutes from './routes/auth.routes';
import scanRoutes from './routes/scan.routes';
import weatherRoutes from './routes/weather.routes';
import aiRoutes from './routes/ai.routes';

dotenv.config();

const app = express();
const PORT = parseInt(process.env.PORT || '3000', 10);

// Initialize optional services
let redis: any = null;
if (process.env.REDIS_URL) {
  import('ioredis').then((mod) => {
    redis = new mod.default(process.env.REDIS_URL!);
    logger.info('Redis connected', { service: 'redis' });
  }).catch((e) => logger.warn('Redis init failed', { error: e.message }));
}

let qdrant: any = null;
if (process.env.QDRANT_URL) {
  import('@qdrant/js-client-rest').then(({ QdrantClient }) => {
    qdrant = new QdrantClient({ url: process.env.QDRANT_URL });
    logger.info('Qdrant connected', { service: 'qdrant' });
  }).catch((e) => logger.warn('Qdrant init failed', { error: e.message }));
}

// Initialize Health Monitor
const healthMonitor = new HealthMonitor(prisma, redis, qdrant);

// Ensure uploads directory exists
const uploadsDir = path.join(process.cwd(), 'uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
  logger.info('Created uploads directory', { path: uploadsDir });
}

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.NODE_ENV === 'production'
    ? (process.env.ALLOWED_ORIGINS?.split(',') || [])
    : true,
  credentials: true,
}));
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Request logging middleware
app.use(requestLogger);
app.use(performanceMonitor);

// Static files
app.use('/uploads', express.static(uploadsDir));

// Apply rate limiting to all routes
app.use(rateLimit());

// Health check endpoint
app.get('/health', async (req: express.Request, res: express.Response) => {
  try {
    const healthStatus = await healthMonitor.getHealthStatus();
    const statusCode = healthStatus.status === 'error' ? 503 : 200;
    res.status(statusCode).json(healthStatus);
  } catch (error) {
    logger.error('Health check failed', { error: (error as Error).message });
    res.status(503).json({
      status: 'error',
      timestamp: new Date().toISOString(),
      error: 'Health check failed',
    });
  }
});

// Public routes
app.use('/api/auth', authRoutes);
app.use('/api/weather', optionalFirebaseAuth, weatherRoutes);

// Protected routes
app.use('/api/scans', firebaseAuth, limitScans, scanRoutes);
app.use('/api/ai', firebaseAuth, limitAI, aiRoutes);

// WebSocket endpoint stub
app.get('/ws/detect', firebaseAuth, limitWebsocket, (req: express.Request, res: express.Response) => {
  res.status(400).json({
    error: 'WebSocket endpoint',
    message: 'Please use WebSocket protocol to connect',
  });
});

// Error logging middleware
app.use(errorLogger);

// Error handling middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  logError(err, {
    path: req.path,
    method: req.method,
    userId: (req as any).userId,
  });
  res.status(err.status || 500).json({
    error: 'Something went wrong!',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined,
  });
});

// 404 handler
app.use((req: express.Request, res: express.Response) => {
  res.status(404).json({ error: 'Route not found' });
});

// Start server
const server = app.listen(PORT, '0.0.0.0', async () => {
  logger.info('Server starting', {
    port: PORT,
    env: process.env.NODE_ENV || 'development',
  });

  try {
    const warmup = new ModelWarmup(
      {
        models: [
          process.env.OLLAMA_VISION_MODEL || 'llava:latest',
          process.env.OLLAMA_CHAT_MODEL || 'phi3:mini',
        ].filter(Boolean) as string[],
        ollamaHost: process.env.OLLAMA_HOST?.replace(/\/$/, '') || 'http://localhost:11434',
        warmupTimeout: 60000,
      },
      healthMonitor
    );

    logger.info('Starting model warmup...');
    const warmupResult = await warmup.warmup();

    if (warmupResult.success) {
      logger.info('Model warmup completed', {
        duration_ms: warmupResult.durationMs,
        loaded: warmupResult.loadedModels,
      });
    } else {
      logger.warn('Model warmup completed with errors', {
        duration_ms: warmupResult.durationMs,
        failed: warmupResult.failedModels,
      });
    }

    warmup.backgroundLoad(['nomic-embed-text', 'all-minilm']);
  } catch (error) {
    logger.warn('Model warmup skipped', { error: (error as Error).message });
  }

  logger.info(`Server ready on port ${PORT}`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received: shutting down gracefully');
  server.close(() => {
    logger.info('Process terminated');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  logger.info('SIGINT received: shutting down gracefully');
  server.close(() => {
    logger.info('Process terminated');
    process.exit(0);
  });
});
