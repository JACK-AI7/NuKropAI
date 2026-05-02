"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const ai_controller_1 = require("../controllers/ai.controller");
const auth_middleware_1 = require("../middleware/auth.middleware");
const router = (0, express_1.Router)();
router.post('/chat', auth_middleware_1.authMiddleware, ai_controller_1.AIController.chat);
router.get('/history', auth_middleware_1.authMiddleware, ai_controller_1.AIController.getChatHistory);
exports.default = router;
