import numpy as np
import torch
import time
from transformers import pipeline
from typing import List, Dict, Any
from config import CLASS_NAMES

# Global cache for preloaded models
_model_cache = {}
_explainer_cache = {}

# Store the optimal device
_optimal_device = None

def get_device():
    """Get the optimal device for model operations."""
    global _optimal_device
    if _optimal_device is None:
        if torch.cuda.is_available():
            device_count = torch.cuda.device_count()
            print(f"🎮 Found {device_count} GPU(s)")
            _optimal_device = 0  # Use first GPU
        else:
            print("💻 No GPU available, using CPU")
            _optimal_device = -1
    return _optimal_device


def preload_model(model_key: str, model_path: str, print_logs=True) -> None:
    """
    Preload a model into memory for faster inference.
    
    Args:
        model_key: The key to store the model under
        model_path: Path to the model
        print_logs: Whether to print loading information
    """
    if model_key not in _model_cache:
        start_time = time.time()
        device = get_device()
        
        if print_logs:
            print(f"🤖 Loading model {model_key} to {'GPU' if device >= 0 else 'CPU'}")
        
        # Check GPU memory before loading if using GPU
        if device >= 0:
            try:
                memory_free = (torch.cuda.get_device_properties(0).total_memory - 
                              torch.cuda.memory_allocated()) / 1024**3
                if memory_free < 2.0:
                    print(f"⚠️ Low GPU memory ({memory_free:.1f} GB), using CPU for {model_key}")
                    device = -1
            except:
                device = -1
        
        classifier = pipeline(
            "text-classification", 
            model=model_path, 
            device=device
        )
        _model_cache[model_key] = classifier
        
        # Log GPU memory after loading
        if device >= 0 and torch.cuda.is_available():
            memory_used = torch.cuda.memory_allocated() / 1024**3
            if print_logs:
                print(f"🎮 GPU memory after loading {model_key}: {memory_used:.2f} GB")
        
        end_time = time.time()
        if print_logs:
            print(f"✅ Model {model_key} loaded in {end_time - start_time:.2f}s on {'GPU' if device >= 0 else 'CPU'}")


def get_cached_model(model_key: str) -> pipeline:
    """
    Get a cached model or raise an error if not found.
    
    Args:
        model_key: The key for the cached model
        
    Returns:
        pipeline: The cached model pipeline
        
    Raises:
        ValueError: If model is not preloaded
    """
    if model_key not in _model_cache:
        # Load on demand if not preloaded
        from model_utils import get_model_path
        model_path = get_model_path(model_key)
        preload_model(model_key, model_path, True)
    return _model_cache[model_key]


def hf_pretrained_classify(model_key: str, texts: str | List[str], label_mapping=None) -> List[Dict[str, Any]]:
    """
    Classify text using a preloaded model.
    
    Args:
        model_key: Key for the preloaded model
        texts: Text or list of texts to classify
        label_mapping: Optional mapping for label names
        
    Returns:
        List[Dict[str, Any]]: Classification results
    """
    start_time = time.time()
    print(f"🔮 Starting prediction with model: {model_key}")
    
    try:
        classifier = get_cached_model(model_key)
        results = classifier(texts)
        
        end_time = time.time()
        text_length = len(texts) if isinstance(texts, str) else sum(len(t) for t in texts)
        print(f"⚡ Prediction completed in {end_time - start_time:.3f}s (text length: {text_length})")
        
        # Log GPU memory usage after prediction
        if torch.cuda.is_available():
            memory_used = torch.cuda.memory_allocated() / 1024**3
            print(f"🎮 GPU memory after prediction: {memory_used:.2f} GB")
            
    except Exception as e:
        print(f"❌ Prediction error with {model_key}: {str(e)}")
        raise
    
    if isinstance(results, dict):
        results = [results]
    
    if label_mapping:
        results = [
            {'label': label_mapping.get(res['label'], res['label']), 'score': res['score']} 
            for res in results
        ]
    return results


def get_pred_probs(model_key: str, texts: str | List[str], label_mapping=None) -> np.ndarray:
    """
    Get prediction probabilities for texts using preloaded model.
    
    Args:
        model_key: Key for the preloaded model
        texts: Text or list of texts to analyze
        label_mapping: Optional mapping for label names
        
    Returns:
        np.ndarray: Probability array for each class
    """
    start_time = time.time()
    print(f"📊 Getting prediction probabilities with model: {model_key}")
    
    try:
        # For probability prediction, we need a separate pipeline with top_k=None
        # Check if we have a probability version cached
        prob_key = f"{model_key}_probs"
        if prob_key not in _model_cache:
            print(f"🔧 Creating probability pipeline for {model_key}")
            
            # Handle custom models differently
            if model_key.startswith("custom_"):
                # For custom models, use the model from cache directly
                if model_key in _model_cache:
                    # Get the pipeline from cache and create a new top_k=None version
                    cached_pipeline = _model_cache[model_key]
                    device = get_device()
                    
                    # Create a new pipeline with top_k=None using the same model path
                    # We need to get the model path from the custom model directory
                    model_code = model_key.replace("custom_", "")
                    from training_routes import CUSTOM_MODELS_DIR
                    model_path = CUSTOM_MODELS_DIR / model_code / 'model'
                    
                    prob_classifier = pipeline(
                        "text-classification",
                        model=str(model_path),
                        top_k=None,
                        device=device
                    )
                else:
                    raise ValueError(f"Custom model {model_key} not found in cache")
            else:
                # For regular models, use the normal path
                from model_utils import get_model_path
                model_path = get_model_path(model_key)
                device = get_device()
                
                # Check GPU memory
                if device >= 0:
                    try:
                        memory_free = (torch.cuda.get_device_properties(0).total_memory - 
                                      torch.cuda.memory_allocated()) / 1024**3
                        if memory_free < 1.0:
                            print(f"⚠️ Low GPU memory ({memory_free:.1f} GB), using CPU for probability pipeline")
                            device = -1
                    except:
                        device = -1
                
                prob_classifier = pipeline(
                    "text-classification", 
                    model=model_path, 
                    top_k=None, 
                    device=device
                )
                
            _model_cache[prob_key] = prob_classifier
            print(f"✅ Probability pipeline cached: {prob_key}")
        
        classifier = _model_cache[prob_key]
        results = classifier(texts)
        
        end_time = time.time()
        print(f"⚡ Probability prediction completed in {end_time - start_time:.3f}s")
        
    except Exception as e:
        print(f"❌ Probability prediction error with {model_key}: {str(e)}")
        raise
    
    # Handle single text input
    if isinstance(texts, str):
        results = [results]
    
    probs = []
    for res in results:
        # Create probability array in the order of class_names
        prob_dict = {}
        for item in res:
            label = label_mapping.get(item['label'], item['label']) if label_mapping else item['label']
            prob_dict[label] = item['score']
        
        # Ensure we have probabilities for both classes
        prob_array = []
        for cls in CLASS_NAMES:
            prob_array.append(prob_dict.get(cls, 0.0))
        
        probs.append(prob_array)
    return np.array(probs)
