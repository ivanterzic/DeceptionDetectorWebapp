from config import AVAILABLE_MODELS


def get_model_path(model_key: str) -> str:
    """
    Get the path to a local model in the backend folder.
    
    Args:
        model_key: The key identifying the model (e.g., 'covid', 'climate', 'combined')
        
    Returns:
        str: Path to the local model
        
    Raises:
        ValueError: If model is not found locally
    """
    model_entry = AVAILABLE_MODELS.get(model_key)
    
    if not model_entry:
        raise ValueError(f"Model {model_key} not configured in AVAILABLE_MODELS")

    # Support both legacy Path values and dict entries
    if isinstance(model_entry, dict):
        local_path = model_entry.get('path')
        hf_id = model_entry.get('hf_id')
    else:
        local_path = model_entry
        hf_id = None
    
    # Check if local model exists
    if local_path and local_path.exists() and any(local_path.iterdir()):
        print(f"Using local model: {local_path}")
        return str(local_path)

    # Fall back to HF model id if available (downloads on demand)
    if hf_id:
        print(f"Using HF model id for on-demand download: {hf_id}")
        return hf_id
    
    raise ValueError(f"Model {model_key} not found locally at {local_path}. Please download the model first.")
