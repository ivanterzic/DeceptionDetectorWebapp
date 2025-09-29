import numpy as np
import torch
import time
from transformers import pipeline
from typing import List, Tuple
from lime.lime_text import LimeTextExplainer
import shap
from config import CLASS_NAMES
from ai_utils import get_pred_probs


def get_lime_explanation(model_key: str, text: str, label_mapping=None) -> List[Tuple[str, float]]:
    """
    Generate LIME explanation for text classification.
    
    Args:
        model_key: Key for the preloaded model
        text: Text to explain
        label_mapping: Optional mapping for label names
        
    Returns:
        List[Tuple[str, float]]: List of (word, importance_score) tuples
    """
    start_time = time.time()
    print(f"🔍 Starting LIME explanation for model: {model_key}")
    print(f"📝 Text length: {len(text)} characters")
    
    try:
        from ai_utils import _model_cache
        
        # Try to get preloaded LIME explainer, fallback to creating new one
        lime_key = f"{model_key}_lime"
        if lime_key in _model_cache:
            explainer = _model_cache[lime_key]
            print(f"✅ Using cached LIME explainer: {lime_key}")
        else:
            print(f"🔧 Creating new LIME explainer for {model_key}")
            explainer = LimeTextExplainer(class_names=CLASS_NAMES)
        
        def predict_fn(texts):
            return get_pred_probs(model_key, texts, label_mapping)
        
        explanation_start = time.time()
        exp = explainer.explain_instance(
            text,
            classifier_fn=predict_fn,
            num_features=10,
            num_samples=500  # Increased for better stability
        )
        explanation_end = time.time()
        
        result = [(str(word), weight) for word, weight in exp.as_list()]
        
        end_time = time.time()
        total_time = end_time - start_time
        explanation_time = explanation_end - explanation_start
        print(f"⚡ LIME explanation completed in {total_time:.2f}s (explanation: {explanation_time:.2f}s, features: {len(result)})")
        
        # Log GPU memory if available
        if torch.cuda.is_available():
            memory_used = torch.cuda.memory_allocated() / 1024**3
            #print(f"🎮 GPU memory after LIME: {memory_used:.2f} GB")
        
        return result
        
    except Exception as e:
        print(f"❌ LIME explanation error for {model_key}: {str(e)}")
        return []


def format_shap_exp(words: List[str], weights: List[float], top_n: int = 10) -> List[Tuple[str, float]]:
    """
    Format SHAP explanation results.
    
    Args:
        words: List of words
        weights: List of importance weights
        top_n: Number of top features to return
        
    Returns:
        List[Tuple[str, float]]: Formatted word-weight pairs
    """
    words = [word.strip() for word in words]
    word_weight_pairs = sorted(zip(words, weights), key=lambda x: abs(x[1]), reverse=True)
    return [(str(word), float(weight)) for word, weight in word_weight_pairs[:top_n]]


def get_shap_explanation(model_key: str, text: str) -> List[Tuple[str, float]]:
    """
    Generate SHAP explanation for text classification.
    
    Args:
        model_key: Key for the preloaded model
        text: Text to explain
        
    Returns:
        List[Tuple[str, float]]: List of (word, importance_score) tuples
    """
    start_time = time.time()
    print(f"📊 Starting SHAP explanation for model: {model_key}")
    print(f"📝 Text length: {len(text)} characters")
    
    try:
        from ai_utils import _model_cache
        
        # Get preloaded SHAP explainer
        shap_key = f"{model_key}_shap"
        if shap_key in _model_cache:
            explainer = _model_cache[shap_key]
            print(f"✅ Using cached SHAP explainer: {shap_key}")
        else:
            # Fallback: create explainer on demand
            print(f"🔧 Creating SHAP explainer on demand for {model_key}")
            from model_utils import get_model_path
            model_path = get_model_path(model_key)
            device = 0 if torch.cuda.is_available() else -1
            
            # Check GPU memory before creating explainer
            if device >= 0:
                try:
                    memory_free = (torch.cuda.get_device_properties(0).total_memory - 
                                  torch.cuda.memory_allocated()) / 1024**3
                    if memory_free < 1.0:
                        print(f"⚠️ Low GPU memory ({memory_free:.1f} GB), using CPU for SHAP explainer")
                        device = -1
                except:
                    device = -1
            
            classifier = pipeline(
                "text-classification", 
                model=model_path, 
                top_k=None, 
                device=device
            )
            explainer = shap.Explainer(classifier)
            _model_cache[shap_key] = explainer
            print(f"✅ SHAP explainer cached: {shap_key}")
        
        explanation_start = time.time()
        shap_output = explainer([text])
        explanation_end = time.time()
        
        words = shap_output.data[0]
        weights = shap_output.values[0][:, 1]
        
        result = format_shap_exp(words, weights, top_n=10)
        
        end_time = time.time()
        total_time = end_time - start_time
        explanation_time = explanation_end - explanation_start
        print(f"⚡ SHAP explanation completed in {total_time:.2f}s (explanation: {explanation_time:.2f}s, features: {len(result)})")
        
        # Log GPU memory if available
        if torch.cuda.is_available():
            memory_used = torch.cuda.memory_allocated() / 1024**3
            #print(f"🎮 GPU memory after SHAP: {memory_used:.2f} GB")
        
        return result
    except Exception as e:
        print(f"❌ SHAP explanation error for {model_key}: {str(e)}")
        return []