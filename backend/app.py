from flask import Flask
from flask_cors import CORS
import torch
import time
from config import API_HOST, API_PORT, DEBUG_MODE, AVAILABLE_MODELS
from routes import register_routes
from ai_utils import preload_model
from model_utils import get_model_path
import base_model_init  # Initialize base model cache on startup


def preload_explainers():
    """Preload LIME and SHAP explainers for all models."""
    print("🧠 Starting Explainer Preloading")
    start_time = time.time()
    
    from ai_utils import _model_cache
    from lime.lime_text import LimeTextExplainer
    import shap
    from transformers import pipeline
    from config import CLASS_NAMES
    
    device = 0 if torch.cuda.is_available() else -1
    print(f"🎮 Explainers will use: {'GPU' if device >= 0 else 'CPU'}")
    
    for model_key in AVAILABLE_MODELS.keys():
        try:
            model_start = time.time()
            model_path = get_model_path(model_key)
            print(f"🔧 Preloading explainers for: {model_key}")
            
            # Preload LIME explainer (just initialize it once, it's model-agnostic)
            lime_key = f"{model_key}_lime"
            if lime_key not in _model_cache:
                lime_explainer = LimeTextExplainer(class_names=CLASS_NAMES)
                _model_cache[lime_key] = lime_explainer
                print(f"✅ LIME explainer cached: {lime_key}")
            
            # Preload probability pipeline for LIME/SHAP
            prob_key = f"{model_key}_probs"
            if prob_key not in _model_cache:
                # Check GPU memory before loading probability pipeline
                if device >= 0:
                    try:
                        memory_free = (torch.cuda.get_device_properties(0).total_memory - 
                                      torch.cuda.memory_allocated()) / 1024**3
                        if memory_free < 1.5:
                            print(f"⚠️ Low GPU memory ({memory_free:.1f} GB), using CPU for prob pipeline")
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
                
                # Log memory after probability pipeline
                if device >= 0 and torch.cuda.is_available():
                    memory_used = torch.cuda.memory_allocated() / 1024**3
                    print(f"🎮 GPU memory after prob pipeline: {memory_used:.2f} GB")
            
            # Preload SHAP explainer
            shap_key = f"{model_key}_shap"
            if shap_key not in _model_cache:
                shap_start = time.time()
                
                shap_explainer = shap.Explainer(_model_cache[prob_key])
                shap_end = time.time()
                _model_cache[shap_key] = shap_explainer
                print(f"✅ SHAP explainer cached: {shap_key} ({shap_end - shap_start:.2f}s)")
                
                # Log memory after SHAP explainer
                if device >= 0 and torch.cuda.is_available():
                    memory_used = torch.cuda.memory_allocated() / 1024**3
                    print(f"🎮 GPU memory after SHAP: {memory_used:.2f} GB")
            
            model_end = time.time()
            print(f"⚡ Explainer preload for {model_key}: {model_end - model_start:.2f}s")
            
        except Exception as e:
            print(f"❌ Failed to preload explainers for {model_key}: {str(e)}")
    
    end_time = time.time()
    print(f"🎉 Explainer preloading completed in {end_time - start_time:.2f}s ({len(AVAILABLE_MODELS)} models)")


def preload_all_models():
    """Preload all available models at startup for faster inference."""
    print("🤖 Starting Model Preloading")
    start_time = time.time()
    
    device = 0 if torch.cuda.is_available() else -1
    print(f"🎮 Models will use: {'GPU' if device >= 0 else 'CPU'}")
    
    # Log GPU info if available
    if torch.cuda.is_available():
        gpu_count = torch.cuda.device_count()
        print(f"🎮 Found {gpu_count} GPU(s)")
        for i in range(gpu_count):
            gpu_name = torch.cuda.get_device_name(i)
            gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1024**3
            print(f"   GPU {i}: {gpu_name} ({gpu_memory:.1f} GB)")
    else:
        print("💻 No GPU available, using CPU")
    
    successful_models = 0
    for model_key in AVAILABLE_MODELS.keys():
        try:
            model_start = time.time()
            model_path = get_model_path(model_key)
            print(f"📦 Loading model: {model_key}")
            
            preload_model(model_key, model_path, True)
            
            model_end = time.time()
            print(f"⚡ Model {model_key} loaded in {model_end - model_start:.2f}s")
            successful_models += 1
            
        except Exception as e:
            print(f"❌ Failed to preload model {model_key}: {str(e)}")
    
    end_time = time.time()
    print(f"🎉 Model preloading completed in {end_time - start_time:.2f}s ({successful_models}/{len(AVAILABLE_MODELS)} models)")
    
    # Also preload explainers
    preload_explainers()


def create_app():
    app = Flask(__name__)
    
    # CORS configuration - restrict to localhost in development
    # For production, update ALLOWED_ORIGINS in config.py
    from config import ALLOWED_ORIGINS
    CORS(app, resources={
        r"/api/*": {
            "origins": ALLOWED_ORIGINS,
            "methods": ["GET", "POST"],
            "allow_headers": ["Content-Type"],
            "max_age": 3600
        }
    })
    
    # Security headers
    @app.after_request
    def add_security_headers(response):
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        # Prevent MIME sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        # XSS protection (legacy but still useful)
        response.headers['X-XSS-Protection'] = '1; mode=block'
        # Referrer policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        # Content Security Policy
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response
    
    register_routes(app)    
    return app


def main():
    print("🚀 Starting Deception Detector API")
    
    # Preload all models before starting the server
    preload_all_models()
    
    # Start cleanup service for custom models
    from cleanup_service import cleanup_service
    cleanup_service.start()
    
    app = create_app()
    print(f"🌐 Server ready to start on http://{API_HOST}:{API_PORT}")
    
    app.run(debug=DEBUG_MODE, host=API_HOST, port=API_PORT)


if __name__ == '__main__':
    main()
