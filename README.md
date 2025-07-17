# Castor Challenge

A full-stack web application built with Python Flask (backend) and Vue.js (frontend), following clean architecture principles and SOLID design patterns. The application provides YouTube video management services including favorites, trend analysis, and personalized recommendations.

## 📁 Project Structure

```
castor_challenge/
├── backend/                 # Python Flask Backend
│   ├── app/
│   │   ├── domain/         # Business entities and logic
│   │   │   ├── models.py   # Domain models
│   │   │   └── repositories.py # Repository interfaces
│   │   ├── use_cases/      # Application orchestration
│   │   │   ├── video_favoritos.py
│   │   │   ├── analisis_tendencias.py
│   │   │   └── recomendaciones.py
│   │   ├── infrastructure/ # Database, external APIs
│   │   │   ├── database_schema.sql
│   │   │   └── repositories/
│   │   │       ├── user_repository.py
│   │   │       ├── favorite_video_repository.py
│   │   │       ├── trend_analysis_repository.py
│   │   │       ├── view_history_repository.py
│   │   │       └── user_preferences_repository.py
│   │   ├── adapters/       # Input/output adapters
│   │   ├── application.py  # Flask app initialization
│   │   ├── config.py       # Configuration management
│   │   └── routes.py       # API routes
│   ├── main.py             # Application entry point
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
├── frontend/               # Vue.js Frontend
│   ├── src/
│   │   ├── assets/        # Static assets
│   │   └── App.vue        # Main application component
│   ├── vite.config.js     # Vite configuration
│   └── .env              # Environment variables
├── docker-compose.yml     # MySQL database setup
└── RULES_GENERAL.md       # General project rules
```

## 🐍 Backend (Python + Flask)

### 🛠️ Technologies
- **Python 3.x**
- **Flask** - Web framework
- **MySQL** - Database
- **YouTube Data API v3** - External video data
- **Architecture**: Hexagonal (Clean Architecture)
- **Design Patterns**: SOLID principles

### ✨ Features
- RESTful API design
- YouTube video management services
- MySQL database integration
- Environment-based configuration
- Modular structure following clean architecture
- **Enhanced User Management System**:
  - Complete CRUD operations for users
  - Advanced search functionality (by ID and name)
  - Bulk user retrieval with pagination support
  - Real-time validation and error handling
  - Clean repository pattern implementation

## 📚 API Documentation

### Base URL
```
http://localhost:5000
```

### 🔧 System Endpoints

#### Test Endpoint
```http
GET /test
```
**Description**: Basic health check endpoint
**Response**: `{"message": "Hello from Castor Challenge!"}`

#### Database Test
```http
GET /test_db
```
**Description**: Test database connection
**Response**: `{"message": "Database connection successful"}`

### 🎥 Video Favorites Service

#### Get User Favorites
```http
GET /api/favorites/{user_id}
```
**Description**: Retrieve all favorite videos for a user
**Parameters**:
- `user_id` (path): User identifier

