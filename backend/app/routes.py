from flask import jsonify, request
from .infrastructure.database import DatabaseConnection
from .use_cases.video_favoritos import FavoriteVideosUseCase
from .use_cases.analisis_tendencias import TrendAnalysisUseCase
from .use_cases.recomendaciones import RecommendationsUseCase
from .infrastructure.youtube_api import YouTubeAPIService
from .infrastructure.repositories.user_repository import MySQLUserRepository
from .infrastructure.repositories.favorite_video_repository import MySQLFavoriteVideoRepository
from .infrastructure.repositories.trend_analysis_repository import MySQLTrendAnalysisRepository
from .infrastructure.repositories.view_history_repository import MySQLViewHistoryRepository
from .infrastructure.repositories.user_preferences_repository import MySQLUserPreferencesRepository

def register_routes(app):
    # Initialize repositories
    user_repo = MySQLUserRepository()
    favorite_video_repo = MySQLFavoriteVideoRepository()
    trend_analysis_repo = MySQLTrendAnalysisRepository()
    view_history_repo = MySQLViewHistoryRepository()
    user_preferences_repo = MySQLUserPreferencesRepository()
    
    # Initialize services
    youtube_service = YouTubeAPIService()
    
    # Initialize use cases
    favorite_videos_use_case = FavoriteVideosUseCase(favorite_video_repo, youtube_service)
    trend_analysis_use_case = TrendAnalysisUseCase(trend_analysis_repo, youtube_service)
    recommendations_use_case = RecommendationsUseCase(view_history_repo, user_preferences_repo, youtube_service)
    
    @app.route("/test", methods=["GET"])
    def test():
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
    
    # YouTube API endpoints
    @app.route("/api/v1/youtube/search", methods=["GET"])
    def search_videos():
        """Search for videos on YouTube"""
        try:
            query = request.args.get('q', '')
            max_results = int(request.args.get('max_results', 10))
            
            if not query:
                return jsonify({"error": "Query parameter 'q' is required"}), 400
            
            videos = youtube_service.search_videos(query, max_results)
            return jsonify({"videos": videos, "total": len(videos)})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/v1/youtube/video/<video_id>", methods=["GET"])
    def get_video_details(video_id):
        """Get detailed information about a specific video"""
        try:
            video = youtube_service.get_video_details(video_id)
            if video:
                return jsonify(video)
            else:
                return jsonify({"error": "Video not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/v1/youtube/trending", methods=["GET"])
    def get_trending_videos():
        """Get trending videos"""
        try:
            region = request.args.get('region', 'US')
            max_results = int(request.args.get('max_results', 20))
            
            videos = youtube_service.get_trending_videos(region, None, max_results)
            return jsonify({"videos": videos, "total": len(videos)})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/v1/youtube/categories", methods=["GET"])
    def get_video_categories():
        """Get available video categories"""
        try:
            region = request.args.get('region', 'US')
            categories = youtube_service.get_video_categories(region)
            return jsonify({"categories": categories})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Favorite Videos endpoints
    @app.route("/api/v1/favorites", methods=["GET"])
    def list_favorites():
        """List user's favorite videos"""
        try:
            user_id = int(request.args.get('user_id', 1))  # Default to test user
            videos = favorite_videos_use_case.list_favorite_videos(user_id)
            return jsonify({
                "favorites": [
                    {
                        "id": video.id,
                        "video_id": video.video_id,
                        "title": video.title,
                        "description": video.description,
                        "url": video.url,
                        "thumbnail": video.thumbnail,
                        "channel": video.channel,
                        "duration": video.duration,
                        "notes": video.notes,
                        "tags": video.tags,
                        "added_at": video.added_at.isoformat()
                    } for video in videos
                ]
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/v1/favorites", methods=["POST"])
    def add_favorite():
        """Add video to favorites"""
        try:
            data = request.get_json()
            user_id = int(data.get('user_id', 1))
            video_id = data.get('video_id')
            notes = data.get('notes')
            tags = data.get('tags', [])
            
            if not video_id:
                return jsonify({"error": "video_id is required"}), 400
            
            video = favorite_videos_use_case.add_favorite_video(user_id, video_id, notes, tags)
            return jsonify({
                "message": "Video added to favorites",
                "favorite": {
                    "id": video.id,
                    "video_id": video.video_id,
                    "title": video.title
                }
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/v1/favorites/<int:video_id>", methods=["PUT"])
    def update_favorite(video_id):
        """Update favorite video notes and tags"""
        try:
            data = request.get_json()
            notes = data.get('notes')
            tags = data.get('tags')
            
            video = favorite_videos_use_case.update_favorite_video(video_id, notes, tags)
            return jsonify({
                "message": "Favorite video updated",
                "favorite": {
                    "id": video.id,
                    "notes": video.notes,
                    "tags": video.tags
                }
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/v1/favorites/<int:video_id>", methods=["DELETE"])
    def remove_favorite(video_id):
        """Remove video from favorites"""
        try:
            success = favorite_videos_use_case.remove_favorite_video(video_id)
            if success:
                return jsonify({"message": "Video removed from favorites"})
            else:
                return jsonify({"error": "Video not found in favorites"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Trend Analysis endpoints
    @app.route("/api/v1/trends", methods=["GET"])
    def list_trends():
        """List user's trend analyses"""
        try:
            user_id = int(request.args.get('user_id', 1))
            analyses = trend_analysis_use_case.list_user_analyses(user_id)
            return jsonify({
                "analyses": [
                    {
                        "id": analysis.id,
                        "category": analysis.category,
                        "region": analysis.region,
                        "analyzed_at": analysis.analyzed_at.isoformat(),
                        "total_videos": analysis.results.get('total_videos', 0)
                    } for analysis in analyses
                ]
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/v1/trends", methods=["POST"])
    def create_trend():
        """Create new trend analysis"""
        try:
            data = request.get_json()
            user_id = int(data.get('user_id', 1))
            category = data.get('category', 'general')
            region = data.get('region', 'US')
            max_results = int(data.get('max_results', 20))
            
            analysis = trend_analysis_use_case.create_trend_analysis(user_id, category, region, max_results)
            return jsonify({
                "message": "Trend analysis created",
                "analysis": {
                    "id": analysis.id,
                    "category": analysis.category,
                    "total_videos": analysis.results.get('total_videos', 0)
                }
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Recommendations endpoints
    @app.route("/api/v1/recommendations", methods=["GET"])
    def get_recommendations():
        """Get video recommendations for user"""
        try:
            user_id = int(request.args.get('user_id', 1))
            max_results = int(request.args.get('max_results', 10))
            
            recommendations = recommendations_use_case.get_recommendations(user_id, max_results)
            return jsonify({
                "recommendations": recommendations,
                "total": len(recommendations)
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/v1/recommendations/register-view", methods=["POST"])
    def register_view():
        """Register a video view"""
        try:
            data = request.get_json()
            user_id = int(data.get('user_id', 1))
            video_id = data.get('video_id')
            title = data.get('title', '')
            view_duration = int(data.get('view_duration', 0))
            completed = data.get('completed', False)
            
            if not video_id:
                return jsonify({"error": "video_id is required"}), 400
            
            history = recommendations_use_case.register_view(user_id, video_id, title, view_duration, completed)
            return jsonify({
                "message": "View registered",
                "history_id": history.id
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500 