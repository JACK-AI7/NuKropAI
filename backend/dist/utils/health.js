"use strict";
/**
 * Health check utilities and status monitoring
 */
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
exports.HealthMonitor = void 0;
const os_1 = __importDefault(require("os"));
const logger_1 = require("./logger");
class HealthMonitor {
    constructor(prisma, redis, qdrant) {
        this.MAX_QUEUE_SIZE = 1000;
        this.startTime = Date.now();
        this.prisma = prisma;
        this.redis = redis;
        this.qdrant = qdrant;
        this.loadedModels = new Map();
        this.inferenceQueue = [];
    }
    /**
     * Get comprehensive health status
     */
    async getHealthStatus() {
        const [redisStatus, qdrantStatus, ollamaStatus, dbStatus, resources] = await Promise.all([
            this.checkRedis(),
            this.checkQdrant(),
            this.checkOllama(),
            this.checkDatabase(),
            this.getResourceUsage(),
        ]);
        const queueStatus = this.getQueueStatus();
        const overallStatus = this.calculateOverallStatus([redisStatus, qdrantStatus, ollamaStatus, dbStatus]);
        return {
            status: overallStatus,
            timestamp: new Date().toISOString(),
            uptime: this.getUptime(),
            version: process.env.npm_package_version || '1.0.0',
            services: {
                redis: redisStatus,
                qdrant: qdrantStatus,
                ollama: ollamaStatus,
                database: dbStatus,
            },
            resources,
            queue: queueStatus,
        };
    }
    /**
     * Check Redis connection
     */
    async checkRedis() {
        if (!this.redis) {
            return { status: 'unknown', error: 'Redis not configured' };
        }
        try {
            const start = Date.now();
            await this.redis.ping();
            const latency = Date.now() - start;
            const info = await this.redis.info();
            const memoryMatch = info.match(/used_memory_human:(\w+)/);
            const memoryUsed = memoryMatch ? memoryMatch[1] : 'unknown';
            return {
                status: 'ok',
                latency_ms: latency,
                memory_used: memoryUsed,
            };
        }
        catch (error) {
            logger_1.logger.error('Redis health check failed', { error: error.message });
            return { status: 'error', error: error.message };
        }
    }
    /**
     * Check Qdrant connection
     */
    async checkQdrant() {
        if (!this.qdrant) {
            return { status: 'unknown', error: 'Qdrant not configured' };
        }
        try {
            const start = Date.now();
            const collections = await this.qdrant.getCollections();
            const latency = Date.now() - start;
            let totalPoints = 0;
            for (const collection of collections.collections) {
                const info = await this.qdrant.getCollection(collection.name);
                totalPoints += info.points_count || 0;
            }
            return {
                status: 'ok',
                latency_ms: latency,
                collections: collections.collections.length,
                points_count: totalPoints,
            };
        }
        catch (error) {
            logger_1.logger.error('Qdrant health check failed', { error: error.message });
            return { status: 'error', error: error.message };
        }
    }
    /**
     * Check Ollama connection and loaded models
     */
    async checkOllama() {
        try {
            const start = Date.now();
            const response = await fetch(`${process.env.OLLAMA_HOST}/api/tags`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            });
            const latency = Date.now() - start;
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            const data = await response.json();
            const models = data.models || [];
            // Check GPU utilization if available
            const gpuInfo = await this.getGpuInfo();
            return {
                status: 'ok',
                latency_ms: latency,
                models_loaded: models.map((m) => m.name),
                model_count: models.length,
                gpu_utilization: gpuInfo?.utilization,
                gpu_memory_mb: gpuInfo?.memoryUsed,
            };
        }
        catch (error) {
            logger_1.logger.error('Ollama health check failed', { error: error.message });
            return { status: 'error', error: error.message };
        }
    }
    /**
     * Check database connection
     */
    async checkDatabase() {
        try {
            const start = Date.now();
            await this.prisma.$queryRaw `SELECT 1`;
            const latency = Date.now() - start;
            const scanCount = await this.prisma.scan.count();
            const userCount = await this.prisma.user.count();
            return {
                status: 'ok',
                latency_ms: latency,
                scan_count: scanCount,
                user_count: userCount,
            };
        }
        catch (error) {
            logger_1.logger.error('Database health check failed', { error: error.message });
            return { status: 'error', error: error.message };
        }
    }
    /**
     * Get system resource usage
     */
    async getResourceUsage() {
        const cpuUsage = await this.getCpuUsage();
        const memory = process.memoryUsage();
        const totalMemory = os_1.default.totalmem();
        const gpuInfo = await this.getGpuInfo();
        return {
            cpu_usage_percent: cpuUsage,
            memory_usage_mb: Math.round(memory.heapUsed / 1024 / 1024),
            memory_total_mb: Math.round(totalMemory / 1024 / 1024),
            gpu_usage_percent: gpuInfo?.utilization,
            gpu_memory_mb: gpuInfo?.memoryUsed,
        };
    }
    /**
     * Get CPU usage percentage
     */
    async getCpuUsage() {
        const cpus = os_1.default.cpus();
        const totalIdle = cpus.reduce((acc, cpu) => acc + Object.values(cpu.times).reduce((a, b) => a + b, 0), 0);
        const totalTick = cpus.reduce((acc, cpu) => acc + Object.values(cpu.times).reduce((a, b) => a + b, 0), 0);
        return Math.round((1 - totalIdle / totalTick) * 100);
    }
    /**
     * Get GPU information
     */
    async getGpuInfo() {
        try {
            // Try to get GPU info from nvidia-smi or similar
            const { execSync } = await Promise.resolve().then(() => __importStar(require('child_process')));
            const output = execSync('nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits', { encoding: 'utf8' });
            const lines = output.trim().split('\n');
            if (lines.length > 0) {
                const [utilization, memoryUsed, memoryTotal] = lines[0].split(',').map(s => parseInt(s.trim()));
                return { utilization, memoryUsed };
            }
        }
        catch (error) {
            // GPU not available or command failed
        }
        return null;
    }
    /**
     * Get queue status
     */
    getQueueStatus() {
        const now = Date.now();
        const oneMinuteAgo = now - 60000;
        // Filter recent queue items
        const recentItems = this.inferenceQueue.filter(item => item.timestamp > oneMinuteAgo);
        const processing = Math.min(recentItems.length, 10); // Assume max 10 concurrent
        const avgWaitTime = recentItems.length > 0
            ? Math.round(recentItems.reduce((sum, item) => sum + item.duration, 0) / recentItems.length)
            : 0;
        const maxWaitTime = recentItems.length > 0
            ? Math.max(...recentItems.map(item => item.duration))
            : 0;
        return {
            size: this.inferenceQueue.length,
            processing,
            avg_wait_time_ms: avgWaitTime,
            max_wait_time_ms: maxWaitTime,
        };
    }
    /**
     * Record inference metrics
     */
    recordInference(durationMs) {
        this.inferenceQueue.push({ timestamp: Date.now(), duration: durationMs });
        // Keep queue size manageable
        if (this.inferenceQueue.length > this.MAX_QUEUE_SIZE) {
            this.inferenceQueue.shift();
        }
    }
    /**
     * Register loaded model
     */
    registerModel(name, version) {
        this.loadedModels.set(name, {
            name,
            version,
            loaded: true,
            lastUsed: new Date().toISOString(),
            inferenceCount: 0,
            avgInferenceTimeMs: 0,
        });
    }
    /**
     * Update model usage
     */
    updateModelUsage(name, inferenceTimeMs) {
        const model = this.loadedModels.get(name);
        if (model) {
            model.lastUsed = new Date().toISOString();
            model.inferenceCount++;
            model.avgInferenceTimeMs =
                (model.avgInferenceTimeMs * (model.inferenceCount - 1) + inferenceTimeMs) / model.inferenceCount;
        }
    }
    /**
     * Get loaded models
     */
    getLoadedModels() {
        return Array.from(this.loadedModels.values());
    }
    /**
     * Calculate overall health status
     */
    calculateOverallStatus(services) {
        const errorCount = services.filter(s => s.status === 'error').length;
        const degradedCount = services.filter(s => s.status === 'degraded').length;
        if (errorCount > 0)
            return 'error';
        if (degradedCount > 0)
            return 'degraded';
        return 'ok';
    }
    /**
     * Get server uptime in seconds
     */
    getUptime() {
        return Math.round((Date.now() - this.startTime) / 1000);
    }
}
exports.HealthMonitor = HealthMonitor;
