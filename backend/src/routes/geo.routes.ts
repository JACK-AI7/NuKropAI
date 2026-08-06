import { FastifyInstance } from 'fastify';
import { pool } from '../config/db';

export default async function geoRoutes(fastify: FastifyInstance) {
    
    // 1. Create a Farm (Polygon)
    fastify.post('/farms', async (request, reply) => {
        const { userId, name, geojsonBoundary } = request.body as any;
        const client = await pool.connect();
        
        try {
            // ST_GeomFromGeoJSON converts standard GeoJSON into PostGIS geometry
            // ST_Area(boundary::geography) computes square meters, we convert to Acres (* 0.000247105)
            const result = await client.query(`
                INSERT INTO farms (user_id, name, boundary, total_acreage)
                VALUES (
                    $1, 
                    $2, 
                    ST_SetSRID(ST_GeomFromGeoJSON($3), 4326),
                    ST_Area(ST_SetSRID(ST_GeomFromGeoJSON($3), 4326)::geography) * 0.000247105
                ) RETURNING id, name, total_acreage
            `, [userId, name, JSON.stringify(geojsonBoundary)]);
            
            return { status: 'success', farm: result.rows[0] };
        } catch (error) {
            fastify.log.error(error);
            return reply.status(500).send({ error: 'Geospatial processing failed' });
        } finally {
            client.release();
        }
    });

    // 2. Get Farms (Returns as GeoJSON FeatureCollection for Mapbox)
    fastify.get('/farms', async (request, reply) => {
        const userId = (request.query as any).userId;
        const client = await pool.connect();
        
        try {
            const result = await client.query(`
                SELECT jsonb_build_object(
                    'type',     'FeatureCollection',
                    'features', jsonb_agg(features.feature)
                ) as geojson
                FROM (
                  SELECT jsonb_build_object(
                    'type',       'Feature',
                    'id',         id,
                    'geometry',   ST_AsGeoJSON(boundary)::jsonb,
                    'properties', to_jsonb(inputs) - 'boundary'
                  ) AS feature
                  FROM (SELECT * FROM farms WHERE user_id = $1) inputs
                ) features;
            `, [userId]);
            
            return result.rows[0].geojson || { type: 'FeatureCollection', features: [] };
        } finally {
            client.release();
        }
    });

    // 3. Create a Zone within a Farm
    fastify.post('/zones', async (request, reply) => {
        const { farmId, name, cropType, plantingDate, geojsonBoundary } = request.body as any;
        const client = await pool.connect();
        
        try {
            // First check if the zone is completely inside the farm boundary (ST_Within)
            const validation = await client.query(`
                SELECT ST_Within(
                    ST_SetSRID(ST_GeomFromGeoJSON($1), 4326),
                    (SELECT boundary FROM farms WHERE id = $2)
                ) as is_valid
            `, [JSON.stringify(geojsonBoundary), farmId]);

            if (!validation.rows[0]?.is_valid) {
                return reply.status(400).send({ error: 'Zone boundary falls outside the Farm boundary' });
            }

            const result = await client.query(`
                INSERT INTO zones (farm_id, name, crop_type, planting_date, boundary, area_acreage)
                VALUES (
                    $1, $2, $3, $4, 
                    ST_SetSRID(ST_GeomFromGeoJSON($5), 4326),
                    ST_Area(ST_SetSRID(ST_GeomFromGeoJSON($5), 4326)::geography) * 0.000247105
                ) RETURNING id, name, crop_type, area_acreage
            `, [farmId, name, cropType, plantingDate, JSON.stringify(geojsonBoundary)]);
            
            return { status: 'success', zone: result.rows[0] };
        } catch (error) {
            fastify.log.error(error);
            return reply.status(500).send({ error: 'Zone creation failed' });
        } finally {
            client.release();
        }
    });
}
