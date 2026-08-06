export interface IotDeviceState {
    status: 'online' | 'offline' | 'fault';
    voltage?: number;
    amperage?: number;
    moisture?: number;
    isRunning: boolean;
    lastHeartbeat: Date;
    rawPayload: any;
}

export abstract class BaseDeviceProvider {
    /**
     * Unique identifier for the provider (e.g., 'tuya', 'mqtt', 'shelly', 'gsm')
     */
    abstract readonly providerName: string;

    /**
     * Initializes the connection to the provider's cloud/broker
     */
    abstract connect(): Promise<void>;

    /**
     * Binds a new device to the platform
     */
    abstract bindDevice(credentials: any): Promise<string>;

    /**
     * Sends a command to the device.
     * Note: This only queues the command at the provider level. 
     * Actual verification depends on async telemetry.
     * 
     * @param deviceId The provider's internal device ID
     * @param command e.g., 'MOTOR_ON' or 'MOTOR_OFF'
     */
    abstract sendCommand(deviceId: string, command: string, payload?: any): Promise<boolean>;

    /**
     * Fetches the immediate known status from the provider's cloud
     */
    abstract getStatus(deviceId: string): Promise<IotDeviceState>;
    
    /**
     * Registers a callback for incoming asynchronous telemetry from this provider
     */
    abstract onTelemetry(callback: (deviceId: string, state: IotDeviceState) => void): void;
}
