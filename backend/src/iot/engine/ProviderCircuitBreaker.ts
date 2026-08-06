/**
 * Enterprise Resilience Pattern: Circuit Breaker
 * Protects the platform from cascading failures if a 3rd party provider (Tuya/Twilio) goes down.
 */
export class ProviderCircuitBreaker {
    private providerName: string;
    private failureCount: number = 0;
    private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';
    
    // Configurable thresholds
    private readonly FAILURE_THRESHOLD = 5;
    private readonly RESET_TIMEOUT_MS = 60000; // 1 minute

    private nextAttemptTime: number = 0;

    constructor(providerName: string) {
        this.providerName = providerName;
    }

    /**
     * Call this before executing an external API request
     */
    canExecute(): boolean {
        if (this.state === 'CLOSED') return true;
        
        if (this.state === 'OPEN') {
            if (Date.now() > this.nextAttemptTime) {
                // Time to test if provider is back up
                this.state = 'HALF_OPEN';
                console.log(`[CircuitBreaker] ${this.providerName} transitioning to HALF_OPEN state. Testing connection...`);
                return true; 
            }
            return false; // Fast-fail
        }

        // HALF_OPEN allows 1 request through to test
        return this.state === 'HALF_OPEN';
    }

    /**
     * Call this after a successful provider request
     */
    onSuccess() {
        if (this.state === 'HALF_OPEN') {
            console.log(`[CircuitBreaker] ${this.providerName} connection restored. Circuit CLOSED.`);
            this.state = 'CLOSED';
            this.failureCount = 0;
        }
    }

    /**
     * Call this when a provider request times out or returns HTTP 500
     */
    onFailure() {
        this.failureCount++;
        console.warn(`[CircuitBreaker] ${this.providerName} failure recorded (${this.failureCount}/${this.FAILURE_THRESHOLD})`);
        
        if (this.failureCount >= this.FAILURE_THRESHOLD && this.state !== 'OPEN') {
            this.state = 'OPEN';
            this.nextAttemptTime = Date.now() + this.RESET_TIMEOUT_MS;
            console.error(`[CircuitBreaker] 🚨 ${this.providerName} CIRCUIT OPENED. Fast-failing requests for ${this.RESET_TIMEOUT_MS / 1000}s.`);
        }
    }
}
