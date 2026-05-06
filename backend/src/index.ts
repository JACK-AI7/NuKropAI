import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import path from 'os';
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
const PORT = process.env.PORT || 3000;

// Initialize Redis
let redis: any = null;
if (process.env.REDIS_URL) {
  const Redis = (await import('ioredis')).default;
  redis = new Redis(process.env.REDIS_URL);
  logger.info('Redis connected', { service: 'redis' });
}

// Initialize Qdrant
let qdrant: any = null;
if (process.env.QDRANT_URL) {
  const { QdrantClient } = await import('@qdrant/js-client-rest');
  qdrant = new QdrantClient({ url: process.env.QDRANT_URL });
  logger.info('Qdrant connected', { service: 'qdrant' });
}

// Initialize Health Monitor
const healthMonitor = new HealthMonitor(prisma, redis, qdrant);

// Ensure uploads directory exists
const uploadsDir = path.join(process.cwd(), 'uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
  logger.info('✅ Created uploads directory', { path: uploadsDir });
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

// Health check endpoint with comprehensive status
app.get('/health', async (req, res) => {
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

// Public routes (no auth required)
app.use('/api/auth', authRoutes);
app.use('/api/weather', optionalFirebaseAuth, weatherRoutes);

// Protected routes (require Firebase auth)
app.use('/api/scans', firebaseAuth, limitScans, scanRoutes);
app.use('/api/ai', firebaseAuth, limitAI, aiRoutes);

// WebSocket endpoint with auth and rate limiting
app.get('/ws/detect', firebaseAuth, limitWebsocket, (req, res) => {
  res.status(400).json({ 
    error: 'WebSocket endpoint',
    message: 'Please use WebSocket protocol to connect'
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
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

// Start server
const server = app.listen(PORT, '0.0.0.0', async () => {
  logger.info('🚀 Server starting', {
    port: PORT,
    env: process.env.NODE_ENV || 'development',
    nodeEnv: process.env.NODE_ENV,
  });

  // Run model warmup
  try {
    const warmup = new ModelWarmup({
      models: [
        process.env.OLLAMA_VISION_MODEL || 'llava:latest',
        process.env.OLLAMA_CHAT_MODEL || 'phi3:mini',
      ].filter(Boolean) as string[],
      ollamaHost: process.env.OLLAMA_HOST?.replace(/\/$/, '') || 'http://localhost:11434',
      warmupTimeout: 60000,
    }, healthMonitor);

    logger.info('Starting model warmup...');
    const warmupResult = await warmup.warmup();
    
    if (warmupResult.success) {
      logger.info('✅ Model warmup completed successfully', {
        duration_ms: warmupResult.durationMs,
        loaded: warmupResult.loadedModels,
      });
    } else {
      logger.warn('⚠️ Model warmup completed with errors', {
        duration_ms: warmupResult.durationMs,
        loaded: warmupResult.loadedModels,
        failed: warmupResult.failedModels,
        errors: warmupResult.errors,
      });
    }

    // Background load additional models
    warmup.backgroundLoad(['nomic-embed-text', 'all-minilm']);

  } catch (error) {
    logger.error('Model warmup failed', { error: (error as Error).message });
  }

  logger.info(`✅ Server ready`);
  logger.info(`📡 Health: http://localhost:${PORT}/health`);
  logger.info(`🔗 API: http://localhost:${PORT}/api`);
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

import authRoutes from './routes/auth.routes';
import scanRoutes from './routes/scan.routes';
import weatherRoutes from './routes/weather.routes';
import aiRoutes from './routes/ai.routes';

dotenv.config();


const app = express();
const PORT = process.env.PORT || 3000;

// Ensure uploads directory exists
const uploadsDir = path.join(process.cwd(), 'uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
  console.log('✅ Created uploads directory:', uploadsDir);
}

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.NODE_ENV === 'production' 
    ? (process.env.ALLOWED_ORIGINS?.split(',') || [])
    : true,
  credentials: true,
}));
app.use(morgan('dev'));
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));
app.use('/uploads', express.static(uploadsDir));

// Routes
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    env: process.env.NODE_ENV || 'development',
    ollama: process.env.OLLAMA_HOST || 'not configured',
    mistral: process.env.MISTRAL_API_KEY ? 'configured' : 'not configured',
  });
});

app.use('/api/auth', authRoutes);
app.use('/api/scans', scanRoutes);
app.use('/api/weather', weatherRoutes);
app.use('/api/ai', aiRoutes);
app.get('/api/recommendations', (req, res) => {
  try {
    const data = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'data', 'crops.json'), 'utf8'));
    res.json(data.crops);
  } catch (err) {
    console.error('Error reading crops data:', err);
    res.status(500).json({ error: 'Failed to load recommendations data' });
  }
});

//Error handling
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error(err.stack);
  res.status(500).json({ 
    error: 'Something went wrong!',
    message: process.env.NODE_ENV === 'development' ? err.message : undefined,
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

const server = app.listen(PORT as number, '0.0.0.0', () => {
  console.log(`🚀 Server running on http://0.0.0.0:${PORT}`);
  console.log(`📡 Health check: http://localhost:${PORT}/health`);
  console.log(`🔗 API base: http://localhost:${PORT}/api`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received: shutting down gracefully');
  server.close(() => {
    console.log('Process terminated');
  });
});