**Response**:
```json
{
  "success": true,
  "favorites": [
    {
      "id": 1,
      "user_id": 1,
      "video_id": "dQw4w9WgXcQ",
      "title": "Video Title",
      "description": "Video description",
      "thumbnail_url": "https://...",
      "channel_title": "Channel Name",
      "published_at": "2023-01-01T00:00:00Z",
      "created_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

#### Add Favorite Video
```http
POST /api/favorites
```
**Description**: Add a video to user's favorites
**Body**:
```json
{
  "user_id": 1,
  "video_id": "dQw4w9WgXcQ",
  "title": "Video Title",
  "description": "Video description",
  "thumbnail_url": "https://...",
  "channel_title": "Channel Name",
  "published_at": "2023-01-01T00:00:00Z"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Video added to favorites",
  "favorite_id": 1
}
```

#### Remove Favorite Video
```http
DELETE /api/favorites/{user_id}/{video_id}
```
**Description**: Remove a video from user's favorites
**Parameters**:
- `user_id` (path): User identifier
- `video_id` (path): YouTube video ID

**Response**:
```json
{
  "success": true,
  "message": "Video removed from favorites"
}
```

### 📊 Trend Analysis Service

#### Get Trending Videos
```http
GET /api/trends
```
**Description**: Get current trending videos from YouTube
**Query Parameters**:
- `region_code` (optional): Country code (default: "US")
- `max_results` (optional): Number of results (default: 10)

**Response**:
```json
{
  "success": true,
  "trends": [
    {
      "id": 1,
      "video_id": "dQw4w9WgXcQ",
      "title": "Trending Video",
      "description": "Video description",
      "thumbnail_url": "https://...",
      "channel_title": "Channel Name",
      "published_at": "2023-01-01T00:00:00Z",
      "view_count": 1000000,
      "like_count": 50000,
      "comment_count": 1000,
      "category_id": 20,
      "region_code": "US",
      "created_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

#### Get Trend Analysis
```http
GET /api/trends/analysis
```
**Description**: Get analyzed trend data with insights
**Query Parameters**:
- `region_code` (optional): Country code (default: "US")
- `category_id` (optional): Video category filter
- `days_back` (optional): Days to analyze (default: 7)

**Response**:
```json
{
  "success": true,
  "analysis": {
    "total_videos": 50,
    "total_views": 50000000,
    "avg_views": 1000000,
    "top_categories": [
      {"category_id": 20, "count": 15, "name": "Gaming"}
    ],
    "top_channels": [
      {"channel": "Channel Name", "videos": 5, "total_views": 10000000}
    ],
    "trending_videos": [...]
  }
}
```

### 🎯 Recommendations Service

#### Get User Recommendations
```http
GET /api/recommendations/{user_id}
```
**Description**: Get personalized video recommendations for a user
**Parameters**:
- `user_id` (path): User identifier

**Query Parameters**:
- `max_results` (optional): Number of recommendations (default: 10)

**Response**:
```json
{
  "success": true,
  "recommendations": [
    {
      "id": 1,
      "video_id": "dQw4w9WgXcQ",
      "title": "Recommended Video",
      "description": "Video description",
      "thumbnail_url": "https://...",
      "channel_title": "Channel Name",
      "published_at": "2023-01-01T00:00:00Z",
      "score": 0.85,
      "reason": "Based on your favorite categories"
    }
  ]
}
```

#### Update User Preferences
```http
POST /api/recommendations/preferences
```
**Description**: Update user preferences for better recommendations
**Body**:
```json
{
  "user_id": 1,
  "preferred_categories": [20, 24, 28],
  "preferred_channels": ["channel1", "channel2"],
  "max_duration_minutes": 30,
  "language": "en"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Preferences updated successfully"
}
```

#### Record Video View
```http
POST /api/recommendations/view
```
**Description**: Record a video view for recommendation learning
**Body**:
```json
{
  "user_id": 1,
  "video_id": "dQw4w9WgXcQ",
  "watch_duration_seconds": 300,
  "completed": true
}
```

**Response**:
```json
{
  "success": true,
  "message": "View recorded successfully"
}
```

### 🗄️ User Management

#### Create User
```http
POST /api/users
```
**Description**: Create a new user
**Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Response**:
```json
{
  "success": true,
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2023-01-01T00:00:00Z"
  }
}
```

#### Get User by ID
```http
GET /api/users/{user_id}
```
**Description**: Get user information by ID
**Parameters**:
- `user_id` (path): User identifier

**Response**:
```json
{
  "success": true,
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2023-01-01T00:00:00Z",
    "active": true
  }
}
```

#### Get All Users
```http
GET /api/users
```
**Description**: Get all users in the system
**Response**:
```json
{
  "success": true,
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "created_at": "2023-01-01T00:00:00Z",
      "active": true
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane@example.com",
      "created_at": "2023-01-02T00:00:00Z",
      "active": true
    }
  ],
  "total": 2
}
```

#### Search Users by Name
```http
GET /api/users/search?name=john
```
**Description**: Search users by name (partial match)
**Query Parameters**:
- `name` (required): Name to search for (supports partial matching)

**Response**:
```json
{
  "success": true,
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "created_at": "2023-01-01T00:00:00Z",
      "active": true
    }
  ],
  "total": 1
}
```

## 🚀 Setup and Run

### 1. Database Setup
```bash
# Option 1: Automated setup (Recommended)
./setup_database.sh

# Option 2: Manual setup
docker-compose up -d
# Wait for MySQL to start, then run:
mysql -h localhost -P 3306 -u root -prootpassword < backend/app/infrastructure/database_schema.sql
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Edit backend/env with your configuration:
# - YouTube API key (REQUIRED for full functionality)
# - Database credentials
# - Other settings

# Run the application
python main.py
```

### 📺 YouTube API Configuration (REQUIRED)

Para que la aplicación funcione completamente con datos reales de YouTube:

1. **Obtener API Key**:
   - Ve a [Google Cloud Console](https://console.cloud.google.com/)
   - Crea un proyecto y habilita YouTube Data API v3
   - Genera una API key

2. **Configurar en la aplicación**:
   - Edita el archivo `backend/env`
   - Reemplaza `your_youtube_api_key_here` con tu API key real

3. **Verificar configuración**:
   - Reinicia el servidor Flask
   - Ve a la página de tendencias para ver videos reales

**Nota**: Sin la API key, la aplicación usará datos mock como fallback.

Para instrucciones detalladas, consulta: `backend/YOUTUBE_API_SETUP.md`

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run development server
npm run dev
```

## 🐳 Docker Configuration

The application uses Docker for the MySQL database. The setup includes:

- **MySQL 8.0** container with persistent data storage
- **Automatic schema initialization** via `docker/init.sql`
- **Persistent volumes** to maintain data between container restarts
- **Health checks** to ensure database is ready before use

### Database Credentials (Docker)
- **Host**: localhost
- **Port**: 3306
- **Database**: castor_db
- **User**: castor_user
- **Password**: castor_password
- **Root Password**: rootpassword

## 🔧 Environment Configuration

### Backend (.env)
```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_NAME=castor_challenge
DB_USER=root
DB_PASSWORD=password

# YouTube API
YOUTUBE_API_KEY=your_youtube_api_key_here

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
```

### Frontend (.env)
```env
VITE_APP_NAME=Castor Challenge
VITE_APP_HOST=localhost
VITE_APP_PORT=5173
VITE_API_BASE_URL=http://localhost:5000
```

## 🧪 Testing Endpoints

### Test Basic Functionality
```bash
# Test backend health
curl http://localhost:5000/test

# Test database connection
curl http://localhost:5000/test_db
```

### Test Video Services
```bash
# Get trending videos
curl http://localhost:5000/api/trends

# Get user favorites (replace USER_ID)
curl http://localhost:5000/api/favorites/1

# Get recommendations (replace USER_ID)
curl http://localhost:5000/api/recommendations/1
```

### Test User Management
```bash
# Get all users
curl http://localhost:5000/api/users

# Get user by ID (replace USER_ID)
curl http://localhost:5000/api/users/1

# Search users by name
curl "http://localhost:5000/api/users/search?name=john"

# Create new user
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com"}'
```

## 🔑 YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Add the API key to your backend `.env` file

## 🏗️ Architecture

The backend follows hexagonal architecture with clear separation of concerns:

- **Domain**: Business entities and pure logic
- **Use Cases**: Application orchestration
- **Infrastructure**: External dependencies (DB, APIs)
- **Adapters**: Input/output interfaces (HTTP, CLI)

### Database Schema
- `users`: User information and authentication
- `favorite_videos`: User's favorite videos with metadata
- `trend_analysis`: Trending video analysis results
- `view_history`: User video viewing history and engagement
- `user_preferences`: User preference settings for recommendations
- `trending_videos_cache`: Cached trending videos from YouTube API
- `video_categories`: Reference table for YouTube video categories

#### Key Features:
- **JSON fields** for flexible data storage (tags, preferences, analysis results)
- **Optimized indexes** for fast queries on common operations
- **Foreign key constraints** for data integrity
- **Caching table** for YouTube trending data to reduce API calls
- **Category reference** for standardized video categorization

## 🎨 Frontend (Vue.js + Vite)

### 🛠️ Technologies
- **Vue 3** - Progressive JavaScript framework
- **Vite** - Build tool and dev server
- **Modern CSS** - Responsive design with CSS variables

### ✨ Features
- Responsive web design
- Environment-based configuration
- Modern, minimalist UI
- Dynamic app name from environment variables
- **Enhanced User Management Interface**:
  - Create new users with real-time validation
  - Search users by ID with error handling
  - Search users by name (partial matching)
  - View all users in the system
  - Elegant user list display with hover effects
  - Form validation with visual feedback
  - Loading states and error messages

### 📦 Build for Production

```bash
npm run build
```

## 📋 Development Rules

The project follows strict development rules documented in separate files:

- `RULES_GENERAL.md` - General project rules and SOLID principles

## 🔑 Key Principles

### 🎯 SOLID Principles
- **S**ingle Responsibility: Each module has one responsibility
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subtypes are substitutable
- **I**nterface Segregation: Prefer specific interfaces
- **D**ependency Inversion: Depend on abstractions

### 🏛️ Clean Architecture
- Domain layer is independent of external concerns
- Business logic is isolated from frameworks
- Dependencies point inward toward the domain

### ✨ Code Quality
- Clean, readable, and maintainable code
- Comments in English explaining the "why"
- Consistent naming conventions
- Modular and reusable components
- **Enhanced Validation**: Real-time form validation with visual feedback
- **Error Handling**: Comprehensive error handling across all layers
- **User Experience**: Loading states, success messages, and intuitive interfaces

## 🚀 Next Steps

1. 🔐 Add authentication system
2. 🎨 Develop frontend components and pages
3. 🧪 Add comprehensive testing
4. 🔄 Set up CI/CD pipeline
5. 📊 Add analytics and monitoring
6. 🔒 Implement rate limiting and security

## 🆕 Recent Updates

### User Management Enhancements (Latest)
- ✅ **New API Endpoints**: Added `/api/users` (GET) and `/api/users/search` (GET)
- ✅ **Enhanced Repository**: Implemented `get_all()` and `search_by_name()` methods
- ✅ **Frontend Improvements**: 
  - Added search by name functionality with partial matching
  - Added "Consult All Users" button
  - Improved user list display with modern UI
  - Enhanced form validation and error handling
  - Added loading states and user feedback
- ✅ **Better UX**: Real-time validation, hover effects, and responsive design

### Technical Improvements
- ✅ **Repository Pattern**: Extended UserRepository interface with new methods
- ✅ **Error Handling**: Comprehensive error handling for all user operations
- ✅ **Validation**: Client-side and server-side validation for all inputs
- ✅ **Performance**: Optimized database queries with proper indexing

## 🤝 Contributing

1. 📖 Follow the established rules and architecture
2. ✍️ Write clean, documented code
3. 🧪 Test your changes
4. 💬 Use meaningful commit messages

## 📄 License

[Add your license information here] 