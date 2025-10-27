"""
Base Model Cache Management
Handles downloading and caching of base models for training to avoid repeated downloads.
"""

import os
import json
import time
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from huggingface_hub import HfApi, model_info


# Base models directory
BASE_MODELS_DIR = Path(__file__).parent / 'base_models'
CACHE_INFO_FILE = BASE_MODELS_DIR / 'cache_info.json'

# Supported base models for fine-tuning
SUPPORTED_BASE_MODELS = {
    'bert-base-uncased': {
        'name': 'BERT Base (Uncased)',
        'description': 'General-purpose BERT model, good for most text classification tasks',
        'size_mb': 440,
        'recommended': True
    },
    'microsoft/deberta-v3-base': {
        'name': 'DeBERTa v3 Base',
        'description': 'Enhanced BERT with disentangled attention, often performs better than BERT',
        'size_mb': 390,
        'recommended': True
    },
    'albert-base-v2': {
        'name': 'ALBERT Base v2',
        'description': 'Lightweight alternative to BERT, faster training with similar performance',
        'size_mb': 47,
        'recommended': True
    },
    'roberta-base': {
        'name': 'RoBERTa Base',
        'description': 'Robustly optimized BERT, often performs well on text classification',
        'size_mb': 500,
        'recommended': True
    },
    'distilbert-base-uncased': {
        'name': 'DistilBERT Base',
        'description': 'Distilled BERT, 40% smaller and 60% faster while retaining 95% performance',
        'size_mb': 255,
        'recommended': True
    }
}


def init_base_models_cache():
    """Initialize the base models cache directory and info file."""
    BASE_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    if not CACHE_INFO_FILE.exists():
        cache_info = {
            'created_at': time.time(),
            'last_updated': time.time(),
            'cached_models': {},
            'total_size_mb': 0
        }
        save_cache_info(cache_info)
        print(f"✅ Initialized base models cache at: {BASE_MODELS_DIR}")


