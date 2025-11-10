"""
JWT Authentication Module for Public API
Similar to Lauba authentication system
"""
import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS
import secrets
import hashlib


# API Keys storage (in production, move to database)
# Format: {api_key: {username, created_at, is_active, rate_limit}}
API_KEYS_DB = {}


def generate_api_key(username):
    """
    Generate a new API key for a user.
    
    Args:
        username: Username for the API key
        
    Returns:
        str: Generated API key
    """
    # Generate secure random API key
    api_key = f"dd_{secrets.token_urlsafe(32)}"
    
    # Store in database (in production, use actual database)
    API_KEYS_DB[api_key] = {
        'username': username,
        'created_at': datetime.datetime.utcnow(),
        'is_active': True,
        'rate_limit': 100  # Default 100 requests per day
    }
    
    return api_key


def validate_api_key(api_key):
    """
    Validate an API key.
    
    Args:
        api_key: API key to validate
        
    Returns:
        tuple: (is_valid, user_info, error_message)
    """
    if not api_key:
        return False, None, "API key is required"
    
    if not api_key.startswith("dd_"):
        return False, None, "Invalid API key format"
    
    user_info = API_KEYS_DB.get(api_key)
    
    if not user_info:
        return False, None, "Invalid API key"
    
    if not user_info.get('is_active', False):
        return False, None, "API key is inactive"
    
    return True, user_info, None


def generate_jwt_token(api_key, user_info):
    """
    Generate JWT token from validated API key.
    
    Args:
        api_key: Validated API key
        user_info: User information dictionary
        
    Returns:
        str: JWT token
    """
    payload = {
        'api_key': api_key,
        'username': user_info['username'],
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt_token(token):
    """
    Verify and decode JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        tuple: (is_valid, payload, error_message)
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
        # Additional validation: check if API key is still valid
        api_key = payload.get('api_key')
        is_valid, user_info, error_msg = validate_api_key(api_key)
        
        if not is_valid:
            return False, None, error_msg
        
        return True, payload, None
        
    except jwt.ExpiredSignatureError:
        return False, None, "Token has expired"
    except jwt.InvalidTokenError as e:
        return False, None, f"Invalid token: {str(e)}"


def require_jwt_auth(f):
    """
    Decorator to require JWT authentication for API endpoints.
    
    Usage:
        @app.route('/api/public/checkDeception', methods=['POST'])
        @require_jwt_auth
        def check_deception():
            # Access token payload via request.token_payload
            username = request.token_payload['username']
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'error': 'Authorization header is required',
                'message': 'Please provide a valid JWT token in Authorization header as "Bearer <token>"'
            }), 401
        
        # Extract token from "Bearer <token>" format
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({
                'error': 'Invalid Authorization header format',
                'message': 'Authorization header must be in format: "Bearer <token>"'
            }), 401
        
        token = parts[1]
        
        # Verify token
        is_valid, payload, error_msg = verify_jwt_token(token)
        
        if not is_valid:
            return jsonify({
                'error': 'Authentication failed',
                'message': error_msg
            }), 401
        
        # Attach payload to request for use in endpoint
        request.token_payload = payload
        
        return f(*args, **kwargs)
    
    return decorated_function


def rate_limit_user(user_info, endpoint_name):
    """
    Check if user has exceeded their rate limit.
    
    Args:
        user_info: User information dictionary
        endpoint_name: Name of the endpoint being accessed
        
    Returns:
        tuple: (is_allowed, remaining_requests, error_message)
    """
    # TODO: Implement actual rate limiting with Redis or database
    # For now, return True
    rate_limit = user_info.get('rate_limit', 100)
    return True, rate_limit, None


def init_demo_api_keys():
    """
    Initialize demo API keys for testing.
    In production, remove this and use proper user registration.
    """
    demo_keys = [
        ('demo_user', generate_api_key('demo_user')),
        ('test_user', generate_api_key('test_user'))
    ]
    
    print("🔑 Demo API Keys Generated:")
    for username, api_key in demo_keys:
        print(f"   {username}: {api_key}")
    
    return demo_keys


# Initialize demo keys on module import (remove in production)
if not API_KEYS_DB:
    init_demo_api_keys()
