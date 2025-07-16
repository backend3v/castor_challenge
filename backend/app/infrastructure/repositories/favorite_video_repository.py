import json
from typing import List, Optional
from datetime import datetime
from ...domain.models import FavoriteVideo
from ...domain.repositories import FavoriteVideoRepository
from ...infrastructure.database import DatabaseConnection

class MySQLFavoriteVideoRepository(FavoriteVideoRepository):
    def __init__(self):
        self.db_connection = DatabaseConnection()
    
    def create(self, video: FavoriteVideo) -> FavoriteVideo:
        """Create a new favorite video"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO favorite_videos 
                (user_id, video_id, title, description, url, thumbnail, channel, duration, published_at, notes, tags)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    video.user_id,
                    video.video_id,
                    video.title,
                    video.description,
                    video.url,
                    video.thumbnail,
                    video.channel,
                    video.duration,
                    video.published_at,
                    video.notes,
                    json.dumps(video.tags) if video.tags else None
                ))
                connection.commit()
                
                # Get the generated ID
                video.id = cursor.lastrowid
                return video
                
        except Exception as e:
            raise Exception(f"Error creating favorite video: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def get_by_id(self, video_id: int) -> Optional[FavoriteVideo]:
        """Get favorite video by ID"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM favorite_videos WHERE id = %s"
                cursor.execute(sql, (video_id,))
                result = cursor.fetchone()
                
                if result:
                    return self._map_to_favorite_video(result)
                return None
                
        except Exception as e:
            raise Exception(f"Error getting favorite video by ID: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def get_by_user(self, user_id: int) -> List[FavoriteVideo]:
        """Get all favorite videos for a user"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM favorite_videos WHERE user_id = %s ORDER BY added_at DESC"
                cursor.execute(sql, (user_id,))
                results = cursor.fetchall()
                
                return [self._map_to_favorite_video(row) for row in results]
                
        except Exception as e:
            raise Exception(f"Error getting favorite videos by user: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def get_by_youtube_id(self, user_id: int, youtube_video_id: str) -> Optional[FavoriteVideo]:
        """Get favorite video by YouTube ID and user"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "SELECT * FROM favorite_videos WHERE user_id = %s AND video_id = %s"
                cursor.execute(sql, (user_id, youtube_video_id))
                result = cursor.fetchone()
                
                if result:
                    return self._map_to_favorite_video(result)
                return None
                
        except Exception as e:
            raise Exception(f"Error getting favorite video by YouTube ID: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def update(self, video: FavoriteVideo) -> FavoriteVideo:
        """Update favorite video"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = """
                UPDATE favorite_videos 
                SET title = %s, description = %s, url = %s, thumbnail = %s, 
                    channel = %s, duration = %s, published_at = %s, notes = %s, tags = %s
                WHERE id = %s
                """
                cursor.execute(sql, (
                    video.title,
                    video.description,
                    video.url,
                    video.thumbnail,
                    video.channel,
                    video.duration,
                    video.published_at,
                    video.notes,
                    json.dumps(video.tags) if video.tags else None,
                    video.id
                ))
                connection.commit()
                return video
                
        except Exception as e:
            raise Exception(f"Error updating favorite video: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def delete(self, video_id: int) -> bool:
        """Delete favorite video"""
        try:
            connection = self.db_connection.get_connection()
            with connection.cursor() as cursor:
                sql = "DELETE FROM favorite_videos WHERE id = %s"
                cursor.execute(sql, (video_id,))
                connection.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            raise Exception(f"Error deleting favorite video: {str(e)}")
        finally:
            if connection:
                connection.close()
    
    def _map_to_favorite_video(self, row: dict) -> FavoriteVideo:
        """Map database row to FavoriteVideo object"""
        return FavoriteVideo(
            id=row['id'],
            user_id=row['user_id'],
            video_id=row['video_id'],
            title=row['title'],
            description=row['description'],
            url=row['url'],
            thumbnail=row['thumbnail'],
            channel=row['channel'],
            duration=row['duration'],
            published_at=row['published_at'],
            notes=row['notes'],
            tags=json.loads(row['tags']) if row['tags'] else [],
            added_at=row['added_at']
        ) 