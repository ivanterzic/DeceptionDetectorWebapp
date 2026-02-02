import torch
from pathlib import Path
from gpu_utils import get_torch_device
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get optimal device using gpu_utils
DEVICE = get_torch_device()

LABEL_MAPPING = {'0': 'deceptive', '1': 'truthful'}
CLASS_NAMES = ['deceptive', 'truthful']

MODELS_DIR = Path(__file__).parent / 'models'
BASE_MODELS_DIR = Path(__file__).parent / 'base_models'

# Default pretrained model list (used when models.txt isn't available)
DEFAULT_MODEL_LIST = [
    'neurips-user/neurips-bert-covid-1',
    'neurips-user/neurips-bert-climate-change-1',
    'neurips-user/neurips-bert-combined-1',
    'neurips-user/neurips-deberta-covid-1',
    'neurips-user/neurips-deberta-climate-change-1',
    'neurips-user/neurips-deberta-combined-1',
]

def get_available_models():
    """Dynamically discover available models from the models directory and models.txt"""
    available_models = {}
    
    # First, try to read from models.txt to get the mapping
    models_file_candidates = [
        Path(__file__).parent / 'models.txt',
        Path(__file__).parent.parent / 'models.txt',
    ]
    models_file = next((p for p in models_file_candidates if p.exists()), None)
    if models_file:
        with open(models_file, 'r') as f:
            model_lines = [line.strip() for line in f.readlines() if line.strip()]
    else:
        model_lines = DEFAULT_MODEL_LIST

    for model_name in model_lines:
        # Extract local name from model path
        local_name = model_name.replace('neurips-user/', '').replace('neurips-', '')
        model_path = MODELS_DIR / local_name
        available_models[local_name] = {
            'path': model_path,
            'hf_id': model_name,
        }
    
    # Also scan the models directory for any existing models
    if MODELS_DIR.exists():
        for model_dir in MODELS_DIR.iterdir():
            if model_dir.is_dir() and any(model_dir.iterdir()):
                local_name = model_dir.name
                if local_name not in available_models:
                    available_models[local_name] = {
                        'path': model_dir,
                        'hf_id': None,
                    }
                else:
                    available_models[local_name]['path'] = model_dir
    
    return available_models

AVAILABLE_MODELS = get_available_models()

API_HOST = '0.0.0.0'
API_PORT = 5000
DEBUG_MODE = True

# CORS allowed origins - restrict to localhost for development
# For production, change to your domain: ['https://yourdomain.com']
ALLOWED_ORIGINS = [
    'http://localhost',       # Nginx default port
    'http://localhost:80',    # Nginx explicit
    'http://localhost:8080',  # Frontend direct
    'http://127.0.0.1',
    'http://127.0.0.1:80',
    'http://127.0.0.1:8080',
    'http://localhost:3000',  # Alternative dev port
    'http://127.0.0.1:3000'
]

# Rate limiting settings (requests per minute)
RATE_LIMIT_ANALYSIS = 30  # Text analysis endpoint
RATE_LIMIT_TRAINING = 30   # Model training endpoint
RATE_LIMIT_DEFAULT = 120   # Other endpoints

# JWT / Public API settings (development defaults; override with env vars)
JWT_SECRET = os.environ.get('JWT_SECRET', 'dev_jwt_secret_change_me')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
JWT_EXP_SECONDS = int(os.environ.get('JWT_EXP_SECONDS', 3600))

# API user credentials
# REQUIRED: Must be set via environment variables - no defaults for security
# Password is stored in plain text here, but client must hash it before sending
API_USERNAME = os.environ.get('API_USERNAME')
API_PASSWORD = os.environ.get('API_PASSWORD')  # Plain text password (for comparison)

# Validate credentials are configured
if not API_USERNAME or not API_PASSWORD:
    import warnings
    warnings.warn(
        "⚠️  API_USERNAME and API_PASSWORD environment variables not set!\n"
        "   Public API will not work. Set them in backend/.env file",
        RuntimeWarning
    )
