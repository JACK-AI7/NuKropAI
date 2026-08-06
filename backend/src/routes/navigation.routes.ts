import { FastifyInstance } from 'fastify';
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

export default async function navigationRoutes(fastify: FastifyInstance) {
    // Sync Field Navigation Path
    fastify.post('/path/sync', async (request, reply) => {
        const { farm_zone_id, path_data, distance_meters, estimated_time_mins } = request.body as any;

        if (!farm_zone_id || !path_data) {
            return reply.status(400).send({ error: 'Missing required payload: farm_zone_id, path_data' });
        }

        const client = await pool.connect();
        try {
            const result = await client.query(`
                INSERT INTO field_navigation_paths (farm_zone_id, path_data, distance_meters, estimated_time_mins)
                VALUES ($1, $2, $3, $4)
                RETURNING id
            `, [farm_zone_id, JSON.stringify(path_data), distance_meters, estimated_time_mins]);

            return reply.send({ success: true, path_id: result.rows[0].id });
        } catch (error: any) {
            request.log.error(error);
            return reply.status(500).send({ error: 'Failed to sync navigation path' });
        } finally {
            client.release();
        }
    });

    // Sync Spray Coverage
    fastify.post('/coverage/sync', async (request, reply) => {
        const { path_id, coverage_polygon, chemical_used, amount_liters } = request.body as any;

        const client = await pool.connect();
        try {
            const result = await client.query(`
                INSERT INTO spray_coverage_logs (path_id, coverage_polygon, chemical_used, amount_liters)
                VALUES ($1, $2, $3, $4)
                RETURNING id
            `, [path_id, JSON.stringify(coverage_polygon), chemical_used, amount_liters]);

            return reply.send({ success: true, coverage_id: result.rows[0].id });
        } catch (error: any) {
            request.log.error(error);
            return reply.status(500).send({ error: 'Failed to sync spray coverage' });
        } finally {
            client.release();
        }
    });
}
