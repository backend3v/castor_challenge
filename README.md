# Castor Challenge

Una aplicación web full-stack construida con Python Flask (backend) y Vue.js (frontend), siguiendo principios de clean architecture y SOLID. Permite la gestión de videos de YouTube: favoritos, tendencias, recomendaciones y usuarios, con autenticación simple.

## 🔒 Sistema de Autenticación


- Registro y login de usuarios
- Todas las funcionalidades requieren estar autenticado (excepto la guía)
- El user_id del usuario autenticado se utiliza automáticamente en todas las peticiones

### Flujo de Autenticación

1. Registro: Los usuarios crean una cuenta con nombre, email y contraseña
2. Login: Los usuarios inician sesión y acceden a las funcionalidades
3. Todas las acciones se realizan con el usuario autenticado, sin ingresar el ID manualmente

## 📁 Estructura del Proyecto

```
castor_challenge/
├── backend/                 # Backend Python Flask
│   ├── app/
│   │   ├── domain/         # Entidades y lógica de negocio
│   │   ├── use_cases/      # Casos de uso
│   │   ├── infrastructure/ # Base de datos y APIs externas
│   │   ├── adapters/       # Adaptadores de entrada/salida
│   │   ├── application.py  # Inicialización Flask
│   │   ├── config.py       # Configuración
│   │   └── routes.py       # Rutas API
│   ├── main.py             # Entry point
│   ├── requirements.txt    # Dependencias
│   └── .env                # Variables de entorno
├── frontend/               # Frontend Vue.js
│   ├── src/
│   │   ├── assets/         # Recursos estáticos
│   │   ├── views/          # Vistas principales
│   │   ├── stores/         # Estado global
│   │   ├── services/       # Servicios API
│   │   ├── components/     # Componentes Vue
│   │   ├── router/         # Vue Router
│   │   └── App.vue         # Componente principal
│   ├── vite.config.js      # Configuración Vite
│   └── .env                # Variables de entorno
├── docker-compose.yml      # Setup de base de datos MySQL
└── docker/init.sql         # Esquema de base de datos
```

## 🚀 Inicio Rápido

### 1. Base de Datos
```bash
# Inicializar la base de datos
# (Asegúrate de tener Docker instalado)
docker-compose up -d
# Para resetear completamente la base de datos:
docker-compose down -v && docker-compose up -d
```

### 2. Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

### 4. Variables de Entorno

#### Backend (.env)
```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=castor_db
DB_USER=castor_user
DB_PASSWORD=castor_password
YOUTUBE_API_KEY=your_youtube_api_key
```

#### Frontend (.env)
```
VITE_API_URL=http://localhost:5000
```

## 📄 Documentación de la API

### URL Base
```
http://localhost:5000
```

### Endpoints Principales

#### Usuarios
- `POST /api/users` - Crear usuario
- `GET /api/users/{id}` - Obtener usuario
- `GET /api/users/search?name=` - Buscar usuario por nombre

#### Favoritos
- `GET /api/favorites/{user_id}` - Obtener favoritos
- `POST /api/favorites` - Agregar favorito
- `DELETE /api/favorites/{user_id}/{video_id}` - Eliminar favorito

#### Tendencias
- `GET /api/trends` - Obtener videos trending
- `GET /api/trends/analysis` - Análisis de tendencias

#### Recomendaciones
- `GET /api/recommendations/{user_id}` - Obtener recomendaciones (solo si el usuario tiene favoritos)
- `POST /api/recommendations/preferences` - Actualizar preferencias
- `POST /api/recommendations/view` - Registrar visualización

## 📝 Notas
- Todas las funcionalidades requieren estar autenticado, excepto la guía.
- El sistema nunca solicita el ID de usuario manualmente.
- La base de datos se inicializa con el esquema de `docker/init.sql`.
- Para pruebas, puedes crear usuarios desde la interfaz o usando los endpoints.

## 🔄 Actualizaciones Recientes

- El frontend usa siempre el usuario autenticado, nunca solicita el ID
- Las recomendaciones solo aparecen si el usuario tiene favoritos
- Se eliminaron scripts y migraciones obsoletas
- Documentación y comentarios traducidos al español

## 📄 Licencia

Este proyecto está licenciado bajo MIT License. 