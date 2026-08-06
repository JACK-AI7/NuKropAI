import { FastifyRequest, FastifyReply } from 'fastify';
import { pool } from '../config/db';

export const reportOutbreak = async (request: FastifyRequest, reply: FastifyReply) => {
  const { pest_name, latitude, longitude, wind_direction, wind_speed } = request.body as any;
  const userId = request.user?.id;

  if (!pest_name || latitude === undefined || longitude === undefined) {
    return reply.status(400).send({ error: 'Pest name and decimal coordinates (latitude/longitude) are required' });
  }

  try {
    const result = await pool.query(
      'INSERT INTO public.pest_outbreaks (pest_name, latitude, longitude, reporter_id, wind_direction, wind_speed) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *',
      [pest_name, parseFloat(latitude), parseFloat(longitude), userId, wind_direction || 'East', parseFloat(wind_speed || 12.0)]
    );
    return reply.status(201).send(result.rows[0]);
  } catch (err) {
    console.error(err);
    return reply.status(500).send({ error: 'Failed to record crowd-sourced pest warning broadcast' });
  }
};

export const getAlerts = async (request: FastifyRequest, reply: FastifyReply) => {
  try {
    const result = await pool.query(
      'SELECT * FROM public.pest_outbreaks ORDER BY reported_at DESC LIMIT 50'
    );
    return reply.send(result.rows);
  } catch (err) {
    console.error(err);
    return reply.status(500).send({ error: 'Failed to fetch warning radar alerts' });
  }
};
