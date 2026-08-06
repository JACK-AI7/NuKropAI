import { IotDeviceState } from './providers/BaseDeviceProvider';
import { IoTGateway } from './Gateway';

export interface AutomationRule {
    id: string;
    deviceId: string;
    conditionMetric: 'moisture' | 'voltage' | 'amperage';
    conditionOp: '<' | '>' | '==';
    conditionValue: number;
    actionCommand: 'MOTOR_ON' | 'MOTOR_OFF';
}

/**
 * Executes automated IF/THEN farming rules based on incoming live telemetry
 */
export class RuleEngine {
    private gateway: IoTGateway;
    private rules: AutomationRule[] = [];

    constructor(gateway: IoTGateway) {
        this.gateway = gateway;
    }

    loadRules(rules: AutomationRule[]) {
        this.rules = rules;
    }

    evaluate(deviceId: string, state: IotDeviceState) {
        const deviceRules = this.rules.filter(r => r.deviceId === deviceId);

        for (const rule of deviceRules) {
            let metricValue: number | undefined;

            switch (rule.conditionMetric) {
                case 'moisture': metricValue = state.moisture; break;
                case 'voltage': metricValue = state.voltage; break;
                case 'amperage': metricValue = state.amperage; break;
            }

            if (metricValue === undefined) continue;

            let conditionMet = false;
            if (rule.conditionOp === '<' && metricValue < rule.conditionValue) conditionMet = true;
            if (rule.conditionOp === '>' && metricValue > rule.conditionValue) conditionMet = true;
            if (rule.conditionOp === '==' && metricValue === rule.conditionValue) conditionMet = true;

            if (conditionMet) {
                console.log(`[RuleEngine] Rule ${rule.id} triggered: ${rule.conditionMetric} ${metricValue} ${rule.conditionOp} ${rule.conditionValue}`);
                
                // Prevent infinite loop if already in target state
                if (rule.actionCommand === 'MOTOR_ON' && state.isRunning) continue;
                if (rule.actionCommand === 'MOTOR_OFF' && !state.isRunning) continue;

                console.log(`[RuleEngine] Executing automated action: ${rule.actionCommand}`);
                this.gateway.executeCommand(deviceId, rule.actionCommand);
            }
        }
    }
}
