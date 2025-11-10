from flask import request, jsonify
import traceback
import time
from transformers import AutoTokenizer
from config import AVAILABLE_MODELS, LABEL_MAPPING, RATE_LIMIT_ANALYSIS, RATE_LIMIT_DEFAULT
from model_utils import get_model_path
from ai_utils import hf_pretrained_classify
from explanations import get_lime_explanation, get_shap_explanation
from training_routes import register_training_routes
from security import (
    validate_text_input, 
    validate_model_key, 
    rate_limit,
    jwt_required,
    authenticate_user
)

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
        if len(text) > 1300:
            return False, -1, "Text is too long. Please limit to 1300 characters."
        return True, -1, None


def register_routes(app):
    """Register all API routes with the Flask app."""
    
    # Register training routes
    register_training_routes(app)

    # ===================== PUBLIC API - JWT Auth =====================

    @app.route('/api/auth/token', methods=['POST'])
    @rate_limit(limit=10, window=60)
    def get_jwt_token():
        """Issue a JWT token for the public API.
        
        Client must send password pre-hashed with SHA256.
        
        Request body: { 
            "username": "externalapiuser", 
            "password_hash": "sha256_hash_of_password" 
        }
        Response: { "token": "<jwt>", "expires_in": 3600 } or error
        """
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            username = data.get('username', '').strip()
            password_hash = data.get('password_hash', '').strip()
            
            is_valid, token_or_err = authenticate_user(username, password_hash)
            if not is_valid:
                return jsonify({'error': token_or_err}), 401
            
            return jsonify({'token': token_or_err, 'expires_in': 3600}), 200
        except Exception as e:
            print(f"❌ Token issuance error: {str(e)}")
            return jsonify({'error': 'Token issuance failed'}), 500

    @app.route('/api/public/checkDeception', methods=['POST'])
    @jwt_required
    @rate_limit(limit=RATE_LIMIT_ANALYSIS, window=60)
    def check_deception():
        """Public API endpoint to check deception with explanations.
        
        Requires JWT in Authorization header: "Bearer <token>"
        
        Request body (JSON):
          {
            "text": "<text_to_analyze>",
            "modelName": "<model_key>",
            "params": { ... optional extra params ... }
          }
        
        Response (JSON):
          {
            "is_deceptive": true/false,
            "confidence": 0.95,
            "shap_words": [["word1", 0.5], ["word2", -0.3], ...],
            "lime_words": [["word1", 0.6], ["word2", -0.2], ...],
            "model_used": "<model_key>"
          }
        """
        start_time = time.time()
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            text = data.get('text', '').strip()
            model_key = data.get('modelName', '').strip()
            # params = data.get('params', {})  # For future extensibility
            
            # Validate text
            is_valid, cleaned_text, error_msg = validate_text_input(text)
            if not is_valid:
                print(f"⚠️ checkDeception - Invalid text: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            # Validate model
            is_valid, error_msg = validate_model_key(model_key, AVAILABLE_MODELS)
            if not is_valid:
                print(f"⚠️ checkDeception - Invalid model key: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            print(f"🔐 checkDeception request - Model: {model_key}, Text length: {len(cleaned_text)}")
            
            # Token length check
            is_valid, token_count, error_msg = check_text_length(cleaned_text, model_key)
            if not is_valid:
                print(f"⚠️ checkDeception - Text too long: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            # Run prediction
            results = hf_pretrained_classify(model_key, cleaned_text, LABEL_MAPPING)
            prediction = results[0]
            
            # Run SHAP explanation
            shap_explanation = get_shap_explanation(model_key, cleaned_text)
            
            # Run LIME explanation
            lime_explanation = get_lime_explanation(model_key, cleaned_text, LABEL_MAPPING)
            
            # Build response
            is_deceptive = (prediction['label'].lower() == 'deceptive')
            response = {
                'is_deceptive': is_deceptive,
                'confidence': prediction['score'],
                'shap_words': shap_explanation,
                'lime_words': lime_explanation,
                'model_used': model_key
            }
            
            end_time = time.time()
            print(f"✅ checkDeception completed in {end_time - start_time:.3f}s - Model: {model_key}, Result: {prediction['label']}, Confidence: {prediction['score']:.3f}")
            
            return jsonify(response), 200
            
        except Exception as e:
            print(f"❌ checkDeception error: {str(e)}")
            return jsonify({'error': 'Check deception failed'}), 500
    
    @app.route('/api/models', methods=['GET'])
    @rate_limit(limit=RATE_LIMIT_DEFAULT, window=60)
    def get_models():
        """Get available pretrained models."""
        return jsonify(list(AVAILABLE_MODELS.keys()))

    @app.route('/api/predict', methods=['POST'])
    @rate_limit(limit=RATE_LIMIT_ANALYSIS, window=60)
    def predict():
        """Predict deception for given text using specified model."""
        start_time = time.time()
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            text = data.get('text', '')
            model_key = data.get('model', '')
            
            # Validate text input
            is_valid, cleaned_text, error_msg = validate_text_input(text)
            if not is_valid:
                print(f"⚠️ Invalid text input: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            # Validate model key
            is_valid, error_msg = validate_model_key(model_key, AVAILABLE_MODELS)
            if not is_valid:
                print(f"⚠️ Invalid model key: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            print(f"📨 Prediction request - Model: {model_key}, Text length: {len(cleaned_text)}")
            
            # Check if text will exceed token limits before processing
            is_valid, token_count, error_msg = check_text_length(cleaned_text, model_key)
            print(f"📊 Token count check: {token_count} tokens, Valid: {is_valid}")
            if not is_valid:
                print(f"⚠️ Text too long: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            results = hf_pretrained_classify(model_key, cleaned_text, LABEL_MAPPING)
            prediction = results[0]
            
            response = {
                'prediction': prediction['label'],
                'confidence': prediction['score'],
                'original_text': cleaned_text,
                'model_used': model_key
            }
            
            end_time = time.time()
            print(f"✅ API prediction completed in {end_time - start_time:.3f}s - Model: {model_key}, Result: {prediction['label']}, Confidence: {prediction['score']:.3f}")
            
            return jsonify(response)
            
        except Exception as e:
            print(f"❌ API prediction error: {str(e)}")
            return jsonify({'error': 'Prediction failed'}), 500

    @app.route('/api/explain/lime', methods=['POST'])
    @rate_limit(limit=RATE_LIMIT_ANALYSIS, window=60)
    def explain_lime():
        """Generate LIME explanation for given text and model."""
        start_time = time.time()
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
                
            text = data.get('text', '')
            model_key = data.get('model', '')
            
            # Validate inputs
            is_valid, cleaned_text, error_msg = validate_text_input(text)
            if not is_valid:
                return jsonify({'error': error_msg}), 400
            
            is_valid, error_msg = validate_model_key(model_key, AVAILABLE_MODELS)
            if not is_valid:
                return jsonify({'error': error_msg}), 400
            
            print(f"🔍 LIME explanation request - Model: {model_key}, Text length: {len(cleaned_text)}")
            
            lime_explanation = get_lime_explanation(model_key, cleaned_text, LABEL_MAPPING)
            
            response = {
                'lime_explanation': lime_explanation,
                'model_used': model_key
            }
            
            end_time = time.time()
            print(f"✅ API LIME explanation completed in {end_time - start_time:.3f}s - Model: {model_key}, Features: {len(lime_explanation)}")
            
            return jsonify(response)
            
        except Exception as e:
            print(f"❌ API LIME explanation error: {str(e)}")
            return jsonify({'error': 'LIME explanation failed'}), 500

    @app.route('/api/explain/shap', methods=['POST'])
    @rate_limit(limit=RATE_LIMIT_ANALYSIS, window=60)
    def explain_shap():
        """Generate SHAP explanation for given text and model."""
        start_time = time.time()
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
                
            text = data.get('text', '')
            model_key = data.get('model', '')
            
            # Validate inputs
            is_valid, cleaned_text, error_msg = validate_text_input(text)
            if not is_valid:
                return jsonify({'error': error_msg}), 400
            
            is_valid, error_msg = validate_model_key(model_key, AVAILABLE_MODELS)
            if not is_valid:
                return jsonify({'error': error_msg}), 400
            
            print(f"📊 SHAP explanation request - Model: {model_key}, Text length: {len(cleaned_text)}")
            
            shap_explanation = get_shap_explanation(model_key, cleaned_text)
            
            response = {
                'shap_explanation': shap_explanation,
                'model_used': model_key
            }
            
            end_time = time.time()
            print(f"✅ API SHAP explanation completed in {end_time - start_time:.3f}s - Model: {model_key}, Features: {len(shap_explanation)}")
            
            return jsonify(response)
            
        except Exception as e:
            print(f"❌ API SHAP explanation error: {str(e)}")
            return jsonify({'error': 'SHAP explanation failed'}), 500
