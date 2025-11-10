import os
import json
import pandas as pd
import threading
from datetime import datetime
from flask import request, jsonify, send_file, Response
from werkzeug.utils import secure_filename
import traceback
import time
from pathlib import Path
import uuid

from security import (
    validate_text_input,
    validate_model_code,
    validate_csv_file,
    validate_training_params,
    rate_limit
)
from config import RATE_LIMIT_TRAINING, RATE_LIMIT_DEFAULT, RATE_LIMIT_ANALYSIS
from model_trainer import (
    FINETUNING_MODELS,
    CUSTOM_MODELS_DIR,
    ModelTrainer,
    generate_model_code,
    validate_csv_data,
    get_model_metadata,
    is_model_completed,
    is_model_expired,
    get_remaining_time,
    create_model_archive,
    cleanup_expired_models,
    cleanup_expired_zips
)
def register_training_routes(app):
    """Register training-related API routes."""

    @app.route('/api/training/cleanup-zips', methods=['POST'])
    @rate_limit(limit=RATE_LIMIT_DEFAULT, window=60)
    def manual_zip_cleanup():
        """Manually trigger cleanup of expired custom model ZIPs (older than 24 hours)."""
        print("🧹 Manual ZIP cleanup triggered")
        try:
            cleanup_expired_zips()
            return jsonify({'success': True, 'message': 'ZIP cleanup completed'})
        except Exception as e:
            print(f"❌ ZIP cleanup error: {str(e)}")
            return jsonify({'error': 'ZIP cleanup failed'}), 500

    # --- Scheduled ZIP Cleanup ---
    def start_zip_cleanup_scheduler():
        def cleanup_loop():
            while True:
                try:
                    cleanup_expired_zips()
                except Exception as e:
                    print(f"❌ Scheduled ZIP cleanup error: {str(e)}")
                time.sleep(3600)  # Run every hour
        thread = threading.Thread(target=cleanup_loop)
        thread.daemon = True
        thread.start()

    start_zip_cleanup_scheduler()
from ai_utils import preload_model, hf_pretrained_classify, _model_cache
from explanations import get_lime_explanation, get_shap_explanation
from config import LABEL_MAPPING

# Global progress tracking for downloads
download_progress = {}


