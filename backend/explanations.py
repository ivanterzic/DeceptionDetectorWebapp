import numpy as np
import torch
from transformers import pipeline
from typing import List, Tuple
from lime.lime_text import LimeTextExplainer
import shap
from config import CLASS_NAMES
from ai_utils import get_pred_probs


def get_lime_explanation(model_path: str, text: str, label_mapping=None) -> List[Tuple[str, float]]:
    """
    Generate LIME explanation for text classification.
    
    Args:
        model_path: Path to the model
        text: Text to explain
        label_mapping: Optional mapping for label names
        
    Returns:
        List[Tuple[str, float]]: List of (word, importance_score) tuples
    """
    try:
        explainer = LimeTextExplainer(class_names=CLASS_NAMES)
        
        def predict_fn(texts):
            return get_pred_probs(model_path, texts, label_mapping)
        
        exp = explainer.explain_instance(
            text,
            classifier_fn=predict_fn,
            num_features=10,
            num_samples=500  # Increased for better stability
        )
        
        return [(str(word), weight) for word, weight in exp.as_list()]
        
    except Exception as e:
        print(f"LIME explanation error: {e}")
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


def get_shap_explanation(model_path: str, text: str) -> List[Tuple[str, float]]:
    """
    Generate SHAP explanation for text classification.
    
    Args:
        model_path: Path to the model
        text: Text to explain
        
    Returns:
        List[Tuple[str, float]]: List of (word, importance_score) tuples
    """
    try:
        classifier = pipeline(
            "text-classification", 
            model=model_path, 
            top_k=None, 
            device=0 if torch.cuda.is_available() else -1
        )
        explainer = shap.Explainer(classifier)
        shap_output = explainer([text])
        
        words = shap_output.data[0]
        weights = shap_output.values[0][:, 1]
        
        return format_shap_exp(words, weights, top_n=10)
    except Exception as e:
        print(f"SHAP explanation error: {e}")
        return []