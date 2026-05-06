# 🚀 NuKropAI Production Deployment Guide

## Zero-Error Deployment for Advanced Agri-OS

This guide ensures bulletproof deployment of the Flutter + FastAPI + Firebase architecture.

---

## 📋 Prerequisites

### 1. Firebase Project Setup
```bash
# Create Firebase project: "nukrop-ai-production"
# Enable Authentication (Google + Phone)
# Create Firestore Database (asia-south1 region)
# Download service account key (JSON file)
```

### 2. API Keys Required
- **HuggingFace API Key**: https://huggingface.co/settings/tokens
- **Google Gemini API Key**: https://aistudio.google.com/app/apikey

### 3. Development Environment
```bash
# Flutter SDK (latest stable)
flutter --version

# Python 3.10+
python --version

# Docker (optional)
docker --version
```

---

## 🔐 PHASE 1: Firebase Configuration

### Step 1: Deploy Security Rules

**Firestore Rules** (`firebase/firestore.rules`):
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    function isAuth() {
      return request.auth != null;
    }

    // Community map is public read, but writing needs auth
    match /community_disease_map/{docId} {
      allow read: if isAuth();
      allow write: if false; // Only backend creates these
    }

    match /users/{userId} {
      allow read, write: if isAuth() && request.auth.uid == userId;
    }

    match /{document=**} {
      allow read, write: if false; // Deny everything else!
    }
  }
}
```

**Storage Rules** (`firebase/storage.rules`):
```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /{allPaths=**} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.uid == resource.metadata.ownerId;
    }
  }
}
```

### Step 2: Minify Firebase Service Account Key

**CRITICAL**: Convert the JSON file to a single-line string:

```bash
# Open the downloaded JSON file and remove all line breaks
# Result should be one continuous line like:
# {"type":"service_account","project_id":"nukrop-ai-production","private_key_id":"abc123...
```

---

## 📱 PHASE 2: Flutter Frontend Setup

### Step 1: Install FlutterFire CLI
```bash
dart pub global activate flutterfire_cli
firebase login
cd nukrop-ai/frontend
flutterfire configure
```

### Step 2: Environment Configuration
```bash
# Create .env file in frontend/ directory
echo "API_URL=http://10.0.2.2:8080/api/v1" > .env
```

### Step 3: Verify Configuration
```bash
flutter pub get
flutter run --debug  # Test on emulator
```

---

## ⚙️ PHASE 3: FastAPI Backend Deployment

### Railway.app Deployment (Recommended)

#### Step 1: Create Railway Project
```bash
# Push backend code to separate GitHub repo
cd nukrop-ai/backend
git init
git add .
git commit -m "NuKropAI Backend v2.0"
git remote add origin https://github.com/yourusername/nukrop-backend.git
git push -u origin main
```

#### Step 2: Deploy on Railway
1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your `nukrop-backend` repository
4. Wait for build completion

#### Step 3: Configure Environment Variables
In Railway project settings → Variables:

```
HUGGINGFACE_API_KEY=your_huggingface_token_here
GEMINI_API_KEY=your_gemini_api_key_here
FIREBASE_ADMIN_CREDENTIALS={"type":"service_account","project_id":"nukrop-ai-production",...}
PORT=8080
```

#### Step 4: Get Production URL
Railway will provide: `https://nukrop-backend-production.up.railway.app`

---

## 🔄 PHASE 4: Update Flutter for Production

### Step 1: Update Environment Variables
```bash
# Update frontend/.env
API_URL=https://nukrop-backend-production.up.railway.app/api/v1
```

### Step 2: Build Production APK
```bash
cd nukrop-ai/frontend
flutter clean
flutter pub get
flutter build apk --release
```

### Step 3: Install and Test
```bash
# Copy APK to device
adb install build/app/outputs/flutter-apk/app-release.apk

# Or use Android File Transfer
# Test authentication and API calls
```

---

## 🐳 Alternative: Docker Deployment

### Docker Compose Setup
```yaml
# docker-compose.yml
version: '3.8'

services:
  nukrop-backend:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      - FIREBASE_ADMIN_CREDENTIALS=${FIREBASE_ADMIN_CREDENTIALS}
      - HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    restart: always
```

