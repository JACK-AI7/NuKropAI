import { Request, Response } from 'express';
import { prisma } from '../index';
import { AIService } from '../services/ai.service';

export class AIController {
  static async chat(req: Request, res: Response) {
    try {
      const userId = (req as any).userId;
      const { message } = req.body;

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

      const response = await AIService.chat(message, history);

      await prisma.chat.create({
        data: { userId, message, response },
      });

      res.json({ response });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: 'Failed to chat' });
    }
  }

  static async getChatHistory(req: Request, res: Response) {
    try {
      const userId = (req as any).userId;
      const chats = await prisma.chat.findMany({
        where: { userId },
        orderBy: { createdAt: 'desc' },
      });
      res.json(chats);
    } catch (error) {
      res.status(500).json({ error: 'Failed to fetch chat history' });
    }
  }
}
