from flask import request, jsonify
import traceback
from config import AVAILABLE_MODELS, LABEL_MAPPING
from model_utils import get_model_path
from ai_utils import hf_pretrained_classify
from explanations import get_lime_explanation, get_shap_explanation


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
