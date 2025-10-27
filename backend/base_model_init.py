"""
Base Model Auto-Initialization
Automatically initializes base model cache on backend startup.
"""

import logging
from pathlib import Path
from base_model_cache import init_base_models_cache, get_cache_statistics

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def auto_init_base_models():
    """
    Automatically initialize base model cache on startup.
    This ensures the cache structure exists even if models aren't downloaded yet.
    """
    try:
        # Initialize cache structure
        init_base_models_cache()
        
        # Get current status
        stats = get_cache_statistics()
        
        logger.info(f"Base model cache initialized: {stats['total_models']} models cached")
        
        if stats['recommended_cached'] < stats['recommended_total']:
            logger.info(f"Only {stats['recommended_cached']}/{stats['recommended_total']} recommended models cached")
            logger.info("Run 'python setup_base_models.py' to download missing models")
            logger.info("Training will download models on-demand if not cached")
        else:
            logger.info("All recommended base models are cached ✅")
        
        return True
        
    except Exception as e:
        logger.warning(f"Failed to initialize base model cache: {str(e)}")
        logger.info("Base model caching will be disabled - models will download on-demand")
        return False


# Auto-initialize on import (when backend starts)
if __name__ != "__main__":
    auto_init_base_models()