def register_training_routes(app):
    """Register training-related API routes."""
    
    # --- Scheduled ZIP Cleanup ---
    def start_zip_cleanup_scheduler():
        def cleanup_loop():
            while True:
                try:
                    cleanup_expired_zips()
                except Exception as e:
                    print(f"❌ Scheduled ZIP cleanup error: {str(e)}")
                time.sleep(3600)  # Run every hour
        thread = threading.Thread(target=cleanup_loop)
        thread.daemon = True
        thread.start()

    start_zip_cleanup_scheduler()

    @app.route('/api/training/models', methods=['GET'])
    @rate_limit(limit=RATE_LIMIT_DEFAULT, window=60)
    def get_training_models():
        """Get available base models for fine-tuning."""
        return jsonify({
            'models': [
                {'key': key, 'name': name} 
                for key, name in FINETUNING_MODELS.items()
            ]
        })
    
    @app.route('/api/training/upload-csv', methods=['POST'])
    @rate_limit(limit=20, window=60)  # Higher limit for CSV validation
    def upload_csv():
        """Upload and validate CSV data for training."""
        start_time = time.time()
        print("📤 CSV upload request received")
        
        try:
            # Check if file is present
            if 'file' not in request.files:
                print("⚠️ No file uploaded")
                return jsonify({'error': 'No file uploaded'}), 400
            
            file = request.files['file']
            if file.filename == '':
                print("⚠️ Empty filename")
                return jsonify({'error': 'No file selected'}), 400
            
            # Validate CSV file
            is_valid, filename, error_msg = validate_csv_file(file)
            if not is_valid:
                print(f"⚠️ File validation failed: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            print(f"📂 Processing file: {filename}")
            
            # Read CSV
            try:
                file.seek(0)  # Reset file pointer after validation
                df = pd.read_csv(file)
                print(f"📊 CSV loaded: {len(df)} rows, {len(df.columns)} columns")
            except Exception as e:
                print(f"❌ CSV read error: {str(e)}")
                return jsonify({'error': 'Error reading CSV file'}), 400
            
            # Validate data
            is_valid, error_msg = validate_csv_data(df)
            
            if not is_valid:
                print(f"⚠️ Validation failed: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            # Get data statistics
            label_counts = df['label'].value_counts().to_dict()
            
            # Convert label keys to strings for JSON serialization
            label_counts = {str(k): v for k, v in label_counts.items()}
            
            end_time = time.time()
            print(f"✅ CSV validation completed in {end_time - start_time:.2f}s")
            
            response = {
                'valid': True,
                'rows': len(df),
                'columns': list(df.columns),
                'label_distribution': label_counts,
                'sample_data': df.head(3).to_dict('records')
            }
            
            return jsonify(response)
            
        except Exception as e:
            print(f"❌ CSV upload error: {str(e)}")
            return jsonify({'error': 'Upload failed'}), 500
    
    @app.route('/api/training/start', methods=['POST'])
    @rate_limit(limit=RATE_LIMIT_TRAINING, window=60)
    def start_training():
        """Start model training with uploaded data."""
        start_time = time.time()
        print("🚀 Training start request received")
        
        try:
            # Get form data
            if 'file' not in request.files:
                return jsonify({'error': 'No training file uploaded'}), 400
            
            file = request.files['file']
            
            # Validate CSV file
            is_valid, filename, error_msg = validate_csv_file(file)
            if not is_valid:
                print(f"⚠️ File validation failed: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            config_json = request.form.get('config', '{}')
            
            try:
                config = json.loads(config_json)
            except:
                return jsonify({'error': 'Invalid configuration JSON'}), 400
            
            # Validate required config fields
            required_fields = ['base_model', 'name']
            missing_fields = [field for field in required_fields if field not in config]
            if missing_fields:
                return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400
            
            if config['base_model'] not in FINETUNING_MODELS:
                return jsonify({'error': 'Invalid base model'}), 400
            
            # Validate training parameters
            is_valid, validated_params, error_msg = validate_training_params(config)
            if not is_valid:
                print(f"⚠️ Training params validation failed: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            print(f"⚙️ Config: {config}")
            
            # Read and validate CSV
            try:
                file.seek(0)  # Reset file pointer after validation
                df = pd.read_csv(file)
                is_valid, error_msg = validate_csv_data(df)
                if not is_valid:
                    return jsonify({'error': error_msg}), 400
            except Exception as e:
                return jsonify({'error': 'Error reading CSV file'}), 400
            
            # Generate unique model code
            model_code = generate_model_code()
            print(f"🆔 Generated model code: {model_code}")
            
            # Clean up expired models before starting new training
            cleanup_expired_models()
            
            # Start training in background thread
            def train_model_async():
                trainer = ModelTrainer(model_code, config['base_model'], config)
                result = trainer.train(df)
                print(f"🏁 Training finished for {model_code}: {result}")
            
            training_thread = threading.Thread(target=train_model_async)
            training_thread.daemon = True
            training_thread.start()
            
            end_time = time.time()
            print(f"✅ Training started in {end_time - start_time:.2f}s")
            
            return jsonify({
                'success': True,
                'model_code': model_code,
                'message': f'Training started for model {model_code}'
            })
            
        except Exception as e:
            print(f"❌ Training start error: {str(e)}")
            return jsonify({'error': 'Failed to start training'}), 500
    
    @app.route('/api/training/status/<model_code>', methods=['GET'])
    @rate_limit(limit=RATE_LIMIT_DEFAULT, window=60)
    def get_training_status(model_code):
        """Get training status for a specific model."""
        print(f"📊 Status check for model: {model_code}")
        
        try:
            # Validate model code format
            is_valid, cleaned_code, error_msg = validate_model_code(model_code)
            if not is_valid:
                print(f"⚠️ Invalid model code: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            metadata = get_model_metadata(model_code)
            if not metadata:
                return jsonify({'error': 'Model not found'}), 404
            
            # Check if expired
            if is_model_expired(model_code):
                return jsonify({'error': 'Model has expired'}), 410
            
            # Add completion status and remaining time
            metadata['completed'] = is_model_completed(model_code)
            metadata['remaining_time'] = get_remaining_time(model_code)
            
            print(f"✅ Status retrieved for {model_code}: {metadata['status']}")
            
            return jsonify(metadata)
            
        except Exception as e:
            print(f"❌ Status check error for {model_code}: {str(e)}")
            return jsonify({'error': 'Status check failed'}), 500
    
    @app.route('/api/custom/predict/<model_code>', methods=['POST'])
    @rate_limit(limit=RATE_LIMIT_ANALYSIS, window=60)
    def predict_custom(model_code):
        """Make prediction using a custom trained model."""
        start_time = time.time()
        print(f"🔮 Custom prediction request for model: {model_code}")
        
        try:
            # Validate model code
            is_valid, cleaned_code, error_msg = validate_model_code(model_code)
            if not is_valid:
                print(f"⚠️ Invalid model code: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            # Check if model exists and is completed
            if not is_model_completed(model_code):
                return jsonify({'error': 'Model not found or not completed'}), 404
            
            # Check if model is expired
            if is_model_expired(model_code):
                return jsonify({'error': 'Model has expired'}), 410
            
            # Get request data
            data = request.get_json()
            text = data.get('text', '').strip()
            
            # Validate text input
            is_valid, cleaned_text, error_msg = validate_text_input(text)
            if not is_valid:
                print(f"⚠️ Text validation failed: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            print(f"📝 Custom prediction - Text length: {len(cleaned_text)}")
            
            # Load custom model if not cached
            custom_key = f"custom_{model_code}"
            if custom_key not in _model_cache:
                model_path = CUSTOM_MODELS_DIR / model_code / 'model'
                if not model_path.exists():
                    return jsonify({'error': 'Model files not found'}), 404
                
                print(f"📦 Loading custom model: {model_code}")
                preload_model(custom_key, str(model_path), True)
            
            # Make prediction
            results = hf_pretrained_classify(custom_key, cleaned_text, LABEL_MAPPING)
            prediction = results[0]
            
            # Get model metadata for response
            metadata = get_model_metadata(model_code)
            
            response = {
                'prediction': prediction['label'],
                'confidence': prediction['score'],
                'original_text': cleaned_text,
                'model_code': model_code,
                'model_name': metadata.get('name', f'Custom Model {model_code}') if metadata else f'Custom Model {model_code}',
                'model_type': 'custom'
            }
            
            end_time = time.time()
            print(f"✅ Custom prediction completed in {end_time - start_time:.3f}s - Result: {prediction['label']}, Confidence: {prediction['score']:.3f}")
            
            return jsonify(response)
            
        except Exception as e:
            print(f"❌ Custom prediction error for {model_code}: {str(e)}")
            return jsonify({'error': 'Prediction failed'}), 500
    
    @app.route('/api/custom/explain/lime/<model_code>', methods=['POST'])
    @rate_limit(limit=RATE_LIMIT_ANALYSIS, window=60)
    def explain_lime_custom(model_code):
        """Generate LIME explanation for custom model."""
        start_time = time.time()
        print(f"🔍 Custom LIME explanation for model: {model_code}")
        
        try:
            # Validate and check model
            is_valid, cleaned_code, error_msg = validate_model_code(model_code)
            if not is_valid:
                print(f"⚠️ Invalid model code: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            if not is_model_completed(model_code) or is_model_expired(model_code):
                return jsonify({'error': 'Model not available'}), 404
            
            # Get request data
            data = request.get_json()
            text = data.get('text', '').strip()
            
            # Validate text input
            is_valid, cleaned_text, error_msg = validate_text_input(text)
            if not is_valid:
                print(f"⚠️ Text validation failed: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            # Ensure model is loaded
            custom_key = f"custom_{model_code}"
            if custom_key not in _model_cache:
                model_path = CUSTOM_MODELS_DIR / model_code / 'model'
                preload_model(custom_key, str(model_path), True)
            
            # Generate LIME explanation
            lime_explanation = get_lime_explanation(custom_key, cleaned_text, LABEL_MAPPING)
            
            metadata = get_model_metadata(model_code)
            
            response = {
                'lime_explanation': lime_explanation,
                'model_code': model_code,
                'model_name': metadata.get('name', f'Custom Model {model_code}') if metadata else f'Custom Model {model_code}'
            }
            
            end_time = time.time()
            print(f"✅ Custom LIME explanation completed in {end_time - start_time:.3f}s - Features: {len(lime_explanation)}")
            
            return jsonify(response)
            
        except Exception as e:
            print(f"❌ Custom LIME explanation error for {model_code}: {str(e)}")
            return jsonify({'error': 'LIME explanation failed'}), 500
    
    @app.route('/api/custom/explain/shap/<model_code>', methods=['POST'])
    @rate_limit(limit=RATE_LIMIT_ANALYSIS, window=60)
    def explain_shap_custom(model_code):
        """Generate SHAP explanation for custom model."""
        start_time = time.time()
        print(f"📊 Custom SHAP explanation for model: {model_code}")
        
        try:
            # Validate and check model
            is_valid, cleaned_code, error_msg = validate_model_code(model_code)
            if not is_valid:
                print(f"⚠️ Invalid model code: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            if not is_model_completed(model_code) or is_model_expired(model_code):
                return jsonify({'error': 'Model not available'}), 404
            
            # Get request data
            data = request.get_json()
            text = data.get('text', '').strip()
            
            # Validate text input
            is_valid, cleaned_text, error_msg = validate_text_input(text)
            if not is_valid:
                print(f"⚠️ Text validation failed: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            # Ensure model is loaded
            custom_key = f"custom_{model_code}"
            if custom_key not in _model_cache:
                model_path = CUSTOM_MODELS_DIR / model_code / 'model'
                preload_model(custom_key, str(model_path), True)
            
            # Generate SHAP explanation
            shap_explanation = get_shap_explanation(custom_key, cleaned_text)
            
            metadata = get_model_metadata(model_code)
            
            response = {
                'shap_explanation': shap_explanation,
                'model_code': model_code,
                'model_name': metadata.get('name', f'Custom Model {model_code}') if metadata else f'Custom Model {model_code}'
            }
            
            end_time = time.time()
            print(f"✅ Custom SHAP explanation completed in {end_time - start_time:.3f}s - Features: {len(shap_explanation)}")
            
            return jsonify(response)
            
        except Exception as e:
            print(f"❌ Custom SHAP explanation error for {model_code}: {str(e)}")
            return jsonify({'error': 'SHAP explanation failed'}), 500
    
    @app.route('/api/custom/download/init/<model_code>', methods=['POST'])
    @rate_limit(limit=RATE_LIMIT_DEFAULT, window=60)
    def init_download(model_code):
        """Initialize a download and return a download ID for progress tracking."""
        try:
            # Validate model code
            is_valid, cleaned_code, error_msg = validate_model_code(model_code)
            if not is_valid:
                print(f"⚠️ Invalid model code: {error_msg}")
                return jsonify({'error': error_msg}), 400
            
            # Check if model exists and is completed
            if not is_model_completed(model_code):
                return jsonify({'error': 'Model not found or not completed'}), 404
            
            # Generate unique download ID
            download_id = str(uuid.uuid4())
            
            # Initialize progress tracking
            download_progress[download_id] = {
                'model_code': model_code,
                'status': 'initialized',
                'progress': 0,
                'phase': 'Download initialized',
                'start_time': time.time(),
                'error': None
            }
            
            print(f"🆔 Download initialized: {download_id} for model {model_code}")
            
            return jsonify({
                'download_id': download_id,
                'model_code': model_code
            })
            
        except Exception as e:
            print(f"❌ Download initialization error: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/custom/download/<model_code>', methods=['GET'])
    @rate_limit(limit=RATE_LIMIT_DEFAULT, window=60)
    def download_custom_model(model_code):
        """Download a trained custom model."""
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        # Check if download_id is provided as query parameter
        download_id = request.args.get('download_id')
        
        if not download_id:
            # Generate new download ID if not provided (fallback for old clients)
            download_id = str(uuid.uuid4())
        
        print(f"⬇️ Download request initiated")
        print(f"   📋 Model code: {model_code}")
        print(f"   🆔 Download ID: {download_id}")
        print(f"   🌐 Client IP: {client_ip}")
        print(f"   🔧 User agent: {user_agent[:100]}...")
        print(f"   ⏰ Request time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Initialize or update progress tracking
        if download_id not in download_progress:
            download_progress[download_id] = {
                'model_code': model_code,
                'status': 'initializing',
                'progress': 0,
                'phase': 'Initializing download...',
                'start_time': time.time(),
                'error': None
            }
        
        try:
            # Validate model code (not included in progress percentage)
            print(f"🔍 Validating model code format...")
            download_progress[download_id].update({
                'status': 'validating',
                'progress': 0,
                'phase': 'Validating model code...'
            })
            time.sleep(0.2)  # Small delay to allow frontend to see this phase
            
            is_valid, cleaned_code, error_msg = validate_model_code(model_code)
            if not is_valid:
                print(f"❌ Invalid model code: {error_msg}")
                download_progress[download_id].update({
                    'status': 'failed',
                    'error': error_msg
                })
                return jsonify({
                    'error': 'Invalid model code format',
                    'download_id': download_id
                }), 400
            print(f"✅ Model code format is valid")
            
            # Check if model exists and is completed (not included in progress percentage)
            print(f"🔍 Checking model existence and completion status...")
            download_progress[download_id].update({
                'status': 'checking',
                'progress': 0,
                'phase': 'Checking model availability...'
            })
            time.sleep(0.2)  # Small delay to allow frontend to see this phase
            
            if not is_model_completed(model_code):
                print(f"❌ Model not found or not completed: {model_code}")
                download_progress[download_id].update({
                    'status': 'failed',
                    'error': 'Model not found or not completed'
                })
                return jsonify({
                    'error': 'Model not found or not completed',
                    'download_id': download_id
                }), 404
            print(f"✅ Model {model_code} exists and is completed")
            
            # Create archive with progress tracking
            print(f"📦 Creating downloadable archive...")
            download_progress[download_id].update({
                'status': 'creating',
                'progress': 0,
                'phase': 'Preparing to create archive...'
            })
            archive_start_time = time.time()
            
            # Import the progress-aware function
            from model_trainer import create_model_archive_with_progress
            archive_path = create_model_archive_with_progress(model_code, download_id)
            archive_time = time.time() - archive_start_time
            
            if not archive_path:
                print(f"❌ Failed to create archive for model {model_code}")
                download_progress[download_id].update({
                    'status': 'failed',
                    'error': 'Failed to create model archive'
                })
                return jsonify({
                    'error': 'Failed to create model archive',
                    'download_id': download_id
                }), 500
            
            # Get archive size
            archive_size = os.path.getsize(archive_path) / (1024 * 1024)  # MB
            print(f"✅ Archive created successfully in {archive_time:.2f}s")
            print(f"� Archive details:")
            print(f"   • Path: {archive_path}")
            print(f"   • Size: {archive_size:.2f} MB")
            
            print(f"📤 Sending file to client...")
            download_progress[download_id].update({
                'status': 'sending',
                'progress': 100,
                'phase': 'Download ready!'
            })
            
            download_start_time = time.time()
            
            # Create response with download ID in headers
            response = send_file(
                archive_path,
                as_attachment=True,
                download_name=f"custom_model_{model_code}.zip",
                mimetype='application/zip'
            )
            
            # Add custom headers for tracking
            response.headers['X-Model-Code'] = model_code
            response.headers['X-Download-ID'] = download_id
            response.headers['X-Archive-Size'] = str(int(archive_size * 1024 * 1024))
            
            # Update final progress
            total_time = time.time() - download_progress[download_id]['start_time']
            download_progress[download_id].update({
                'status': 'completed',
                'progress': 100,
                'phase': 'Download completed!',
                'total_time': total_time,
                'archive_size_mb': archive_size
            })
            
            print(f"✅ Download completed successfully!")
            print(f"📊 Download statistics:")
            print(f"   • Total processing time: {total_time:.2f}s")
            print(f"   • Archive creation time: {archive_time:.2f}s")
            print(f"   • File size: {archive_size:.2f} MB")
            print(f"   • Client: {client_ip}")
            print(f"   • Model: {model_code}")
            print(f"   • Download ID: {download_id}")
            
            return response
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Download failed for model {model_code}")
            print(f"   🔍 Error details: {error_msg}")
            print(f"   🌐 Client: {client_ip}")
            print(f"   ⏰ Failed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   🆔 Download ID: {download_id}")
            
            download_progress[download_id].update({
                'status': 'failed',
                'error': error_msg,
                'phase': f'Error: {error_msg}'
            })
            
            return jsonify({
                'error': f'Download failed: {error_msg}',
                'download_id': download_id
            }), 500
    
    @app.route('/api/custom/download-progress/<download_id>', methods=['GET'])
    @rate_limit(limit=120, window=60)  # Higher limit for progress polling (2 requests/sec)
    def get_download_progress(download_id):
        """Get progress of a download operation."""
        if download_id not in download_progress:
            return jsonify({'error': 'Download ID not found'}), 404
        
        progress_data = download_progress[download_id].copy()
        
        # Calculate elapsed time
        if 'start_time' in progress_data:
            progress_data['elapsed_time'] = time.time() - progress_data['start_time']
        
        # Clean up completed or failed downloads after 5 minutes
        if progress_data['status'] in ['completed', 'failed']:
            if progress_data.get('elapsed_time', 0) > 300:  # 5 minutes
                del download_progress[download_id]
        
        return jsonify(progress_data)
    
    @app.route('/api/training/cleanup', methods=['POST'])
    @rate_limit(limit=RATE_LIMIT_DEFAULT, window=60)
    def manual_cleanup():
        """Manually trigger cleanup of expired models."""
        print("🧹 Manual cleanup triggered")
        
        try:
            cleanup_expired_models()
            return jsonify({'success': True, 'message': 'Cleanup completed'})
            
        except Exception as e:
            print(f"❌ Cleanup error: {str(e)}")
            return jsonify({'error': 'Cleanup failed'}), 500