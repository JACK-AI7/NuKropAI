import { Pool } from 'pg';
import pino from 'pino';

const logger = pino({
  transport: {
    target: 'pino-pretty'
  }
});

const pool = new Pool({
  connectionString: process.env.DATABASE_URL
});

interface FarmerProfile {
  state: string;
  crop: string;
  land_size_hectares: number;
  social_category?: string;
}

export class SubsidyEngine {
  /**
   * Evaluates eligibility for subsidies based on farmer profile
   */
  async evaluateEligibility(profile: FarmerProfile): Promise<any[]> {
    logger.info({ profile }, 'Evaluating subsidy eligibility');

    const client = await pool.connect();
    try {
      // Query structured database instead of relying on prompt-only LLM logic
      const query = `
        SELECT s.id, s.name, s.description, s.agency, s.amount, s.amount_type
        FROM subsidies s
        JOIN subsidy_eligibility_rules r ON s.id = r.subsidy_id
        WHERE (r.state IS NULL OR r.state = $1)
          AND (r.crop IS NULL OR r.crop = $2)
          AND (r.min_land_size_hectares IS NULL OR r.min_land_size_hectares <= $3)
          AND (r.max_land_size_hectares IS NULL OR r.max_land_size_hectares >= $3)
          AND (r.social_category IS NULL OR r.social_category = $4)
      `;
      
      const values = [
        profile.state,
        profile.crop,
        profile.land_size_hectares,
        profile.social_category || 'general'
      ];

      const result = await client.query(query, values);
      logger.info(`Found ${result.rows.length} eligible subsidies`);
      
      return result.rows;
    } catch (error) {
      logger.error({ error }, 'Failed to evaluate subsidies');
      throw error;
    } finally {
      client.release();
    }
  }
}

export const subsidyEngine = new SubsidyEngine();
