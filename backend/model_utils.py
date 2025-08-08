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
    local_path = AVAILABLE_MODELS.get(model_key)
    
    if not local_path:
        raise ValueError(f"Model {model_key} not configured in AVAILABLE_MODELS")
    
    # Check if local model exists
    if local_path.exists() and any(local_path.iterdir()):
        print(f"Using local model: {local_path}")
        return str(local_path)
    
    raise ValueError(f"Model {model_key} not found locally at {local_path}. Please download the model first.")
