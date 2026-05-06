/**
 * Health check utilities and status monitoring
 */

import { PrismaClient } from '@prisma/client';
import Redis from 'ioredis';
import { QdrantClient } from '@qdrant/js-client-rest';
import { logger } from './logger';

export interface HealthStatus {
  status: 'ok' | 'degraded' | 'error';
  timestamp: string;
  uptime: number;
  version: string;
  services: {
    redis: ServiceStatus;
    qdrant: ServiceStatus;
    ollama: ServiceStatus;
    database: ServiceStatus;
  };
  resources: ResourceStatus;
  queue: QueueStatus;
}

export interface ServiceStatus {
  status: 'ok' | 'degraded' | 'error' | 'unknown';
  latency_ms?: number;
  error?: string;
  [key: string]: any;
}

export interface ResourceStatus {
  cpu_usage_percent: number;
  memory_usage_mb: number;
  memory_total_mb: number;
  gpu_usage_percent?: number;
  gpu_memory_mb?: number;
  disk_usage_percent?: number;
}

export interface QueueStatus {
  size: number;
  processing: number;
  avg_wait_time_ms: number;
  max_wait_time_ms: number;
}

export interface ModelInfo {
  name: string;
  version: string;
  loaded: boolean;
  lastUsed: string;
  inferenceCount: number;
  avgInferenceTimeMs: number;
}

export class HealthMonitor {
  private startTime: number;
  private prisma: PrismaClient;
  private redis: Redis | null;
  private qdrant: QdrantClient | null;
  private loadedModels: Map<string, ModelInfo>;
  private inferenceQueue: Array<{ timestamp: number; duration: number }>;
  private readonly MAX_QUEUE_SIZE = 1000;

  constructor(
    prisma: PrismaClient,
    redis: Redis | null,
    qdrant: QdrantClient | null
  ) {
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
  async getHealthStatus(): Promise<HealthStatus> {
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
  private async checkRedis(): Promise<ServiceStatus> {
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
    } catch (error) {
      logger.error('Redis health check failed', { error: (error as Error).message });
      return { status: 'error', error: (error as Error).message };
    }
  }

  /**
   * Check Qdrant connection
   */
  private async checkQdrant(): Promise<ServiceStatus> {
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
    } catch (error) {
      logger.error('Qdrant health check failed', { error: (error as Error).message });
      return { status: 'error', error: (error as Error).message };
    }
  }

  /**
   * Check Ollama connection and loaded models
   */
  private async checkOllama(): Promise<ServiceStatus> {
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
        models_loaded: models.map((m: any) => m.name),
        model_count: models.length,
        gpu_utilization: gpuInfo?.utilization,
        gpu_memory_mb: gpuInfo?.memoryUsed,
      };
    } catch (error) {
      logger.error('Ollama health check failed', { error: (error as Error).message });
      return { status: 'error', error: (error as Error).message };
    }
  }

  /**
   * Check database connection
   */
  private async checkDatabase(): Promise<ServiceStatus> {
    try {
      const start = Date.now();
      await this.prisma.$queryRaw`SELECT 1`;
      const latency = Date.now() - start;

      const scanCount = await this.prisma.scan.count();
      const userCount = await this.prisma.user.count();

      return {
        status: 'ok',
        latency_ms: latency,
        scan_count: scanCount,
        user_count: userCount,
      };
    } catch (error) {
      logger.error('Database health check failed', { error: (error as Error).message });
      return { status: 'error', error: (error as Error).message };
    }
  }

  /**
   * Get system resource usage
   */
  private async getResourceUsage(): Promise<ResourceStatus> {
    const cpuUsage = await this.getCpuUsage();
    const memory = process.memoryUsage();
    const totalMemory = os.totalmem();
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
  private async getCpuUsage(): Promise<number> {
    const cpus = os.cpus();
    const totalIdle = cpus.reduce((acc, cpu) => acc + Object.values(cpu.times).reduce((a, b) => a + b), 0);
    const totalTick = cpus.reduce((acc, cpu) => acc + Object.values(cpu.times).reduce((a, b) => a + b), 0);
    return Math.round((1 - totalIdle / totalTick) * 100);
  }

  /**
   * Get GPU information
   */
  private async getGpuInfo(): Promise<{ utilization: number; memoryUsed: number } | null> {
    try {
      // Try to get GPU info from nvidia-smi or similar
      const { execSync } = await import('child_process');
      const output = execSync('nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits', { encoding: 'utf8' });
      const lines = output.trim().split('\n');
      if (lines.length > 0) {
        const [utilization, memoryUsed, memoryTotal] = lines[0].split(',').map(s => parseInt(s.trim()));
        return { utilization, memoryUsed };
      }
    } catch (error) {
      // GPU not available or command failed
    }
    return null;
  }

  /**
   * Get queue status
   */
  private getQueueStatus(): QueueStatus {
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
  recordInference(durationMs: number): void {
    this.inferenceQueue.push({ timestamp: Date.now(), duration: durationMs });
    
    // Keep queue size manageable
    if (this.inferenceQueue.length > this.MAX_QUEUE_SIZE) {
      this.inferenceQueue.shift();
    }
  }

  /**
   * Register loaded model
   */
  registerModel(name: string, version: string): void {
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
  updateModelUsage(name: string, inferenceTimeMs: number): void {
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
  getLoadedModels(): ModelInfo[] {
    return Array.from(this.loadedModels.values());
  }

  /**
   * Calculate overall health status
   */
  private calculateOverallStatus(services: ServiceStatus[]): 'ok' | 'degraded' | 'error' {
    const errorCount = services.filter(s => s.status === 'error').length;
    const degradedCount = services.filter(s => s.status === 'degraded').length;

    if (errorCount > 0) return 'error';
    if (degradedCount > 0) return 'degraded';
    return 'ok';
  }

  /**
   * Get server uptime in seconds
   */
  private getUptime(): number {
    return Math.round((Date.now() - this.startTime) / 1000);
  }
}
