"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AIController = void 0;
const prisma_1 = require("../lib/prisma");
const ai_service_1 = require("../services/ai.service");
class AIController {
    static async chat(req, res) {
        try {
            const userId = req.userId;
            const { message } = req.body;
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
            const response = await ai_service_1.AIService.chat(message, history);
            await prisma_1.prisma.chat.create({
                data: { userId, message, response },
            });
            res.json({ response });
        }
        catch (error) {
            console.error(error);
            res.status(500).json({ error: 'Failed to chat' });
        }
    }
    static async getChatHistory(req, res) {
        try {
            const userId = req.userId;
            const chats = await prisma_1.prisma.chat.findMany({
                where: { userId },
                orderBy: { createdAt: 'desc' },
            });
            res.json(chats);
        }
        catch (error) {
            res.status(500).json({ error: 'Failed to fetch chat history' });
        }
    }
}
exports.AIController = AIController;
