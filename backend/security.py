"""
Security utilities for input validation and sanitization.
"""
import re
from functools import wraps
from flask import request, jsonify
import time
from collections import defaultdict
from threading import Lock
import jwt
import datetime
import hashlib
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_SECONDS, API_USERNAME, API_PASSWORD

# Constants
MAX_TEXT_LENGTH = 1300
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
ALLOWED_EXTENSIONS = {'csv'}
MODEL_CODE_PATTERN = re.compile(r'^[a-zA-Z0-9]{6}$')

# Simple in-memory rate limiting (for development)
# In production, use Redis or similar
class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = Lock()
    
    def is_allowed(self, identifier, limit=10, window=60):
        """
        Check if request is allowed based on rate limit.
        
        Args:
            identifier: IP address or other identifier
            limit: Number of requests allowed
            window: Time window in seconds
        
        Returns:
            bool: True if allowed, False if rate limited
        """
        now = time.time()
        
        with self.lock:
            # Clean old requests
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if now - req_time < window
            ]
            
            # Check if under limit
            if len(self.requests[identifier]) >= limit:
                return False
            
            # Add current request
            self.requests[identifier].append(now)
            return True

# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit(limit=10, window=60):
    """
    Decorator for rate limiting endpoints.
    
    Args:
        limit: Number of requests allowed per window
        window: Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Get real IP address from proxy headers (nginx forwards X-Real-IP)
            # Fall back to remote_addr if not behind proxy
            identifier = request.headers.get('X-Real-IP') or \
                        request.headers.get('X-Forwarded-For', '').split(',')[0].strip() or \
                        request.remote_addr
            
            if not rate_limiter.is_allowed(identifier, limit, window):
                return jsonify({
                    'error': 'Rate limit exceeded. Please try again later.'
                }), 429
            
            return f(*args, **kwargs)
        return wrapped
    return decorator


def validate_text_input(text):
    """
    Validate text input for analysis.
    
    Args:
        text: Input text string
    
    Returns:
        tuple: (is_valid, cleaned_text, error_message)
    """
    if not text or not isinstance(text, str):
        return False, None, "Invalid text input"
    
    # Remove null bytes and other problematic characters
    text = text.replace('\x00', '').strip()
    
    if not text:
        return False, None, "Text cannot be empty"
    
    if len(text) > MAX_TEXT_LENGTH:
        return False, None, f"Text exceeds maximum length of {MAX_TEXT_LENGTH} characters"
    
    # Basic XSS prevention (though this is a backend API, still good practice)
    if re.search(r'<script|javascript:|onerror=|onclick=', text, re.IGNORECASE):
        return False, None, "Text contains potentially malicious content"
    
    return True, text, None


def validate_model_key(model_key, available_models):
    """
    Validate model key.
    
    Args:
        model_key: Model identifier
        available_models: Dict or list of valid model keys
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not model_key or not isinstance(model_key, str):
        return False, "Model key is required"
    
    # Prevent path traversal
    if '..' in model_key or '/' in model_key or '\\' in model_key:
        return False, "Invalid model key format"
    
    if model_key not in available_models:
        return False, f"Unknown model: {model_key}"
    
    return True, None


def validate_model_code(code):
    """
    Validate model access code format.
    
    Args:
        code: 6-character alphanumeric code
    
    Returns:
        tuple: (is_valid, cleaned_code, error_message)
    """
    if not code or not isinstance(code, str):
        return False, None, "Model code is required"
    
    code = code.strip()
    
    if not MODEL_CODE_PATTERN.match(code):
        return False, None, "Model code must be exactly 6 alphanumeric characters"
    
    return True, code.lower(), None


def validate_csv_file(file):
    """
    Validate uploaded CSV file.
    
    Args:
        file: FileStorage object from Flask
    
    Returns:
        tuple: (is_valid, filename, error_message)
    """
    if not file:
        return False, None, "No file provided"
    
    filename = file.filename
    
    if not filename:
        return False, None, "Empty filename"
    
    # Check extension
    if '.' not in filename:
        return False, None, "File has no extension"
    
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, None, f"Invalid file type. Only {', '.join(ALLOWED_EXTENSIONS)} files are allowed"
    
    # Check file size
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning
    
    if file_size == 0:
        return False, None, "File is empty"
    
    if file_size > MAX_FILE_SIZE:
        return False, None, f"File size exceeds maximum of {MAX_FILE_SIZE / (1024*1024):.0f} MB"
    
    # Sanitize filename to prevent path traversal
    filename = re.sub(r'[^\w\s.-]', '', filename)
    filename = filename.replace('..', '')
    
    return True, filename, None


