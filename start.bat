@echo off
REM CryptoTracker Quick Start Script for Windows
REM This script sets up and runs CryptoTracker

echo.
echo ========================================
echo   CryptoTracker - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

echo [OK] Python 3 found
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -q -r requirements.txt
echo [OK] Dependencies installed
echo.

REM Check if .env exists
if not exist ".env" (
    echo [INFO] Creating .env file from template...
    copy .env.example .env
    echo.
    echo [WARNING] Please edit .env and add your API keys before running the application
    echo           You can get a free Etherscan API key at: https://etherscan.io/apis
    echo.
    pause
)

REM Create necessary directories
if not exist "data" mkdir data
if not exist "static" mkdir static
if not exist "templates" mkdir templates

echo.
echo ========================================
echo   Starting CryptoTracker...
echo ========================================
echo.
echo [INFO] Application will be available at: http://localhost:5000
echo [INFO] Documentation: README.md
echo [INFO] Press Ctrl+C to stop the application
echo.

REM Run the application
python app.py