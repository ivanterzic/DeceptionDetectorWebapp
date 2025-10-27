@echo off
echo ========================================
echo   Downloading Base Models for Training
echo ========================================
echo.

echo This script will download and cache base models used for fine-tuning.
echo This prevents repeated downloads during training and speeds up the process.
echo.

cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing requirements for model caching...
pip install torch transformers huggingface_hub

echo.
echo Initializing base model cache and downloading recommended models...
echo This may take several minutes depending on your internet connection.
echo.

python -c "from base_model_cache import init_base_models_cache, download_all_recommended_models; init_base_models_cache(); download_all_recommended_models()"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   Base Model Setup Complete!
    echo ========================================
    echo.
    echo All recommended base models have been downloaded and cached.
    echo Training will now use these local models instead of downloading each time.
    echo.
    echo You can manage the model cache using:
    echo   python manage_base_models.py status
    echo   python manage_base_models.py download --all
    echo.
) else (
    echo.
    echo ========================================
    echo   Setup Warning
    echo ========================================
    echo.
    echo Some base models may not have downloaded successfully.
    echo You can retry later with: python manage_base_models.py download --all
    echo Training will still work but may download models on-demand.
    echo.
)

cd ..
pause