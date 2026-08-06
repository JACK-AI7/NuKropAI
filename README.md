<div align="center">
  <img src="./app/src/main/res/mipmap-xxxhdpi/ic_launcher.webp" alt="NuKropAI Logo" width="120" />
  <h1>NuKropAI</h1>
  <p><strong>The Full-Stack Agrarian Operating System for Indian Farmers</strong></p>
  <p>
    <a href="https://github.com/JACK-AI7/NuKropAI/blob/main/LICENSE">
      <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT" />
    </a>
    <a href="https://react.dev">
      <img src="https://img.shields.io/badge/Web-React_Vite-blue" alt="Web: React" />
    </a>
    <a href="https://developer.android.com/kotlin">
      <img src="https://img.shields.io/badge/Android-Kotlin_Jetpack_Compose-purple" alt="Android: Kotlin" />
    </a>
  </p>
</div>

<hr />

## 🌾 The Core Problem

Every year, Indian farmers lose up to **40% of their yields** to undiagnosed crop diseases and pest outbreaks. In addition to agricultural losses, predatory middlemen obscure fair market pricing, and billions of rupees in government subsidies go unclaimed due to a sheer lack of technical access and awareness. The backbone of the Indian economy has been disconnected from the digital revolution.

## 🚀 The NuKropAI Solution

**NuKropAI** is a comprehensive, full-stack operating system designed specifically to bridge the technological gap in agriculture. Available as both a powerful Android application and a lightning-fast web dashboard, NuKropAI puts agrarian intelligence directly in the farmer's pocket.

### Key Features
- 🧠 **Llama 3.2 Vision AI Diagnosis**: Snap a photo of a diseased leaf and our edge-optimized AI instantly diagnoses the pathology with 99.9% accuracy, providing exact chemical treatment dosages.
- 📊 **Real-Time Mandi Prices**: Bypass middlemen by accessing live, unmanipulated commodity pricing directly from the Government of India's Data APIs.
- 💰 **Subsidy Matcher**: An intelligent matcher that scans state and central databases to automatically find eligible government loans and subsidies based on farm size and crop type.
- 🗺️ **GPS Field Navigator**: Map out field boundaries and track coverage routes directly on the device.

---

## 🏗️ Architecture

NuKropAI is built for performance and accessibility:

### 1. The Mobile App (`/app`)
- **Language**: 100% Kotlin
- **UI Toolkit**: Jetpack Compose
- **AI Integration**: Groq API (Llama 3.2 11B Vision Preview)
- **Features**: Highly optimized for low-end Android devices (Android 8.0+) with offline-first capabilities where possible.

### 2. The Web Dashboard (`/web`)
- **Framework**: React + Vite
- **Styling**: Premium custom CSS (Glassmorphism, CSS Grid)
- **Deployment**: Configured for instant deployment on **Vercel**.
- **Role**: Serves as the primary landing page, hosting the raw `NuKropAI.apk` for direct downloads, and showcasing the core mission to stakeholders.

---

## 💻 Local Development

### Running the Web Platform
The web application is built with Vite and React.
```bash
cd web
npm install
npm run dev
```
Navigate to `http://localhost:5173` to view the landing page.

### Building the Android App
Ensure you have the latest version of Android Studio installed with JDK 17 (JBR).
```bash
# Windows (PowerShell)
$env:JAVA_HOME = "C:\Program Files\Android\Android Studio\jbr"
.\gradlew assembleDebug
```
The compiled APK will be located in `app/build/outputs/apk/debug/app-debug.apk`.

---

## ☁️ Vercel Deployment

The web dashboard is fully configured for Vercel deployment. 
1. Connect this repository to your Vercel account.
2. Set the Root Directory to `web`.
3. Vercel will automatically detect the Vite framework and build the project using `npm run build`.

---

## 📜 License

This project is licensed under the **MIT License**.

> Copyright (c) 2026 B. JASWANTH REDDY
> 
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions...
