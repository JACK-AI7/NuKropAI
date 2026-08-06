import { BaseDeviceProvider, IotDeviceState } from './BaseDeviceProvider';

/**
 * Shelly API Provider Implementation
 * Interacts with Shelly Relays via REST API / CoAP
 */
export class ShellyProvider extends BaseDeviceProvider {
    readonly providerName = 'shelly';
    private telemetryCallback?: (deviceId: string, state: IotDeviceState) => void;

    async connect(): Promise<void> {
        console.log(`[${this.providerName}] Initializing Shelly API Integration...`);
    }

    async bindDevice(credentials: any): Promise<string> {
        // credentials.ipAddress or credentials.shellyCloudId
        console.log(`[${this.providerName}] Binding Shelly Relay IP: ${credentials.ipAddress}`);
        return credentials.ipAddress;
    }

    async sendCommand(deviceId: string, command: string, payload?: any): Promise<boolean> {
        const turnOn = command === 'MOTOR_ON' ? 'on' : 'off';
        console.log(`[${this.providerName}] HTTP GET http://${deviceId}/relay/0?turn=${turnOn}`);
        // await fetch(`http://${deviceId}/relay/0?turn=${turnOn}`);
        return true;
    }

    async getStatus(deviceId: string): Promise<IotDeviceState> {
        console.log(`[${this.providerName}] HTTP GET http://${deviceId}/status`);
        // const response = await fetch(`http://${deviceId}/status`).then(r => r.json());
        return {
            status: 'online',
            isRunning: false,
            lastHeartbeat: new Date(),
            rawPayload: {}
        };
    }

    onTelemetry(callback: (deviceId: string, state: IotDeviceState) => void): void {
        this.telemetryCallback = callback;
        // Shelly devices can be configured to call HTTP webhooks upon state change
    }
}
