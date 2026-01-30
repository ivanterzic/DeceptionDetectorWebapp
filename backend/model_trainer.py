import os
import json
import torch
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from pathlib import Path
import random
import string
import shutil
from typing import Dict, List, Optional, Tuple
from datasets import Dataset
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification, 
    TrainingArguments, Trainer, DataCollatorWithPadding
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import time
from base_model_cache import get_cached_model_path, download_base_model, is_model_cached


# Configuration for fine-tuning models
FINETUNING_MODELS = {
    'bert-base-uncased': 'BERT Base (Uncased)',
    'microsoft/deberta-v3-base': 'DeBERTa v3 Base', 
    'albert-base-v2': 'ALBERT Base v2',
    'roberta-base': 'RoBERTa Base',
    'distilbert-base-uncased': 'DistilBERT Base'
}

CUSTOM_MODELS_DIR = Path(__file__).parent / 'custom_models'
ZIP_EXPIRY_HOURS = 24
# --- ZIP Cleanup Logic ---
def cleanup_expired_zips():
    """
    Delete custom model ZIP archives older than ZIP_EXPIRY_HOURS (24 hours).
    """
    zip_count = 0
    now = time.time()
    for zip_file in CUSTOM_MODELS_DIR.parent.glob("*_model.zip"):
        try:
            mtime = zip_file.stat().st_mtime
            age_hours = (now - mtime) / 3600
            if age_hours > ZIP_EXPIRY_HOURS:
                zip_file.unlink()
                print(f"🗑️ Deleted expired ZIP: {zip_file} ({age_hours:.1f} hours old)")
                zip_count += 1
        except Exception as e:
            print(f"❌ Error deleting ZIP {zip_file}: {str(e)}")
    if zip_count > 0:
        print(f"🧹 Cleaned up {zip_count} expired ZIP archives")
MODEL_EXPIRY_DAYS = 7
MAX_SEQUENCE_LENGTH = 512


def generate_model_code() -> str:
    """Generate a unique 6-digit alphanumeric code for a model."""
    while True:
        # Generate 6 random characters (letters and numbers)
        code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        model_path = CUSTOM_MODELS_DIR / code
        if not model_path.exists():
            return code


