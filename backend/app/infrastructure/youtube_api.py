import requests
from typing import Dict, List, Optional, Any
from ..config import Config

class YouTubeAPIService:
    def __init__(self):
        self.config = Config()
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.api_key = self.config.YOUTUBE_API_KEY
        
        if not self.api_key:
            raise Exception("YouTube API key not configured")
    
    def search_videos(self, query: str, max_results: int = 10, region_code: str = "US") -> List[Dict[str, Any]]:
        """Search for videos using YouTube Data API"""
        try:
            url = f"{self.base_url}/search"
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'maxResults': max_results,
                'regionCode': region_code,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._format_search_results(data.get('items', []))
            
        except requests.RequestException as e:
            raise Exception(f"YouTube API request failed: {str(e)}")
    
    def get_video_details(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific video"""
        try:
            url = f"{self.base_url}/videos"
            params = {
                'part': 'snippet,statistics,contentDetails',
                'id': video_id,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            items = data.get('items', [])
            
            if items:
                return self._format_video_details(items[0])
            return None
            
        except requests.RequestException as e:
            raise Exception(f"YouTube API request failed: {str(e)}")
    
    def get_trending_videos(self, region_code: str = "US", category_id: Optional[str] = None, max_results: int = 20) -> List[Dict[str, Any]]:
        """Get trending videos for a specific region and category"""
        try:
            url = f"{self.base_url}/videos"
            params = {
                'part': 'snippet,statistics,contentDetails',
                'chart': 'mostPopular',
                'regionCode': region_code,
                'maxResults': max_results,
                'key': self.api_key
            }
            
            if category_id:
                params['videoCategoryId'] = category_id
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return [self._format_video_details(item) for item in data.get('items', [])]
            
        except requests.RequestException as e:
            raise Exception(f"YouTube API request failed: {str(e)}")
    
    def get_video_categories(self, region_code: str = "US") -> List[Dict[str, Any]]:
        """Get available video categories for a region"""
        try:
            url = f"{self.base_url}/videoCategories"
            params = {
                'part': 'snippet',
                'regionCode': region_code,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return [
                {
                    'id': item['id'],
                    'title': item['snippet']['title'],
                    'assignable': item['snippet'].get('assignable', False)
                }
                for item in data.get('items', [])
            ]
            
        except requests.RequestException as e:
            raise Exception(f"YouTube API request failed: {str(e)}")
    
    def _format_search_results(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format search results to a consistent structure"""
        formatted_results = []
        for item in items:
            snippet = item.get('snippet', {})
            formatted_results.append({
                'video_id': item['id']['videoId'],
                'title': snippet.get('title', ''),
                'description': snippet.get('description', ''),
                'channel_title': snippet.get('channelTitle', ''),
                'published_at': snippet.get('publishedAt', ''),
                'thumbnail': snippet.get('thumbnails', {}).get('medium', {}).get('url', ''),
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            })
        return formatted_results
    
    def _format_video_details(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Format video details to a consistent structure"""
        snippet = item.get('snippet', {})
        statistics = item.get('statistics', {})
        content_details = item.get('contentDetails', {})
        
        return {
            'video_id': item['id'],
            'title': snippet.get('title', ''),
            'description': snippet.get('description', ''),
            'channel_title': snippet.get('channelTitle', ''),
            'channel_id': snippet.get('channelId', ''),
            'published_at': snippet.get('publishedAt', ''),
            'thumbnail': snippet.get('thumbnails', {}).get('medium', {}).get('url', ''),
            'url': f"https://www.youtube.com/watch?v={item['id']}",
            'duration': content_details.get('duration', ''),
            'view_count': int(statistics.get('viewCount', 0)),
            'like_count': int(statistics.get('likeCount', 0)),
            'comment_count': int(statistics.get('commentCount', 0)),
            'tags': snippet.get('tags', [])
        } 