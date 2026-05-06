"use strict";
/**
 * Model warmup system
 * Pre-loads models and initializes GPU on startup
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ModelWarmup = void 0;
const logger_1 = require("./logger");
class ModelWarmup {
    constructor(config, healthMonitor) {
        this.config = { warmupTimeout: 60000, batchSize: 1, ...config };
        this.healthMonitor = healthMonitor;
    }
    /**
     * Warm up all models
     */
    async warmup() {
        const startTime = Date.now();
        const loadedModels = [];
        const failedModels = [];
        const errors = [];
        logger_1.logger.info('Starting model warmup', {
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
                logger_1.logger.info(`Model loaded successfully`, {
                    service: 'model-warmup',
                    model,
                    loaded: loadedModels.length,
                    total: this.config.models.length,
                });
            }
            catch (error) {
                failedModels.push(model);
                const errorMsg = error.message;
                errors.push(`${model}: ${errorMsg}`);
                logger_1.logger.error(`Failed to load model`, {
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
        logger_1.logger.info('Model warmup completed', {
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
    async checkOllama() {
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
            logger_1.logger.info('Ollama is available', {
                service: 'model-warmup',
                models: data.models?.map((m) => m.name) || [],
            });
            return true;
        }
        catch (error) {
            logger_1.logger.error('Ollama is not available', {
                service: 'model-warmup',
                error: error.message,
            });
            return false;
        }
    }
    /**
     * Load a model into Ollama
     */
    async loadModel(model) {
        logger_1.logger.info(`Loading model`, { service: 'model-warmup', model });
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
        logger_1.logger.info(`Model pulled successfully`, { service: 'model-warmup', model });
    }
    /**
     * Run dummy inference to initialize GPU and model
     */
    async runDummyInference(models) {
        logger_1.logger.info('Running dummy inference to initialize GPU', { service: 'model-warmup' });
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
                logger_1.logger.info('Dummy inference completed', {
                    service: 'model-warmup',
                    model,
                    duration_ms: durationMs,
                });
            }
            catch (error) {
                logger_1.logger.warn('Dummy inference failed (non-critical)', {
                    service: 'model-warmup',
                    model,
                    error: error.message,
                });
            }
        }
    }
    /**
     * Background loading of additional models
     */
    async backgroundLoad(models) {
        logger_1.logger.info('Starting background model loading', {
            service: 'model-warmup',
            models,
        });
        // Load in background without blocking
        setTimeout(async () => {
            for (const model of models) {
                try {
                    await this.loadModel(model);
                    this.healthMonitor.registerModel(model, 'latest');
                    logger_1.logger.info('Background model loaded', { service: 'model-warmup', model });
                }
                catch (error) {
                    logger_1.logger.error('Background model loading failed', {
                        service: 'model-warmup',
                        model,
                        error: error.message,
                    });
                }
            }
        }, 0);
    }
    /**
     * Pre-compute and cache embeddings
     */
    async cacheEmbeddings(queries) {
        logger_1.logger.info('Caching embeddings for common queries', {
            service: 'model-warmup',
            queryCount: queries.length,
        });
        // This would integrate with your embedding service
        // For now, just log the intent
        for (const query of queries) {
            logger_1.logger.debug('Would cache embedding', {
                service: 'model-warmup',
                query,
            });
        }
    }
}
exports.ModelWarmup = ModelWarmup;
