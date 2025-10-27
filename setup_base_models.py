#!/usr/bin/env python3
"""
Setup Base Models
Cross-platform script to initialize and download base models for training.
"""

import sys
import os
from pathlib import Path

def setup_base_models():
    """Set up base models for training."""
    print("=" * 50)
    print("   Setting Up Base Models for Training")
    print("=" * 50)
    print()
    
    print("This script will download and cache base models used for fine-tuning.")
    print("This prevents repeated downloads during training and speeds up the process.")
    print()
    
    try:
        # Import required modules
        print("Importing required libraries...")
        
        # Change to backend directory if not already there
        backend_dir = Path(__file__).parent / 'backend'
        if backend_dir.exists():
            os.chdir(backend_dir)
        
        from base_model_cache import init_base_models_cache, download_all_recommended_models, get_cache_statistics
        
        print("✓ Libraries imported successfully")
        print()
        
        # Initialize cache
        print("Initializing base model cache...")
        init_base_models_cache()
        
        # Check current status
        stats = get_cache_statistics()
        print(f"Current status: {stats['recommended_cached']}/{stats['recommended_total']} recommended models cached")
        
        if stats['recommended_cached'] < stats['recommended_total']:
            print()
            print("Downloading missing recommended models...")
            print("This may take several minutes depending on your internet connection.")
            print()
            
            results = download_all_recommended_models()
            
            success_count = sum(1 for success, _ in results.values() if success)
            total_count = len(results)
            
            print()
            print("=" * 50)
            print(f"Download Summary: {success_count}/{total_count} successful")
            print("=" * 50)
            
            for model_name, (success, message) in results.items():
                status = "✅" if success else "❌"
                print(f"  {status} {model_name}")
                if not success:
                    print(f"      Error: {message}")
            
            print()
            
            if success_count == total_count:
                print("🎉 All base models downloaded successfully!")
                print("Training will now use these local models instead of downloading each time.")
            else:
                print("⚠️ Some models failed to download.")
                print("Training will still work but may download models on-demand.")
        else:
            print("✅ All recommended models are already cached!")
        
        print()
        final_stats = get_cache_statistics()
        total_size_gb = final_stats['total_size_mb'] / 1024
        print(f"Cache summary: {final_stats['total_models']} models, {total_size_gb:.2f} GB total")
        
        print()
        print("🔧 You can manage the model cache using:")
        print("  python manage_base_models.py status")
        print("  python manage_base_models.py download --all")
        print("  python manage_base_models.py list")
        
    except ImportError as e:
        print(f"❌ Missing required libraries: {str(e)}")
        print()
        print("Please ensure you have the required packages installed:")
        print("  pip install torch transformers huggingface_hub")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        print()
        print("Please check your internet connection and try again.")
        print("You can also run this script later with:")
        print("  python setup_base_models.py")
        sys.exit(1)


if __name__ == "__main__":
    setup_base_models()