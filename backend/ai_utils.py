import numpy as np
import torch
from transformers import pipeline
from typing import List, Dict, Any
from config import CLASS_NAMES


def hf_pretrained_classify(model_path: str, texts: str | List[str], label_mapping=None) -> List[Dict[str, Any]]:
    """
    Classify text using a pre-trained model (local or HuggingFace).
    
    Args:
        model_path: Path to the model (local path or HuggingFace model name)
        texts: Text or list of texts to classify
        label_mapping: Optional mapping for label names
        
    Returns:
        List[Dict[str, Any]]: Classification results
    """
    classifier = pipeline(
        "text-classification", 
        model=model_path, 
        device=0 if torch.cuda.is_available() else -1
    )
    results = classifier(texts)
    
    if isinstance(results, dict):
        results = [results]
    
    if label_mapping:
        results = [
            {'label': label_mapping.get(res['label'], res['label']), 'score': res['score']} 
            for res in results
        ]
    return results


def get_pred_probs(model_path: str, texts: str | List[str], label_mapping=None) -> np.ndarray:
    """
    Get prediction probabilities for texts.
    
    Args:
        model_path: Path to the model
        texts: Text or list of texts to analyze
        label_mapping: Optional mapping for label names
        
    Returns:
        np.ndarray: Probability array for each class
    """
    classifier = pipeline(
        "text-classification", 
        model=model_path, 
        top_k=None, 
        device=0 if torch.cuda.is_available() else -1
    )
    results = classifier(texts)
    
    # Handle single text input
    if isinstance(texts, str):
        results = [results]
    
    probs = []
    for res in results:
        # Create probability array in the order of class_names
        prob_dict = {}
        for item in res:
            label = label_mapping.get(item['label'], item['label']) if label_mapping else item['label']
            prob_dict[label] = item['score']
        
        # Ensure we have probabilities for both classes
        prob_array = []
        for cls in CLASS_NAMES:
            prob_array.append(prob_dict.get(cls, 0.0))
        
        probs.append(prob_array)
    return np.array(probs)
