from flask import request, jsonify
import traceback
import time
from transformers import AutoTokenizer
from config import AVAILABLE_MODELS, LABEL_MAPPING
from model_utils import get_model_path
from ai_utils import hf_pretrained_classify
from explanations import get_lime_explanation, get_shap_explanation

def check_text_length(text, model_key, max_tokens=512):
    """
    Check if text will exceed the model's token limit
    
    Args:
        text: Input text to check
        model_key: Key for the model (for tokenizer)
        max_tokens: Maximum tokens allowed (default 512 for BERT)
        
    Returns:
        tuple: (is_valid, token_count, error_message)
    """
    try:
        model_path = get_model_path(model_key)
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
        start_time = time.time()
        try:
            data = request.get_json()
            text = data.get('text', '').strip()
            model_key = data.get('model', '')
            
            print(f"📨 Prediction request - Model: {model_key}, Text length: {len(text)}")
            
            if not text:
                print("⚠️ Prediction request failed: No text provided")
                return jsonify({'error': 'Text is required'}), 400
            
            if not model_key or model_key not in AVAILABLE_MODELS:
                print(f"⚠️ Prediction request failed: Invalid model '{model_key}'")
                return jsonify({'error': 'Invalid model'}), 400
            
            # Check if text will exceed token limits before processing
            is_valid, token_count, error_msg = check_text_length(text, model_key)
            print(f"📊 Token count check: {token_count} tokens, Valid: {is_valid}")
            if not is_valid:
                print(f"⚠️ Text too long: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            results = hf_pretrained_classify(model_key, text, LABEL_MAPPING)
            prediction = results[0]
            
            response = {
                'prediction': prediction['label'],
                'confidence': prediction['score'],
                'original_text': text,
                'model_used': model_key
            }
            
            end_time = time.time()
            print(f"✅ API prediction completed in {end_time - start_time:.3f}s - Model: {model_key}, Result: {prediction['label']}, Confidence: {prediction['score']:.3f}")
            
            return jsonify(response)
            
        except Exception as e:
            print(f"❌ API prediction error: {str(e)}")
            return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

    @app.route('/api/explain/lime', methods=['POST'])
    def explain_lime():
        """Generate LIME explanation for given text and model."""
        start_time = time.time()
        try:
            data = request.get_json()
            text = data.get('text', '').strip()
            model_key = data.get('model', '')
            
            print(f"🔍 LIME explanation request - Model: {model_key}, Text length: {len(text)}")
            
            if not text:
                print("⚠️ LIME explanation request failed: No text provided")
                return jsonify({'error': 'Text is required'}), 400
            
            if not model_key or model_key not in AVAILABLE_MODELS:
                print(f"⚠️ LIME explanation request failed: Invalid model '{model_key}'")
                return jsonify({'error': 'Invalid model'}), 400
            
            lime_explanation = get_lime_explanation(model_key, text, LABEL_MAPPING)
            
            response = {
                'lime_explanation': lime_explanation,
                'model_used': model_key
            }
            
            end_time = time.time()
            print(f"✅ API LIME explanation completed in {end_time - start_time:.3f}s - Model: {model_key}, Features: {len(lime_explanation)}")
            
            return jsonify(response)
            
        except Exception as e:
            print(f"❌ API LIME explanation error: {str(e)}")
            return jsonify({'error': f'LIME explanation failed: {str(e)}'}), 500

    @app.route('/api/explain/shap', methods=['POST'])
    def explain_shap():
        """Generate SHAP explanation for given text and model."""
        start_time = time.time()
        try:
            data = request.get_json()
            text = data.get('text', '').strip()
            model_key = data.get('model', '')
            
            print(f"📊 SHAP explanation request - Model: {model_key}, Text length: {len(text)}")
            
            if not text:
                print("⚠️ SHAP explanation request failed: No text provided")
                return jsonify({'error': 'Text is required'}), 400
            
            if not model_key or model_key not in AVAILABLE_MODELS:
                print(f"⚠️ SHAP explanation request failed: Invalid model '{model_key}'")
                return jsonify({'error': 'Invalid model'}), 400
            
            shap_explanation = get_shap_explanation(model_key, text)
            
            response = {
                'shap_explanation': shap_explanation,
                'model_used': model_key
            }
            
            end_time = time.time()
            print(f"✅ API SHAP explanation completed in {end_time - start_time:.3f}s - Model: {model_key}, Features: {len(shap_explanation)}")
            
            return jsonify(response)
            
        except Exception as e:
            print(f"❌ API SHAP explanation error: {str(e)}")
            return jsonify({'error': f'SHAP explanation failed: {str(e)}'}), 500
