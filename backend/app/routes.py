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
    
    # User endpoints
    @app.route("/api/users", methods=["POST"])
    def create_user():
        """Create a new user"""
        try:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            
            if not name or not email:
                return jsonify({"error": "name and email are required"}), 400
            
            user = User(
                id=0,
                name=name,
                email=email,
                created_at=datetime.now(),
                active=True
            )
            user = user_repo.create(user)
            return jsonify({
                "success": True,
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "created_at": user.created_at.isoformat()
                }
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        """Get user by ID"""
        try:
            user = user_repo.get_by_id(user_id)
            if user:
                return jsonify({
                    "success": True,
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "created_at": user.created_at.isoformat(),
                        "active": user.active
                    }
                })
            else:
                return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Favorites endpoints
    @app.route("/api/favorites/<int:user_id>", methods=["GET"])
    def get_favorites(user_id):
        """Get user's favorite videos"""
        try:
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
        """Add video to favorites"""
        try:
            data = request.get_json()
            
            # Create FavoriteVideo object from data
            video = FavoriteVideo(
                id=0,
                user_id=data.get('user_id', 1),
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
            return jsonify({
                "success": True,
                "message": "Video added to favorites",
                "favorite_id": video.id
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/favorites/<int:user_id>/<video_id>", methods=["DELETE"])
    def remove_favorite_video(user_id, video_id):
        """Remove video from favorites"""
        try:
            favorite = favorite_video_repo.get_by_youtube_id(user_id, video_id)
            if favorite:
                favorite_video_repo.delete(favorite.id)
                return jsonify({
                    "success": True,
                    "message": "Video removed from favorites"
                })
            else:
                return jsonify({"error": "Favorite not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Trends endpoints
    @app.route("/api/trends", methods=["GET"])
    def get_trends():
        """Get trending videos"""
        try:
            region_code = request.args.get('region_code', 'US')
            max_results = int(request.args.get('max_results', 10))
            
            # Use real YouTube API to get trending videos
            try:
                trends = youtube_service.get_trending_videos(region_code, None, max_results)
                return jsonify({
                    "success": True,
                    "trends": trends
                })
            except Exception as api_error:
                # Fallback to mock data if API fails
                print(f"YouTube API error: {api_error}")
                trends = [
                    {
                        "id": 1,
                        "video_id": "dQw4w9WgXcQ",
                        "title": "Rick Astley - Never Gonna Give You Up",
                        "description": "The official music video for 'Never Gonna Give You Up' by Rick Astley",
                        "thumbnail_url": "https://via.placeholder.com/120x90/ff0000/ffffff?text=Music",
                        "channel_title": "Rick Astley",
                        "published_at": "2009-10-25T06:57:33Z",
                        "view_count": 1500000000,
                        "like_count": 15000000,
                        "comment_count": 500000,
                        "category_id": 10,
                        "region_code": region_code,
                        "created_at": "2023-01-01T00:00:00Z"
                    }
                ]
                return jsonify({
                    "success": True,
                    "trends": trends,
                    "note": "Using fallback data due to API error"
                })
                
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/trends/analysis", methods=["GET"])
    def get_trend_analysis():
        """Get trend analysis"""
        try:
            region_code = request.args.get('region_code', 'US')
            category_id = request.args.get('category_id')
            days_back = int(request.args.get('days_back', 7))
            
            try:
                # Get trending videos from YouTube API
                trending_videos = youtube_service.get_trending_videos(region_code, category_id, 50)
                
                # Calculate analysis from real data
                total_videos = len(trending_videos)
                total_views = sum(video.get('view_count', 0) for video in trending_videos)
                avg_views = total_views // total_videos if total_videos > 0 else 0
                
                # Get categories
                categories = youtube_service.get_video_categories(region_code)
                category_map = {cat['id']: cat['title'] for cat in categories}
                
                # Analyze top categories
                category_counts = {}
                for video in trending_videos:
                    cat_id = str(video.get('category_id', 'unknown'))
                    category_counts[cat_id] = category_counts.get(cat_id, 0) + 1
                
                top_categories = [
                    {"category_id": cat_id, "count": count, "name": category_map.get(cat_id, "Unknown")}
                    for cat_id, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                ]
                
                # Analyze top channels
                channel_counts = {}
                channel_views = {}
                for video in trending_videos:
                    channel = video.get('channel_title', 'Unknown')
                    channel_counts[channel] = channel_counts.get(channel, 0) + 1
                    channel_views[channel] = channel_views.get(channel, 0) + video.get('view_count', 0)
                
                top_channels = [
                    {"channel": channel, "videos": count, "total_views": channel_views[channel]}
                    for channel, count in sorted(channel_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                ]
                
                analysis = {
                    "total_videos": total_videos,
                    "total_views": total_views,
                    "avg_views": avg_views,
                    "top_categories": top_categories,
                    "top_channels": top_channels,
                    "trending_videos": trending_videos[:10]  # Top 10 for preview
                }
                
                return jsonify({
                    "success": True,
                    "analysis": analysis
                })
                
            except Exception as api_error:
                # Fallback to mock analysis data if API fails
                print(f"YouTube API error in analysis: {api_error}")
                analysis = {
                    "total_videos": 50,
                    "total_views": 50000000,
                    "avg_views": 1000000,
                    "top_categories": [
                        {"category_id": 20, "count": 15, "name": "Gaming"}
                    ],
                    "top_channels": [
                        {"channel": "Sample Channel", "videos": 5, "total_views": 10000000}
                    ],
                    "trending_videos": []
                }
                
                return jsonify({
                    "success": True,
                    "analysis": analysis,
                    "note": "Using fallback data due to API error"
                })
                
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Recommendations endpoints
    @app.route("/api/recommendations/<int:user_id>", methods=["GET"])
    def get_user_recommendations(user_id):
        """Get user recommendations"""
        try:
            max_results = int(request.args.get('max_results', 10))
            
            try:
                # Get user's favorite videos to understand preferences
                user_favorites = favorite_video_repo.get_by_user(user_id)
                
                # Extract common themes from favorites
                favorite_channels = [fav.channel for fav in user_favorites if fav.channel]
                favorite_tags = []
                for fav in user_favorites:
                    if fav.tags:
                        favorite_tags.extend(fav.tags)
                
                # Search for videos based on user preferences
                recommendations = []
                if favorite_channels:
                    # Search for videos from favorite channels
                    for channel in favorite_channels[:3]:  # Top 3 channels
                        try:
                            channel_videos = youtube_service.search_videos(f"channel:{channel}", 3)
                            recommendations.extend(channel_videos)
                        except:
                            continue
                
                if favorite_tags and len(recommendations) < max_results:
                    # Search for videos with favorite tags
                    for tag in favorite_tags[:3]:  # Top 3 tags
                        try:
                            tag_videos = youtube_service.search_videos(tag, 3)
                            recommendations.extend(tag_videos)
                        except:
                            continue
                
                # If no favorites, get trending videos as recommendations
                if not recommendations:
                    trending = youtube_service.get_trending_videos("US", None, max_results)
                    recommendations = trending
                
                # Remove duplicates and limit results
                seen_ids = set()
                unique_recommendations = []
                for rec in recommendations:
                    if rec['video_id'] not in seen_ids and len(unique_recommendations) < max_results:
                        seen_ids.add(rec['video_id'])
                        unique_recommendations.append(rec)
                
                return jsonify({
                    "success": True,
                    "recommendations": unique_recommendations
                })
                
            except Exception as api_error:
                # Fallback to mock recommendations if API fails
                print(f"YouTube API error in recommendations: {api_error}")
                recommendations = [
                    {
                        "id": 1,
                        "video_id": "dQw4w9WgXcQ",
                        "title": "Recommended Video",
                        "description": "This is a recommended video",
                        "thumbnail_url": "https://via.placeholder.com/120x90",
                        "channel_title": "Recommended Channel",
                        "published_at": "2023-01-01T00:00:00Z",
                        "score": 0.85,
                        "reason": "Based on your favorite categories"
                    }
                ]
                
                return jsonify({
                    "success": True,
                    "recommendations": recommendations,
                    "note": "Using fallback data due to API error"
                })
                
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/recommendations/preferences", methods=["POST"])
    def update_preferences():
        """Update user preferences"""
        try:
            data = request.get_json()
            # Mock implementation
            return jsonify({
                "success": True,
                "message": "Preferences updated successfully"
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route("/api/recommendations/view", methods=["POST"])
    def record_view():
        """Record video view"""
        try:
            data = request.get_json()
            # Mock implementation
            return jsonify({
                "success": True,
                "message": "View recorded successfully"
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
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