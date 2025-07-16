import json
from typing import List, Optional
from datetime import datetime
from ...domain.models import UserPreferences
from ...domain.repositories import UserPreferencesRepository
from ...infrastructure.database import DatabaseConnection

class MySQLUserPreferencesRepository(UserPreferencesRepository):
    def __init__(self):
        self.db_connection = DatabaseConnection()
    
    def create(self, preferences: UserPreferences) -> UserPreferences:
        """Create new user preferences"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO user_preferences 
                (user_id, genres, topics, languages, min_duration, max_duration)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    preferences.user_id,
                    json.dumps(preferences.genres) if preferences.genres else None,
                    json.dumps(preferences.topics) if preferences.topics else None,
                    json.dumps(preferences.languages) if preferences.languages else None,
                    preferences.min_duration,
                    preferences.max_duration
                ))
                connection.commit()
                
                # Get the generated ID
                preferences.id = cursor.lastrowid
                return preferences
                
        except Exception as e:
            raise Exception(f"Error creating user preferences: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def get_by_user(self, user_id: int) -> Optional[UserPreferences]:
        """Get user preferences by user ID"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM user_preferences WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                result = cursor.fetchone()
                
                if result:
                    return self._map_to_user_preferences(result)
                return None
                
        except Exception as e:
            raise Exception(f"Error getting user preferences: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def update(self, preferences: UserPreferences) -> UserPreferences:
        """Update user preferences"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = """
                UPDATE user_preferences 
                SET genres = %s, topics = %s, languages = %s, min_duration = %s, max_duration = %s
                WHERE id = %s
                """
                cursor.execute(sql, (
                    json.dumps(preferences.genres) if preferences.genres else None,
                    json.dumps(preferences.topics) if preferences.topics else None,
                    json.dumps(preferences.languages) if preferences.languages else None,
                    preferences.min_duration,
                    preferences.max_duration,
                    preferences.id
                ))
                connection.commit()
                return preferences
                
        except Exception as e:
            raise Exception(f"Error updating user preferences: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def delete(self, preferences_id: int) -> bool:
        """Delete user preferences"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "DELETE FROM user_preferences WHERE id = %s"
                cursor.execute(sql, (preferences_id,))
                connection.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            raise Exception(f"Error deleting user preferences: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def _map_to_user_preferences(self, row: dict) -> UserPreferences:
        """Map database row to UserPreferences object"""
        return UserPreferences(
            id=row['id'],
            user_id=row['user_id'],
            genres=json.loads(row['genres']) if row['genres'] else [],
            topics=json.loads(row['topics']) if row['topics'] else [],
            languages=json.loads(row['languages']) if row['languages'] else [],
            min_duration=row['min_duration'],
            max_duration=row['max_duration'],
            updated_at=row['updated_at']
        ) 