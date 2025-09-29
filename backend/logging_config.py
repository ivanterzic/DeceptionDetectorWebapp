import logging
import sys
import torch
from datetime import datetime
from pathlib import Path

def setup_logging():
    """Setup comprehensive logging for the application."""
    
    # Create logs directory
    logs_dir = Path(__file__).parent / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / 'app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    return logger

def log_gpu_info(logger):
    """Log detailed GPU information."""
    logger.info("=== GPU Information ===")
    
    if torch.cuda.is_available():
        gpu_count = torch.cuda.device_count()
        logger.info(f"CUDA available: True")
        logger.info(f"GPU count: {gpu_count}")
        
        for i in range(gpu_count):
            gpu_name = torch.cuda.get_device_name(i)
            gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1024**3
            logger.info(f"GPU {i}: {gpu_name} ({gpu_memory:.1f} GB)")
            
        current_device = torch.cuda.current_device()
        logger.info(f"Current GPU device: {current_device}")
        
        # Log memory usage
        if torch.cuda.is_available():
            memory_allocated = torch.cuda.memory_allocated() / 1024**3
            memory_cached = torch.cuda.memory_reserved() / 1024**3
            memory_total = torch.cuda.get_device_properties(0).total_memory / 1024**3
            logger.info(f"GPU Memory - Allocated: {memory_allocated:.2f} GB, Cached: {memory_cached:.2f} GB, Total: {memory_total:.2f} GB")
    else:
        logger.warning("CUDA not available - models will run on CPU")
        
    logger.info("========================")

def log_performance_metrics(logger, operation, start_time, end_time, additional_info=None):
    """Log performance metrics for operations."""
    duration = end_time - start_time
    logger.info(f"Performance - {operation}: {duration:.3f}s" + (f" ({additional_info})" if additional_info else ""))
    
    # Log GPU memory after operation if available
    if torch.cuda.is_available():
        memory_allocated = torch.cuda.memory_allocated() / 1024**3
        memory_cached = torch.cuda.memory_reserved() / 1024**3
        logger.info(f"GPU Memory after {operation} - Allocated: {memory_allocated:.2f} GB, Cached: {memory_cached:.2f} GB")

def log_model_info(logger, model_key, model_path, device):
    """Log model loading information."""
    logger.info(f"Loading model: {model_key}")
    logger.info(f"Model path: {model_path}")
    logger.info(f"Target device: {device}")
    
def log_error_with_context(logger, error, context):
    """Log errors with additional context."""
    logger.error(f"Error in {context}: {str(error)}")
    logger.error(f"Error type: {type(error).__name__}")
    import traceback
    logger.error(f"Traceback: {traceback.format_exc()}")