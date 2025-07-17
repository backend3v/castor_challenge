import bcrypt
from typing import Optional, Dict, Any, Tuple
from ..domain.models import User
from .repositories.auth_repository import MySQLAuthRepository

class AuthService:
    def __init__(self):
        self.auth_repo = MySQLAuthRepository()
    
    def hash_password(self, password: str) -> str:
        """Hash a password and return the hash"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception:
            return False
    
    def register_user(self, name: str, email: str, password: str) -> Dict[str, Any]:
        """Register a new user (simple)"""
        try:
            existing_user = self.auth_repo.get_user_by_email(email)
            if existing_user:
                return {
                    'success': False,
                    'error': 'User with this email already exists'
                }
            password_hash = self.hash_password(password)
            user = User(
                id=0,
                name=name,
                email=email,
                password_hash=password_hash,
                is_active=True,
                email_verified=False
            )
            user = self.auth_repo.create_user(user)
            return {
                'success': True,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'created_at': user.created_at.isoformat()
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Login a user (simple)"""
        try:
            user = self.auth_repo.get_user_by_email(email)
            if not user or not user.is_active:
                return {
                    'success': False,
                    'error': 'Invalid email or password'
                }
            if not self.verify_password(password, user.password_hash):
                return {
                    'success': False,
                    'error': 'Invalid email or password'
                }
            return {
                'success': True,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            } 