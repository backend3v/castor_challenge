from datetime import datetime, timedelta
from typing import Optional, List
from ...domain.models import User, UserSession, RefreshToken, UserRole, AuthAuditLog
from ..database import DatabaseConnection
import hashlib
import secrets

class MySQLAuthRepository:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_user(self, user: User) -> User:
        """Create a new user with authentication data"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO users (name, email, password_hash, created_at, is_active, email_verified)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    user.name,
                    user.email,
                    user.password_hash,
                    user.created_at,
                    user.is_active,
                    user.email_verified
                ))
                user.id = cursor.lastrowid
                connection.commit()
                
                # Create default role for user
                self._create_default_role(user.id)
                
            connection.close()
            return user
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = """
                SELECT id, name, email, password_hash, created_at, is_active, email_verified
                FROM users WHERE email = %s
                """
                cursor.execute(sql, (email,))
                result = cursor.fetchone()
            connection.close()
            
            if result:
                return User(
                    id=result['id'],
                    name=result['name'],
                    email=result['email'],
                    password_hash=result['password_hash'],
                    created_at=result['created_at'],
                    is_active=result['is_active'],
                    email_verified=result['email_verified']
                )
            return None
        except Exception as e:
            raise Exception(f"Error getting user by email: {str(e)}")
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = """
                SELECT id, name, email, password_hash, created_at, is_active, email_verified
                FROM users WHERE id = %s
                """
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
            connection.close()
            
            if result:
                return User(
                    id=result['id'],
                    name=result['name'],
                    email=result['email'],
                    password_hash=result['password_hash'],
                    created_at=result['created_at'],
                    is_active=result['is_active'],
                    email_verified=result['email_verified']
                )
            return None
        except Exception as e:
            raise Exception(f"Error getting user by ID: {str(e)}")
    
    def update_last_login(self, user_id: int) -> bool:
        """Update user's last login timestamp"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = "UPDATE users SET last_login = %s WHERE id = %s"
                cursor.execute(sql, (datetime.now(), user_id))
                connection.commit()
            connection.close()
            return True
        except Exception as e:
            raise Exception(f"Error updating last login: {str(e)}")
    
    def create_session(self, session: UserSession) -> UserSession:
        """Create a new user session"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO user_sessions (user_id, token_hash, expires_at, created_at, last_activity, is_active)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    session.user_id,
                    session.token_hash,
                    session.expires_at,
                    session.created_at,
                    session.last_activity,
                    session.is_active
                ))
                session.id = cursor.lastrowid
                connection.commit()
            connection.close()
            return session
        except Exception as e:
            raise Exception(f"Error creating session: {str(e)}")
    
    def get_session_by_token(self, token_hash: str) -> Optional[UserSession]:
        """Get session by token hash"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = """
                SELECT id, user_id, token_hash, expires_at, created_at, last_activity, is_active
                FROM user_sessions 
                WHERE token_hash = %s AND is_active = TRUE AND expires_at > %s
                """
                cursor.execute(sql, (token_hash, datetime.now()))
                result = cursor.fetchone()
            connection.close()
            
            if result:
                return UserSession(
                    id=result['id'],
                    user_id=result['user_id'],
                    token_hash=result['token_hash'],
                    expires_at=result['expires_at'],
                    created_at=result['created_at'],
                    last_activity=result['last_activity'],
                    is_active=result['is_active']
                )
            return None
        except Exception as e:
            raise Exception(f"Error getting session: {str(e)}")
    
    def update_session_activity(self, session_id: int) -> bool:
        """Update session last activity"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = "UPDATE user_sessions SET last_activity = %s WHERE id = %s"
                cursor.execute(sql, (datetime.now(), session_id))
                connection.commit()
            connection.close()
            return True
        except Exception as e:
            raise Exception(f"Error updating session activity: {str(e)}")
    
    def deactivate_session(self, session_id: int) -> bool:
        """Deactivate a session"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = "UPDATE user_sessions SET is_active = FALSE WHERE id = %s"
                cursor.execute(sql, (session_id,))
                connection.commit()
            connection.close()
            return True
        except Exception as e:
            raise Exception(f"Error deactivating session: {str(e)}")
    
    def deactivate_all_user_sessions(self, user_id: int) -> bool:
        """Deactivate all sessions for a user"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = "UPDATE user_sessions SET is_active = FALSE WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                connection.commit()
            connection.close()
            return True
        except Exception as e:
            raise Exception(f"Error deactivating user sessions: {str(e)}")
    
    def create_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        """Create a new refresh token"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO refresh_tokens (user_id, token_hash, expires_at, created_at, is_revoked)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    refresh_token.user_id,
                    refresh_token.token_hash,
                    refresh_token.expires_at,
                    refresh_token.created_at,
                    refresh_token.is_revoked
                ))
                refresh_token.id = cursor.lastrowid
                connection.commit()
            connection.close()
            return refresh_token
        except Exception as e:
            raise Exception(f"Error creating refresh token: {str(e)}")
    
    def get_refresh_token(self, token_hash: str) -> Optional[RefreshToken]:
        """Get refresh token by hash"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = """
                SELECT id, user_id, token_hash, expires_at, created_at, is_revoked
                FROM refresh_tokens 
                WHERE token_hash = %s AND is_revoked = FALSE AND expires_at > %s
                """
                cursor.execute(sql, (token_hash, datetime.now()))
                result = cursor.fetchone()
            connection.close()
            
            if result:
                return RefreshToken(
                    id=result['id'],
                    user_id=result['user_id'],
                    token_hash=result['token_hash'],
                    expires_at=result['expires_at'],
                    created_at=result['created_at'],
                    is_revoked=result['is_revoked']
                )
            return None
        except Exception as e:
            raise Exception(f"Error getting refresh token: {str(e)}")
    
    def revoke_refresh_token(self, token_hash: str) -> bool:
        """Revoke a refresh token"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = "UPDATE refresh_tokens SET is_revoked = TRUE WHERE token_hash = %s"
                cursor.execute(sql, (token_hash,))
                connection.commit()
            connection.close()
            return True
        except Exception as e:
            raise Exception(f"Error revoking refresh token: {str(e)}")
    
    def get_user_roles(self, user_id: int) -> List[UserRole]:
        """Get all roles for a user"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT id, user_id, role_name, created_at FROM user_roles WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                results = cursor.fetchall()
            connection.close()
            
            return [
                UserRole(
                    id=row['id'],
                    user_id=row['user_id'],
                    role_name=row['role_name'],
                    created_at=row['created_at']
                ) for row in results
            ]
        except Exception as e:
            raise Exception(f"Error getting user roles: {str(e)}")
    
    def add_user_role(self, user_id: int, role_name: str) -> UserRole:
        """Add a role to a user"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = "INSERT INTO user_roles (user_id, role_name) VALUES (%s, %s)"
                cursor.execute(sql, (user_id, role_name))
                role_id = cursor.lastrowid
                connection.commit()
            connection.close()
            
            return UserRole(
                id=role_id,
                user_id=user_id,
                role_name=role_name
            )
        except Exception as e:
            raise Exception(f"Error adding user role: {str(e)}")
    
    def log_auth_event(self, audit_log: AuthAuditLog) -> AuthAuditLog:
        """Log an authentication event"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO auth_audit_log (user_id, action, ip_address, user_agent, success, details)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    audit_log.user_id,
                    audit_log.action,
                    audit_log.ip_address,
                    audit_log.user_agent,
                    audit_log.success,
                    str(audit_log.details) if audit_log.details else None
                ))
                audit_log.id = cursor.lastrowid
                connection.commit()
            connection.close()
            return audit_log
        except Exception as e:
            raise Exception(f"Error logging auth event: {str(e)}")
    
    def _create_default_role(self, user_id: int) -> None:
        """Create default 'user' role for new user"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = "INSERT INTO user_roles (user_id, role_name) VALUES (%s, 'user')"
                cursor.execute(sql, (user_id,))
                connection.commit()
            connection.close()
        except Exception as e:
            # Log error but don't fail user creation
            print(f"Warning: Could not create default role for user {user_id}: {str(e)}")
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions and return count of cleaned sessions"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = "UPDATE user_sessions SET is_active = FALSE WHERE expires_at < %s AND is_active = TRUE"
                cursor.execute(sql, (datetime.now(),))
                cleaned_count = cursor.rowcount
                connection.commit()
            connection.close()
            return cleaned_count
        except Exception as e:
            raise Exception(f"Error cleaning up expired sessions: {str(e)}")
    
    def cleanup_expired_refresh_tokens(self) -> int:
        """Clean up expired refresh tokens and return count of cleaned tokens"""
        try:
            connection = self.db.get_connection()
            with connection.cursor() as cursor:
                sql = "UPDATE refresh_tokens SET is_revoked = TRUE WHERE expires_at < %s AND is_revoked = FALSE"
                cursor.execute(sql, (datetime.now(),))
                cleaned_count = cursor.rowcount
                connection.commit()
            connection.close()
            return cleaned_count
        except Exception as e:
            raise Exception(f"Error cleaning up expired refresh tokens: {str(e)}") 