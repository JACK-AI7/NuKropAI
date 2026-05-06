"use strict";
/**
 * Request/Response Logging Middleware
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.performanceMonitor = exports.errorLogger = exports.requestLogger = void 0;
const logger_1 = require("../utils/logger");
const uuid_1 = require("uuid");
const requestLogger = (req, res, next) => {
    const requestId = (0, uuid_1.v4)();
    const traceId = (0, uuid_1.v4)();
    const startTime = Date.now();
    // Create request context
    const requestContext = {
        requestId,
        traceId,
        userId: req.userId,
        ip: req.ip,
        userAgent: req.get('User-Agent'),
        method: req.method,
        url: req.originalUrl,
        startTime,
    };
    // Attach request logger to request object
    req.requestLogger = (0, logger_1.createRequestLogger)(requestContext);
    // Log request
    logger_1.logger.info('Incoming request', {
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
        (0, logger_1.logRequest)(req.method, req.originalUrl, res.statusCode, Date.now() - startTime, req.userId, {
            requestId,
            traceId,
            contentLength: body?.length || 0,
        });
        return originalSend.call(this, body);
    };
    res.json = function (body) {
        (0, logger_1.logRequest)(req.method, req.originalUrl, res.statusCode, Date.now() - startTime, req.userId, {
            requestId,
            traceId,
            responseSize: JSON.stringify(body).length,
        });
        return originalJson.call(this, body);
    };
    // Error handling
    res.on('finish', () => {
        if (res.statusCode >= 400) {
            logger_1.logger.warn('Request completed with error status', {
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
exports.requestLogger = requestLogger;
/**
 * Error logging middleware
 */
const errorLogger = (error, req, res, next) => {
    const requestId = req.requestId || 'unknown';
    const traceId = req.traceId || 'unknown';
    (0, logger_1.logError)(error, {
        requestId,
        traceId,
        method: req.method,
        url: req.originalUrl,
        userId: req.userId,
        statusCode: res.statusCode,
    });
    next(error);
};
exports.errorLogger = errorLogger;
/**
 * Performance monitoring middleware
 */
const performanceMonitor = (req, res, next) => {
    const startTime = Date.now();
    const startMemory = process.memoryUsage().heapUsed;
    res.on('finish', () => {
        const duration = Date.now() - startTime;
        const memoryUsed = process.memoryUsage().heapUsed - startMemory;
        // Log slow requests
        if (duration > 1000) {
            logger_1.logger.warn('Slow request detected', {
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
            logger_1.logger.warn('High memory usage detected', {
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
exports.performanceMonitor = performanceMonitor;
