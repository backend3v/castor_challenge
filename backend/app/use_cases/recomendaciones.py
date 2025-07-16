from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from ..domain.models import ViewHistory, UserPreferences
from ..domain.repositories import ViewHistoryRepository, UserPreferencesRepository
from ..infrastructure.youtube_api import YouTubeAPIService

class RecommendationsUseCase:
    def __init__(self, history_repo: ViewHistoryRepository, 
                 preferences_repo: UserPreferencesRepository, 
                 youtube_service: YouTubeAPIService):
        self.history_repo = history_repo
        self.preferences_repo = preferences_repo
        self.youtube_service = youtube_service
    
    def register_view(self, user_id: int, video_id: str, title: str, 
                     view_duration: int, completed: bool = False) -> ViewHistory:
        """Register a video viewing in user's history"""
        history = ViewHistory(
            id=0,  # Will be set by database
            user_id=user_id,
            video_id=video_id,
            title=title,
            viewed_at=datetime.now(),
            view_duration=view_duration,
            completed=completed
        )
        
        return self.history_repo.create(history)
    
    def get_recommendations(self, user_id: int, max_results: int = 10) -> List[Dict[str, Any]]:
        """Get personalized video recommendations for a user"""
        # Get user preferences
        preferences = self.preferences_repo.get_by_user(user_id)
        if not preferences:
            # Return general trending videos if no preferences
            return self.youtube_service.get_trending_videos(max_results=max_results)
        
        # Get recent viewing history
        history = self.history_repo.get_by_user(user_id)
        
        # Generate search queries based on preferences and history
        queries = self._generate_recommendation_queries(preferences, history)
        
        # Search for videos using generated queries
        recommendations = []
        for query in queries[:3]:  # Use top 3 queries
            try:
                videos = self.youtube_service.search_videos(query, max_results=max_results//3)
                recommendations.extend(videos)
            except Exception:
                continue
        
        # Remove duplicates and limit results
        seen_videos = set()
        unique_recommendations = []
        for video in recommendations:
            if video['video_id'] not in seen_videos and len(unique_recommendations) < max_results:
                seen_videos.add(video['video_id'])
                unique_recommendations.append(video)
        
        return unique_recommendations
    
    def update_preferences(self, user_id: int, genres: Optional[List[str]] = None,
                          topics: Optional[List[str]] = None, languages: Optional[List[str]] = None,
                          min_duration: Optional[int] = None, max_duration: Optional[int] = None) -> UserPreferences:
        """Update user preferences"""
        preferences = self.preferences_repo.get_by_user(user_id)
        
        if preferences:
            # Update existing preferences
            if genres is not None:
                preferences.genres = genres
            if topics is not None:
                preferences.topics = topics
            if languages is not None:
                preferences.languages = languages
            if min_duration is not None:
                preferences.min_duration = min_duration
            if max_duration is not None:
                preferences.max_duration = max_duration
            
            preferences.updated_at = datetime.now()
            return self.preferences_repo.update(preferences)
        else:
            # Create new preferences
            preferences = UserPreferences(
                id=0,
                user_id=user_id,
                genres=genres or [],
                topics=topics or [],
                languages=languages or [],
                min_duration=min_duration,
                max_duration=max_duration
            )
            return self.preferences_repo.create(preferences)
    
    def get_view_history(self, user_id: int, days_back: int = 30) -> List[ViewHistory]:
        """Get user's viewing history for the last N days"""
        history = self.history_repo.get_by_user(user_id)
        limit_date = datetime.now() - timedelta(days=days_back)
        
        return [h for h in history if h.viewed_at >= limit_date]
    
    def remove_from_history(self, history_id: int) -> bool:
        """Remove a video from viewing history"""
        return self.history_repo.delete(history_id)
    
    def _generate_recommendation_queries(self, preferences: UserPreferences, history: List[ViewHistory]) -> List[str]:
        """Generate search queries based on user preferences and viewing history"""
        queries = []
        
        # Add queries based on user preferences
        if preferences.topics:
            queries.extend(preferences.topics[:3])  # Top 3 topics
        
        if preferences.genres:
            queries.extend(preferences.genres[:2])  # Top 2 genres
        
        # Add queries based on recent viewing history
        if history:
            # Get most viewed videos in the last week
            one_week_ago = datetime.now() - timedelta(days=7)
            recent_videos = [h for h in history if h.viewed_at >= one_week_ago]
            
            if recent_videos:
                # Extract keywords from recent video titles
                titles = [h.title for h in recent_videos]
                keywords = self._extract_keywords(titles)
                queries.extend(keywords[:2])  # Top 2 keywords
        
        # Add some general popular topics if we don't have enough queries
        if len(queries) < 3:
            queries.extend(['music', 'technology', 'gaming'])
        
        return queries[:5]  # Return top 5 queries
    
    def _extract_keywords(self, titles: List[str]) -> List[str]:
        """Extract keywords from video titles"""
        # Simple keyword extraction - in a real implementation, you might use NLP
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        all_words = []
        for title in titles:
            words = title.lower().split()
            filtered_words = [w for w in words if w not in common_words and len(w) > 2]
            all_words.extend(filtered_words)
        
        # Count word frequency
        from collections import Counter
        counter = Counter(all_words)
        
        return [word for word, _ in counter.most_common(5)] 