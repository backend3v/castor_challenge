-- Database initialization script for Castor Challenge (simple login)
-- Este script se ejecuta automáticamente al iniciar el contenedor MySQL

CREATE DATABASE IF NOT EXISTS castor_db;
USE castor_db;

-- Tabla de usuarios (solo autenticación simple)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    INDEX idx_email (email),
    INDEX idx_is_active (is_active)
);

-- Tabla de favoritos
CREATE TABLE IF NOT EXISTS favorite_videos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    video_id VARCHAR(20) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    url VARCHAR(500) NOT NULL,
    thumbnail VARCHAR(500),
    channel VARCHAR(255) NOT NULL,
    duration VARCHAR(20),
    published_at TIMESTAMP,
    notes TEXT,
    tags JSON,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_video (user_id, video_id),
    INDEX idx_user_id (user_id),
    INDEX idx_video_id (video_id),
    INDEX idx_added_at (added_at),
    INDEX idx_channel (channel)
);

-- Tabla de análisis de tendencias
CREATE TABLE IF NOT EXISTS trend_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(100) NOT NULL,
    region VARCHAR(10) NOT NULL,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    results JSON NOT NULL,
    criteria JSON,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_category (category),
    INDEX idx_region (region),
    INDEX idx_analyzed_at (analyzed_at)
);

-- Tabla de historial de vistas
CREATE TABLE IF NOT EXISTS view_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    video_id VARCHAR(20) NOT NULL,
    title VARCHAR(500) NOT NULL,
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    view_duration INT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_video_id (video_id),
    INDEX idx_viewed_at (viewed_at),
    INDEX idx_completed (completed)
);

-- Tabla de preferencias de usuario
CREATE TABLE IF NOT EXISTS user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    genres JSON,
    topics JSON,
    languages JSON,
    min_duration INT,
    max_duration INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_preferences (user_id),
    INDEX idx_user_id (user_id)
);

-- Cache de videos en tendencia
CREATE TABLE IF NOT EXISTS trending_videos_cache (
    id INT AUTO_INCREMENT PRIMARY KEY,
    video_id VARCHAR(20) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    thumbnail_url VARCHAR(500),
    channel_title VARCHAR(255) NOT NULL,
    published_at TIMESTAMP,
    view_count BIGINT,
    like_count INT,
    comment_count INT,
    category_id INT,
    region_code VARCHAR(10) NOT NULL,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_video_region (video_id, region_code),
    INDEX idx_region_code (region_code),
    INDEX idx_category_id (category_id),
    INDEX idx_cached_at (cached_at),
    INDEX idx_view_count (view_count)
);

-- Tabla de categorías de video
CREATE TABLE IF NOT EXISTS video_categories (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name)
);

-- Usuario de prueba (hash bcrypt para 'test1234')
INSERT IGNORE INTO users (name, email, password_hash, is_active, email_verified) 
VALUES ('Usuario Prueba', 'prueba@example.com', '$2b$12$w8QwQwQwQwQwQwQwQwQwQeQwQwQwQwQwQwQwQwQwQwQwQwQwQwQw', TRUE, FALSE);

-- Categorías de video
INSERT IGNORE INTO video_categories (id, name, description) VALUES
(1, 'Film & Animation', 'Film and animation videos'),
(2, 'Autos & Vehicles', 'Automotive and vehicle related content'),
(10, 'Music', 'Music videos and performances'),
(15, 'Pets & Animals', 'Pet and animal videos'),
(17, 'Sports', 'Sports and athletic content'),
(19, 'Travel & Events', 'Travel and event videos'),
(20, 'Gaming', 'Video game content'),
(22, 'People & Blogs', 'Personal vlogs and blogs'),
(23, 'Comedy', 'Comedy and humor videos'),
(24, 'Entertainment', 'Entertainment content'),
(25, 'News & Politics', 'News and political content'),
(26, 'Howto & Style', 'How-to and style videos'),
(27, 'Education', 'Educational content'),
(28, 'Science & Technology', 'Science and technology videos'),
(29, 'Nonprofits & Activism', 'Nonprofit and activist content'); 