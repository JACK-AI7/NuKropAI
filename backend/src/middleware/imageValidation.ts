/**
 * Image Upload Validation Middleware
 * Validates size, format, and dimensions
 */

import { Request, Response, NextFunction } from 'express';
import multer from 'multer';
import path from 'path';
import fs from 'fs';
import { logger } from '../utils/logger';
import { createCanvas, loadImage } from 'canvas';

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
 * Validate image dimensions
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
    const image = await loadImage(filePath);
    const { width, height } = image;

    if (requireDimensions && (width < minWidth || height < minHeight)) {
      throw new Error(
        `Image dimensions too small. Minimum: ${minWidth}x${minHeight}, Actual: ${width}x${height}`
      );
    }

    if (width > maxWidth || height > maxHeight) {
      throw new Error(
        `Image dimensions too large. Maximum: ${maxWidth}x${maxHeight}, Actual: ${width}x${height}`
      );
    }

    return { width, height };
  } catch (error) {
    throw new Error(`Failed to read image dimensions: ${(error as Error).message}`);
  }
}

/**
 * Compress image if needed
 */
export const compressImage = async (
  filePath: string,
  maxSize: number = 2 * 1024 * 1024 // 2MB default
): Promise<string> => {
  try {
    const image = await loadImage(filePath);
    const { width, height } = image;

    // If already small enough, return original
    const stats = fs.statSync(filePath);
    if (stats.size <= maxSize) {
      return filePath;
    }

    // Calculate new dimensions (maintain aspect ratio)
    let newWidth = width;
    let newHeight = height;
    const aspectRatio = width / height;

    if (width > height) {
      newWidth = 1024;
      newHeight = Math.round(1024 / aspectRatio);
    } else {
      newHeight = 1024;
      newWidth = Math.round(1024 * aspectRatio);
    }

    // Create compressed version
    const canvas = createCanvas(newWidth, newHeight);
    const ctx = canvas.getContext('2d');
    ctx.drawImage(image, 0, 0, newWidth, newHeight);

    // Save as JPEG with quality
    const buffer = canvas.toBuffer('image/jpeg', { quality: 0.8 });
    const compressedPath = filePath.replace(/\.[^/.]+$/, '-compressed.jpg');
    fs.writeFileSync(compressedPath, buffer);

    // Remove original if compressed is smaller
    const compressedStats = fs.statSync(compressedPath);
    if (compressedStats.size < stats.size) {
      fs.unlinkSync(filePath);
      return compressedPath;
    }

    fs.unlinkSync(compressedPath);
    return filePath;
  } catch (error) {
    logger.error('Image compression failed', {
      service: 'image-compression',
      error: (error as Error).message,
      filePath,
    });
    return filePath;
  }
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
