@echo off
echo ========================================
echo   Downloading Deception Detection Models
echo ========================================
echo.

echo This script will download the required Hugging Face models.
echo This may take several minutes depending on your internet connection.
echo.

if not exist backend\venv (
    echo Creating virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

echo Activating virtual environment...
call backend\venv\Scripts\activate

echo Installing minimal requirements for model download...
pip install torch transformers huggingface_hub

echo.
echo Downloading models to local directory...
echo.

echo Running Python download script...
python download_models.py

echo.
echo ========================================
echo   Model Download Complete!
echo ========================================
echo.
echo All models have been downloaded and cached locally.
echo.
pause
