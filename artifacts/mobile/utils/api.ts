const API_BASE = process.env["EXPO_PUBLIC_DOMAIN"]
  ? `https://${process.env["EXPO_PUBLIC_DOMAIN"]}`
  : "";

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

export interface RequestOptions extends RequestInit {
  timeout?: number;
}

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { timeout = 12000, ...fetchOptions } = options;
  const maxRetries = 3;
  let lastError: any;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const url = path.startsWith("http") ? path : `${API_BASE}${path}`;
      const response = await fetch(url, {
        ...fetchOptions,
        headers: {
          "Content-Type": "application/json",
          ...fetchOptions.headers,
        },
        signal: options.signal || controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        if (response.status >= 500 && attempt < maxRetries - 1) {
          // Retry on server errors
          const delay = Math.pow(2, attempt) * 1000;
          await new Promise(r => setTimeout(r, delay));
          continue;
        }
        throw new ApiError(response.status, `HTTP ${response.status}: ${response.statusText}`);
      }

      return (await response.json()) as T;
    } catch (error: any) {
      clearTimeout(timeoutId);
      lastError = error;

      if (error.name === "AbortError" && attempt < maxRetries - 1) {
        const delay = Math.pow(2, attempt) * 500;
        await new Promise(r => setTimeout(r, delay));
        continue;
      }
      
      if (attempt === maxRetries - 1) {
        if (error.name === "AbortError") {
          throw new Error("Request timed out. Please check your connection.");
        }
        throw error;
      }
    }
  }
  throw lastError;
}
