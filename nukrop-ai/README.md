# NuKropAI - Advanced Agri-OS

**A production-grade agricultural intelligence platform** featuring offline-first architecture, AI video analysis, rural voice assistants, and gamified farm management.

## 🚀 Key Features

### 🔬 AI Video Crop Analysis
- **OpenCV Frame Extraction**: Extract frames from 4-second videos
- **Multi-Frame Analysis**: Process up to 6 frames asynchronously
- **HuggingFace Integration**: Disease detection using ViT models
- **Confidence Scoring**: Aggregate results across frames

### 🎙️ Rural Voice Assistant
- **Speech-to-Text**: Native language recognition (English/Telugu)
- **Text-to-Speech**: Voice responses in local languages
- **Farm Memory Context**: Local history injection for personalized advice
- **Offline-First**: Works without internet connectivity

### 📊 Gamified Farm Health Dashboard
- **Real-time Scoring**: Soil, Crop, Water metrics aggregation
- **Visual Feedback**: Color-coded health percentages
- **Offline Storage**: Local data with Hive/NoSQL
- **Achievement System**: Unlock features based on farm health

### 🏗️ Enterprise Architecture
- **FastAPI Backend**: Python async microservices
- **Flutter Frontend**: Riverpod state management
- **Firebase Auth**: Secure user authentication
- **Docker Deployment**: Production-ready containers

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance async Python web framework
- **OpenCV**: Computer vision for video frame analysis
- **HuggingFace**: Pre-trained vision models for disease detection
- **Google Gemini**: Advanced conversational AI
- **Firebase Admin**: Secure authentication
- **Docker**: Containerized deployment

### Frontend
- **Flutter**: Cross-platform mobile development
- **Riverpod**: Reactive state management
- **Hive**: Local NoSQL database for offline storage
- **Speech-to-Text**: Native voice recognition
- **Text-to-Speech**: Voice synthesis
- **Camera**: Video recording capabilities

### Infrastructure
- **Docker Compose**: Multi-service orchestration
- **Railway/Render**: Cloud deployment platforms
- **Firebase**: Authentication and data storage
- **CI/CD**: Automated deployment pipelines

## 📁 Project Structure

```
nukrop-ai/
├── backend/                  # FastAPI Python Backend
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── core/            # Firebase auth, config
│   │   ├── api/             # Route handlers
│   │   ├── services/        # HuggingFace, Gemini services
│   │   └── models/          # Pydantic schemas
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Container configuration
├── frontend/                 # Flutter Mobile App
│   ├── lib/
│   │   ├── main.dart        # App entry point
│   │   ├── core/            # Local sync, themes
│   │   ├── features/        # Dashboard, voice, scanner
│   │   └── shared/          # Reusable components
│   └── pubspec.yaml         # Flutter dependencies
└── docker-compose.yml       # Multi-service orchestration
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd nukrop-ai
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Set environment variables
export FIREBASE_ADMIN_CREDENTIALS='{"type":"service_account",...}'
export HUGGINGFACE_API_KEY='your-hf-token'
export GEMINI_API_KEY='your-gemini-key'

# Run development server
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### 3. Frontend Setup
```bash
cd ../frontend
flutter pub get
flutter run
```

### 4. Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🔐 Environment Configuration

### Backend Environment Variables
```env
FIREBASE_ADMIN_CREDENTIALS={"type":"service_account",...}
HUGGINGFACE_API_KEY=your_huggingface_token
GEMINI_API_KEY=your_google_gemini_key
PORT=8080
```

### Firebase Setup
1. Create Firebase project
2. Enable Authentication
3. Download service account key
4. Add to environment variables

## 📊 API Endpoints

### Video Analysis
```
POST /api/v1/scan/video
- Accepts: MP4 video files (max 4 seconds)
- Returns: Disease analysis with confidence scores
```

### Voice Chat
```
POST /api/v1/chat/rural
- Accepts: Text message + farm history + language
- Returns: AI-powered agricultural advice
```

### Health Check
```
GET /health
- Returns: Service status and version info
```

## 🎨 UI/UX Features

### Farm Health Dashboard
- **Real-time Metrics**: Visual health scoring (0-100%)
- **Color Coding**: Green (80%+), Orange (60-79%), Red (<60%)
- **Component Breakdown**: Soil, Crop, Water sub-scores
- **Gamification**: Achievement-based feature unlocks

### Voice Companion
- **Long-press Activation**: Hold mic button to start listening
- **Visual Feedback**: Lottie animations during speech processing
- **Local Language Support**: English and Telugu recognition
- **Offline Capability**: Works without internet

### Video Scanner
- **4-Second Capture**: Optimized for mobile processing
- **Frame Extraction**: OpenCV processes 6 frames per video
- **Real-time Feedback**: Upload progress and analysis status
- **Results Display**: Disease identification with treatment plans

## 🔧 Development Features

### Offline-First Architecture
- **Hive Database**: Local NoSQL storage for all user data
- **Sync Engine**: Background upload when connectivity available
- **Zero Dependency**: App works without internet
- **Data Persistence**: Farm history and analytics stored locally

### AI Integration
- **Multi-Model Support**: HuggingFace ViT + Google Gemini
- **Async Processing**: Concurrent frame analysis
- **Confidence Routing**: Automatic fallback between models
- **Context Awareness**: Farm history injection into AI prompts

### Performance Optimizations
- **Lazy Loading**: Models loaded on-demand
- **Caching**: Response caching for repeated queries
- **Compression**: Image/video compression before upload
- **Background Processing**: Non-blocking AI operations

## 🚀 Production Deployment

### Railway/Render Deployment
```yaml
# railway.toml or render.yaml
services:
  - name: nukrop-ai-backend
    source: ./backend
    runtime: python3
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Firebase Configuration
```javascript
// Firebase Security Rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

## 📈 Business ROI

### Cost Savings
- **Database Costs**: 99% reduction via local Hive storage
- **API Limits**: Smart caching and offline-first design
- **Bandwidth**: Compressed uploads and local processing

### User Acquisition
- **Voice Interface**: Bridges literacy gap in rural areas
- **Offline Capability**: Works in low-connectivity regions
- **Gamification**: Increases user engagement and retention

### Technical Advantages
- **Scalability**: Async FastAPI handles high concurrent loads
- **Reliability**: Circuit breakers and retry logic
- **Maintainability**: Clean architecture with Riverpod

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **HuggingFace**: Pre-trained vision models
- **Google**: Gemini AI and Firebase
- **Flutter**: Cross-platform framework
- **FastAPI**: Python web framework

## 📞 Support

For support, email support@nukropai.com or join our Discord community.

---

**Built with ❤️ for farmers worldwide** 🌾🤖