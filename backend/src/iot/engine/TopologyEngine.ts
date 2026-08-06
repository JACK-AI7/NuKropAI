import { pool } from '../../config/db';

/**
 * Farm Topology Graph Intelligence
 * Understands the physical layout of the farm (Pumps -> Valves -> Zones).
 * Used by the Orchestrator to validate commands before they hit hardware.
 */
export class TopologyEngine {
    
    /**
     * Graph traversal: Validates if starting a specific pump is safe based on 
     * its downstream physical connections.
     */
    async validatePumpStart(pumpDeviceId: string): Promise<boolean> {
        const client = await pool.connect();
        try {
            // Find all valves connected to this pump
            const res = await client.query(`
                SELECT target_device_id 
                FROM irrigation_topology 
                WHERE source_device_id = $1
            `, [pumpDeviceId]);

            // If a pump is directly connected to a zone without valves, it's safe to start.
            if (res.rows.length === 0) return true;

            // Otherwise, we must verify that AT LEAST ONE downstream valve is currently OPEN.
            // If we start a pump against all closed valves, the pipe will burst.
            for (const row of res.rows) {
                const valveId = row.target_device_id;
                const valveState = await this.getLatestDeviceState(valveId);
                if (valveState === 'OPEN') {
                    return true; // Graph traversal found an open path for water.
                }
            }

            console.error(`[TopologyEngine] 🚨 WATER DEADHEAD PREVENTED: Attempted to start Pump ${pumpDeviceId} but all downstream valves are closed!`);
            return false;

        } finally {
            client.release();
        }
    }

    private async getLatestDeviceState(deviceId: string): Promise<string> {
        // In production, this reads from the live Gateway memory or Redis state cache
        return 'CLOSED'; 
    }
}