### Environment File
```bash
# .env file for docker-compose
FIREBASE_ADMIN_CREDENTIALS='{"type":"service_account",...}'
HUGGINGFACE_API_KEY=your_huggingface_token
GEMINI_API_KEY=your_gemini_api_key
```

### Deploy with Docker
```bash
docker-compose up --build -d
```

---

## 🧪 Testing Deployment

### Health Check
```bash
curl https://your-railway-url/health
# Should return: {"status": "Online", "mode": "Agronomy AI Active", "firebase": true}
```

### Authentication Test
```bash
# Test with Firebase token
curl -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
  https://your-railway-url/api/v1/health
```

### Video Analysis Test
```bash
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@test_video.mp4" \
  https://your-railway-url/api/v1/scan/video
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Firebase Initialization Error
**Error**: "Failed to boot backend security"
**Fix**: Verify `FIREBASE_ADMIN_CREDENTIALS` is properly minified JSON

#### 2. CORS Blocks in Flutter
**Error**: Network requests failing
**Fix**: Ensure API_URL in `.env` is correct and CORS is configured

#### 3. Model Loading Errors
**Error**: "Ollama model not found"
**Fix**: Check `OLLAMA_HOST` environment variable

#### 4. APK Build Failures
**Error**: Flutter build errors
**Fix**: Run `flutter clean && flutter pub get`

### Debug Commands

```bash
# Check Railway logs
railway logs

# Check Flutter connectivity
flutter doctor

# Test local backend
cd backend && python -m uvicorn app.main:app --reload

# Check Firebase auth
firebase projects:list
```

---

## 📊 Performance Optimization

### Backend Optimization
```python
# Add to main.py
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Connection pooling for external APIs
import httpx
client = httpx.AsyncClient(limits=httpx.Limits(max_keepalive_connections=20))
```

### Frontend Optimization
```dart
// Add to main.dart
import 'package:flutter/foundation.dart';
if (kReleaseMode) {
  // Production optimizations
}
```

---

## 🔒 Security Checklist

- [ ] Firebase service account key properly minified
- [ ] API keys stored as environment variables
- [ ] CORS configured for production domains
- [ ] Authentication required for all protected routes
- [ ] No hardcoded secrets in source code
- [ ] HTTPS enabled in production

---

## 🚀 Production Launch Steps

1. ✅ **Firebase Setup**: Project created, rules deployed
2. ✅ **API Keys**: HuggingFace and Gemini configured
3. ✅ **Backend Deployed**: Railway/Render deployment complete
4. ✅ **Frontend Configured**: Environment variables updated
5. ✅ **APK Built**: Production APK generated
6. ✅ **Testing Complete**: All endpoints verified
7. ✅ **Security Audit**: All credentials properly secured

---

## 🎯 Success Metrics

### Performance Targets
- **API Response Time**: <500ms for text, <3s for video
- **APK Size**: <90MB (universal)
- **Offline Capability**: 100% core functionality
- **Authentication**: Zero failed auth attempts

### User Experience
- **Voice Recognition**: 95% accuracy (English/Telugu)
- **Video Processing**: 6 frames analyzed in <2s
- **Farm Health**: Real-time scoring updates
- **Offline Sync**: Automatic background upload

---

## 📞 Support

**Deployment Issues:**
- Check Railway logs: `railway logs`
- Verify environment variables
- Test API endpoints with curl

**Flutter Issues:**
- Run `flutter doctor`
- Check `.env` configuration
- Test on physical device

**Firebase Issues:**
- Verify service account key format
- Check Firestore security rules
- Test authentication flow

---

## 🎉 Launch Complete!

Your **NuKropAI Advanced Agri-OS** is now production-ready with:

✅ **Zero-Error Firebase Configuration**  
✅ **Bulletproof FastAPI Backend**  
✅ **Production Flutter App**  
✅ **Docker Deployment Ready**  
✅ **Enterprise Security**  
✅ **Offline-First Architecture**  

**Ready to empower Indian farmers with AI! 🌾🤖**

---

*For questions or issues, contact the development team or check the troubleshooting section above.*