def validate_csv_data(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate CSV data for training.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    # Check required columns
    required_columns = ['text', 'label']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    # Check for empty data
    if len(df) == 0:
        return False, "CSV file is empty"
    
    # Check minimum rows for training
    if len(df) < 10:
        return False, "Need at least 10 rows for training"
    
    # Check for missing values
    if df['text'].isnull().any() or df['text'].str.strip().eq('').any():
        return False, "Found empty text values"
    
    if df['label'].isnull().any():
        return False, "Found missing label values"
    
    # Check label values (should be 0 or 1, or deceptive/truthful)
    unique_labels = df['label'].unique()
    valid_labels = {0, 1, '0', '1', 'deceptive', 'truthful'}
    
    if not all(label in valid_labels for label in unique_labels):
        return False, f"Invalid label values. Expected 0/1 or deceptive/truthful, got: {list(unique_labels)}"
    
    # Check class distribution
    label_counts = df['label'].value_counts()
    if len(label_counts) < 2:
        return False, "Need at least 2 different classes for training"
    
    min_class_count = label_counts.min()
    if min_class_count < 5:
        return False, f"Each class needs at least 5 examples, minimum found: {min_class_count}"
    
    # Check text length
    max_chars = df['text'].str.len().max()
    if max_chars > 10000:
        return False, f"Text too long (max {max_chars} chars). Please limit to 10,000 characters per text."
    
    return True, ""


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the DataFrame for training.
    
    Args:
        df: Raw DataFrame
        
    Returns:
        pd.DataFrame: Preprocessed DataFrame
    """
    # Create a copy
    df = df.copy()
    
    # Clean text
    df['text'] = df['text'].str.strip()
    
    # Normalize labels to 0/1
    label_mapping = {
        'deceptive': 0, '0': 0, 0: 0,
        'truthful': 1, '1': 1, 1: 1
    }
    df['label'] = df['label'].map(label_mapping)
    
    # Remove any rows that couldn't be mapped
    df = df.dropna(subset=['label'])
    
    # Convert labels to int
    df['label'] = df['label'].astype(int)
    
    return df


def tokenize_data(texts: List[str], tokenizer, max_length: int = MAX_SEQUENCE_LENGTH):
    """Tokenize text data for training."""
    return tokenizer(
        texts,
        truncation=True,
        padding=True,
        max_length=max_length,
        return_tensors="pt"
    )


def compute_metrics(eval_pred):
    """Compute metrics for evaluation."""
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return {
        'accuracy': accuracy_score(labels, predictions)
    }


class ModelTrainer:
    """Custom model trainer for fine-tuning."""
    
    def __init__(self, model_code: str, base_model: str, config: Dict):
        """
        Initialize the trainer.
        
        Args:
            model_code: Unique 6-digit code for the model
            base_model: Base HuggingFace model to fine-tune
            config: Training configuration
        """
        self.model_code = model_code
        self.base_model = base_model
        self.config = config
        self.model_dir = CUSTOM_MODELS_DIR / model_code
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize metadata
        self.metadata = {
            'model_code': model_code,
            'base_model': base_model,
            'name': config.get('name', f'Custom Model {model_code}'),
            'notes': config.get('notes', ''),
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=MODEL_EXPIRY_DAYS)).isoformat(),
            'status': 'training',
            'epochs': config.get('epochs', 3),
            'learning_rate': config.get('learning_rate', 2e-5),
            'validation_split': config.get('validation_split', 0.2),
            'train_size': 0,
            'val_size': 0,
            'accuracy': None,
            'training_time': None
        }
        
        self._save_metadata()
    
    def _save_metadata(self):
        """Save model metadata to file."""
        with open(self.model_dir / 'metadata.json', 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def train(self, df: pd.DataFrame) -> Dict:
        """
        Train the model with provided data.
        
        Args:
            df: Training data DataFrame
            
        Returns:
            Dict: Training results
        """
        print(f"🚀 Starting training for model {self.model_code}")
        start_time = time.time()
        
        try:
            # Preprocess data
            df = preprocess_data(df)
            print(f"📊 Dataset size: {len(df)} samples")
            
            # Get validation split from config (default to 0.2 if not specified)
            validation_split = float(self.config.get('validation_split', 0.2))
            print(f"📋 Using validation split: {validation_split} ({validation_split*100:.0f}% for validation)")
            
            # Split data based on validation_split setting
            if validation_split > 0:
                train_texts, val_texts, train_labels, val_labels = train_test_split(
                    df['text'].tolist(),
                    df['label'].tolist(),
                    test_size=validation_split,
                    random_state=42,
                    stratify=df['label']
                )
            else:
                # No validation split - use all data for training
                train_texts = df['text'].tolist()
                train_labels = df['label'].tolist()
                val_texts = []
                val_labels = []
            
            print(f"📈 Train: {len(train_texts)}, Validation: {len(val_texts)}")
            
            # Update metadata
            self.metadata['train_size'] = len(train_texts)
            self.metadata['val_size'] = len(val_texts)
            self.metadata['validation_split'] = validation_split
            self._save_metadata()
            
            # Load tokenizer and model using optimal GPU device
            from gpu_utils import get_torch_device, monitor_gpu_memory, get_optimal_device
            device = get_torch_device()
            device_id = get_optimal_device()
            print(f"🎮 Using device: {device}")
            monitor_gpu_memory("before_model_load", device_id if device_id != -1 else None)
            
            # Check if base model is cached, download if not
            cached_model_path = get_cached_model_path(self.base_model)
            if cached_model_path:
                print(f"📂 Using cached base model: {cached_model_path}")
                model_source = cached_model_path
            else:
                print(f"📥 Base model not cached, downloading: {self.base_model}")
                success, message = download_base_model(self.base_model)
                if success:
                    cached_model_path = get_cached_model_path(self.base_model)
                    print(f"✅ Successfully cached and using: {cached_model_path}")
                    model_source = cached_model_path
                else:
                    print(f"⚠️ Failed to cache model, using HuggingFace directly: {message}")
                    model_source = self.base_model
            
            tokenizer = AutoTokenizer.from_pretrained(model_source)
            model = AutoModelForSequenceClassification.from_pretrained(
                model_source,
                num_labels=2,
                id2label={0: "deceptive", 1: "truthful"},
                label2id={"deceptive": 0, "truthful": 1}
            )
            
            # Tokenize training data
            train_encodings = tokenizer(
                train_texts,
                truncation=True,
                padding=True,
                max_length=MAX_SEQUENCE_LENGTH,
                return_tensors="pt"
            )
            
            # Create training dataset
            train_dataset = Dataset.from_dict({
                'input_ids': train_encodings['input_ids'],
                'attention_mask': train_encodings['attention_mask'],
                'labels': train_labels
            })
            
            # Handle validation data (if validation split > 0)
            val_dataset = None
            if validation_split > 0 and len(val_texts) > 0:
                val_encodings = tokenizer(
                    val_texts,
                    truncation=True,
                    padding=True,
                    max_length=MAX_SEQUENCE_LENGTH,
                    return_tensors="pt"
                )
                
                val_dataset = Dataset.from_dict({
                    'input_ids': val_encodings['input_ids'],
                    'attention_mask': val_encodings['attention_mask'],
                    'labels': val_labels
                })
            
            # Training arguments (conditional on validation data)
            training_args_dict = {
                'output_dir': str(self.model_dir / 'checkpoints'),
                'num_train_epochs': self.config.get('epochs', 3),
                'per_device_train_batch_size': 8,
                'per_device_eval_batch_size': 16,
                'warmup_steps': 500,
                'weight_decay': 0.01,
                'learning_rate': float(self.config.get('learning_rate', 2e-5)),
                'logging_dir': str(self.model_dir / 'logs'),
                'logging_steps': 10,
                'save_strategy': "epoch",
                'save_total_limit': 2,
                'report_to': "none"  # Disable tracking integrations
            }
            
            # Add evaluation settings only if we have validation data
            if val_dataset is not None:
                training_args_dict.update({
                    'eval_strategy': "epoch",
                    'load_best_model_at_end': True,
                    'metric_for_best_model': "accuracy",
                    'greater_is_better': True,
                })
            else:
                print("⚠️ No validation data - training without evaluation")
            
            training_args = TrainingArguments(**training_args_dict)
            
            # Initialize trainer
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=val_dataset,  # Will be None if no validation data
                data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
                compute_metrics=compute_metrics if val_dataset is not None else None,
            )
            
            # Train the model
            print(f"🏋️ Training model with {self.metadata['epochs']} epochs...")
            trainer.train()
            
            # Evaluate the model (only if validation data exists)
            if val_dataset is not None:
                eval_results = trainer.evaluate()
                accuracy = eval_results['eval_accuracy']
                print(f"✅ Training completed! Validation Accuracy: {accuracy:.4f}")
                self.metadata['accuracy'] = accuracy
            else:
                print(f"✅ Training completed! (No validation data for accuracy measurement)")
                self.metadata['accuracy'] = None
            
            # Save the final model
            final_model_path = self.model_dir / 'model'
            trainer.save_model(str(final_model_path))
            tokenizer.save_pretrained(str(final_model_path))
            
            # Update metadata
            end_time = time.time()
            training_time = end_time - start_time
            
            self.metadata['status'] = 'completed'
            # accuracy is already set above based on validation data availability
            self.metadata['training_time'] = training_time
            self._save_metadata()
            
            # Create completion flag
            with open(self.model_dir / '.completed', 'w') as f:
                f.write(datetime.now().isoformat())
            
            print(f"🎉 Model {self.model_code} training completed in {training_time:.2f}s")
            
            return {
                'success': True,
                'model_code': self.model_code,
                'accuracy': self.metadata['accuracy'],
                'training_time': training_time
            }
            
        except Exception as e:
            print(f"❌ Training failed for model {self.model_code}: {str(e)}")
            
            # Update metadata with error
            self.metadata['status'] = 'failed'
            self.metadata['error'] = str(e)
            self._save_metadata()
            
            return {
                'success': False,
                'error': str(e)
            }


def get_model_metadata(model_code: str) -> Optional[Dict]:
    """
    Get metadata for a custom model.
    
    Args:
        model_code: 6-digit model code
        
    Returns:
        Dict: Model metadata or None if not found
    """
    model_dir = CUSTOM_MODELS_DIR / model_code
    metadata_path = model_dir / 'metadata.json'
    
    if not metadata_path.exists():
        return None
    
    try:
        with open(metadata_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error reading metadata for {model_code}: {str(e)}")
        return None


def is_model_completed(model_code: str) -> bool:
    """
    Check if a model training is completed.
    
    Args:
        model_code: 6-digit model code
        
    Returns:
        bool: True if completed, False otherwise
    """
    model_dir = CUSTOM_MODELS_DIR / model_code
    return (model_dir / '.completed').exists()


def is_model_expired(model_code: str) -> bool:
    """
    Check if a model has expired.
    
    Args:
        model_code: 6-digit model code
        
    Returns:
        bool: True if expired, False otherwise
    """
    metadata = get_model_metadata(model_code)
    if not metadata:
        return True
    
    try:
        expires_at = datetime.fromisoformat(metadata['expires_at'])
        return datetime.now() > expires_at
    except:
        return True


def cleanup_expired_models():
    """Clean up models that have expired (7+ days old)."""
    if not CUSTOM_MODELS_DIR.exists():
        return
    
    cleaned_count = 0
    for model_dir in CUSTOM_MODELS_DIR.iterdir():
        if model_dir.is_dir() and len(model_dir.name) == 6:
            if is_model_expired(model_dir.name):
                try:
                    shutil.rmtree(model_dir)
                    print(f"🗑️ Cleaned up expired model: {model_dir.name}")
                    cleaned_count += 1
                except Exception as e:
                    print(f"❌ Error cleaning up model {model_dir.name}: {str(e)}")
    
    if cleaned_count > 0:
        print(f"🧹 Cleaned up {cleaned_count} expired models")


def get_remaining_time(model_code: str) -> Optional[str]:
    """
    Get remaining time before model expires.
    
    Args:
        model_code: 6-digit model code
        
    Returns:
        str: Human-readable remaining time or None
    """
    metadata = get_model_metadata(model_code)
    if not metadata:
        return None
    
    try:
        expires_at = datetime.fromisoformat(metadata['expires_at'])
        now = datetime.now()
        
        if now > expires_at:
            return "Expired"
        
        remaining = expires_at - now
        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        
        if days > 0:
            return f"{days} days, {hours} hours"
        elif hours > 0:
            return f"{hours} hours"
        else:
            minutes = remainder // 60
            return f"{minutes} minutes"
            
    except Exception:
        return "Unknown"


def create_model_archive(model_code: str) -> Optional[str]:
    """
    Create a downloadable archive of the trained model.
    
    Args:
        model_code: 6-digit model code
        
    Returns:
        str: Path to the archive file or None if failed
    """
    print(f"📦 Starting archive creation for model {model_code}")
    
    model_dir = CUSTOM_MODELS_DIR / model_code
    
    # Validate model directory exists
    if not model_dir.exists():
        print(f"❌ Model directory does not exist: {model_dir}")
        return None
        
    if not is_model_completed(model_code):
        print(f"❌ Model {model_code} is not in completed state")
        return None
    
    print(f"✅ Model directory found: {model_dir}")
    
    try:
        # Check model directory contents
        model_files = list(model_dir.glob('*'))
        print(f"📁 Model directory contains {len(model_files)} files:")
        for file_path in model_files:
            file_size = file_path.stat().st_size / (1024 * 1024)  # MB
            print(f"   • {file_path.name}: {file_size:.2f} MB")
        
        archive_path = model_dir.parent / f"{model_code}_model.zip"
        
        # Remove existing archive if present
        if archive_path.exists():
            print(f"🗑️ Removing existing archive: {archive_path}")
            archive_path.unlink()
        
        print(f"🗜️ Creating ZIP archive...")
        archive_start = time.time()
        
        # Create zip archive
        shutil.make_archive(
            str(archive_path.with_suffix('')),
            'zip',
            str(model_dir)
        )
        
        archive_time = time.time() - archive_start
        archive_size = archive_path.stat().st_size / (1024 * 1024)  # MB
        
        print(f"✅ Archive created successfully!")
        print(f"📊 Archive statistics:")
        print(f"   • Creation time: {archive_time:.2f}s")
        print(f"   • Archive size: {archive_size:.2f} MB")
        print(f"   • Archive path: {archive_path}")
        print(f"   • Compression ratio: {(sum(f.stat().st_size for f in model_files) / (1024*1024)) / archive_size:.1f}:1")
        
        return str(archive_path)
        
    except Exception as e:
        print(f"❌ Error creating archive for {model_code}")
        print(f"   🔍 Error details: {str(e)}")
        print(f"   📁 Model directory: {model_dir}")
        print(f"   📊 Directory exists: {model_dir.exists()}")
        if model_dir.exists():
            try:
                files = list(model_dir.glob('*'))
                print(f"   📁 Directory contents: {len(files)} files")
            except Exception as list_error:
                print(f"   ❌ Could not list directory contents: {list_error}")
        return None


def create_model_archive_with_progress(model_code: str, download_id: str = None) -> Optional[str]:
    """
    Create a downloadable archive of the trained model with progress tracking.
    Progress is calculated based on actual ZIP file size vs total folder size.
    
    Args:
        model_code: 6-digit model code
        download_id: Optional download ID for progress tracking
        
    Returns:
        str: Path to the archive file or None if failed
    """
    # Import here to avoid circular imports
    try:
        from training_routes import download_progress
    except ImportError:
        download_progress = {}
    
    def update_progress(progress: int, phase: str):
        """Helper function to update progress"""
        if download_id and download_id in download_progress:
            download_progress[download_id].update({
                'progress': min(progress, 99),  # Cap at 99% until fully complete
                'phase': phase
            })
            print(f"📊 Progress update: {progress}% - {phase}")
    
    print(f"📦 Starting archive creation for model {model_code}")
    update_progress(0, "Scanning model files...")
    
    model_dir = CUSTOM_MODELS_DIR / model_code
    
    # Validate model directory exists
    if not model_dir.exists():
        print(f"❌ Model directory does not exist: {model_dir}")
        return None
        
    if not is_model_completed(model_code):
        print(f"❌ Model {model_code} is not in completed state")
        return None
    
    print(f"✅ Model directory found: {model_dir}")
    
    try:
        # Check model directory contents
        update_progress(5, "Calculating folder size...")
        model_files = list(model_dir.rglob('*'))  # Use rglob to get all files recursively
        file_list = [f for f in model_files if f.is_file()]  # Only files, not directories
        total_size = sum(f.stat().st_size for f in file_list)
        total_size_mb = total_size / (1024 * 1024)
        
        print(f"📁 Model directory contains {len(file_list)} files ({total_size_mb:.2f} MB):")
        for file_path in file_list[:10]:  # Show first 10 files
            file_size = file_path.stat().st_size / (1024 * 1024)  # MB
            relative_path = file_path.relative_to(model_dir)
            print(f"   • {relative_path}: {file_size:.2f} MB")
        if len(file_list) > 10:
            print(f"   ... and {len(file_list) - 10} more files")
        
        update_progress(10, "Preparing archive...")
        archive_path = model_dir.parent / f"{model_code}_model.zip"
        
        # Remove existing archive if present
        if archive_path.exists():
            print(f"🗑️ Removing existing archive: {archive_path}")
            archive_path.unlink()
        
        update_progress(15, "Creating ZIP archive...")
        print(f"🗜️ Creating ZIP archive...")
        archive_start = time.time()
        
        # Create zip archive with progress tracking based on file size
        import zipfile
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            processed_size = 0
            last_progress = 15
            
            for i, file_path in enumerate(file_list):
                relative_path = file_path.relative_to(model_dir)
                
                # Add file to archive
                zipf.write(file_path, relative_path)
                processed_size += file_path.stat().st_size
                
                # Calculate progress based on processed size (15% to 95% range)
                size_progress = int(15 + (processed_size / total_size) * 80)
                
                # Update progress every 5% or for large files
                if size_progress >= last_progress + 5 or file_path.stat().st_size > 10 * 1024 * 1024:
                    file_name = str(relative_path)
                    if len(file_name) > 50:
                        file_name = "..." + file_name[-47:]
                    update_progress(size_progress, f"Compressing: {file_name}")
                    last_progress = size_progress
                    
                # Log progress for large files
                if file_path.stat().st_size > 10 * 1024 * 1024:  # > 10MB
                    file_size_mb = file_path.stat().st_size / (1024 * 1024)
                    print(f"   📦 Compressed {relative_path} ({file_size_mb:.1f} MB)")
        
        archive_time = time.time() - archive_start
        archive_size = archive_path.stat().st_size / (1024 * 1024)  # MB
        compression_ratio = total_size_mb / archive_size if archive_size > 0 else 0
        
        update_progress(99, "Finalizing archive...")
        
        print(f"✅ Archive created successfully!")
        print(f"📊 Archive statistics:")
        print(f"   • Creation time: {archive_time:.2f}s")
        print(f"   • Original size: {total_size_mb:.2f} MB")
        print(f"   • Archive size: {archive_size:.2f} MB")
        print(f"   • Archive path: {archive_path}")
        print(f"   • Compression ratio: {compression_ratio:.1f}:1")
        print(f"   • Compression efficiency: {(1 - archive_size/total_size_mb)*100:.1f}%")
        
        return str(archive_path)
        
    except Exception as e:
        print(f"❌ Error creating archive for {model_code}")
        print(f"   🔍 Error details: {str(e)}")
        print(f"   📁 Model directory: {model_dir}")
        print(f"   📊 Directory exists: {model_dir.exists()}")
        if model_dir.exists():
            try:
                files = list(model_dir.glob('*'))
                print(f"   📁 Directory contents: {len(files)} files")
            except Exception as list_error:
                print(f"   ❌ Could not list directory contents: {list_error}")
        return None


# Initialize custom models directory
CUSTOM_MODELS_DIR.mkdir(exist_ok=True)