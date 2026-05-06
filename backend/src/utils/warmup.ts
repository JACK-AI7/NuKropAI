/**
 * Model warmup system
 * Pre-loads models and initializes GPU on startup
 */

import { logger } from './logger';
import { HealthMonitor } from './health';

export interface WarmupConfig {
  models: string[];
  ollamaHost: string;
  warmupTimeout?: number;
  batchSize?: number;
}

export interface WarmupResult {
  success: boolean;
  loadedModels: string[];
  failedModels: string[];
  durationMs: number;
  errors: string[];
}

export class ModelWarmup {
  private config: WarmupConfig;
  private healthMonitor: HealthMonitor;

  constructor(config: WarmupConfig, healthMonitor: HealthMonitor) {
    this.config = { warmupTimeout: 60000, batchSize: 1, ...config };
    this.healthMonitor = healthMonitor;
  }

  /**
   * Warm up all models
   */
  async warmup(): Promise<WarmupResult> {
    const startTime = Date.now();
    const loadedModels: string[] = [];
    const failedModels: string[] = [];
    const errors: string[] = [];

    logger.info('Starting model warmup', {
      service: 'model-warmup',
      modelCount: this.config.models.length,
      models: this.config.models,
    });

    // Step 1: Check Ollama availability
    const ollamaReady = await this.checkOllama();
    if (!ollamaReady) {
      throw new Error('Ollama is not available. Cannot warm up models.');
    }

    // Step 2: Load models sequentially
    for (const model of this.config.models) {
      try {
        await this.loadModel(model);
        loadedModels.push(model);
        this.healthMonitor.registerModel(model, 'latest');
        logger.info(`Model loaded successfully`, {
          service: 'model-warmup',
          model,
          loaded: loadedModels.length,
          total: this.config.models.length,
        });
      } catch (error) {
        failedModels.push(model);
        const errorMsg = (error as Error).message;
        errors.push(`${model}: ${errorMsg}`);
        logger.error(`Failed to load model`, {
          service: 'model-warmup',
          model,
          error: errorMsg,
        });
      }
    }

    // Step 3: Run inference on dummy data
    if (loadedModels.length > 0) {
      await this.runDummyInference(loadedModels);
    }

    const durationMs = Date.now() - startTime;

    logger.info('Model warmup completed', {
      service: 'model-warmup',
      duration_ms: durationMs,
      loaded: loadedModels.length,
      failed: failedModels.length,
      success: failedModels.length === 0,
    });

    return {
      success: failedModels.length === 0,
      loadedModels,
      failedModels,
      durationMs,
      errors,
    };
  }

  /**
   * Check if Ollama is available
   */
  private async checkOllama(): Promise<boolean> {
    try {
      const response = await fetch(`${this.config.ollamaHost}/api/tags`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        signal: AbortSignal.timeout(10000),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      logger.info('Ollama is available', {
        service: 'model-warmup',
        models: data.models?.map((m: any) => m.name) || [],
      });

      return true;
    } catch (error) {
      logger.error('Ollama is not available', {
        service: 'model-warmup',
        error: (error as Error).message,
      });
      return false;
    }
  }

  /**
   * Load a model into Ollama
   */
  private async loadModel(model: string): Promise<void> {
    logger.info(`Loading model`, { service: 'model-warmup', model });

    // Pull model
    const pullResponse = await fetch(`${this.config.ollamaHost}/api/pull`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: model,
        stream: false,
      }),
    });

    if (!pullResponse.ok) {
      throw new Error(`Failed to pull model: HTTP ${pullResponse.status}`);
    }

    const pullData = await pullResponse.json();
    
    if (pullData.error) {
      throw new Error(pullData.error);
    }

    logger.info(`Model pulled successfully`, { service: 'model-warmup', model });
  }

  /**
   * Run dummy inference to initialize GPU and model
   */
  private async runDummyInference(models: string[]): Promise<void> {
    logger.info('Running dummy inference to initialize GPU', { service: 'model-warmup' });

    for (const model of models) {
      try {
        const startTime = Date.now();

        const response = await fetch(`${this.config.ollamaHost}/api/generate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            model,
            prompt: 'Hello',
            stream: false,
            options: {
              num_predict: 1,
              temperature: 0,
            },
          }),
          signal: AbortSignal.timeout(30000),
        });

        const durationMs = Date.now() - startTime;

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
          throw new Error(data.error);
        }

        this.healthMonitor.updateModelUsage(model, durationMs);

        logger.info('Dummy inference completed', {
          service: 'model-warmup',
          model,
          duration_ms: durationMs,
        });
      } catch (error) {
        logger.warn('Dummy inference failed (non-critical)', {
          service: 'model-warmup',
          model,
          error: (error as Error).message,
        });
      }
    }
  }

  /**
   * Background loading of additional models
   */
  async backgroundLoad(models: string[]): Promise<void> {
    logger.info('Starting background model loading', {
      service: 'model-warmup',
      models,
    });

    // Load in background without blocking
    setTimeout(async () => {
      for (const model of models) {
        try {
          await this.loadModel(model);
          this.healthMonitor.registerModel(model, 'latest');
          logger.info('Background model loaded', { service: 'model-warmup', model });
        } catch (error) {
          logger.error('Background model loading failed', {
            service: 'model-warmup',
            model,
            error: (error as Error).message,
          });
        }
      }
    }, 0);
  }

  /**
   * Pre-compute and cache embeddings
   */
  async cacheEmbeddings(queries: string[]): Promise<void> {
    logger.info('Caching embeddings for common queries', {
      service: 'model-warmup',
      queryCount: queries.length,
    });

    // This would integrate with your embedding service
    // For now, just log the intent
    for (const query of queries) {
      logger.debug('Would cache embedding', {
        service: 'model-warmup',
        query,
      });
    }
  }
}
