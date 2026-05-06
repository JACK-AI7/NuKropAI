/**
 * Firebase JWT Verification Middleware
 * Replaces X-API-Key with Firebase user token verification
 */

import { Request, Response, NextFunction } from 'express';
import * as admin from 'firebase-admin';
import { logger } from '../utils/logger';

// Initialize Firebase Admin if not already initialized
if (!admin.apps.length) {
  const serviceAccount = process.env.FIREBASE_SERVICE_ACCOUNT;
  if (serviceAccount) {
    admin.initializeApp({
      credential: admin.credential.cert(JSON.parse(serviceAccount)),
    });
  } else {
    // Fallback to default credentials
    admin.initializeApp();
  }
}

export const firebaseAuth = async (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ 
      error: 'No token provided',
      message: 'Authorization header with Bearer token is required'
    });
  }

  const token = authHeader.split(' ')[1];

  try {
    // Verify Firebase ID token
    const decodedToken = await admin.auth().verifyIdToken(token);
    
    // Attach user info to request
    (req as any).user = {
      uid: decodedToken.uid,
      email: decodedToken.email,
      email_verified: decodedToken.email_verified,
      name: decodedToken.name,
      picture: decodedToken.picture,
      firebase: decodedToken.firebase,
    };

    // Also set userId for backward compatibility
    (req as any).userId = decodedToken.uid;

    logger.info('Firebase token verified', {
      service: 'auth',
      uid: decodedToken.uid,
      email: decodedToken.email,
      path: req.path,
    });

    next();
  } catch (error: any) {
    logger.error('Firebase token verification failed', {
      service: 'auth',
      error: error.message,
      path: req.path,
      code: error.code,
    });

    return res.status(401).json({ 
      error: 'Invalid token',
      message: 'The provided authentication token is invalid or expired'
    });
  }
};

/**
 * Optional Firebase auth (for public endpoints that can use user context)
 */
export const optionalFirebaseAuth = async (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers.authorization;

  if (authHeader && authHeader.startsWith('Bearer ')) {
    const token = authHeader.split(' ')[1];
    
    try {
      const decodedToken = await admin.auth().verifyIdToken(token);
      
      (req as any).user = {
        uid: decodedToken.uid,
        email: decodedToken.email,
      };
      (req as any).userId = decodedToken.uid;
    } catch (error) {
      // Token is invalid but optional, continue without user context
      logger.warn('Optional Firebase token invalid', {
        service: 'auth',
        error: (error as Error).message,
      });
    }
  }

  next();
};
