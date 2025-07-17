import json
from typing import List, Optional
from datetime import datetime
from ...domain.models import User
from ...domain.repositories import UserRepository
from ...infrastructure.database import DatabaseConnection

class MySQLUserRepository(UserRepository):
    def __init__(self):
        self.db_connection = DatabaseConnection()
    
    def create(self, user: User) -> User:
        """Create a new user"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO users (name, email, created_at, active)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    user.name,
                    user.email,
                    user.created_at,
                    user.active
                ))
                connection.commit()
                
                # Get the generated ID
                user.id = cursor.lastrowid
                return user
                
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE id = %s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                
                if result:
                    return self._map_to_user(result)
                return None
                
        except Exception as e:
            raise Exception(f"Error getting user by ID: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE email = %s"
                cursor.execute(sql, (email,))
                result = cursor.fetchone()
                
                if result:
                    return self._map_to_user(result)
                return None
                
        except Exception as e:
            raise Exception(f"Error getting user by email: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def get_all(self) -> List[User]:
        """Get all users"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users ORDER BY name ASC"
                cursor.execute(sql)
                results = cursor.fetchall()
                
                return [self._map_to_user(row) for row in results]
                
        except Exception as e:
            raise Exception(f"Error getting all users: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def search_by_name(self, name: str) -> List[User]:
        """Search users by name (partial match)"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM users WHERE name LIKE %s ORDER BY name ASC"
                cursor.execute(sql, (f'%{name}%',))
                results = cursor.fetchall()
                
                return [self._map_to_user(row) for row in results]
                
        except Exception as e:
            raise Exception(f"Error searching users by name: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def update(self, user: User) -> User:
        """Update user"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = """
                UPDATE users 
                SET name = %s, email = %s, active = %s
                WHERE id = %s
                """
                cursor.execute(sql, (
                    user.name,
                    user.email,
                    user.active,
                    user.id
                ))
                connection.commit()
                return user
                
        except Exception as e:
            raise Exception(f"Error updating user: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def delete(self, user_id: int) -> bool:
        """Delete user"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "DELETE FROM users WHERE id = %s"
                cursor.execute(sql, (user_id,))
                connection.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            raise Exception(f"Error deleting user: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def _map_to_user(self, row: dict) -> User:
        """Map database row to User object"""
        return User(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            created_at=row['created_at'],
            active=row['active']
        ) 