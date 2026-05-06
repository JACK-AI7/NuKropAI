import winston from 'winston';
import DailyRotateFile from 'winston-daily-rotate-file';
import { v4 as uuidv4 } from 'uuid';

// Custom log levels
const logLevels = {
  error: 0,
  warn: 1,
  info: 2,
  http: 3,
  verbose: 4,
  debug: 5,
  silly: 6,
} as const;

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
const jsonFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.errors({ stack: true }),
  winston.format.json()
);

// Human readable formatter for console
const consoleFormat = winston.format.combine(
  winston.format.colorize(),
  winston.format.timestamp({ format: 'HH:mm:ss' }),
  winston.format.printf(({ timestamp, level, message, service, operation, ...metadata }) => {
    let msg = `${timestamp} [${level}]`;
    if (service) msg += ` [${service}]`;
    if (operation) msg += ` [${operation}]`;
    msg += `: ${message}`;
    if (Object.keys(metadata).length > 0) {
      msg += ` ${JSON.stringify(metadata)}`;
    }
    return msg;
  })
);

// Create logger instance
export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  levels: logLevels,
  transports: [
    // Console transport (human readable)
    new winston.transports.Console({
      format: consoleFormat,
      level: process.env.NODE_ENV === 'development' ? 'debug' : 'info',
    }),
    // Daily rotating file transport (JSON)
    new DailyRotateFile({
      filename: 'logs/application-%DATE%.log',
      datePattern: 'YYYY-MM-DD',
      zippedArchive: true,
      maxSize: '20m',
      maxFiles: '14d',
      format: jsonFormat,
      level: 'info',
    }),
    // Error log file
    new DailyRotateFile({
      filename: 'logs/error-%DATE%.log',
      datePattern: 'YYYY-MM-DD',
      zippedArchive: true,
      maxSize: '20m',
      maxFiles: '14d',
      format: jsonFormat,
      level: 'error',
    }),
    // HTTP request log file
    new DailyRotateFile({
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
    new DailyRotateFile({
      filename: 'logs/exceptions-%DATE%.log',
      datePattern: 'YYYY-MM-DD',
      zippedArchive: true,
      maxSize: '20m',
      maxFiles: '14d',
      format: jsonFormat,
    }),
  ],
  rejectionHandlers: [
    new DailyRotateFile({
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
winston.addColors(logColors);

// Request context interface
export interface RequestContext {
  requestId: string;
  traceId: string;
  userId?: string;
  ip?: string;
  userAgent?: string;
  method?: string;
  url?: string;
  startTime?: number;
}

// Create child logger with request context
export const createRequestLogger = (context: RequestContext) => {
  return logger.child({ ...context });
};

// Log inference metrics
export const logInference = (
  model: string,
  operation: string,
  durationMs: number,
  confidence?: number,
  gpuUtilization?: number,
  metadata?: Record<string, unknown>
) => {
  logger.info('Inference completed', {
    service: 'ai-inference',
    operation,
    model,
    duration_ms: durationMs,
    confidence,
    gpu_utilization: gpuUtilization,
    ...metadata,
  });
};

// Log GPU metrics
export const logGpuMetrics = (
  utilization: number,
  memoryUsed: number,
  memoryTotal: number,
  temperature?: number
) => {
  logger.info('GPU metrics', {
    service: 'gpu-monitor',
    gpu_utilization: utilization,
    gpu_memory_used_mb: memoryUsed,
    gpu_memory_total_mb: memoryTotal,
    gpu_temperature: temperature,
  });
};

// Log request
export const logRequest = (
  method: string,
  url: string,
  statusCode: number,
  durationMs: number,
  userId?: string,
  metadata?: Record<string, unknown>
) => {
  logger.http('HTTP Request', {
    service: 'http-server',
    method,
    url,
    status_code: statusCode,
    duration_ms: durationMs,
    user_id: userId,
    ...metadata,
  });
};

// Log error with context
export const logError = (
  error: Error,
  context: Record<string, unknown> = {},
  level: 'error' | 'warn' = 'error'
) => {
  logger[level]('Error occurred', {
    error: error.message,
    stack: error.stack,
    ...context,
  });
};

export default logger;
