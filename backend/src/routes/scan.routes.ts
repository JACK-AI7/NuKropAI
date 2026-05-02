import { Router } from 'express';
import multer from 'multer';
import path from 'path';
import { ScanController } from '../controllers/scan.controller';
import { authMiddleware } from '../middleware/auth.middleware';

const router = Router();

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  },
});

const upload = multer({ storage });

router.post('/', authMiddleware, upload.single('image'), ScanController.createScan);
router.get('/history', authMiddleware, ScanController.getHistory);
router.get('/:id', authMiddleware, ScanController.getScanById);

export default router;
