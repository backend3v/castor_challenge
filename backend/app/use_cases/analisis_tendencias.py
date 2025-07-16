from typing import List, Optional, Dict, Any
from datetime import datetime
from ..domain.models import TrendAnalysis
from ..domain.repositories import TrendAnalysisRepository
from ..infrastructure.youtube_api import YouTubeAPIService

class TrendAnalysisUseCase:
    def __init__(self, analysis_repo: TrendAnalysisRepository, youtube_service: YouTubeAPIService):
        self.analysis_repo = analysis_repo
        self.youtube_service = youtube_service
    
    def create_trend_analysis(self, user_id: int, category: str, region: str = "US", max_results: int = 20) -> TrendAnalysis:
        """Create a new trend analysis for a specific category"""
        # Get trending videos from YouTube API
        trending_videos = self.youtube_service.get_trending_videos(region, None, max_results)
        
        # Calculate statistics
        statistics = self._calculate_statistics(trending_videos)
        
        # Create analysis object
        analysis = TrendAnalysis(
            id=0,  # Will be set by database
            user_id=user_id,
            category=category,
            region=region,
            analyzed_at=datetime.now(),
            results={
                'videos': trending_videos,
                'statistics': statistics,
                'total_videos': len(trending_videos)
            },
            criteria={
                'max_results': max_results,
                'region': region
            }
        )
        
        return self.analysis_repo.create(analysis)
    
    def list_user_analyses(self, user_id: int) -> List[TrendAnalysis]:
        """List all trend analyses for a user"""
        return self.analysis_repo.get_by_user(user_id)
    
    def get_analysis_by_id(self, analysis_id: int) -> Optional[TrendAnalysis]:
        """Get a specific trend analysis by ID"""
        return self.analysis_repo.get_by_id(analysis_id)
    
    def update_analysis_criteria(self, analysis_id: int, new_criteria: Dict[str, Any]) -> TrendAnalysis:
        """Update analysis criteria"""
        analysis = self.analysis_repo.get_by_id(analysis_id)
        if not analysis:
            raise Exception("Analysis not found")
        
        analysis.criteria.update(new_criteria)
        return self.analysis_repo.update(analysis)
    
    def delete_analysis(self, analysis_id: int) -> bool:
        """Delete a trend analysis"""
        return self.analysis_repo.delete(analysis_id)
    
    def get_available_categories(self, region: str = "US") -> List[Dict[str, Any]]:
        """Get available video categories for trend analysis"""
        return self.youtube_service.get_video_categories(region)
    
    def _calculate_statistics(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics from trending videos"""
        if not videos:
            return {}
        
        total_views = sum(video.get('view_count', 0) for video in videos)
        total_likes = sum(video.get('like_count', 0) for video in videos)
        total_comments = sum(video.get('comment_count', 0) for video in videos)
        
        # Find top performing videos
        top_by_views = max(videos, key=lambda x: x.get('view_count', 0))
        top_by_likes = max(videos, key=lambda x: x.get('like_count', 0))
        
        return {
            'total_views': total_views,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'average_views': total_views // len(videos),
            'average_likes': total_likes // len(videos),
            'average_comments': total_comments // len(videos),
            'top_video_views': {
                'title': top_by_views.get('title', ''),
                'views': top_by_views.get('view_count', 0),
                'channel': top_by_views.get('channel_title', '')
            },
            'top_video_likes': {
                'title': top_by_likes.get('title', ''),
                'likes': top_by_likes.get('like_count', 0),
                'channel': top_by_likes.get('channel_title', '')
            }
        } 