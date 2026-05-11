# NuKropAI 🌾🤖

> **Empowering Indian Farmers with Intelligent AI Solutions.**

NuKropAI is a production-grade, AI-powered agricultural platform designed specifically for the Indian farming landscape. It provides instant crop disease diagnosis, expert multilingual advice, and real-time agricultural intelligence to help farmers optimize their yield and protect their crops.

![NuKropAI Banner](https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?auto=format&fit=crop&q=80&w=2000)

## ✨ Core Features

- **📸 AI Crop Scanner**: Instant diagnosis of crop diseases using state-of-the-art computer vision. Get confidence scores, severity assessments, and detailed treatment plans.
- **💬 Multilingual AI Assistant**: Chat with "NuKropAI" in **English, Hindi (हिंदी)**, or **Telugu (తెలుగు)**. Get expert advice on pest management, fertilizers, and government schemes.
- **🎙️ Voice-First Input**: Specifically designed for accessibility; farmers can speak their questions and receive text/audio guidance.
- **⛅ Weather Intelligence**: Real-time hyper-local weather tracking with AI-generated crop recommendations based on upcoming conditions.
- **📊 Agricultural Analytics**: Track farm health over time with visual disease breakdown charts, weekly scan trends, and proactive advisory reports.
- **🛡️ Production Ready**: Hardened for low-connectivity environments with robust offline persistence, request timeouts, and exponential backoff.

## 🛠️ Technology Stack

### Mobile (Expo App)
- **Framework**: Expo SDK 54 / React Native
- **Navigation**: Expo Router (File-based routing)
- **Animations**: React Native Reanimated (Cinematic micro-animations)
- **Styling**: Premium Dark Theme (Custom Forest Green palette)
- **Persistence**: AsyncStorage (Zero-data-loss background syncing)
- **State**: React Context API (Farmer Profile & History)

### Backend (API Server)
- **Runtime**: Node.js / TypeScript
- **Framework**: Express 5
- **AI Engine**: Phi-4 / Qwen (via OpenAI-compatible streaming API)
- **Validation**: Zod (End-to-end type safety)
- **Infrastructure**: Centralized API utility with robust timeout/retry logic

## 🚀 Getting Started

### Prerequisites
- Node.js 20+
- pnpm 9+
- Expo Go (for testing on real devices)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/user/nukropai.git
   cd nukropai
   ```
2. Install dependencies:
   ```bash
   pnpm install
   ```
3. Set up environment variables:
   - Create a `.env` file in `artifacts/mobile` and `artifacts/api-server`.
   - Refer to `.env.example` in both directories.

### Running Locally
1. Start the API Server:
   ```bash
   pnpm --filter @workspace/api-server run dev
   ```
2. Start the Mobile App:
   ```bash
   pnpm --filter @workspace/mobile run dev
   ```

## 📦 Building for Production

NuKropAI uses **EAS (Expo Application Services)** for automated builds.

### 1. Preview APK (Testing)
```bash
cd artifacts/mobile
npx eas-cli build --platform android --profile preview
```

### 2. Production AAB (Play Store)
```bash
cd artifacts/mobile
npx eas-cli build --platform android --profile production
```

## 🏗️ Architecture Overview

NuKropAI follows a modular monorepo architecture:
- `artifacts/mobile`: React Native frontend with complex animation systems and local AI state management.
- `artifacts/api-server`: High-performance Express server handling AI streaming, image processing, and weather data.
- `lib/`: Shared integration libraries and UI components.

## 🤝 Contributing

We welcome contributions to help empower farmers. Please see our [CONTRIBUTING.md](CONTRIBUTING.md) (coming soon) for details.

## 📄 License

NuKropAI is released under the [MIT License](LICENSE).

---
*Built with ❤️ for the future of Indian Agriculture.*
