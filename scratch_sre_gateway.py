import re

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\backend\src\iot\Gateway.ts", "r", encoding="utf-8") as f:
    content = f.read()

# Import PowerIntelligence
content = content.replace("import { TuyaProvider } from './providers/TuyaProvider';", 
    "import { TuyaProvider } from './providers/TuyaProvider';\nimport { PowerIntelligenceEngine } from './engine/PowerIntelligenceEngine';")

# Add class properties
props = """    private powerEngine: PowerIntelligenceEngine;
    // Idempotency cache for deduplication
    private commandCache: Set<string> = new Set();
    // Retry tracking Map<internalDeviceId, timeoutHandle>
    private retryQueue: Map<string, any> = new Map();"""

content = content.replace('private deviceRegistry: Map<string, { provider: string, providerDeviceId: string }> = new Map();', 
    'private deviceRegistry: Map<string, { provider: string, providerDeviceId: string }> = new Map();\n' + props)

# Initialize PowerEngine
content = content.replace('this.registerProvider(new TuyaProvider());', 
    'this.registerProvider(new TuyaProvider());\n        this.powerEngine = new PowerIntelligenceEngine(this);')

# Rewrite executeCommand with Idempotency and Retry logic
old_exec = """    async executeCommand(internalDeviceId: string, command: string, payload?: any): Promise<void> {
        const mapping = this.deviceRegistry.get(internalDeviceId);
        if (!mapping) throw new Error('Device not registered in gateway memory');

        const provider = this.providers.get(mapping.provider);
        if (!provider) throw new Error('Provider not loaded');

        // 1. Update DB: Status = 'verification'
        console.log(`[IoTGateway] Updating DB to verification state for ${internalDeviceId}`);

        // 2. Dispatch command
        const success = await provider.sendCommand(mapping.providerDeviceId, command, payload);
        if (!success) {
            console.error(`[IoTGateway] Provider failed to dispatch command to ${internalDeviceId}`);
            // DB Status = 'failed'
            return;
        }

        console.log(`[IoTGateway] Command dispatched. Awaiting async telemetry verification for ${internalDeviceId}...`);
        
        // At this point, the HTTP request from the mobile app should return HTTP 202 Accepted.
        // The mobile UI goes into a 'Pending/Starting' spinner.
        // Actual status change will be pushed via WebSocket when `handleIncomingTelemetry` fires.
    }"""

new_exec = """    async executeCommand(internalDeviceId: string, command: string, payload?: any, retryCount: number = 0): Promise<void> {
        // 1. Idempotency Check
        const idempotencyKey = `${internalDeviceId}_${command}_${Date.now() / 5000 | 0}`; // Dedupe within 5 seconds
        if (this.commandCache.has(idempotencyKey) && retryCount === 0) {
            console.warn(`[IoTGateway] DEDUPLICATED command ${command} for ${internalDeviceId}`);
            return;
        }
        if (retryCount === 0) this.commandCache.add(idempotencyKey);

        const mapping = this.deviceRegistry.get(internalDeviceId);
        if (!mapping) throw new Error('Device not registered in gateway memory');
        const provider = this.providers.get(mapping.provider);
        if (!provider) throw new Error('Provider not loaded');

        // 2. Event Sourcing DB Logging
        console.log(`[IoTGateway] [Event Sourcing] Logging COMMAND_ISSUED: ${command} for ${internalDeviceId}`);

        // 3. Dispatch
        const success = await provider.sendCommand(mapping.providerDeviceId, command, payload);
        if (!success) {
            console.error(`[IoTGateway] Provider dispatch failed. Event Sourcing: FAULT_DETECTED`);
            return;
        }

        console.log(`[IoTGateway] Dispatched (Retry ${retryCount}). Awaiting async telemetry verification...`);

        // 4. Retry Engine (Fail-safe timeout)
        if (this.retryQueue.has(internalDeviceId)) {
            clearTimeout(this.retryQueue.get(internalDeviceId));
        }

        const timeout = setTimeout(() => {
            console.warn(`[IoTGateway] 🚨 TIMEOUT: No async telemetry received for ${internalDeviceId} after command ${command}`);
            if (retryCount < 3) {
                console.log(`[IoTGateway] Initiating Retry ${retryCount + 1} for ${internalDeviceId}`);
                this.executeCommand(internalDeviceId, command, payload, retryCount + 1);
            } else {
                console.error(`[IoTGateway] 🚨 SRE FATAL: Command ${command} permanently failed after 3 retries.`);
                // Broadcast fault to Android
                this.broadcastWebSocketUpdate(internalDeviceId, { status: 'fault', isRunning: false, lastHeartbeat: new Date(), rawPayload: { error: 'TELEMETRY_TIMEOUT' } });
            }
        }, 15000); // 15 second SRE timeout

        this.retryQueue.set(internalDeviceId, timeout);
    }"""

content = content.replace(old_exec, new_exec)

# Integrate Event Sourcing and Power Intelligence into Telemetry Handler
telemetry_hook = """        // 2. State Verification Logic
        // If command was MOTOR_ON, we verify it actually turned on by checking amperage > threshold
        if (state.isRunning && state.amperage && state.amperage > 1.0) {
            console.log(`[IoTGateway] HARDWARE VERIFIED: Motor is drawing ${state.amperage}A. State confirmed.`);
            // Update DB command_queue status = 'completed'
        } else if (state.isRunning && state.amperage && state.amperage <= 0.1) {
            console.warn(`[IoTGateway] FAULT DETECTED: Motor reports ON but drawing 0A (Dry Run / Phase Failure)`);
            state.status = 'fault';
        }"""

new_telemetry_hook = """        // Clear any pending Retry Timeouts since telemetry arrived
        if (this.retryQueue.has(internalDeviceId)) {
            clearTimeout(this.retryQueue.get(internalDeviceId));
            this.retryQueue.delete(internalDeviceId);
            console.log(`[IoTGateway] Async telemetry received. Cleared Retry Queue for ${internalDeviceId}`);
        }

        // Event Sourcing Log
        // SQL: INSERT INTO device_events (event_type) VALUES ('TELEMETRY_RECEIVED')

        // SRE: Run Power Intelligence Protection
        this.powerEngine.evaluateTelemetry(internalDeviceId, state);

        // State Verification
        if (state.status !== 'fault' && state.isRunning && state.amperage && state.amperage > 1.0) {
            console.log(`[IoTGateway] HARDWARE VERIFIED: ${state.amperage}A. Logging STATE_CONFIRMED.`);
        } else if (state.isRunning && state.amperage && state.amperage <= 0.1) {
            console.warn(`[IoTGateway] FAULT DETECTED: Dry Run (0A). Logging FAULT_DETECTED.`);
            state.status = 'fault';
        }"""

content = content.replace(telemetry_hook, new_telemetry_hook)

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\backend\src\iot\Gateway.ts", "w", encoding="utf-8") as f:
    f.write(content)
