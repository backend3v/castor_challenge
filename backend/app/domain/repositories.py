from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from .models import User, FavoriteVideo, TrendAnalysis, ViewHistory, UserPreferences

class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass

class FavoriteVideoRepository(ABC):
    @abstractmethod
    def create(self, video: FavoriteVideo) -> FavoriteVideo:
        pass
    
    @abstractmethod
    def get_by_id(self, video_id: int) -> Optional[FavoriteVideo]:
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[FavoriteVideo]:
        pass
    
    @abstractmethod
    def get_by_youtube_id(self, user_id: int, youtube_video_id: str) -> Optional[FavoriteVideo]:
        pass
    
    @abstractmethod
    def update(self, video: FavoriteVideo) -> FavoriteVideo:
        pass
    
    @abstractmethod
    def delete(self, video_id: int) -> bool:
        pass

class TrendAnalysisRepository(ABC):
    @abstractmethod
    def create(self, analysis: TrendAnalysis) -> TrendAnalysis:
        pass
    
    @abstractmethod
    def get_by_id(self, analysis_id: int) -> Optional[TrendAnalysis]:
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[TrendAnalysis]:
        pass
    
    @abstractmethod
    def update(self, analysis: TrendAnalysis) -> TrendAnalysis:
        pass
    
    @abstractmethod
    def delete(self, analysis_id: int) -> bool:
        pass

class ViewHistoryRepository(ABC):
    @abstractmethod
    def create(self, history: ViewHistory) -> ViewHistory:
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: int) -> List[ViewHistory]:
        pass
    
    @abstractmethod
    def update(self, history: ViewHistory) -> ViewHistory:
        pass
    
    @abstractmethod
    def delete(self, history_id: int) -> bool:
        pass

class UserPreferencesRepository(ABC):
    @abstractmethod
    def create(self, preferences: UserPreferences) -> UserPreferences:
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: int) -> Optional[UserPreferences]:
        pass
    
    @abstractmethod
    def update(self, preferences: UserPreferences) -> UserPreferences:
        pass
    
    @abstractmethod
    def delete(self, preferences_id: int) -> bool:
        pass 