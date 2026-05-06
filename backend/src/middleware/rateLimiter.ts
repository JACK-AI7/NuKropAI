/**
 * Rate Limiting Middleware
 * Uses in-memory store with Redis support option
 * Prevents abuse and protects GPU resources
 */

import { Request, Response, NextFunction } from 'express';
import { logger } from '../utils/logger';
import Redis from 'ioredis';

interface RateLimitOptions {
  windowMs: number; // Time window in milliseconds
  max: number; // Max requests per window
  message?: string;
  skipSuccessfulRequests?: boolean;
  keyGenerator?: (req: Request) => string;
  redis?: Redis;
}

interface RateLimitInfo {
  limit: number;
  remaining: number;
  resetTime: number;
  used: number;
}

class RateLimiter {
  private store: Map<string, { count: number; resetTime: number }>;
  private redis: Redis | null;
  private defaultOptions: RateLimitOptions;

  constructor(options?: Partial<RateLimitOptions>) {
    this.store = new Map();
    this.redis = null;
    this.defaultOptions = {
      windowMs: 15 * 60 * 1000, // 15 minutes
      max: 100, // 100 requests per window
      message: 'Too many requests, please try again later.',
      skipSuccessfulRequests: false,
      keyGenerator: (req) => req.ip || 'unknown',
      ...options,
    };
  }

  /**
   * Configure Redis for distributed rate limiting
   */
  useRedis(redis: Redis) {
    this.redis = redis;
  }

  /**
   * Create rate limiter middleware
   */
  create(options: Partial<RateLimitOptions> = {}) {
    const opts = { ...this.defaultOptions, ...options };

    return async (req: Request, res: Response, next: NextFunction) => {
      const key = opts.keyGenerator!(req);
      const now = Date.now();
      const windowStart = now - opts.windowMs;

      try {
        if (this.redis) {
          await this.handleRedisRateLimit(key, opts, now, windowStart, req, res, next);
        } else {
          await this.handleMemoryRateLimit(key, opts, now, windowStart, req, res, next);
        }
      } catch (error) {
        logger.error('Rate limiter error', {
          service: 'rate-limiter',
          error: (error as Error).message,
          key,
        });
        // Fail open - allow request if rate limiter fails
        next();
      }
    };
  }

  /**
   * Handle rate limiting with Redis (distributed)
   */
  private async handleRedisRateLimit(
    key: string,
    opts: RateLimitOptions,
    now: number,
    windowStart: number,
    req: Request,
    res: Response,
    next: NextFunction
  ) {
    if (!this.redis) {
      throw new Error('Redis not configured');
    }

    const redisKey = `rate_limit:${key}`;
    const pipeline = this.redis.pipeline();
    
    // Remove old entries
    pipeline.zremrangebyscore(redisKey, 0, windowStart);
    // Add current request
    pipeline.zadd(redisKey, now.toString(), now.toString());
    // Get count
    pipeline.zcard(redisKey);
    // Set expiry
    pipeline.expire(redisKey, Math.ceil(opts.windowMs / 1000));

    const results = await pipeline.exec();
    const count = results != null ? (results[2][1] as number) : 0;

    const info: RateLimitInfo = {
      limit: opts.max,
      remaining: Math.max(0, opts.max - count),
      resetTime: windowStart + opts.windowMs,
      used: count,
    };

    this.setRateLimitHeaders(res, info);

    if (count > opts.max) {
      await this.logRateLimitExceeded(key, info, req);
      return res.status(429).json({
        error: 'Too Many Requests',
        message: opts.message,
        retryAfter: Math.ceil((info.resetTime - now) / 1000),
        limit: info.limit,
        remaining: info.remaining,
        resetTime: new Date(info.resetTime).toISOString(),
      });
    }

    (req as any).rateLimitInfo = info;
    next();
  }

