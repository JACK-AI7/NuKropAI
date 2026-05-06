/**
 * Retry logic with exponential backoff and jitter
 */
export interface RetryOptions {
  maxRetries?: number;
  initialDelay?: number;
  maxDelay?: number;
  backoffFactor?: number;
  jitter?: boolean;
  onRetry?: (error: Error, attempt: number) => void;
  shouldRetry?: (error: Error) => boolean;
}

const DEFAULT_RETRY_OPTIONS: Required<RetryOptions> = {
  maxRetries: 3,
  initialDelay: 100,
  maxDelay: 5000,
  backoffFactor: 2,
  jitter: true,
  onRetry: () => {},
  shouldRetry: (error: Error) => {
    // Retry on network errors, timeouts, and 5xx errors
    const message = error.message.toLowerCase();
    const name = error.name.toLowerCase();
    
    return (
      name.includes('timeout') ||
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
      message.includes('504')
    );
  },
};

/**
 * Calculate delay with exponential backoff and optional jitter
 */
function calculateDelay(
  attempt: number,
  initialDelay: number,
  maxDelay: number,
  backoffFactor: number,
  jitter: boolean
): number {
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
function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Execute function with retry logic
 */
export async function retry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const opts = { ...DEFAULT_RETRY_OPTIONS, ...options };
  let lastError: Error;

  for (let attempt = 1; attempt <= opts.maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      // Check if we should retry
      if (attempt === opts.maxRetries || !opts.shouldRetry(lastError)) {
        throw lastError;
      }

      // Calculate delay and wait
      const delay = calculateDelay(
        attempt,
        opts.initialDelay!,
        opts.maxDelay!,
        opts.backoffFactor!,
        opts.jitter!
      );

      // Call retry callback
      opts.onRetry?.(lastError, attempt);

      // Wait before retry
      await sleep(delay);
    }
  }

  throw lastError!;
}

/**
 * Retry with timeout protection
 */
export async function retryWithTimeout<T>(
  fn: () => Promise<T>,
  timeoutMs: number,
  retryOptions?: RetryOptions
): Promise<T> {
  return retry(
    () => withTimeout(fn, timeoutMs, 'Operation timed out'),
    retryOptions
  );
}

/**
 * Execute function with timeout protection
 */
export async function withTimeout<T>(
  fn: () => Promise<T>,
  timeoutMs: number,
  timeoutMessage: string = 'Operation timed out'
): Promise<T> {
  return Promise.race([
    fn(),
    new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error(timeoutMessage)), timeoutMs)
    ),
  ]);
}

/**
 * Circuit breaker state
 */
export enum CircuitBreakerState {
  CLOSED = 'CLOSED',    // Normal operation
  OPEN = 'OPEN',        // Failing, reject requests
  HALF_OPEN = 'HALF_OPEN', // Testing if service recovered
}

/**
 * Circuit breaker for fault tolerance
 */
export class CircuitBreaker<T> {
  private state: CircuitBreakerState = CircuitBreakerState.CLOSED;
  private failureCount: number = 0;
  private successCount: number = 0;
  private lastFailureTime: number | null = null;
  private nextAttemptTime: number | null = null;

  constructor(
    private fn: () => Promise<T>,
    private options: {
      failureThreshold?: number;
      successThreshold?: number;
      timeout?: number;
      resetTimeout?: number;
    } = {}
  ) {}

  async execute(): Promise<T> {
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
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    this.failureCount = 0;
    
    if (this.state === CircuitBreakerState.HALF_OPEN) {
      this.successCount++;
      if (this.successCount >= (this.options.successThreshold || 2)) {
        this.state = CircuitBreakerState.CLOSED;
        this.successCount = 0;
      }
    }
  }

  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    this.successCount = 0;

    if (this.failureCount >= (this.options.failureThreshold || 5)) {
      this.state = CircuitBreakerState.OPEN;
      this.nextAttemptTime = Date.now() + (this.options.resetTimeout || 30000);
    }
  }

  getState(): CircuitBreakerState {
    return this.state;
  }

  reset(): void {
    this.state = CircuitBreakerState.CLOSED;
    this.failureCount = 0;
    this.successCount = 0;
    this.lastFailureTime = null;
    this.nextAttemptTime = null;
  }
}
