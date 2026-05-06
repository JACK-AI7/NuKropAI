"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.CircuitBreaker = exports.CircuitBreakerState = void 0;
exports.retry = retry;
exports.retryWithTimeout = retryWithTimeout;
exports.withTimeout = withTimeout;
const DEFAULT_RETRY_OPTIONS = {
    maxRetries: 3,
    initialDelay: 100,
    maxDelay: 5000,
    backoffFactor: 2,
    jitter: true,
    onRetry: () => { },
    shouldRetry: (error) => {
        // Retry on network errors, timeouts, and 5xx errors
        const message = error.message.toLowerCase();
        const name = error.name.toLowerCase();
        return (name.includes('timeout') ||
            name.includes('network') ||
            name.includes('connection') ||
            name.includes('econn') ||
            message.includes('timeout') ||
            message.includes('network') ||
            message.includes('connection') ||
            message.includes('econn') ||
            message.includes('500') ||
            message.includes('502') ||
            message.includes('503') ||
            message.includes('504'));
    },
};
/**
 * Calculate delay with exponential backoff and optional jitter
 */
function calculateDelay(attempt, initialDelay, maxDelay, backoffFactor, jitter) {
    let delay = Math.min(initialDelay * Math.pow(backoffFactor, attempt - 1), maxDelay);
    if (jitter) {
        // Add random jitter (±25% of delay)
        const jitterAmount = delay * 0.25;
        delay = delay - jitterAmount + Math.random() * jitterAmount * 2;
    }
    return delay;
}
/**
 * Sleep for specified milliseconds
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
/**
 * Execute function with retry logic
 */
async function retry(fn, options = {}) {
    const opts = { ...DEFAULT_RETRY_OPTIONS, ...options };
    let lastError;
    for (let attempt = 1; attempt <= opts.maxRetries; attempt++) {
        try {
            return await fn();
        }
        catch (error) {
            lastError = error;
            // Check if we should retry
            if (attempt === opts.maxRetries || !opts.shouldRetry(lastError)) {
                throw lastError;
            }
            // Calculate delay and wait
            const delay = calculateDelay(attempt, opts.initialDelay, opts.maxDelay, opts.backoffFactor, opts.jitter);
            // Call retry callback
            opts.onRetry?.(lastError, attempt);
            // Wait before retry
            await sleep(delay);
        }
    }
    throw lastError;
}
/**
 * Retry with timeout protection
 */
async function retryWithTimeout(fn, timeoutMs, retryOptions) {
    return retry(() => withTimeout(fn, timeoutMs, 'Operation timed out'), retryOptions);
}
/**
 * Execute function with timeout protection
 */
async function withTimeout(fn, timeoutMs, timeoutMessage = 'Operation timed out') {
    return Promise.race([
        fn(),
        new Promise((_, reject) => setTimeout(() => reject(new Error(timeoutMessage)), timeoutMs)),
    ]);
}
/**
 * Circuit breaker state
 */
var CircuitBreakerState;
(function (CircuitBreakerState) {
    CircuitBreakerState["CLOSED"] = "CLOSED";
    CircuitBreakerState["OPEN"] = "OPEN";
    CircuitBreakerState["HALF_OPEN"] = "HALF_OPEN";
})(CircuitBreakerState || (exports.CircuitBreakerState = CircuitBreakerState = {}));
/**
 * Circuit breaker for fault tolerance
 */
class CircuitBreaker {
    constructor(fn, options = {}) {
        this.fn = fn;
        this.options = options;
        this.state = CircuitBreakerState.CLOSED;
        this.failureCount = 0;
        this.successCount = 0;
        this.lastFailureTime = null;
        this.nextAttemptTime = null;
    }
    async execute() {
        const { failureThreshold = 5, successThreshold = 2, timeout = 60000, resetTimeout = 30000 } = this.options;
        // Check circuit state
        if (this.state === CircuitBreakerState.OPEN) {
            if (this.nextAttemptTime && Date.now() < this.nextAttemptTime) {
                throw new Error('Circuit breaker is OPEN');
            }
            // Try again
            this.state = CircuitBreakerState.HALF_OPEN;
        }
        try {
            const result = await withTimeout(this.fn, timeout);
            this.onSuccess();
            return result;
        }
        catch (error) {
            this.onFailure();
            throw error;
        }
    }
    onSuccess() {
        this.failureCount = 0;
        if (this.state === CircuitBreakerState.HALF_OPEN) {
            this.successCount++;
            if (this.successCount >= (this.options.successThreshold || 2)) {
                this.state = CircuitBreakerState.CLOSED;
                this.successCount = 0;
            }
        }
    }
    onFailure() {
        this.failureCount++;
        this.lastFailureTime = Date.now();
        this.successCount = 0;
        if (this.failureCount >= (this.options.failureThreshold || 5)) {
            this.state = CircuitBreakerState.OPEN;
            this.nextAttemptTime = Date.now() + (this.options.resetTimeout || 30000);
        }
    }
    getState() {
        return this.state;
    }
    reset() {
        this.state = CircuitBreakerState.CLOSED;
        this.failureCount = 0;
        this.successCount = 0;
        this.lastFailureTime = null;
        this.nextAttemptTime = null;
    }
}
exports.CircuitBreaker = CircuitBreaker;
