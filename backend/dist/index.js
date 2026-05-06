"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const helmet_1 = __importDefault(require("helmet"));
const dotenv_1 = __importDefault(require("dotenv"));
const path_1 = __importDefault(require("path"));
const fs_1 = __importDefault(require("fs"));
const prisma_1 = require("./lib/prisma");
const logger_1 = require("./utils/logger");
const health_1 = require("./utils/health");
const warmup_1 = require("./utils/warmup");
const firebaseAuth_1 = require("./middleware/firebaseAuth");
const rateLimiter_1 = require("./middleware/rateLimiter");
const logging_1 = require("./middleware/logging");
// Routes
const auth_routes_1 = __importDefault(require("./routes/auth.routes"));
const scan_routes_1 = __importDefault(require("./routes/scan.routes"));
const weather_routes_1 = __importDefault(require("./routes/weather.routes"));
const ai_routes_1 = __importDefault(require("./routes/ai.routes"));
dotenv_1.default.config();
const app = (0, express_1.default)();
const PORT = parseInt(process.env.PORT || '3000', 10);
// Initialize optional services
let redis = null;
if (process.env.REDIS_URL) {
    Promise.resolve().then(() => __importStar(require('ioredis'))).then((mod) => {
        redis = new mod.default(process.env.REDIS_URL);
        logger_1.logger.info('Redis connected', { service: 'redis' });
    }).catch((e) => logger_1.logger.warn('Redis init failed', { error: e.message }));
}
let qdrant = null;
if (process.env.QDRANT_URL) {
    Promise.resolve().then(() => __importStar(require('@qdrant/js-client-rest'))).then(({ QdrantClient }) => {
        qdrant = new QdrantClient({ url: process.env.QDRANT_URL });
        logger_1.logger.info('Qdrant connected', { service: 'qdrant' });
    }).catch((e) => logger_1.logger.warn('Qdrant init failed', { error: e.message }));
}
// Initialize Health Monitor
const healthMonitor = new health_1.HealthMonitor(prisma_1.prisma, redis, qdrant);
// Ensure uploads directory exists
const uploadsDir = path_1.default.join(process.cwd(), 'uploads');
if (!fs_1.default.existsSync(uploadsDir)) {
    fs_1.default.mkdirSync(uploadsDir, { recursive: true });
    logger_1.logger.info('Created uploads directory', { path: uploadsDir });
}
// Middleware
app.use((0, helmet_1.default)());
app.use((0, cors_1.default)({
    origin: process.env.NODE_ENV === 'production'
        ? (process.env.ALLOWED_ORIGINS?.split(',') || [])
        : true,
    credentials: true,
}));
app.use(express_1.default.json({ limit: '50mb' }));
app.use(express_1.default.urlencoded({ extended: true, limit: '50mb' }));
// Request logging middleware
app.use(logging_1.requestLogger);
app.use(logging_1.performanceMonitor);
// Static files
app.use('/uploads', express_1.default.static(uploadsDir));
// Apply rate limiting to all routes
app.use((0, rateLimiter_1.rateLimit)());
// Health check endpoint
app.get('/health', async (req, res) => {
    try {
        const healthStatus = await healthMonitor.getHealthStatus();
        const statusCode = healthStatus.status === 'error' ? 503 : 200;
        res.status(statusCode).json(healthStatus);
    }
    catch (error) {
        logger_1.logger.error('Health check failed', { error: error.message });
        res.status(503).json({
            status: 'error',
            timestamp: new Date().toISOString(),
            error: 'Health check failed',
        });
    }
});
// Public routes
app.use('/api/auth', auth_routes_1.default);
app.use('/api/weather', firebaseAuth_1.optionalFirebaseAuth, weather_routes_1.default);
// Protected routes
app.use('/api/scans', firebaseAuth_1.firebaseAuth, rateLimiter_1.limitScans, scan_routes_1.default);
app.use('/api/ai', firebaseAuth_1.firebaseAuth, rateLimiter_1.limitAI, ai_routes_1.default);
// WebSocket endpoint stub
app.get('/ws/detect', firebaseAuth_1.firebaseAuth, rateLimiter_1.limitWebsocket, (req, res) => {
    res.status(400).json({
        error: 'WebSocket endpoint',
        message: 'Please use WebSocket protocol to connect',
    });
});
// Error logging middleware
app.use(logging_1.errorLogger);
// Error handling middleware
app.use((err, req, res, next) => {
    (0, logger_1.logError)(err, {
        path: req.path,
        method: req.method,
        userId: req.userId,
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
    logger_1.logger.info('Server starting', {
        port: PORT,
        env: process.env.NODE_ENV || 'development',
    });
    try {
        const warmup = new warmup_1.ModelWarmup({
            models: [
                process.env.OLLAMA_VISION_MODEL || 'llava:latest',
                process.env.OLLAMA_CHAT_MODEL || 'phi3:mini',
            ].filter(Boolean),
            ollamaHost: process.env.OLLAMA_HOST?.replace(/\/$/, '') || 'http://localhost:11434',
            warmupTimeout: 60000,
        }, healthMonitor);
        logger_1.logger.info('Starting model warmup...');
        const warmupResult = await warmup.warmup();
        if (warmupResult.success) {
            logger_1.logger.info('Model warmup completed', {
                duration_ms: warmupResult.durationMs,
                loaded: warmupResult.loadedModels,
            });
        }
        else {
            logger_1.logger.warn('Model warmup completed with errors', {
                duration_ms: warmupResult.durationMs,
                failed: warmupResult.failedModels,
            });
        }
        warmup.backgroundLoad(['nomic-embed-text', 'all-minilm']);
    }
    catch (error) {
        logger_1.logger.warn('Model warmup skipped', { error: error.message });
    }
    logger_1.logger.info(`Server ready on port ${PORT}`);
});
// Graceful shutdown
process.on('SIGTERM', () => {
    logger_1.logger.info('SIGTERM received: shutting down gracefully');
    server.close(() => {
        logger_1.logger.info('Process terminated');
        process.exit(0);
    });
});
process.on('SIGINT', () => {
    logger_1.logger.info('SIGINT received: shutting down gracefully');
    server.close(() => {
        logger_1.logger.info('Process terminated');
        process.exit(0);
    });
});
