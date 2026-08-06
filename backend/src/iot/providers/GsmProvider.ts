import { BaseDeviceProvider, IotDeviceState } from './BaseDeviceProvider';

/**
 * GSM SMS Provider Implementation
 * Uses Twilio or local SMS gateway to send AT commands to remote GSM starters
 */
export class GsmProvider extends BaseDeviceProvider {
    readonly providerName = 'gsm';
    private telemetryCallback?: (deviceId: string, state: IotDeviceState) => void;

    async connect(): Promise<void> {
        console.log(`[${this.providerName}] Connecting to Twilio SMS Gateway...`);
    }

    async bindDevice(credentials: any): Promise<string> {
        // credentials.phoneNumber
        console.log(`[${this.providerName}] Binding GSM Starter with Phone: ${credentials.phoneNumber}`);
        return credentials.phoneNumber;
    }

    async sendCommand(deviceId: string, command: string, payload?: any): Promise<boolean> {
        const smsText = command === 'MOTOR_ON' ? 'START' : 'STOP';
        console.log(`[${this.providerName}] Sending SMS '${smsText}' to ${deviceId}`);
        // await twilioClient.messages.create({ body: smsText, to: deviceId, from: '+123456789' });
        return true;
    }

    async getStatus(deviceId: string): Promise<IotDeviceState> {
        return {
            status: 'offline', // GSM doesn't have immediate status unless polled via SMS
            isRunning: false,
            lastHeartbeat: new Date(),
            rawPayload: {}
        };
    }

    onTelemetry(callback: (deviceId: string, state: IotDeviceState) => void): void {
        this.telemetryCallback = callback;
        // This is usually triggered by an incoming Webhook from Twilio when the GSM module replies "MOTOR IS ON"
    }

    handleIncomingSmsWebhook(fromNumber: string, messageBody: string) {
        if (!this.telemetryCallback) return;
        
        const isRunning = messageBody.includes('ON');
        this.telemetryCallback(fromNumber, {
            status: 'online',
            isRunning: isRunning,
            lastHeartbeat: new Date(),
            rawPayload: { sms: messageBody }
        });
    }
}
