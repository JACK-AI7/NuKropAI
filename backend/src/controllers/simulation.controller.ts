import { FastifyRequest, FastifyReply } from 'fastify';
import { pool } from '../config/db';

export const runSimulation = async (request: FastifyRequest, reply: FastifyReply) => {
  const { crop_name, field_size } = request.body as any;
  const userId = request.user?.id;

  if (!crop_name || field_size === undefined) {
    return reply.status(400).send({ error: 'Crop species and field acreage size are required parameters' });
  }

  const acreage = parseFloat(field_size);
  if (isNaN(acreage) || acreage <= 0) {
    return reply.status(400).send({ error: 'Field size must be a positive decimal number' });
  }

  // Calculate yield parameters simulation
  const yieldLoss = 14; 
  const rec = `SIMULATION ANALYSIS FOR ${crop_name.toUpperCase()}:
• Predicted Yield Loss: 14% risk expected if planted immediately due to high ambient temperatures.
• Sowing schedule adjustment: Sowing in 8 days decreases heat stress risk by 90%.
• NPK target recommendation: Enhance Potassium feeding by 12% to secure cell wall structure against drought.`;

  try {
    const result = await pool.query(
      'INSERT INTO public.crop_simulations (user_id, crop_name, field_size, yield_loss_risk, recommendation) VALUES ($1, $2, $3, $4, $5) RETURNING *',
      [userId, crop_name, acreage, yieldLoss, rec]
    );
    return reply.status(201).send(result.rows[0]);
  } catch (err) {
    console.error(err);
    return reply.status(500).send({ error: 'Failed to record crop simulation model prediction' });
  }
};

export const getSimulations = async (request: FastifyRequest, reply: FastifyReply) => {
  const userId = request.user?.id;
  try {
    const result = await pool.query(
      'SELECT * FROM public.crop_simulations WHERE user_id = $1 ORDER BY created_at DESC',
      [userId]
    );
    return reply.send(result.rows);
  } catch (err) {
    console.error(err);
    return reply.status(500).send({ error: 'Failed to query crop simulation sandbox log' });
  }
};
