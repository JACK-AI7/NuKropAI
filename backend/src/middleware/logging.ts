/**
 * Request/Response Logging Middleware
 */

import { Request, Response, NextFunction } from 'express';
import { logger, createRequestLogger, logRequest, logError } from '../utils/logger';
import { v4 as uuidv4 } from 'uuid';

export const requestLogger = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const requestId = uuidv4();
  const traceId = uuidv4();
  const startTime = Date.now();

  // Create request context
  const requestContext = {
    requestId,
    traceId,
    userId: (req as any).userId,
    ip: req.ip,
    userAgent: req.get('User-Agent'),
    method: req.method,
    url: req.originalUrl,
    startTime,
  };

  // Attach request logger to request object
  (req as any).requestLogger = createRequestLogger(requestContext);

  // Log request
  logger.info('Incoming request', {
    service: 'http-server',
    requestId,
    traceId,
    method: req.method,
    url: req.originalUrl,
    ip: req.ip,
    userAgent: req.get('User-Agent'),
    headers: {
      'content-type': req.get('Content-Type'),
      'content-length': req.get('Content-Length'),
    },
  });

  // Capture response
  const originalSend = res.send;
  const originalJson = res.json;

  res.send = function (body) {
    logRequest(req.method!, req.originalUrl, res.statusCode, Date.now() - startTime, (req as any).userId, {
      requestId,
      traceId,
      contentLength: body?.length || 0,
    });
    return originalSend.call(this, body);
  };

  res.json = function (body) {
    logRequest(req.method!, req.originalUrl, res.statusCode, Date.now() - startTime, (req as any).userId, {
      requestId,
      traceId,
      responseSize: JSON.stringify(body).length,
    });
    return originalJson.call(this, body);
  };

  // Error handling
  res.on('finish', () => {
    if (res.statusCode >= 400) {
      logger.warn('Request completed with error status', {
        service: 'http-server',
        requestId,
        traceId,
        method: req.method,
        url: req.originalUrl,
        statusCode: res.statusCode,
        duration_ms: Date.now() - startTime,
      });
    }
  });

  next();
};

/**
 * Error logging middleware
 */
export const errorLogger = (
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const requestId = (req as any).requestId || 'unknown';
  const traceId = (req as any).traceId || 'unknown';

  logError(error, {
    requestId,
    traceId,
    method: req.method,
    url: req.originalUrl,
    userId: (req as any).userId,
    statusCode: res.statusCode,
  });

  next(error);
};

/**
 * Performance monitoring middleware
 */
export const performanceMonitor = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const startTime = Date.now();
  const startMemory = process.memoryUsage().heapUsed;

  res.on('finish', () => {
    const duration = Date.now() - startTime;
    const memoryUsed = process.memoryUsage().heapUsed - startMemory;

    // Log slow requests
    if (duration > 1000) {
      logger.warn('Slow request detected', {
        service: 'performance-monitor',
        method: req.method,
        url: req.originalUrl,
        duration_ms: duration,
        memory_used_mb: Math.round(memoryUsed / 1024 / 1024),
        statusCode: res.statusCode,
      });
    }

    // Log memory usage for large responses
    if (memoryUsed > 10 * 1024 * 1024) { // 10MB
      logger.warn('High memory usage detected', {
        service: 'performance-monitor',
        method: req.method,
        url: req.originalUrl,
        memory_used_mb: Math.round(memoryUsed / 1024 / 1024),
        statusCode: res.statusCode,
      });
    }
  });

  next();
};
