import { FastifyRequest, FastifyReply } from 'fastify';
import { redisClient } from '../config/redis';
import crypto from 'crypto';

/**
 * Validates GPS Coordinates
 */
export const validateGPS = (lat?: number, lon?: number): boolean => {
    if (lat === undefined || lon === undefined) return false;
    if (lat < -90 || lat > 90) return false;
    if (lon < -180 || lon > 180) return false;
    return true;
};

/**
 * Validates Telemetry ranges for basic sanitization
 */
export const validateTelemetryRanges = (payload: any): boolean => {
    if (payload.moisture !== undefined && (payload.moisture < 0 || payload.moisture > 100)) return false;
    if (payload.ph !== undefined && (payload.ph < 0 || payload.ph > 14)) return false;
    return true;
};

/**
 * Fastify PreHandler Hook for Deduplication and Anomaly Filtering
 * Uses Redis to drop identical telemetry payloads sent within 5 seconds.
 */
export const telemetrySanitizationHook = async (request: FastifyRequest, reply: FastifyReply) => {
    const payload = request.body as any;

    if (!payload) return;

    // 1. Basic Range Sanitization
    if (!validateTelemetryRanges(payload)) {
        request.log.warn({ payload }, 'Telemetry rejected: Out of bounds');
        return reply.status(400).send({ error: 'Telemetry data out of bounds' });
    }

    if (payload.latitude !== undefined && payload.longitude !== undefined) {
        if (!validateGPS(payload.latitude, payload.longitude)) {
            request.log.warn({ payload }, 'GPS rejected: Invalid coordinates');
            return reply.status(400).send({ error: 'Invalid GPS coordinates' });
        }
    }

    // 2. Duplicate Suppression (Redis)
    // Create a hash of the payload and device ID
    const deviceId = payload.device_id || 'unknown';
    const hashData = JSON.stringify(payload);
    const hash = crypto.createHash('sha256').update(hashData).digest('hex');
    
    const cacheKey = `telemetry:dedup:${deviceId}:${hash}`;

    try {
        const exists = await redisClient.get(cacheKey);
        if (exists) {
            request.log.info({ deviceId }, 'Duplicate telemetry suppressed');
            return reply.status(202).send({ status: 'Suppressed duplicate' }); // Accepted but not processed again
        }

        // Lock for 5 seconds
        await redisClient.set(cacheKey, '1', 'EX', 5);
    } catch (err) {
        request.log.error(err, 'Redis deduplication check failed');
        // Continue processing if Redis fails to ensure high availability
    }
};
