"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AIController = void 0;
const prisma_1 = require("../lib/prisma");
const ai_service_1 = require("../services/ai.service");
const retry_1 = require("../utils/retry");
const logger_1 = require("../utils/logger");
class AIController {
    static async chat(req, res) {
        try {
            const userId = req.userId;
            const { message } = req.body;
            if (!message || message.trim().length === 0) {
                return res.status(400).json({ error: 'Message is required' });
            }
            // Fetch history for context
            const prevChats = await prisma_1.prisma.chat.findMany({
                where: { userId },
                orderBy: { createdAt: 'desc' },
                take: 5
            });
            const history = prevChats.reverse().map(c => ([
                { role: 'user', parts: [{ text: c.message }] },
                { role: 'model', parts: [{ text: c.response }] }
            ])).flat();
            // Use retry with timeout for AI inference
            const response = await (0, retry_1.retryWithTimeout)(() => ai_service_1.AIService.chat(message, history), 30000, // 30 second timeout
            {
                maxRetries: 2,
                onRetry: (error, attempt) => {
                    logger_1.logger.warn('AI chat retry attempt', {
                        service: 'ai-controller',
                        attempt,
                        error: error.message,
                        userId,
                    });
                }
            });
            await prisma_1.prisma.chat.create({
                data: { userId, message, response },
            });
            logger_1.logger.info('AI chat completed', {
                service: 'ai-controller',
                userId,
                messageLength: message.length,
                responseLength: response.length,
            });
            res.json({ response });
        }
        catch (error) {
            logger_1.logger.error('AI chat failed', {
                service: 'ai-controller',
                error: error.message,
                userId: req.userId,
            });
            res.status(500).json({ error: 'Failed to process chat request' });
        }
    }
    static async getChatHistory(req, res) {
        try {
            const userId = req.userId;
            const chats = await prisma_1.prisma.chat.findMany({
                where: { userId },
                orderBy: { createdAt: 'desc' },
                take: 50,
            });
            res.json(chats);
        }
        catch (error) {
            logger_1.logger.error('Failed to fetch chat history', {
                service: 'ai-controller',
                error: error.message,
                userId: req.userId,
            });
            res.status(500).json({ error: 'Failed to fetch chat history' });
        }
    }
}
exports.AIController = AIController;
