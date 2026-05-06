"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.logError = exports.logRequest = exports.logGpuMetrics = exports.logInference = exports.createRequestLogger = exports.logger = void 0;
const winston_1 = __importDefault(require("winston"));
const winston_daily_rotate_file_1 = __importDefault(require("winston-daily-rotate-file"));
// Custom log levels
const logLevels = {
    error: 0,
    warn: 1,
    info: 2,
    http: 3,
    verbose: 4,
    debug: 5,
    silly: 6,
};
// Custom colors for log levels
const logColors = {
    error: 'red',
    warn: 'yellow',
    info: 'green',
    http: 'magenta',
    verbose: 'cyan',
    debug: 'blue',
    silly: 'gray',
};
// JSON formatter for structured logging
const jsonFormat = winston_1.default.format.combine(winston_1.default.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }), winston_1.default.format.errors({ stack: true }), winston_1.default.format.json());
// Human readable formatter for console
const consoleFormat = winston_1.default.format.combine(winston_1.default.format.colorize(), winston_1.default.format.timestamp({ format: 'HH:mm:ss' }), winston_1.default.format.printf(({ timestamp, level, message, service, operation, ...metadata }) => {
    let msg = `${timestamp} [${level}]`;
    if (service)
        msg += ` [${service}]`;
    if (operation)
        msg += ` [${operation}]`;
    msg += `: ${message}`;
    if (Object.keys(metadata).length > 0) {
        msg += ` ${JSON.stringify(metadata)}`;
    }
    return msg;
}));
// Create logger instance
exports.logger = winston_1.default.createLogger({
    level: process.env.LOG_LEVEL || 'info',
    levels: logLevels,
    transports: [
        // Console transport (human readable)
        new winston_1.default.transports.Console({
            format: consoleFormat,
            level: process.env.NODE_ENV === 'development' ? 'debug' : 'info',
        }),
        // Daily rotating file transport (JSON)
        new winston_daily_rotate_file_1.default({
            filename: 'logs/application-%DATE%.log',
            datePattern: 'YYYY-MM-DD',
            zippedArchive: true,
            maxSize: '20m',
            maxFiles: '14d',
            format: jsonFormat,
            level: 'info',
        }),
        // Error log file
        new winston_daily_rotate_file_1.default({
            filename: 'logs/error-%DATE%.log',
            datePattern: 'YYYY-MM-DD',
            zippedArchive: true,
            maxSize: '20m',
            maxFiles: '14d',
            format: jsonFormat,
            level: 'error',
        }),
        // HTTP request log file
        new winston_daily_rotate_file_1.default({
            filename: 'logs/http-%DATE%.log',
            datePattern: 'YYYY-MM-DD',
            zippedArchive: true,
            maxSize: '20m',
            maxFiles: '14d',
            format: jsonFormat,
            level: 'http',
        }),
    ],
    exceptionHandlers: [
        new winston_daily_rotate_file_1.default({
            filename: 'logs/exceptions-%DATE%.log',
            datePattern: 'YYYY-MM-DD',
            zippedArchive: true,
            maxSize: '20m',
            maxFiles: '14d',
            format: jsonFormat,
        }),
    ],
    rejectionHandlers: [
        new winston_daily_rotate_file_1.default({
            filename: 'logs/rejections-%DATE%.log',
            datePattern: 'YYYY-MM-DD',
            zippedArchive: true,
            maxSize: '20m',
            maxFiles: '14d',
            format: jsonFormat,
        }),
    ],
});
// Add color support
winston_1.default.addColors(logColors);
// Create child logger with request context
const createRequestLogger = (context) => {
    return exports.logger.child({ ...context });
};
exports.createRequestLogger = createRequestLogger;
// Log inference metrics
const logInference = (model, operation, durationMs, confidence, gpuUtilization, metadata) => {
    exports.logger.info('Inference completed', {
        service: 'ai-inference',
        operation,
        model,
        duration_ms: durationMs,
        confidence,
        gpu_utilization: gpuUtilization,
        ...metadata,
    });
};
exports.logInference = logInference;
// Log GPU metrics
const logGpuMetrics = (utilization, memoryUsed, memoryTotal, temperature) => {
    exports.logger.info('GPU metrics', {
        service: 'gpu-monitor',
        gpu_utilization: utilization,
        gpu_memory_used_mb: memoryUsed,
        gpu_memory_total_mb: memoryTotal,
        gpu_temperature: temperature,
    });
};
exports.logGpuMetrics = logGpuMetrics;
// Log request
const logRequest = (method, url, statusCode, durationMs, userId, metadata) => {
    exports.logger.http('HTTP Request', {
        service: 'http-server',
        method,
        url,
        status_code: statusCode,
        duration_ms: durationMs,
        user_id: userId,
        ...metadata,
    });
};
exports.logRequest = logRequest;
// Log error with context
const logError = (error, context = {}, level = 'error') => {
    exports.logger[level]('Error occurred', {
        error: error.message,
        stack: error.stack,
        ...context,
    });
};
exports.logError = logError;
exports.default = exports.logger;
