from flask import jsonify, request
from datetime import datetime
from .infrastructure.database import DatabaseConnection
from .domain.models import User, FavoriteVideo
from .use_cases.video_favoritos import FavoriteVideosUseCase
from .use_cases.analisis_tendencias import TrendAnalysisUseCase
from .use_cases.recomendaciones import RecommendationsUseCase
from .infrastructure.youtube_api import YouTubeAPIService
from .infrastructure.repositories.user_repository import MySQLUserRepository
from .infrastructure.repositories.favorite_video_repository import MySQLFavoriteVideoRepository
from .infrastructure.repositories.trend_analysis_repository import MySQLTrendAnalysisRepository
from .infrastructure.repositories.view_history_repository import MySQLViewHistoryRepository
from .infrastructure.repositories.user_preferences_repository import MySQLUserPreferencesRepository
from .infrastructure.auth_service import AuthService

def register_routes(app):
    # Initialize repositories
    user_repo = MySQLUserRepository()
    favorite_video_repo = MySQLFavoriteVideoRepository()
    trend_analysis_repo = MySQLTrendAnalysisRepository()
    view_history_repo = MySQLViewHistoryRepository()
    user_preferences_repo = MySQLUserPreferencesRepository()
    
    # Initialize services
    youtube_service = YouTubeAPIService()
    auth_service = AuthService()
    
    # Initialize use cases
    favorite_videos_use_case = FavoriteVideosUseCase(favorite_video_repo, youtube_service)
    trend_analysis_use_case = TrendAnalysisUseCase(trend_analysis_repo, youtube_service)
    recommendations_use_case = RecommendationsUseCase(view_history_repo, user_preferences_repo, youtube_service)
    
    @app.route("/test", methods=["GET"])
    def test():
        """Health check endpoint"""
        return jsonify({"project": "castor_challenge"})
    
    @app.route("/test_db", methods=["GET"])
    def test_db():
        """Test database connection endpoint"""
        try:
            db_connection = DatabaseConnection()
            result = db_connection.test_connection()
            return jsonify(result)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    
    # Simple registration endpoint
    @app.route("/api/auth/register", methods=["POST"])
    def register():
        """Register a new user"""
        try:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            if not name or not email or not password:
                return jsonify({"success": False, "error": "name, email, and password are required"}), 400
            result = auth_service.register_user(name, email, password)
            if result['success']:
                return jsonify(result), 201
            else:
                return jsonify(result), 400
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    # Simple login endpoint
    @app.route("/api/auth/login", methods=["POST"])
    def login():
        """Login user"""
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            if not email or not password:
                return jsonify({"success": False, "error": "email and password are required"}), 400
            result = auth_service.login_user(email, password)
            if result['success']:
                return jsonify(result)
            else:
                return jsonify(result), 401
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    # Favorites endpoints (user_id required)
    @app.route("/api/favorites", methods=["GET"])
    def get_favorites():
        """Get user's favorite videos"""
        try:
            user_id = int(request.args.get('user_id'))
            videos = favorite_video_repo.get_by_user(user_id)
            return jsonify({
                "success": True,
                "favorites": [
                    {
                        "id": video.id,
                        "user_id": video.user_id,
                        "video_id": video.video_id,
                        "title": video.title,
                        "description": video.description,
                        "url": video.url,
                        "thumbnail": video.thumbnail,
                        "channel": video.channel,
                        "duration": video.duration,
                        "published_at": video.published_at.isoformat() if video.published_at else None,
                        "notes": video.notes,
                        "tags": video.tags,
                        "added_at": video.added_at.isoformat()
                    } for video in videos
                ]
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/favorites", methods=["POST"])
    def add_favorite_video():
        """Add a video to user's favorites"""
        try:
            data = request.get_json()
            user_id = int(data.get('user_id'))
            video = FavoriteVideo(
                id=0,
                user_id=user_id,
                video_id=data.get('video_id'),
                title=data.get('title', ''),
                description=data.get('description', ''),
                url=data.get('url', ''),
                thumbnail=data.get('thumbnail', ''),
                channel=data.get('channel', ''),
                duration=data.get('duration', ''),
                published_at=datetime.fromisoformat(data.get('published_at', datetime.now().isoformat())),
                notes=data.get('notes'),
                tags=data.get('tags', [])
            )
            video = favorite_video_repo.create(video)
            return jsonify({"success": True, "message": "Video added to favorites", "favorite_id": video.id}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/favorites/<video_id>", methods=["DELETE"])
    def remove_favorite_video(video_id):
        """Remove a video from user's favorites"""
        try:
            user_id = int(request.args.get('user_id'))
            favorites = favorite_video_repo.get_by_user(user_id)
            favorite_to_delete = None
            for fav in favorites:
                if fav.video_id == video_id:
                    favorite_to_delete = fav
                    break
            if not favorite_to_delete:
                return jsonify({"error": "Favorite not found"}), 404
            favorite_video_repo.delete(favorite_to_delete.id)
            return jsonify({"success": True, "message": "Video removed from favorites"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Trends endpoints (user_id required)
    @app.route("/api/trends", methods=["GET"])
    def get_trends():
        """Get trending videos for the user"""
        try:
            user_id = int(request.args.get('user_id'))
            region = request.args.get('region', 'AR')
            category = request.args.get('category', '0')
            max_results = int(request.args.get('max_results', 10))
            videos = youtube_service.get_trending_videos(region, category, max_results)
            return jsonify({
                "success": True,
                "trends": videos,
                "region": region,
                "category": category,
                "total": len(videos),
                "user_id": user_id
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Recommendations endpoints (user_id required)
    @app.route("/api/recommendations", methods=["GET"])
    def get_user_recommendations():
        """Get personalized recommendations for the user"""
        try:
            user_id = int(request.args.get('user_id'))
            max_results = int(request.args.get('max_results', 10))
            recommendations = recommendations_use_case.get_recommendations(user_id=user_id, max_results=max_results)
            return jsonify({
                "success": True,
                "recommendations": recommendations,
                "total": len(recommendations)
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Preferences endpoints (user_id required)
    @app.route("/api/recommendations/preferences", methods=["POST"])
    def update_preferences():
        """Update user preferences"""
        try:
            data = request.get_json()
            user_id = int(data.get('user_id'))
            user_preferences_repo.update_preferences(
                user_id=user_id,
                genres=data.get('genres', []),
                topics=data.get('topics', []),
                languages=data.get('languages', []),
                min_duration=data.get('min_duration'),
                max_duration=data.get('max_duration')
            )
            return jsonify({"success": True, "message": "Preferences updated successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # View history endpoints (user_id required)
    @app.route("/api/recommendations/view", methods=["POST"])
    def record_view():
        """Record a video view for the user"""
        try:
            data = request.get_json()
            user_id = int(data.get('user_id'))
            view_history_repo.record_view(
                user_id=user_id,
                video_id=data.get('video_id'),
                title=data.get('title', ''),
                view_duration=data.get('view_duration', 0),
                completed=data.get('completed', False)
            )
            return jsonify({"success": True, "message": "View recorded successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # YouTube API endpoints (public)
    @app.route("/api/v1/youtube/search", methods=["GET"])
    def search_videos():
        """Search YouTube videos (public endpoint)"""
        try:
            query = request.args.get('q', '')
            max_results = int(request.args.get('max_results', 10))
            if not query:
                return jsonify({"error": "Query parameter 'q' is required"}), 400
            videos = youtube_service.search_videos(query, max_results)
            return jsonify({"success": True, "videos": videos})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/v1/youtube/video/<video_id>", methods=["GET"])
    def get_video_details(video_id):
        """Get YouTube video details (public endpoint)"""
        try:
            video = youtube_service.get_video_details(video_id)
            if video:
                return jsonify({"success": True, "video": video})
            else:
                return jsonify({"error": "Video not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/v1/youtube/trending", methods=["GET"])
    def get_trending_videos():
        """Get trending videos (public endpoint)"""
        try:
            region = request.args.get('region', 'AR')
            max_results = int(request.args.get('max_results', 10))
            videos = youtube_service.get_trending_videos(region, max_results=max_results)
            return jsonify({"success": True, "videos": videos})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/v1/youtube/categories", methods=["GET"])
    def get_video_categories():
        """Get video categories (public endpoint)"""
        try:
            region = request.args.get('region', 'AR')
            categories = youtube_service.get_video_categories(region)
            return jsonify({"success": True, "categories": categories})
        except Exception as e:
            return jsonify({"error": str(e)}), 500 