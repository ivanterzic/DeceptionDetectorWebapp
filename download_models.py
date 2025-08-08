import sys
from pathlib import Path

def download_models():
    """Download all required models to local directory."""
    
    print("=" * 50)
    print("   Downloading Deception Detection Models")
    print("=" * 50)
    print()
    
    print("This script will download the required Hugging Face models to local storage.")
    print("This may take several minutes depending on your internet connection.")
    print()
    
    # Create models directory in backend folder
    models_dir = Path("backend") / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Models will be saved to: {models_dir.absolute()}")
    print()
    
    # Read models from models.txt
    models_file = Path("models.txt")
    if not models_file.exists():
        print(f"✗ Error: {models_file} not found")
        print("Please ensure models.txt exists in the project root with model names.")
        sys.exit(1)
    
    with open(models_file, 'r') as f:
        model_lines = [line.strip() for line in f.readlines() if line.strip()]
    
    if not model_lines:
        print("✗ Error: No models found in models.txt")
        sys.exit(1)
    
    # Parse models and create local names
    models = []
    for model_name in model_lines:
        # Extract local name from model path
        # Remove 'neurips-user/' and 'neurips-' prefixes, keep the descriptive part
        local_name = model_name.replace('neurips-user/', '').replace('neurips-', '')
        models.append((model_name, local_name))
    
    print(f"Found {len(models)} models to download:")
    for _, local_name in models:
        print(f"  - {local_name}")
    print()
    
    try:
        # Import required libraries
        print("Importing required libraries...")
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        print("✓ Libraries imported successfully")
        print()
        
        # Download each model
        for i, (model_name, local_name) in enumerate(models, 1):
            print(f"[{i}/{len(models)}] Downloading {local_name}: {model_name}")
            
            local_model_path = models_dir / local_name
            
            # Check if model already exists
            if local_model_path.exists() and any(local_model_path.iterdir()):
                print(f"  - Model already exists at {local_model_path}")
                print(f"  ✓ {local_name} is ready")
                print()
                continue
            
            try:
                # Create directory for this model
                local_model_path.mkdir(exist_ok=True)
                
                # Download tokenizer
                print(f"  - Downloading tokenizer to {local_model_path}...")
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                tokenizer.save_pretrained(local_model_path)
                
                # Download model
                print(f"  - Downloading model to {local_model_path}...")
                model = AutoModelForSequenceClassification.from_pretrained(model_name)
                model.save_pretrained(local_model_path)
                
                print(f"  ✓ {local_name} downloaded successfully to {local_model_path}")
                print()
                
            except Exception as e:
                print(f"  ✗ Failed to download {local_name}: {str(e)}")
                print(f"    You may need to check your internet connection or try again later.")
                print()
                # Clean up partial download
                if local_model_path.exists():
                    import shutil
                    shutil.rmtree(local_model_path, ignore_errors=True)
                continue
        
        print("=" * 50)
        print("   Model Download Complete!")
        print("=" * 50)
        print()
        print("All models have been downloaded to the local models directory.")
        print(f"Models location: {models_dir.absolute()}")
        print("The app will now use these local models instead of downloading from the internet.")
        
    except ImportError as e:
        print(f"✗ Missing required libraries: {str(e)}")
        print("Please install the required packages:")
        print("  pip install torch transformers huggingface_hub")
        sys.exit(1)
        
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    download_models()
