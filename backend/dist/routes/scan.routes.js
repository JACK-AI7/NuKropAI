"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const multer_1 = __importDefault(require("multer"));
const scan_controller_1 = require("../controllers/scan.controller");
const auth_middleware_1 = require("../middleware/auth.middleware");
const router = (0, express_1.Router)();
const storage = multer_1.default.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, `${Date.now()}-${file.originalname}`);
    },
});
const upload = (0, multer_1.default)({ storage });
router.post('/', auth_middleware_1.authMiddleware, upload.single('image'), scan_controller_1.ScanController.createScan);
router.get('/history', auth_middleware_1.authMiddleware, scan_controller_1.ScanController.getHistory);
router.get('/:id', auth_middleware_1.authMiddleware, scan_controller_1.ScanController.getScanById);
exports.default = router;
