import pino from 'pino';
import { Pool } from 'pg';
import { redisClient } from '../../config/redis';

const logger = pino({
  transport: {
    target: 'pino-pretty'
  }
});

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

export async function handleMandiIngestion(data: any) {
  logger.info('Starting Mandi Price Ingestion from Government APIs');
  
  try {
    // In a real-world scenario, you would fetch from data.gov.in
    // For this implementation, we will simulate fetching and then perform DB operations
    // and anomaly detection.
    
    // Example external API call (simulated)
    const fetchedData = [
      { state: 'Punjab', district: 'Ludhiana', market: 'Ludhiana', commodity: 'Wheat', variety: 'Other', arrival_date: new Date().toISOString(), min_price: 2125, max_price: 2200, modal_price: 2150 },
      { state: 'Maharashtra', district: 'Pune', market: 'Pune', commodity: 'Onion', variety: 'Red', arrival_date: new Date().toISOString(), min_price: 1500, max_price: 2500, modal_price: 2000 }
    ];

    const client = await pool.connect();
    try {
      await client.query('BEGIN');
      
      for (const item of fetchedData) {
        // Insert or update mandi_live_rates
        const res = await client.query(`
          INSERT INTO mandi_live_rates (state, district, market, commodity, variety, arrival_date, min_price, max_price, modal_price)
          VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
          RETURNING id
        `, [item.state, item.district, item.market, item.commodity, item.variety, item.arrival_date, item.min_price, item.max_price, item.modal_price]);

        // Simple Anomaly Detection
        // e.g. If modal_price > 3000 for Onion, flag it
        if (item.commodity === 'Onion' && item.modal_price > 1800) {
            await client.query(`
                INSERT INTO mandi_price_anomalies (market, commodity, expected_price, actual_price, anomaly_reason)
                VALUES ($1, $2, $3, $4, $5)
            `, [item.market, item.commodity, 1500, item.modal_price, 'Price surged above historical average thresholds']);
            logger.warn(`Anomaly detected for ${item.commodity} at ${item.market}`);
        }
      }

      await client.query('COMMIT');

      // Clear the Redis cache for mandi data so the API serves fresh data
      const keys = await redisClient.keys('cache:mandi:*');
      if (keys.length > 0) {
        await redisClient.del(keys);
      }
      
      logger.info('Mandi ingestion completed successfully and cache invalidated');
    } catch (e) {
      await client.query('ROLLBACK');
      throw e;
    } finally {
      client.release();
    }

  } catch (error) {
    logger.error({ error }, 'Failed to ingest Mandi data');
    throw error; // Let BullMQ handle retries
  }
}
