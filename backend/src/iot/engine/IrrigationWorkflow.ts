import { IoTGateway, CommandPriority } from '../Gateway';

export enum WorkflowState {
    IDLE,
    CHECKING_POWER,
    OPENING_VALVE,
    STARTING_PUMP,
    IRRIGATING,
    CLOSING_VALVE,
    FAULT
}

/**
 * Autonomous Orchestration: Workflow State Machine Engine
 * Executes multi-step, dependency-aware irrigation sequences instead of basic ON/OFF commands.
 */
export class IrrigationWorkflow {
    private gateway: IoTGateway;
    private currentState: WorkflowState = WorkflowState.IDLE;
    private zoneValveId: string;
    private mainPumpId: string;
    private durationMs: number;

    constructor(gateway: IoTGateway, zoneValveId: string, mainPumpId: string, durationMins: number) {
        this.gateway = gateway;
        this.zoneValveId = zoneValveId;
        this.mainPumpId = mainPumpId;
        this.durationMs = durationMins * 60 * 1000;
    }

    async execute() {
        console.log(`[Workflow Engine] Initiating autonomous workflow for Zone Valve ${this.zoneValveId}`);
        
        try {
            // STEP 1: Power Verification (Simulated check)
            this.currentState = WorkflowState.CHECKING_POWER;
            
            // STEP 2: Open Zone Valve first to prevent burst pipes
            this.currentState = WorkflowState.OPENING_VALVE;
            await this.gateway.executeCommand(this.zoneValveId, 'VALVE_OPEN', null, 0, CommandPriority.HIGH);
            
            // Assume webhook or telemetry confirms valve is open within 5 seconds...
            await new Promise(res => setTimeout(res, 5000));
            
            // STEP 3: Start Main Pump
            this.currentState = WorkflowState.STARTING_PUMP;
            await this.gateway.executeCommand(this.mainPumpId, 'MOTOR_ON', null, 0, CommandPriority.HIGH);

            // STEP 4: Irrigation Timer
            this.currentState = WorkflowState.IRRIGATING;
            console.log(`[Workflow Engine] Irrigating for ${this.durationMs / 1000 / 60} minutes...`);

            // When timer finishes, shut down safely
            setTimeout(() => this.shutdown(), this.durationMs);

        } catch (error) {
            this.currentState = WorkflowState.FAULT;
            console.error(`[Workflow Engine] Fault in workflow execution. Triggering rollback.`, error);
            this.rollback();
        }
    }

    private async shutdown() {
        console.log(`[Workflow Engine] Irrigation complete. Safe shutdown sequence initiated.`);
        
        // 1. Stop pump first
        await this.gateway.executeCommand(this.mainPumpId, 'MOTOR_OFF', null, 0, CommandPriority.HIGH);
        await new Promise(res => setTimeout(res, 2000)); // Let pressure drop
        
        // 2. Close Valve
        this.currentState = WorkflowState.CLOSING_VALVE;
        await this.gateway.executeCommand(this.zoneValveId, 'VALVE_CLOSE', null, 0, CommandPriority.STANDARD);
        
        this.currentState = WorkflowState.IDLE;
    }

    private async rollback() {
        // Emergency kill switch on the pump, standard close on the valve
        await this.gateway.executeCommand(this.mainPumpId, 'MOTOR_OFF', { reason: 'WORKFLOW_ROLLBACK' }, 0, CommandPriority.CRITICAL_KILL_SWITCH);
        await this.gateway.executeCommand(this.zoneValveId, 'VALVE_CLOSE', null, 0, CommandPriority.HIGH);
    }
}