  /**
   * Handle rate limiting with in-memory store
   */
  private async handleMemoryRateLimit(
    key: string,
    opts: RateLimitOptions,
    now: number,
    windowStart: number,
    req: Request,
    res: Response,
    next: NextFunction
  ) {
    const record = this.store.get(key);

    if (!record || record.resetTime < windowStart) {
      // New window
      const resetTime = now + opts.windowMs;
      this.store.set(key, { count: 1, resetTime });
      
      const info: RateLimitInfo = {
        limit: opts.max,
        remaining: opts.max - 1,
        resetTime,
        used: 1,
      };

      this.setRateLimitHeaders(res, info);
      (req as any).rateLimitInfo = info;
      next();
      return;
    }

    // Increment count
    record.count++;

    const info: RateLimitInfo = {
      limit: opts.max,
      remaining: Math.max(0, opts.max - record.count),
      resetTime: record.resetTime,
      used: record.count,
    };

    this.setRateLimitHeaders(res, info);

    if (record.count > opts.max) {
      await this.logRateLimitExceeded(key, info, req);
      return res.status(429).json({
        error: 'Too Many Requests',
        message: opts.message,
        retryAfter: Math.ceil((info.resetTime - now) / 1000),
        limit: info.limit,
        remaining: info.remaining,
        resetTime: new Date(info.resetTime).toISOString(),
      });
    }

    (req as any).rateLimitInfo = info;
    next();
  }

  /**
   * Set rate limit headers
   */
  private setRateLimitHeaders(res: Response, info: RateLimitInfo) {
    res.setHeader('X-RateLimit-Limit', info.limit.toString());
    res.setHeader('X-RateLimit-Remaining', info.remaining.toString());
    res.setHeader('X-RateLimit-Reset', info.resetTime.toString());
    res.setHeader('X-RateLimit-Used', info.used.toString());
  }

  /**
   * Log rate limit exceeded
   */
  private async logRateLimitExceeded(key: string, info: RateLimitInfo, req: Request) {
    logger.warn('Rate limit exceeded', {
      service: 'rate-limiter',
      key,
      limit: info.limit,
      used: info.used,
      path: req.path,
      method: req.method,
      ip: req.ip,
      userId: (req as any).userId,
    });
  }

  /**
   * Get current rate limit info for a key
   */
  async getRateLimitInfo(key: string): Promise<RateLimitInfo | null> {
    if (this.redis) {
      const redisKey = `rate_limit:${key}`;
      const count = await this.redis.zcard(redisKey);
      const ttl = await this.redis.ttl(redisKey);
      
      return {
        limit: this.defaultOptions.max,
        remaining: Math.max(0, this.defaultOptions.max - count),
        resetTime: Date.now() + (ttl * 1000),
        used: count,
      };
    } else {
      const record = this.store.get(key);
      if (!record) return null;
      
      return {
        limit: this.defaultOptions.max,
        remaining: Math.max(0, this.defaultOptions.max - record.count),
        resetTime: record.resetTime,
        used: record.count,
      };
    }
  }

  /**
   * Reset rate limit for a key
   */
  async resetRateLimit(key: string): Promise<void> {
    if (this.redis) {
      await this.redis.del(`rate_limit:${key}`);
    } else {
      this.store.delete(key);
    }
  }

  /**
   * Cleanup old entries (memory store only)
   */
  cleanup() {
    if (this.redis) return;

    const now = Date.now();
    for (const [key, record] of this.store.entries()) {
      if (record.resetTime < now) {
        this.store.delete(key);
      }
    }
  }
}

// Create rate limiter instances for different endpoints
export const generalRateLimiter = new RateLimiter({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per 15 minutes
});

export const scanRateLimiter = new RateLimiter({
  windowMs: 24 * 60 * 60 * 1000, // 24 hours
  max: 100, // 100 scans per day
  keyGenerator: (req) => {
    // Use user ID if authenticated, otherwise IP
    return (req as any).userId || req.ip || 'unknown';
  },
});

export const aiRateLimiter = new RateLimiter({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 50, // 50 AI requests per hour
  keyGenerator: (req) => {
    return (req as any).userId || req.ip || 'unknown';
  },
});

export const websocketRateLimiter = new RateLimiter({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // 10 WebSocket connections per minute
  keyGenerator: (req) => {
    return (req as any).userId || req.ip || 'unknown';
  },
});

// Default middleware exports
export const rateLimit = generalRateLimiter.create.bind(generalRateLimiter);
export const limitScans = scanRateLimiter.create.bind(scanRateLimiter);
export const limitAI = aiRateLimiter.create.bind(aiRateLimiter);
export const limitWebsocket = websocketRateLimiter.create.bind(websocketRateLimiter);
