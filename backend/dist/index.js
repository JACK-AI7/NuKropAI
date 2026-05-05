"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const helmet_1 = __importDefault(require("helmet"));
const morgan_1 = __importDefault(require("morgan"));
const dotenv_1 = __importDefault(require("dotenv"));
const path_1 = __importDefault(require("path"));
const fs_1 = __importDefault(require("fs"));
const auth_routes_1 = __importDefault(require("./routes/auth.routes"));
const scan_routes_1 = __importDefault(require("./routes/scan.routes"));
const weather_routes_1 = __importDefault(require("./routes/weather.routes"));
const ai_routes_1 = __importDefault(require("./routes/ai.routes"));
dotenv_1.default.config();
const app = (0, express_1.default)();
const PORT = process.env.PORT || 3000;
// Ensure uploads directory exists
const uploadsDir = path_1.default.join(process.cwd(), 'uploads');
if (!fs_1.default.existsSync(uploadsDir)) {
    fs_1.default.mkdirSync(uploadsDir, { recursive: true });
    console.log('✅ Created uploads directory:', uploadsDir);
}
// Middleware
app.use((0, helmet_1.default)());
app.use((0, cors_1.default)({
    origin: process.env.NODE_ENV === 'production'
        ? (process.env.ALLOWED_ORIGINS?.split(',') || [])
        : true,
    credentials: true,
}));
app.use((0, morgan_1.default)('dev'));
app.use(express_1.default.json({ limit: '50mb' }));
app.use(express_1.default.urlencoded({ extended: true, limit: '50mb' }));
app.use('/uploads', express_1.default.static(uploadsDir));
// Routes
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        env: process.env.NODE_ENV || 'development',
        ollama: process.env.OLLAMA_HOST || 'not configured',
        mistral: process.env.MISTRAL_API_KEY ? 'configured' : 'not configured',
    });
});
app.use('/api/auth', auth_routes_1.default);
app.use('/api/scans', scan_routes_1.default);
app.use('/api/weather', weather_routes_1.default);
app.use('/api/ai', ai_routes_1.default);
app.get('/api/recommendations', (req, res) => {
    try {
        const data = JSON.parse(fs_1.default.readFileSync(path_1.default.join(process.cwd(), 'data', 'crops.json'), 'utf8'));
        res.json(data.crops);
    }
    catch (err) {
        console.error('Error reading crops data:', err);
        res.status(500).json({ error: 'Failed to load recommendations data' });
    }
});
//Error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        error: 'Something went wrong!',
        message: process.env.NODE_ENV === 'development' ? err.message : undefined,
    });
});
// 404 handler
app.use((req, res) => {
    res.status(404).json({ error: 'Route not found' });
});
const server = app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Server running on http://0.0.0.0:${PORT}`);
    console.log(`📡 Health check: http://localhost:${PORT}/health`);
    console.log(`🔗 API base: http://localhost:${PORT}/api`);
});
// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received: shutting down gracefully');
    server.close(() => {
        console.log('Process terminated');
    });
});
