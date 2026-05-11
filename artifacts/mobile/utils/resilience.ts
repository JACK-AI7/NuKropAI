export interface RetryOptions {
  maxRetries: number;
  backoffMs: number;
}

export async function withRetry<T>(
  fn: () => Promise<T>, 
  options: RetryOptions = { maxRetries: 3, backoffMs: 1000 }
): Promise<T> {
  let attempt = 0;
  while (attempt < options.maxRetries) {
    try {
      return await fn();
    } catch (err) {
      attempt++;
      if (attempt === options.maxRetries) throw err;
      const delay = options.backoffMs * Math.pow(2, attempt);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  throw new Error("Retry failed");
}

export async function verifySyncIntegrity(localData: any, cloudData: any): Promise<boolean> {
  // Checksums or version vector comparison
  return JSON.stringify(localData) === JSON.stringify(cloudData);
}

export async function executeFallbackWorkflow(action: string) {
  console.log(`[RESILIENCE] Executing fallback for: ${action}`);
  // Logic to use local cached intelligence if cloud is unreachable
}
