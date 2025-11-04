import torch
from pathlib import Path
from gpu_utils import get_torch_device

# Get optimal device using gpu_utils
DEVICE = get_torch_device()

LABEL_MAPPING = {'0': 'deceptive', '1': 'truthful'}
CLASS_NAMES = ['deceptive', 'truthful']

MODELS_DIR = Path(__file__).parent / 'models'
BASE_MODELS_DIR = Path(__file__).parent / 'base_models'

def get_available_models():
    """Dynamically discover available models from the models directory and models.txt"""
    available_models = {}
    
    # First, try to read from models.txt to get the mapping
    models_file = Path(__file__).parent.parent / 'models.txt'
    if models_file.exists():
        with open(models_file, 'r') as f:
            model_lines = [line.strip() for line in f.readlines() if line.strip()]
        
        for model_name in model_lines:
            # Extract local name from model path
            local_name = model_name.replace('neurips-user/', '').replace('neurips-', '')
            model_path = MODELS_DIR / local_name
            available_models[local_name] = model_path
    
    # Also scan the models directory for any existing models
    if MODELS_DIR.exists():
        for model_dir in MODELS_DIR.iterdir():
            if model_dir.is_dir() and any(model_dir.iterdir()):
                local_name = model_dir.name
                if local_name not in available_models:
                    available_models[local_name] = model_dir
    
    return available_models

AVAILABLE_MODELS = get_available_models()

API_HOST = '0.0.0.0'
API_PORT = 5000
DEBUG_MODE = True

# CORS allowed origins - restrict to localhost for development
# For production, change to your domain: ['https://yourdomain.com']
ALLOWED_ORIGINS = [
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'http://localhost:3000',  # Alternative dev port
    'http://127.0.0.1:3000'
]

# Rate limiting settings (requests per minute)
RATE_LIMIT_ANALYSIS = 20  # Text analysis endpoint
RATE_LIMIT_TRAINING = 5   # Model training endpoint
RATE_LIMIT_DEFAULT = 60   # Other endpoints
