# Castor Challenge

A full-stack web application built with Python Flask (backend) and Vue.js (frontend), following clean architecture principles and SOLID design patterns.

## 📁 Project Structure

```
castor_challenge/
├── backend/                 # Python Flask Backend
│   ├── app/
│   │   ├── domain/         # Business entities and logic
│   │   ├── use_cases/      # Application orchestration
│   │   ├── infrastructure/ # Database, external APIs
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
└── RULES_GENERAL.md       # General project rules
```

## 🐍 Backend (Python + Flask)

### 🛠️ Technologies
- **Python 3.x**
- **Flask** - Web framework
- **Architecture**: Hexagonal (Clean Architecture)
- **Design Patterns**: SOLID principles

### ✨ Features
- RESTful API design
- Environment-based configuration
- Modular structure following clean architecture
- Test endpoint available at `/test`

### 🚀 Setup and Run

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   Create a `.env` file in the `backend/` directory:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=mydatabase
   DB_USER=user
   DB_PASSWORD=password
   EXTERNAL_API_URL=https://api.example.com
   EXTERNAL_API_KEY=your_api_key
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

4. **Test the API:**
   ```bash
   curl http://localhost:5000/test
   ```

### 🏗️ Architecture

The backend follows hexagonal architecture with clear separation of concerns:

- **Domain**: Business entities and pure logic
- **Use Cases**: Application orchestration
- **Infrastructure**: External dependencies (DB, APIs)
- **Adapters**: Input/output interfaces (HTTP, CLI)

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

### 🚀 Setup and Run

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment:**
   Create a `.env` file in the `frontend/` directory:
   ```env
   VITE_APP_NAME=castor_challenge
   VITE_APP_HOST=localhost
   VITE_APP_PORT=5173
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

4. **Access the application:**
   Open `http://localhost:5173` in your browser

### 📦 Build for Production

```bash
npm run build
```

## 📋 Development Rules

The project follows strict development rules documented in separate files:

- `RULES_GENERAL.md` - General project rules and SOLID principles
- `backend/RULES_BACKEND.md` - Backend-specific rules
- `frontend/RULES_FRONTEND.md` - Frontend-specific rules
- `frontend/RULES_MARKUP.md` - HTML/Vue markup rules
- `frontend/RULES_CSS.md` - CSS styling rules

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

## ⚙️ Environment Configuration

Both backend and frontend use environment variables for configuration:

- **Backend**: Database connections, external API settings
- **Frontend**: App name, host, port, API endpoints

This approach ensures:
- 🔒 Security (no hardcoded secrets)
- 🔄 Flexibility (different configs per environment)
- 🛠️ Maintainability (centralized configuration)

## 🚀 Next Steps

1. 🔗 Implement database integration
2. 🔐 Add authentication system
3. 📡 Create API endpoints for business logic
4. 🎨 Develop frontend components and pages
5. 🧪 Add comprehensive testing
6. 🔄 Set up CI/CD pipeline

## 🤝 Contributing

1. 📖 Follow the established rules and architecture
2. ✍️ Write clean, documented code
3. 🧪 Test your changes
4. 💬 Use meaningful commit messages

## 📄 License

[Add your license information here] 