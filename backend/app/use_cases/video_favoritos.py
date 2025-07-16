from typing import List, Optional, Dict, Any
from datetime import datetime
from ..domain.models import FavoriteVideo
from ..domain.repositories import FavoriteVideoRepository
from ..infrastructure.youtube_api import YouTubeAPIService

class FavoriteVideosUseCase:
    def __init__(self, video_repo: FavoriteVideoRepository, youtube_service: YouTubeAPIService):
        self.video_repo = video_repo
        self.youtube_service = youtube_service
    
    def add_favorite_video(self, user_id: int, video_id: str, notes: Optional[str] = None, tags: Optional[List[str]] = None) -> FavoriteVideo:
        """Add a video to user's favorites"""
        # Check if video already exists in favorites
        existing_video = self.video_repo.get_by_youtube_id(user_id, video_id)
        if existing_video:
            raise Exception("Video already exists in favorites")
        
        # Get video details from YouTube API
        video_details = self.youtube_service.get_video_details(video_id)
        if not video_details:
            raise Exception("Video not found on YouTube")
        
        # Create FavoriteVideo object
        favorite_video = FavoriteVideo(
            id=0,  # Will be set by database
            user_id=user_id,
            video_id=video_id,
            title=video_details['title'],
            description=video_details['description'],
            url=video_details['url'],
            thumbnail=video_details['thumbnail'],
            channel=video_details['channel_title'],
            duration=video_details['duration'],
            published_at=datetime.fromisoformat(video_details['published_at'].replace('Z', '+00:00')),
            notes=notes,
            tags=tags or []
        )
        
        return self.video_repo.create(favorite_video)
    
    def list_favorite_videos(self, user_id: int) -> List[FavoriteVideo]:
        """List all favorite videos for a user"""
        return self.video_repo.get_by_user(user_id)
    
    def update_favorite_video(self, video_id: int, notes: Optional[str] = None, tags: Optional[List[str]] = None) -> FavoriteVideo:
        """Update a favorite video's notes and tags"""
        video = self.video_repo.get_by_id(video_id)
        if not video:
            raise Exception("Video not found in favorites")
        
        if notes is not None:
            video.notes = notes
        if tags is not None:
            video.tags = tags
        
        return self.video_repo.update(video)
    
    def remove_favorite_video(self, video_id: int) -> bool:
        """Remove a video from favorites"""
        return self.video_repo.delete(video_id)
    
    def search_youtube_videos(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for videos on YouTube"""
        return self.youtube_service.search_videos(query, max_results) 