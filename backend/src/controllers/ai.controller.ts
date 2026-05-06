import { Request, Response } from 'express';
import { prisma } from '../lib/prisma';
import { AIService } from '../services/ai.service';
import { retryWithTimeout } from '../utils/retry';
import { logger } from '../utils/logger';

export class AIController {
  static async chat(req: Request, res: Response) {
    try {
      const userId = (req as any).userId;
      const { message } = req.body;

      if (!message || message.trim().length === 0) {
        return res.status(400).json({ error: 'Message is required' });
      }

      // Fetch history for context
      const prevChats = await prisma.chat.findMany({
        where: { userId },
        orderBy: { createdAt: 'desc' },
        take: 5
      });

      const history = prevChats.reverse().map(c => ([
        { role: 'user', parts: [{ text: c.message }] },
        { role: 'model', parts: [{ text: c.response }] }
      ])).flat();

      // Use retry with timeout for AI inference
      const response = await retryWithTimeout(
        () => AIService.chat(message, history),
        30000, // 30 second timeout
        { 
          maxRetries: 2,
          onRetry: (error, attempt) => {
            logger.warn('AI chat retry attempt', {
              service: 'ai-controller',
              attempt,
              error: error.message,
              userId,
            });
          }
        }
      );

      await prisma.chat.create({
        data: { userId, message, response },
      });

      logger.info('AI chat completed', {
        service: 'ai-controller',
        userId,
        messageLength: message.length,
        responseLength: response.length,
      });

      res.json({ response });
    } catch (error) {
      logger.error('AI chat failed', {
        service: 'ai-controller',
        error: (error as Error).message,
        userId: (req as any).userId,
      });
      res.status(500).json({ error: 'Failed to process chat request' });
    }
  }

  static async getChatHistory(req: Request, res: Response) {
    try {
      const userId = (req as any).userId;
      const chats = await prisma.chat.findMany({
        where: { userId },
        orderBy: { createdAt: 'desc' },
        take: 50,
      });

      res.json(chats);
    } catch (error) {
      logger.error('Failed to fetch chat history', {
        service: 'ai-controller',
        error: (error as Error).message,
        userId: (req as any).userId,
      });
      res.status(500).json({ error: 'Failed to fetch chat history' });
    }
  }
}
