import json
from typing import List, Optional
from datetime import datetime
from ...domain.models import ViewHistory
from ...domain.repositories import ViewHistoryRepository
from ...infrastructure.database import DatabaseConnection

class MySQLViewHistoryRepository(ViewHistoryRepository):
    def __init__(self):
        self.db_connection = DatabaseConnection()
    
    def create(self, history: ViewHistory) -> ViewHistory:
        """Create a new view history entry"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO view_history 
                (user_id, video_id, title, viewed_at, view_duration, completed)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    history.user_id,
                    history.video_id,
                    history.title,
                    history.viewed_at,
                    history.view_duration,
                    history.completed
                ))
                connection.commit()
                
                # Get the generated ID
                history.id = cursor.lastrowid
                return history
                
        except Exception as e:
            raise Exception(f"Error creating view history: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def get_by_user(self, user_id: int) -> List[ViewHistory]:
        """Get all view history for a user"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM view_history WHERE user_id = %s ORDER BY viewed_at DESC"
                cursor.execute(sql, (user_id,))
                results = cursor.fetchall()
                
                return [self._map_to_view_history(row) for row in results]
                
        except Exception as e:
            raise Exception(f"Error getting view history by user: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def update(self, history: ViewHistory) -> ViewHistory:
        """Update view history"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = """
                UPDATE view_history 
                SET title = %s, view_duration = %s, completed = %s
                WHERE id = %s
                """
                cursor.execute(sql, (
                    history.title,
                    history.view_duration,
                    history.completed,
                    history.id
                ))
                connection.commit()
                return history
                
        except Exception as e:
            raise Exception(f"Error updating view history: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def delete(self, history_id: int) -> bool:
        """Delete view history entry"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "DELETE FROM view_history WHERE id = %s"
                cursor.execute(sql, (history_id,))
                connection.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            raise Exception(f"Error deleting view history: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def record_view(self, user_id: int, video_id: str, title: str = '', 
                   view_duration: int = 0, completed: bool = False) -> ViewHistory:
        """Record a video view for a user"""
        try:
            history = ViewHistory(
                id=0,
                user_id=user_id,
                video_id=video_id,
                title=title,
                viewed_at=datetime.now(),
                view_duration=view_duration,
                completed=completed
            )
            return self.create(history)
        except Exception as e:
            raise Exception(f"Error recording view: {str(e)}")
    
    def _map_to_view_history(self, row: dict) -> ViewHistory:
        """Map database row to ViewHistory object"""
        return ViewHistory(
            id=row['id'],
            user_id=row['user_id'],
            video_id=row['video_id'],
            title=row['title'],
            viewed_at=row['viewed_at'],
            view_duration=row['view_duration'],
            completed=row['completed']
        ) 