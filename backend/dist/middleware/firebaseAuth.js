"use strict";
/**
 * Firebase JWT Verification Middleware
 * Replaces X-API-Key with Firebase user token verification
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.optionalFirebaseAuth = exports.firebaseAuth = void 0;
const admin = __importStar(require("firebase-admin"));
const logger_1 = require("../utils/logger");
// Initialize Firebase Admin if not already initialized
if (!admin.apps.length) {
    const serviceAccount = process.env.FIREBASE_SERVICE_ACCOUNT;
    if (serviceAccount) {
        admin.initializeApp({
            credential: admin.credential.cert(JSON.parse(serviceAccount)),
        });
    }
    else {
        // Fallback to default credentials
        admin.initializeApp();
    }
}
const firebaseAuth = async (req, res, next) => {
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
        req.user = {
            uid: decodedToken.uid,
            email: decodedToken.email,
            email_verified: decodedToken.email_verified,
            name: decodedToken.name,
            picture: decodedToken.picture,
            firebase: decodedToken.firebase,
        };
        // Also set userId for backward compatibility
        req.userId = decodedToken.uid;
        logger_1.logger.info('Firebase token verified', {
            service: 'auth',
            uid: decodedToken.uid,
            email: decodedToken.email,
            path: req.path,
        });
        next();
    }
    catch (error) {
        logger_1.logger.error('Firebase token verification failed', {
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
exports.firebaseAuth = firebaseAuth;
/**
 * Optional Firebase auth (for public endpoints that can use user context)
 */
const optionalFirebaseAuth = async (req, res, next) => {
    const authHeader = req.headers.authorization;
    if (authHeader && authHeader.startsWith('Bearer ')) {
        const token = authHeader.split(' ')[1];
        try {
            const decodedToken = await admin.auth().verifyIdToken(token);
            req.user = {
                uid: decodedToken.uid,
                email: decodedToken.email,
            };
            req.userId = decodedToken.uid;
        }
        catch (error) {
            // Token is invalid but optional, continue without user context
            logger_1.logger.warn('Optional Firebase token invalid', {
                service: 'auth',
                error: error.message,
            });
        }
    }
    next();
};
exports.optionalFirebaseAuth = optionalFirebaseAuth;
