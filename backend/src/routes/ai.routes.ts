import { Router } from 'express';
import { AIController } from '../controllers/ai.controller';
import { authMiddleware } from '../middleware/auth.middleware';

const router = Router();

router.post('/chat', authMiddleware, AIController.chat);
router.get('/history', authMiddleware, AIController.getChatHistory);

export default router;
