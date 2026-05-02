@echo off
echo ========================================
echo KropAI - Free AI Setup with Ollama
echo ========================================
echo.

echo Step 1: Checking if Ollama is installed...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Ollama not found!
    echo Please install Ollama from: https://ollama.ai
    echo After installing, run this script again.
    pause
    exit /b 1
)

echo Ollama is installed! Version:
ollama --version
echo.

echo Step 2: Pulling required AI models (this may take a few minutes)...
echo.

echo Pulling llava:13b (Vision model for crop/soil analysis)...
ollama pull llava:13b
if errorlevel 1 (
    echo [WARNING] Failed to pull llava:13b. Trying smaller variant...
    ollama pull llava
)

echo.
echo Pulling phi3:mini (Fast chat model)...
ollama pull phi3:mini
if errorlevel 1 (
    echo [WARNING] Failed to pull phi3:mini. Trying phi3...
    ollama pull phi3
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start Ollama (it runs automatically after install, or run: ollama serve)
echo 2. In another terminal, navigate to backend folder
echo 3. Run: npm run dev
echo 4. Open the mobile app and start scanning!
echo.
echo Models available:
echo   - Vision: llava:13b (or llava)
echo   - Chat: phi3:mini (or phi3)
echo.
pause
