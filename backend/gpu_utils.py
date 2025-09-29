import torch
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def get_optimal_device() -> int:
    """
    Get the optimal device for model inference.
    
    Returns:
        int: Device ID (0+ for GPU, -1 for CPU)
    """
    if torch.cuda.is_available():
        device_count = torch.cuda.device_count()
        
        if device_count == 1:
            return 0
        
        # If multiple GPUs, select the one with most free memory
        max_free_memory = 0
        best_device = 0
        
        for i in range(device_count):
            torch.cuda.set_device(i)
            free_memory = torch.cuda.get_device_properties(i).total_memory - torch.cuda.memory_allocated(i)
            
            if free_memory > max_free_memory:
                max_free_memory = free_memory
                best_device = i
        
        logger.info(f"Selected GPU {best_device} with {max_free_memory / 1024**3:.1f} GB free memory")
        return best_device
    
    logger.info("CUDA not available, using CPU")
    return -1

def monitor_gpu_memory(operation_name: str, device_id: Optional[int] = None) -> None:
    """
    Monitor and log GPU memory usage.
    
    Args:
        operation_name: Name of the operation for logging
        device_id: Specific device to monitor (None for current device)
    """
    if not torch.cuda.is_available():
        return
        
    if device_id is not None:
        current_device = torch.cuda.current_device()
        torch.cuda.set_device(device_id)
    
    try:
        memory_allocated = torch.cuda.memory_allocated() / 1024**3
        memory_reserved = torch.cuda.memory_reserved() / 1024**3
        memory_total = torch.cuda.get_device_properties(torch.cuda.current_device()).total_memory / 1024**3
        memory_free = memory_total - memory_allocated
        
        logger.info(f"GPU Memory [{operation_name}] - "
                   f"Allocated: {memory_allocated:.2f} GB, "
                   f"Reserved: {memory_reserved:.2f} GB, "
                   f"Free: {memory_free:.2f} GB, "
                   f"Total: {memory_total:.2f} GB")
        
        # Warn if memory usage is high
        usage_percent = (memory_allocated / memory_total) * 100
        if usage_percent > 90:
            logger.warning(f"High GPU memory usage: {usage_percent:.1f}%")
        elif usage_percent > 75:
            logger.info(f"GPU memory usage: {usage_percent:.1f}%")
            
    finally:
        if device_id is not None:
            torch.cuda.set_device(current_device)

def clear_gpu_cache() -> None:
    """Clear GPU cache to free up memory."""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        logger.info("GPU cache cleared")

def ensure_gpu_available(min_memory_gb: float = 1.0) -> bool:
    """
    Ensure sufficient GPU memory is available.
    
    Args:
        min_memory_gb: Minimum required memory in GB
        
    Returns:
        bool: True if sufficient memory is available
    """
    if not torch.cuda.is_available():
        logger.warning("GPU not available")
        return False
    
    try:
        memory_free = (torch.cuda.get_device_properties(0).total_memory - 
                      torch.cuda.memory_allocated()) / 1024**3
        
        if memory_free < min_memory_gb:
            logger.warning(f"Insufficient GPU memory: {memory_free:.1f} GB available, "
                          f"{min_memory_gb:.1f} GB required")
            clear_gpu_cache()
            
            # Check again after cache clear
            memory_free = (torch.cuda.get_device_properties(0).total_memory - 
                          torch.cuda.memory_allocated()) / 1024**3
            
            if memory_free < min_memory_gb:
                logger.error(f"Still insufficient memory after cache clear: {memory_free:.1f} GB")
                return False
        
        logger.info(f"Sufficient GPU memory available: {memory_free:.1f} GB")
        return True
        
    except Exception as e:
        logger.error(f"Error checking GPU memory: {e}")
        return False