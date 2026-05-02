"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AuthController = void 0;
const bcryptjs_1 = __importDefault(require("bcryptjs"));
const jsonwebtoken_1 = __importDefault(require("jsonwebtoken"));
const index_1 = require("../index");
const JWT_SECRET = process.env.JWT_SECRET || 'fallback_secret';
class AuthController {
    static async register(req, res) {
        try {
            const { email, password, name } = req.body;
            const existingUser = await index_1.prisma.user.findUnique({ where: { email } });
            if (existingUser) {
                return res.status(400).json({ error: 'User already exists' });
            }
            const hashedPassword = await bcryptjs_1.default.hash(password, 10);
            const user = await index_1.prisma.user.create({
                data: { email, password: hashedPassword, name },
            });
            const token = jsonwebtoken_1.default.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });
            res.status(201).json({ user: { id: user.id, email: user.email, name: user.name }, token });
        }
        catch (error) {
            res.status(500).json({ error: 'Failed to register' });
        }
    }
    static async login(req, res) {
        try {
            const { email, password } = req.body;
            const user = await index_1.prisma.user.findUnique({ where: { email } });
            if (!user) {
                return res.status(400).json({ error: 'Invalid credentials' });
            }
            const isValid = await bcryptjs_1.default.compare(password, user.password);
            if (!isValid) {
                return res.status(400).json({ error: 'Invalid credentials' });
            }
            const token = jsonwebtoken_1.default.sign({ userId: user.id }, JWT_SECRET, { expiresIn: '7d' });
            res.json({ user: { id: user.id, email: user.email, name: user.name }, token });
        }
        catch (error) {
            res.status(500).json({ error: 'Failed to login' });
        }
    }
    static async me(req, res) {
        try {
            const userId = req.userId;
            const user = await index_1.prisma.user.findUnique({ where: { id: userId } });
            if (!user)
                return res.status(404).json({ error: 'User not found' });
            res.json({ user: { id: user.id, email: user.email, name: user.name } });
        }
        catch (error) {
            res.status(500).json({ error: 'Failed to get user' });
        }
    }
}
exports.AuthController = AuthController;