def load_cache_info() -> Dict:
    """Load cache information from the info file."""
    if not CACHE_INFO_FILE.exists():
        init_base_models_cache()
        return load_cache_info()
    
    try:
        with open(CACHE_INFO_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("⚠️ Cache info file corrupted, reinitializing...")
        init_base_models_cache()
        return load_cache_info()


def save_cache_info(cache_info: Dict):
    """Save cache information to the info file."""
    cache_info['last_updated'] = time.time()
    with open(CACHE_INFO_FILE, 'w') as f:
        json.dump(cache_info, f, indent=2)


def get_model_cache_path(model_name: str) -> Path:
    """Get the local cache path for a model."""
    # Clean model name for directory (replace "/" with "_")
    clean_name = model_name.replace("/", "_").replace("\\", "_")
    return BASE_MODELS_DIR / clean_name


def is_model_cached(model_name: str) -> bool:
    """Check if a model is already cached locally."""
    model_path = get_model_cache_path(model_name)
    if not model_path.exists():
        return False
    
    # Check if both tokenizer and model files exist
    required_files = ['config.json', 'tokenizer_config.json']
    model_files = ['pytorch_model.bin', 'model.safetensors']
    
    has_config = all((model_path / file).exists() for file in required_files)
    has_model = any((model_path / file).exists() for file in model_files)
    
    return has_config and has_model


def get_model_size_mb(model_path: Path) -> float:
    """Calculate the total size of a cached model in MB."""
    if not model_path.exists():
        return 0.0
    
    total_size = 0
    for file_path in model_path.rglob('*'):
        if file_path.is_file():
            total_size += file_path.stat().st_size
    
    return total_size / (1024 * 1024)  # Convert to MB


def download_base_model(model_name: str, force_redownload: bool = False) -> Tuple[bool, str]:
    """
    Download and cache a base model locally.
    
    Args:
        model_name: HuggingFace model name (e.g., 'bert-base-uncased')
        force_redownload: Whether to redownload even if already cached
        
    Returns:
        Tuple[bool, str]: (success, message)
    """
    model_path = get_model_cache_path(model_name)
    
    # Check if already cached
    if not force_redownload and is_model_cached(model_name):
        return True, f"Model {model_name} already cached at {model_path}"
    
    print(f"📥 Downloading base model: {model_name}")
    print(f"Cache location: {model_path}")
    
    try:
        # Create model directory
        model_path.mkdir(parents=True, exist_ok=True)
        
        # Clear existing files if force redownload
        if force_redownload and model_path.exists():
            shutil.rmtree(model_path)
            model_path.mkdir(parents=True, exist_ok=True)
        
        start_time = time.time()
        
        # Download tokenizer
        print(f"  📝 Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(model_path)
        
        # Download model
        print(f"  🤖 Downloading model...")
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=2,  # For binary classification
            id2label={0: "deceptive", 1: "truthful"},
            label2id={"deceptive": 0, "truthful": 1}
        )
        model.save_pretrained(model_path)
        
        end_time = time.time()
        
        # Update cache info
        cache_info = load_cache_info()
        model_size = get_model_size_mb(model_path)
        
        cache_info['cached_models'][model_name] = {
            'cached_at': time.time(),
            'model_path': str(model_path),
            'size_mb': model_size,
            'download_time_seconds': end_time - start_time,
            'version': 'latest'
        }
        
        # Recalculate total size
        cache_info['total_size_mb'] = sum(
            info['size_mb'] for info in cache_info['cached_models'].values()
        )
        
        save_cache_info(cache_info)
        
        print(f"  ✅ Downloaded {model_name} in {end_time - start_time:.2f}s ({model_size:.1f} MB)")
        return True, f"Successfully cached {model_name}"
        
    except Exception as e:
        # Clean up partial download
        if model_path.exists():
            shutil.rmtree(model_path, ignore_errors=True)
        
        error_msg = f"Failed to download {model_name}: {str(e)}"
        print(f"  ❌ {error_msg}")
        return False, error_msg


def download_all_recommended_models() -> Dict[str, Tuple[bool, str]]:
    """Download all recommended base models for training."""
    print("📦 Downloading all recommended base models...")
    print("This may take several minutes depending on your internet connection.\n")
    
    results = {}
    recommended_models = [
        model_name for model_name, info in SUPPORTED_BASE_MODELS.items() 
        if info.get('recommended', False)
    ]
    
    for i, model_name in enumerate(recommended_models, 1):
        print(f"[{i}/{len(recommended_models)}] Processing {model_name}...")
        results[model_name] = download_base_model(model_name)
        print()
    
    return results


def get_cached_model_path(model_name: str) -> Optional[str]:
    """
    Get the local path for a cached model, or None if not cached.
    
    Args:
        model_name: HuggingFace model name
        
    Returns:
        Optional[str]: Local path to cached model, or None if not cached
    """
    if not is_model_cached(model_name):
        return None
    
    return str(get_model_cache_path(model_name))


def list_cached_models() -> List[Dict]:
    """List all cached models with their information."""
    cache_info = load_cache_info()
    cached_models = []
    
    for model_name, info in cache_info.get('cached_models', {}).items():
        model_info = {
            'model_name': model_name,
            'size_mb': info.get('size_mb', 0),
            'cached_at': info.get('cached_at', 0),
            'download_time': info.get('download_time_seconds', 0),
            'path': info.get('model_path', ''),
            'is_recommended': SUPPORTED_BASE_MODELS.get(model_name, {}).get('recommended', False),
            'description': SUPPORTED_BASE_MODELS.get(model_name, {}).get('description', 'Custom model')
        }
        cached_models.append(model_info)
    
    return sorted(cached_models, key=lambda x: x['cached_at'], reverse=True)


def cleanup_model_cache(model_name: str) -> bool:
    """Remove a specific model from cache."""
    model_path = get_model_cache_path(model_name)
    
    try:
        if model_path.exists():
            shutil.rmtree(model_path)
        
        # Update cache info
        cache_info = load_cache_info()
        if model_name in cache_info.get('cached_models', {}):
            del cache_info['cached_models'][model_name]
            
            # Recalculate total size
            cache_info['total_size_mb'] = sum(
                info['size_mb'] for info in cache_info['cached_models'].values()
            )
            
            save_cache_info(cache_info)
        
        print(f"✅ Removed {model_name} from cache")
        return True
        
    except Exception as e:
        print(f"❌ Failed to remove {model_name}: {str(e)}")
        return False


def get_cache_statistics() -> Dict:
    """Get statistics about the model cache."""
    cache_info = load_cache_info()
    cached_models = cache_info.get('cached_models', {})
    
    stats = {
        'total_models': len(cached_models),
        'total_size_mb': cache_info.get('total_size_mb', 0),
        'total_size_gb': cache_info.get('total_size_mb', 0) / 1024,
        'cache_created': cache_info.get('created_at', 0),
        'last_updated': cache_info.get('last_updated', 0),
        'recommended_cached': sum(
            1 for model_name in cached_models 
            if SUPPORTED_BASE_MODELS.get(model_name, {}).get('recommended', False)
        ),
        'recommended_total': sum(
            1 for info in SUPPORTED_BASE_MODELS.values() 
            if info.get('recommended', False)
        )
    }
    
    return stats


def validate_cache() -> List[str]:
    """Validate the integrity of cached models and return any issues."""
    issues = []
    cache_info = load_cache_info()
    
    for model_name, info in cache_info.get('cached_models', {}).items():
        model_path = Path(info.get('model_path', ''))
        
        if not model_path.exists():
            issues.append(f"Missing directory for {model_name}: {model_path}")
            continue
        
        if not is_model_cached(model_name):
            issues.append(f"Incomplete model files for {model_name}")
            continue
    
    return issues


if __name__ == "__main__":
    # Initialize cache and download recommended models
    init_base_models_cache()
    
    print("Base Model Cache Management")
    print("=" * 50)
    
    stats = get_cache_statistics()
    print(f"Cached models: {stats['total_models']}")
    print(f"Total size: {stats['total_size_gb']:.2f} GB")
    print(f"Recommended models cached: {stats['recommended_cached']}/{stats['recommended_total']}")
    print()
    
    if stats['recommended_cached'] < stats['recommended_total']:
        print("Downloading missing recommended models...")
        download_all_recommended_models()
    else:
        print("All recommended models are already cached! ✅")