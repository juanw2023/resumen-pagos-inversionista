@echo off
REM Setup script for Facebook Marketplace Scraper (Windows)

echo ========================================
echo Facebook Marketplace Scraper - Setup
echo ========================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing Python dependencies...
pip install -r requirements.txt

REM Install Playwright browsers
echo.
echo Installing Playwright browsers...
playwright install chromium

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo .env file created
    echo.
    echo WARNING: Edit .env file and add your credentials:
    echo    - FACEBOOK_EMAIL
    echo    - FACEBOOK_PASSWORD
    echo    - GOOGLE_API_KEY
    echo.
) else (
    echo.
    echo .env file already exists
)

REM Run tests
echo.
echo Running setup tests...
python test_setup.py

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your credentials
echo 2. Run: venv\Scripts\activate.bat
echo 3. Run: python marketplace_scraper.py
echo.
pause
