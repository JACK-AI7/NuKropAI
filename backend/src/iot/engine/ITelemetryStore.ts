import { IotDeviceState } from '../providers/BaseDeviceProvider';

/**
 * Time-Series Data Abstraction Layer.
 * Currently uses PostgreSQL (JSONB), but structurally designed for a 
 * zero-downtime migration to TimescaleDB Hypertable architecture 
 * when the farm scales past 100,000 active telemetry streams per minute.
 */
export interface ITelemetryStore {
    
    /**
     * Ingests a high-throughput telemetry packet.
     * In TimescaleDB, this will hit a hypertable partitioned by `timestamp`.
     */
    insertTelemetry(deviceId: string, state: IotDeviceState): Promise<void>;

    /**
     * Retrieves the time-bucketed average amperage over the last 30 days.
     * Used by PredictiveMaintenanceAI.ts
     */
    getHistoricalAmperage(deviceId: string, daysBack: number): Promise<number[]>;

    /**
     * Rolls up older telemetry into 1-hour chunks to save disk space.
     * (Native TimescaleDB Continuous Aggregate feature)
     */
    executeRetentionPolicy(): Promise<void>;
}
