import { FastifyRequest, FastifyReply } from 'fastify';
import { Pool } from 'pg';
import crypto from 'crypto';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

export const getLatestRelease = async (request: FastifyRequest, reply: FastifyReply) => {
  const client = await pool.connect();
  try {
    const result = await client.query(`
      SELECT version_code, version_name, download_url, sha256_hash, release_notes, is_mandatory
      FROM ota_releases
      WHERE signature_status = 'verified'
      ORDER BY version_code DESC
      LIMIT 1
    `);

    if (result.rows.length === 0) {
      return reply.status(404).send({ error: 'No verified releases found' });
    }

    return reply.send({ success: true, release: result.rows[0] });
  } catch (error: any) {
    request.log.error(error);
    return reply.status(500).send({ error: 'Failed to fetch OTA release' });
  } finally {
    client.release();
  }
};

export const verifyRelease = async (request: FastifyRequest, reply: FastifyReply) => {
  const { version_code, client_sha256 } = request.body as { version_code: number, client_sha256: string };

  const client = await pool.connect();
  try {
    const result = await client.query(`
      SELECT sha256_hash FROM ota_releases WHERE version_code = $1
    `, [version_code]);

    if (result.rows.length === 0) {
      return reply.status(404).send({ error: 'Release not found' });
    }

    const serverHash = result.rows[0].sha256_hash;
    
    // Constant time comparison to prevent timing attacks
    const isValid = crypto.timingSafeEqual(
      Buffer.from(client_sha256, 'hex'),
      Buffer.from(serverHash, 'hex')
    );

    if (isValid) {
      return reply.send({ success: true, message: 'Integrity verified' });
    } else {
      request.log.warn(`OTA Integrity check failed for version ${version_code}`);
      return reply.status(400).send({ error: 'Integrity check failed. APK might be corrupted or tampered.' });
    }
  } catch (error: any) {
    request.log.error(error);
    return reply.status(500).send({ error: 'Failed to verify OTA release' });
  } finally {
    client.release();
  }
};
