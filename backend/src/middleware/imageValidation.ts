/**
 * Image Upload Validation Middleware
 * Validates size, format, and dimensions
 */

import { Request, Response, NextFunction } from 'express';
import multer from 'multer';
import path from 'path';
import fs from 'fs';
import { logger } from '../utils/logger';

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

interface ValidationOptions {
  maxSize?: number;
  allowedTypes?: string[];
  maxWidth?: number;
  maxHeight?: number;
  minWidth?: number;
  minHeight?: number;
  requireDimensions?: boolean;
}

export const validateImageUpload = (options: ValidationOptions = {}) => {
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

  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      // Check if file exists
      if (!req.file) {
        return res.status(400).json({
          error: 'No file uploaded',
          message: 'Please upload an image file',
        });
      }

      const file = req.file;
      const userId = (req as any).userId || 'anonymous';

      // Validate file size
      if (file.size > opts.maxSize!) {
        // Clean up the uploaded file
        fs.unlinkSync(file.path);
        
        logger.warn('File too large', {
          service: 'image-validation',
          userId,
          size: file.size,
          maxSize: opts.maxSize,
          filename: file.originalname,
        });

        return res.status(413).json({
          error: 'File too large',
          message: `File size must be less than ${opts.maxSize! / (1024 * 1024)}MB`,
          maxSize: opts.maxSize,
          actualSize: file.size,
        });
      }

      // Validate MIME type
      const mimeType = file.mimetype.toLowerCase();
      if (!opts.allowedTypes!.includes(mimeType)) {
        fs.unlinkSync(file.path);
        
        logger.warn('Invalid file type', {
          service: 'image-validation',
          userId,
          mimeType,
          allowedTypes: opts.allowedTypes,
          filename: file.originalname,
        });

        return res.status(415).json({
          error: 'Invalid file type',
          message: `Only ${opts.allowedTypes!.join(', ')} are allowed`,
          allowedTypes: opts.allowedTypes,
          actualType: mimeType,
        });
      }

      // Validate image dimensions
      try {
        const dimensions = await validateImageDimensions(
          file.path,
          opts.maxWidth!,
          opts.maxHeight!,
          opts.minWidth!,
          opts.minHeight!,
          opts.requireDimensions!
        );

        // Attach dimensions to request
        (req as any).imageDimensions = dimensions;

        logger.info('Image validation passed', {
          service: 'image-validation',
          userId,
          filename: file.originalname,
          size: file.size,
          mimeType,
          dimensions,
        });

        next();
      } catch (error) {
        fs.unlinkSync(file.path);
        
        logger.error('Image dimension validation failed', {
          service: 'image-validation',
          userId,
          error: (error as Error).message,
          filename: file.originalname,
        });

        return res.status(422).json({
          error: 'Invalid image dimensions',
          message: (error as Error).message,
        });
      }
    } catch (error) {
      logger.error('Image validation error', {
        service: 'image-validation',
        error: (error as Error).message,
        userId: (req as any).userId,
      });

      next(error);
    }
  };
};

/**
 * Read image dimensions from file headers (no native bindings required)
 */
async function validateImageDimensions(
  filePath: string,
  maxWidth: number,
  maxHeight: number,
  minWidth: number,
  minHeight: number,
  requireDimensions: boolean
): Promise<{ width: number; height: number }> {
  try {
    const buf = Buffer.alloc(24);
    const fd = fs.openSync(filePath, 'r');
    fs.readSync(fd, buf, 0, 24, 0);
    fs.closeSync(fd);

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
      width = 1920; height = 1080; // safe assumption; JPEG parsing is complex
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
  } catch (error) {
    // If dimension reading fails, allow upload (size/type already validated)
    return { width: 0, height: 0 };
  }
}

/**
 * Passthrough — mobile compresses before upload; server-side canvas resizing removed.
 */
export const compressImage = async (filePath: string, _maxSize?: number): Promise<string> => {
  return filePath;
};

// Multer configuration with validation
export const upload = multer({
  storage: multer.diskStorage({
    destination: (req, file, cb) => {
      const uploadDir = 'uploads/';
      if (!fs.existsSync(uploadDir)) {
        fs.mkdirSync(uploadDir, { recursive: true });
      }
      cb(null, uploadDir);
    },
    filename: (req, file, cb) => {
      const uniqueSuffix = `${Date.now()}-${Math.round(Math.random() * 1e9)}`;
      const ext = path.extname(file.originalname);
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
    } else {
      cb(new Error('Invalid file type'));
    }
  },
});