def validate_training_params(params):
    """
    Validate model training parameters.
    
    Args:
        params: Dict of training parameters
    
    Returns:
        tuple: (is_valid, validated_params, error_message)
    """
    validated = {}
    
    # Model name (accept both 'name' and 'model_name' for compatibility)
    model_name = params.get('model_name') or params.get('name', '')
    model_name = model_name.strip() if model_name else ''
    if not model_name:
        return False, None, "Model name is required"
    if len(model_name) > 100:
        return False, None, "Model name too long (max 100 characters)"
    validated['model_name'] = model_name
    validated['name'] = model_name  # Include both for compatibility
    
    # Base model
    base_model = params.get('base_model', '').strip()
    valid_base_models = [
        'bert-base-uncased',
        'microsoft/deberta-v3-base',
        'albert-base-v2',
        'roberta-base',
        'distilbert-base-uncased'
    ]
    if base_model not in valid_base_models:
        return False, None, f"Invalid base model. Must be one of: {', '.join(valid_base_models)}"
    validated['base_model'] = base_model
    
    # Epochs (1-10)
    try:
        epochs = int(params.get('epochs', 3))
        if epochs < 1 or epochs > 10:
            return False, None, "Epochs must be between 1 and 10"
        validated['epochs'] = epochs
    except (ValueError, TypeError):
        return False, None, "Epochs must be a valid integer"
    
    # Batch size (4-32)
    try:
        batch_size = int(params.get('batch_size', 16))
        if batch_size < 4 or batch_size > 32:
            return False, None, "Batch size must be between 4 and 32"
        validated['batch_size'] = batch_size
    except (ValueError, TypeError):
        return False, None, "Batch size must be a valid integer"
    
    # Learning rate (1e-6 to 1e-2 - wide range for flexibility)
    try:
        learning_rate = float(params.get('learning_rate', 2e-5))
        if learning_rate < 1e-6 or learning_rate > 1e-2:
            return False, None, "Learning rate must be between 1e-6 (0.000001) and 1e-2 (0.01)"
        validated['learning_rate'] = learning_rate
    except (ValueError, TypeError):
        return False, None, "Learning rate must be a valid number"
    
    # Validation split (0.1-0.3)
    try:
        val_split = float(params.get('validation_split', 0.2))
        if val_split < 0.1 or val_split > 0.3:
            return False, None, "Validation split must be between 0.1 and 0.3"
        validated['validation_split'] = val_split
    except (ValueError, TypeError):
        return False, None, "Validation split must be a valid number"
    
    return True, validated, None


def secure_filename(filename):
    """
    Sanitize filename to prevent path traversal and other attacks.
    
    Args:
        filename: Original filename
    
    Returns:
        str: Sanitized filename
    """
    # Remove any directory components
    filename = filename.split('/')[-1].split('\\')[-1]
    
    # Remove potentially dangerous characters
    filename = re.sub(r'[^\w\s.-]', '', filename)
    
    # Remove path traversal attempts
    filename = filename.replace('..', '')
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:250] + ('.' + ext if ext else '')
    
    return filename or 'unnamed'


# ---------------------- JWT helpers ----------------------
def create_jwt_token(subject: str = 'public_api', expires_in: int = None):
    """Create a JWT token for the subject.

    Returns a compact JWT string.
    """
    expires_in = expires_in or JWT_EXP_SECONDS
    now = datetime.datetime.utcnow()
    payload = {
        'sub': subject,
        'iat': now,
        'exp': now + datetime.timedelta(seconds=expires_in)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # PyJWT >=2 returns str, <=1 returns bytes
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def verify_jwt_token(token: str):
    """Verify JWT token and return (is_valid, payload, error_message)"""
    if not token or not isinstance(token, str):
        return False, None, 'Missing token'
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return True, payload, None
    except jwt.ExpiredSignatureError:
        return False, None, 'Token expired'
    except jwt.InvalidTokenError as e:
        return False, None, f'Invalid token: {str(e)}'


def jwt_required(f):
    """Decorator to require JWT in Authorization header (Bearer)."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return jsonify({'error': 'Missing or malformed Authorization header'}), 401
        token = auth.split(' ', 1)[1].strip()
        is_valid, payload, err = verify_jwt_token(token)
        if not is_valid:
            return jsonify({'error': err}), 401
        # Attach payload to request context for downstream handlers if needed
        request.jwt_payload = payload
        return f(*args, **kwargs)
    return wrapped


def hash_password(password: str) -> str:
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate_user(username: str, password_hash: str):
    """Authenticate user with username and pre-hashed password.
    
    Client must send password already hashed with SHA256.
    
    Args:
        username: Username string
        password_hash: SHA256 hash of password (hexdigest)
    
    Returns:
        tuple: (is_valid, token_or_error)
    """
    if not username or not isinstance(username, str):
        return False, 'Username required'
    if not password_hash or not isinstance(password_hash, str):
        return False, 'Password hash required'
    
    # Validate credentials are configured
    if not API_USERNAME or not API_PASSWORD:
        return False, 'API credentials not configured on server'
    
    # Compute expected hash from stored plain password
    expected_hash = hashlib.sha256(API_PASSWORD.encode()).hexdigest()
    
    # Check username and password hash match
    if username != API_USERNAME or password_hash.lower() != expected_hash.lower():
        return False, 'Invalid credentials'
    
    # Create token with username as subject
    token = create_jwt_token(subject=username)
    return True, token
