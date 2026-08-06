import { IotDeviceState } from '../providers/BaseDeviceProvider';
import { IoTGateway } from '../Gateway';

/**
 * Enterprise Hardware Protection SRE Module
 * Specifically designed for volatile rural grids (India/Africa)
 */
export class PowerIntelligenceEngine {
    private gateway: IoTGateway;
    
    // Configurable thresholds per device, mocked defaults here
    private readonly MIN_SAFE_VOLTAGE = 180;
    private readonly MAX_SAFE_VOLTAGE = 250;
    private readonly MIN_LOAD_AMPS = 0.5; // Dry Run Threshold

    constructor(gateway: IoTGateway) {
        this.gateway = gateway;
    }

    /**
     * Ingests real-time telemetry and calculates hardware risk.
     * Executes instant kill-switch commands if thresholds are breached.
     */
    evaluateTelemetry(internalDeviceId: string, state: IotDeviceState) {
        if (!state.isRunning) return; // Only protect actively running hardware

        let protectionTriggered = false;
        let faultReason = '';

        // 1. Grid Voltage Protection (Phase Failure / Voltage Drop)
        if (state.voltage !== undefined) {
            if (state.voltage < this.MIN_SAFE_VOLTAGE) {
                protectionTriggered = true;
                faultReason = `UNDER_VOLTAGE (${state.voltage}V < ${this.MIN_SAFE_VOLTAGE}V)`;
            } else if (state.voltage > this.MAX_SAFE_VOLTAGE) {
                protectionTriggered = true;
                faultReason = `OVER_VOLTAGE (${state.voltage}V > ${this.MAX_SAFE_VOLTAGE}V)`;
            }
        }

        // 2. Dry Run / Coil Overload Protection
        if (state.amperage !== undefined) {
            if (state.amperage < this.MIN_LOAD_AMPS) {
                protectionTriggered = true;
                faultReason = `DRY_RUN (${state.amperage}A < ${this.MIN_LOAD_AMPS}A)`;
            }
            // For overload, we would ideally compare to a historical baseline
            // e.g., if (state.amperage > baseline * 1.5) ...
        }

        if (protectionTriggered) {
            console.error(`[Power Intelligence] 🚨 CRITICAL FAULT on ${internalDeviceId}: ${faultReason}. INITIATING AUTO-SHUTOFF!`);
            
            // Immediately dispatch hardware shutdown to save the coil
            this.gateway.executeCommand(internalDeviceId, 'MOTOR_OFF', {
                source: 'power_intelligence_kill_switch',
                reason: faultReason
            }).catch(console.error);

            // Log to Event Sourcing table
            this.logProtectionEvent(internalDeviceId, faultReason, state);
            
            // Mark state as faulted locally so UI reflects it immediately
            state.status = 'fault';
        }
    }

    private logProtectionEvent(deviceId: string, reason: string, telemetrySnapshot: any) {
        // SQL: INSERT INTO device_events (device_id, event_type, payload) VALUES (...)
        // 'PROTECTION_TRIGGERED', { reason, telemetry: telemetrySnapshot }
    }
}
