import { FastifyRequest, FastifyReply } from 'fastify';
import { pool } from '../config/db';

export const getValves = async (request: FastifyRequest, reply: FastifyReply) => {
  try {
    const result = await pool.query(
      'SELECT DISTINCT ON (valve_name) * FROM public.valve_operations ORDER BY valve_name, logged_at DESC'
    );
    return reply.send(result.rows);
  } catch (err) {
    console.error(err);
    return reply.status(500).send({ error: 'Failed to query valve registry' });
  }
};

export const toggleValve = async (request: FastifyRequest, reply: FastifyReply) => {
  const { valve_name, state, flow_rate, triggered_by } = request.body as any;

  if (!valve_name || !state) {
    return reply.status(400).send({ error: 'Valve name and operation state (OPEN/CLOSED) are required' });
  }

  if (!['OPEN', 'CLOSED'].includes(state)) {
    return reply.status(400).send({ error: 'Invalid valve state specified' });
  }

  try {
    const result = await pool.query(
      'INSERT INTO public.valve_operations (valve_name, state, flow_rate, triggered_by) VALUES ($1, $2, $3, $4) RETURNING *',
      [valve_name, state, flow_rate || 0.0, triggered_by || 'manual']
    );
    return reply.status(201).send(result.rows[0]);
  } catch (err) {
    console.error(err);
    return reply.status(500).send({ error: 'Failed to record valve configuration state changes' });
  }
};
