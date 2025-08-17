from flask import request, jsonify
import traceback
from transformers import AutoTokenizer
from config import AVAILABLE_MODELS, LABEL_MAPPING
from model_utils import get_model_path
from ai_utils import hf_pretrained_classify
from explanations import get_lime_explanation, get_shap_explanation

def check_text_length(text, model_path, max_tokens=512):
    """
    Check if text will exceed the model's token limit
    
    Args:
        text: Input text to check
        model_path: Path to the model (for tokenizer)
        max_tokens: Maximum tokens allowed (default 512 for BERT)
        
    Returns:
        tuple: (is_valid, token_count, error_message)
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        tokens = tokenizer.encode(text, truncation=False, add_special_tokens=True)
        token_count = len(tokens)
        
        if token_count > max_tokens:
            return False, token_count, f"Text contains {token_count} tokens, but model limit is {max_tokens}. Please reduce text length."
        
        return True, token_count, None
        
    except Exception as e:
        # Fallback to character count if tokenizer fails
        if len(text) > 2000:
            return False, -1, "Text is too long. Please limit to 2000 characters."
        return True, -1, None


def register_routes(app):
    """Register all API routes with the Flask app."""
    
    @app.route('/api/models', methods=['GET'])
    def get_models():
        """Get available models."""
        return jsonify(list(AVAILABLE_MODELS.keys()))

    @app.route('/api/predict', methods=['POST'])
    def predict():
        """Predict deception for given text using specified model."""
        try:
            data = request.get_json()
            text = data.get('text', '').strip()
            model_key = data.get('model', '')
            
            if not text:
                return jsonify({'error': 'Text is required'}), 400
            
            if not model_key or model_key not in AVAILABLE_MODELS:
                return jsonify({'error': 'Invalid model'}), 400
            
            model_path = get_model_path(model_key)
            
            # Check if text will exceed token limits before processing
            is_valid, token_count, error_msg = check_text_length(text, model_path)
            if not is_valid:
                return jsonify({'error': error_msg}), 400
            
            results = hf_pretrained_classify(model_path, text, LABEL_MAPPING)
            prediction = results[0]
            
            # Generate explanations
            try:
                lime_explanation = get_lime_explanation(model_path, text, LABEL_MAPPING)
            except Exception as e:
                print(f"LIME explanation failed: {e}")
                lime_explanation = []
            
            try:
                shap_explanation = get_shap_explanation(model_path, text)
            except Exception as e:
                print(f"SHAP explanation failed: {e}")
                shap_explanation = []
            
            response = {
                'prediction': prediction['label'],
                'confidence': prediction['score'],
                'original_text': text,
                'explanations': {
                    'lime': lime_explanation,
                    'shap': shap_explanation
                },
                'model_used': model_key
            }
            
            return jsonify(response)
            
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'error': f'Prediction failed: {str(e)}'}), 500
