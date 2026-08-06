import { FastifyRequest, FastifyReply } from 'fastify';
import { pool } from '../config/db';

export const getContracts = async (request: FastifyRequest, reply: FastifyReply) => {
  try {
    const result = await pool.query(
      'SELECT * FROM public.escrow_contracts ORDER BY created_at DESC'
    );
    return reply.send(result.rows);
  } catch (err) {
    console.error(err);
    return reply.status(500).send({ error: 'Failed to query purchase contract ledger' });
  }
};

export const createContract = async (request: FastifyRequest, reply: FastifyReply) => {
  const { buyer_name, commodity, amount } = request.body as any;

  if (!buyer_name || !commodity || !amount) {
    return reply.status(400).send({ error: 'Corporate buyer name, commodity, and contract value are required' });
  }

  const numAmount = parseFloat(amount);
  if (isNaN(numAmount) || numAmount <= 0) {
    return reply.status(400).send({ error: 'Contract amount must be a positive number' });
  }

  const mockAddr = '0x' + Array.from({length: 40}, () => Math.floor(Math.random()*16).toString(16)).join('');
  const qrVerification = 'QR-' + Math.floor(100000 + Math.random() * 900000);

  try {
    const result = await pool.query(
      'INSERT INTO public.escrow_contracts (contract_address, buyer_name, commodity, amount, funds_status, qr_verification_code) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *',
      [mockAddr, buyer_name, commodity, numAmount, 'LOCKED', qrVerification]
    );
    return reply.status(201).send(result.rows[0]);
  } catch (err) {
    console.error(err);
    return reply.status(500).send({ error: 'Failed to initialize escrow ledger records' });
  }
};

export const verifyQr = async (request: FastifyRequest, reply: FastifyReply) => {
  const { contract_id, qr_code } = request.body as any;

  if (!contract_id || !qr_code) {
    return reply.status(400).send({ error: 'Contract ID and verification QR code are required' });
  }

  try {
    const check = await pool.query('SELECT * FROM public.escrow_contracts WHERE id = $1', [contract_id]);
    if (check.rows.length === 0) {
      return reply.status(404).send({ error: 'Target purchase contract not found' });
    }

    const contract = check.rows[0];
    if (contract.funds_status !== 'LOCKED') {
      return reply.status(400).send({ error: 'Funds associated with this contract are already released or returned' });
    }

    if (contract.qr_verification_code !== qr_code) {
      return reply.status(400).send({ error: 'Invalid verification QR code matching this contract signature' });
    }

    const result = await pool.query(
      "UPDATE public.escrow_contracts SET funds_status = 'RELEASED', verified_at = CURRENT_TIMESTAMP WHERE id = $1 RETURNING *",
      [contract_id]
    );
    return reply.send(result.rows[0]);
  } catch (err) {
    console.error(err);
    return reply.status(500).send({ error: 'Failed to release escrow ledger funds' });
  }
};
