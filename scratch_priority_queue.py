import re

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\backend\src\iot\Gateway.ts", "r", encoding="utf-8") as f:
    content = f.read()

# Add Priority enum and priorityQueue
priority_logic = """export enum CommandPriority {
    LOW = 0,
    STANDARD = 1,
    HIGH = 2,
    CRITICAL_KILL_SWITCH = 99
}

interface QueuedCommand {
    internalDeviceId: string;
    command: string;
    payload?: any;
    priority: CommandPriority;
    retryCount: number;
}
"""

content = priority_logic + content

# Inside Gateway class, add priority queue processing
content = content.replace("private commandCache: Set<string> = new Set();", 
    "private commandCache: Set<string> = new Set();\n    private priorityQueue: QueuedCommand[] = [];\n    private isProcessingQueue = false;")

# Rewrite executeCommand to queue by priority and process
new_exec = """    async executeCommand(internalDeviceId: string, command: string, payload?: any, retryCount: number = 0, priority: CommandPriority = CommandPriority.STANDARD): Promise<void> {
        // 1. CRITICAL BYPASS
        if (priority === CommandPriority.CRITICAL_KILL_SWITCH) {
            console.log(`[IoTGateway] 🚨 CRITICAL PRIORITY: Bypassing DLQ and Queues for ${command} to ${internalDeviceId}`);
            await this.dispatchToProvider(internalDeviceId, command, payload, retryCount);
            return;
        }

        // 2. Standard Queueing
        this.priorityQueue.push({ internalDeviceId, command, payload, priority, retryCount });
        
        // Sort by priority descending
        this.priorityQueue.sort((a, b) => b.priority - a.priority);
        
        if (!this.isProcessingQueue) {
            this.processQueue();
        }
    }

    private async processQueue() {
        this.isProcessingQueue = true;
        while (this.priorityQueue.length > 0) {
            const nextCmd = this.priorityQueue.shift();
            if (nextCmd) {
                await this.dispatchToProvider(nextCmd.internalDeviceId, nextCmd.command, nextCmd.payload, nextCmd.retryCount);
                // Introduce small 50ms delay to prevent rate-limiting downstream
                await new Promise(res => setTimeout(res, 50));
            }
        }
        this.isProcessingQueue = false;
    }

    private async dispatchToProvider(internalDeviceId: string, command: string, payload?: any, retryCount: number = 0): Promise<void> {"""

content = content.replace("async executeCommand(internalDeviceId: string, command: string, payload?: any, retryCount: number = 0): Promise<void> {", new_exec)

# Fix references to recursion in retry
content = content.replace("this.executeCommand(internalDeviceId, command, payload, retryCount + 1);", 
    "this.executeCommand(internalDeviceId, command, payload, retryCount + 1, CommandPriority.HIGH); // Retry at high priority")

with open(r"c:\Users\bjasw\Downloads\agriculture-ai-os\backend\src\iot\Gateway.ts", "w", encoding="utf-8") as f:
    f.write(content)
