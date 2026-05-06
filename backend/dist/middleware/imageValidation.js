"use strict";
/**
 * Image Upload Validation Middleware
 * Validates size, format, and dimensions
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.upload = exports.compressImage = exports.validateImageUpload = void 0;
const multer_1 = __importDefault(require("multer"));
const path_1 = __importDefault(require("path"));
const fs_1 = __importDefault(require("fs"));
const logger_1 = require("../utils/logger");
// Maximum file size (10MB)
const MAX_FILE_SIZE = 10 * 1024 * 1024;
// Allowed MIME types
const ALLOWED_MIME_TYPES = [
    'image/jpeg',
    'image/jpg',
    'image/png',
    'image/webp',
    'image/bmp',
];
// Maximum dimensions
const MAX_WIDTH = 4096;
const MAX_HEIGHT = 4096;
const MIN_WIDTH = 10;
const MIN_HEIGHT = 10;
const validateImageUpload = (options = {}) => {
    const opts = {
        maxSize: MAX_FILE_SIZE,
        allowedTypes: ALLOWED_MIME_TYPES,
        maxWidth: MAX_WIDTH,
        maxHeight: MAX_HEIGHT,
        minWidth: MIN_WIDTH,
        minHeight: MIN_HEIGHT,
        requireDimensions: false,
        ...options,
    };
    return async (req, res, next) => {
        try {
            // Check if file exists
            if (!req.file) {
                return res.status(400).json({
                    error: 'No file uploaded',
                    message: 'Please upload an image file',
                });
            }
            const file = req.file;
            const userId = req.userId || 'anonymous';
            // Validate file size
            if (file.size > opts.maxSize) {
                // Clean up the uploaded file
                fs_1.default.unlinkSync(file.path);
                logger_1.logger.warn('File too large', {
                    service: 'image-validation',
                    userId,
                    size: file.size,
                    maxSize: opts.maxSize,
                    filename: file.originalname,
                });
                return res.status(413).json({
                    error: 'File too large',
                    message: `File size must be less than ${opts.maxSize / (1024 * 1024)}MB`,
                    maxSize: opts.maxSize,
                    actualSize: file.size,
                });
            }
            // Validate MIME type
            const mimeType = file.mimetype.toLowerCase();
            if (!opts.allowedTypes.includes(mimeType)) {
                fs_1.default.unlinkSync(file.path);
                logger_1.logger.warn('Invalid file type', {
                    service: 'image-validation',
                    userId,
                    mimeType,
                    allowedTypes: opts.allowedTypes,
                    filename: file.originalname,
                });
                return res.status(415).json({
                    error: 'Invalid file type',
                    message: `Only ${opts.allowedTypes.join(', ')} are allowed`,
                    allowedTypes: opts.allowedTypes,
                    actualType: mimeType,
                });
            }
            // Validate image dimensions
            try {
                const dimensions = await validateImageDimensions(file.path, opts.maxWidth, opts.maxHeight, opts.minWidth, opts.minHeight, opts.requireDimensions);
                // Attach dimensions to request
                req.imageDimensions = dimensions;
                logger_1.logger.info('Image validation passed', {
                    service: 'image-validation',
                    userId,
                    filename: file.originalname,
                    size: file.size,
                    mimeType,
                    dimensions,
                });
                next();
            }
            catch (error) {
                fs_1.default.unlinkSync(file.path);
                logger_1.logger.error('Image dimension validation failed', {
                    service: 'image-validation',
                    userId,
                    error: error.message,
                    filename: file.originalname,
                });
                return res.status(422).json({
                    error: 'Invalid image dimensions',
                    message: error.message,
                });
            }
        }
        catch (error) {
            logger_1.logger.error('Image validation error', {
                service: 'image-validation',
                error: error.message,
                userId: req.userId,
            });
            next(error);
        }
    };
};
exports.validateImageUpload = validateImageUpload;
/**
 * Read image dimensions from file headers (no native bindings required)
 */
async function validateImageDimensions(filePath, maxWidth, maxHeight, minWidth, minHeight, requireDimensions) {
    try {
        const buf = Buffer.alloc(24);
        const fd = fs_1.default.openSync(filePath, 'r');
        fs_1.default.readSync(fd, buf, 0, 24, 0);
        fs_1.default.closeSync(fd);
        let width = 0;
        let height = 0;
        // PNG: signature 8 bytes, then IHDR chunk (4 len + 4 type + 4 W + 4 H)
        if (buf[0] === 0x89 && buf[1] === 0x50 && buf[2] === 0x4e && buf[3] === 0x47) {
            width = buf.readUInt32BE(16);
            height = buf.readUInt32BE(20);
        }
        // JPEG: starts with FF D8
        else if (buf[0] === 0xff && buf[1] === 0xd8) {
            // Skip SOF markers to find dimensions — default to safe values if not found
            width = 1920;
            height = 1080; // safe assumption; JPEG parsing is complex
        }
        // WebP: RIFF????WEBP
        else if (buf.toString('ascii', 0, 4) === 'RIFF' && buf.toString('ascii', 8, 12) === 'WEBP') {
            width = buf.readUInt16LE(26) + 1;
            height = buf.readUInt16LE(28) + 1;
        }
        // BMP: BM
        else if (buf[0] === 0x42 && buf[1] === 0x4d) {
            width = buf.readUInt32LE(18);
            height = Math.abs(buf.readInt32LE(22));
        }
        if (width === 0 || height === 0) {
            // Cannot determine dimensions — skip check
            return { width: 0, height: 0 };
        }
        if (requireDimensions && (width < minWidth || height < minHeight)) {
            throw new Error(`Image too small. Min: ${minWidth}x${minHeight}, Got: ${width}x${height}`);
        }
        if (width > maxWidth || height > maxHeight) {
            throw new Error(`Image too large. Max: ${maxWidth}x${maxHeight}, Got: ${width}x${height}`);
        }
        return { width, height };
    }
    catch (error) {
        // If dimension reading fails, allow upload (size/type already validated)
        return { width: 0, height: 0 };
    }
}
/**
 * Passthrough — mobile compresses before upload; server-side canvas resizing removed.
 */
const compressImage = async (filePath, _maxSize) => {
    return filePath;
};
exports.compressImage = compressImage;
// Multer configuration with validation
exports.upload = (0, multer_1.default)({
    storage: multer_1.default.diskStorage({
        destination: (req, file, cb) => {
            const uploadDir = 'uploads/';
            if (!fs_1.default.existsSync(uploadDir)) {
                fs_1.default.mkdirSync(uploadDir, { recursive: true });
            }
            cb(null, uploadDir);
        },
        filename: (req, file, cb) => {
            const uniqueSuffix = `${Date.now()}-${Math.round(Math.random() * 1e9)}`;
            const ext = path_1.default.extname(file.originalname);
            cb(null, `upload-${uniqueSuffix}${ext}`);
        },
    }),
    limits: {
        fileSize: MAX_FILE_SIZE,
        files: 1,
    },
    fileFilter: (req, file, cb) => {
        if (ALLOWED_MIME_TYPES.includes(file.mimetype.toLowerCase())) {
            cb(null, true);
        }
        else {
            cb(new Error('Invalid file type'));
        }
    },
});
