from functools import wraps
from flask import request, jsonify
from .auth_service import AuthService

def require_auth(f):
    """Decorator to require authentication for a route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({
                'success': False,
                'error': 'Authorization header is required'
            }), 401
        
        # Check if it's a Bearer token
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Invalid authorization header format. Use: Bearer <token>'
            }), 401
        
        # Extract token
        token = auth_header.split(' ')[1]
        
        # Verify token
        auth_service = AuthService()
        payload = auth_service.verify_token(token)
        
        if not payload:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token'
            }), 401
        
        # Add user info to request
        request.user_id = payload.get('user_id')
        request.user_email = payload.get('email')
        request.user_name = payload.get('name')
        
        return f(*args, **kwargs)
    
    return decorated_function

def optional_auth(f):
    """Decorator for routes that can work with or without authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            auth_service = AuthService()
            payload = auth_service.verify_token(token)
            
            if payload:
                # Add user info to request
                request.user_id = payload.get('user_id')
                request.user_email = payload.get('email')
                request.user_name = payload.get('name')
                request.is_authenticated = True
            else:
                request.is_authenticated = False
        else:
            request.is_authenticated = False
        
        return f(*args, **kwargs)
    
    return decorated_function 