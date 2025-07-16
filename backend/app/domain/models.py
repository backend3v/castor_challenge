from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any, Union

@dataclass
class User:
    id: int
    name: str
    email: str
    created_at: datetime
    active: bool = True

@dataclass
class FavoriteVideo:
    id: int
    user_id: int
    video_id: str  # YouTube video ID
    title: str
    description: str
    url: str
    thumbnail: str
    channel: str
    duration: str
    published_at: datetime
    notes: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    added_at: datetime = field(default_factory=datetime.now)

@dataclass
class TrendAnalysis:
    id: int
    user_id: int
    category: str
    region: str
    analyzed_at: datetime
    results: Dict[str, Any]  # JSON with statistics and videos
    criteria: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ViewHistory:
    id: int
    user_id: int
    video_id: str
    title: str
    viewed_at: datetime
    view_duration: int  # in seconds
    completed: bool = False

@dataclass
class UserPreferences:
    id: int
    user_id: int
    genres: List[str]
    topics: List[str]
    languages: List[str]
    min_duration: Optional[int] = None  # in seconds
    max_duration: Optional[int] = None  # in seconds
    updated_at: datetime = field(default_factory=datetime.now) 