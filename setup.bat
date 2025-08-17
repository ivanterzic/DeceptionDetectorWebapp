@echo off
echo ========================================
echo   Deception Detector App Setup
echo ========================================
echo.

echo [1/4] Setting up Backend...
cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment and installing requirements...
call venv\Scripts\activate && pip install -r requirements.txt

cd ..

echo.
echo [2/4] Setting up Frontend...
cd frontend

if not exist node_modules (
    echo Installing npm dependencies...
    npm install
)

cd ..

echo.
echo [3/4] Downloading Models...
echo This may take several minutes for first-time setup.
echo.
call download-models.bat
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Warning: Model download encountered issues.
    echo You can run 'download-models.bat' later to retry.
    echo The app will still work but may be slower on first prediction because of model downloading.
    echo.
)

echo.
echo [4/4] Setup Complete!
echo.
echo To start the application:
echo 1. Run 'start-backend.bat' in one terminal
echo 2. Run 'start-frontend.bat' in another terminal
echo 3. Open http://localhost:8080 in your browser
echo.
echo Note: Make sure both Python and Node.js are installed on your system.
echo If models fail to download, run 'download-models.bat' separately.
echo.
pause
