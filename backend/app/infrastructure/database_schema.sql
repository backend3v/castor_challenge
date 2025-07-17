-- Database schema for Castor Challenge application
-- All tables use English naming conventions and match domain models exactly

-- Users table (updated with authentication fields)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL DEFAULT '',
    salt VARCHAR(255) NOT NULL DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    active BOOLEAN DEFAULT TRUE, -- For backward compatibility
    email_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255) NULL,
    reset_token VARCHAR(255) NULL,
    reset_token_expires TIMESTAMP NULL,
    INDEX idx_email (email),
    INDEX idx_active (active),
    INDEX idx_is_active (is_active)
);

-- User sessions table for JWT token management
CREATE TABLE user_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_sessions_user_id (user_id),
    INDEX idx_user_sessions_token_hash (token_hash),
    INDEX idx_user_sessions_expires_at (expires_at)
);

-- Refresh tokens table
CREATE TABLE refresh_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_revoked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_refresh_tokens_user_id (user_id),
    INDEX idx_refresh_tokens_token_hash (token_hash),
    INDEX idx_refresh_tokens_expires_at (expires_at)
);

-- User roles table (for future role-based access)
CREATE TABLE user_roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role_name VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_role (user_id, role_name),
    INDEX idx_user_roles_user_id (user_id)
);

-- Audit log table for authentication events
CREATE TABLE auth_audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    action VARCHAR(50) NOT NULL, -- 'login', 'logout', 'register', 'password_reset', etc.
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    success BOOLEAN DEFAULT TRUE,
    details JSON NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_auth_audit_user_id (user_id),
    INDEX idx_auth_audit_action (action),
    INDEX idx_auth_audit_created_at (created_at)
);

-- Favorite videos table
CREATE TABLE favorite_videos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    video_id VARCHAR(20) NOT NULL, -- YouTube video ID
    title VARCHAR(500) NOT NULL,
    description TEXT,
    url VARCHAR(500) NOT NULL,
    thumbnail VARCHAR(500),
    channel VARCHAR(255) NOT NULL,
    duration VARCHAR(20),
    published_at TIMESTAMP,
    notes TEXT,
    tags JSON, -- Store tags as JSON array
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_video (user_id, video_id),
    INDEX idx_user_id (user_id),
    INDEX idx_video_id (video_id),
    INDEX idx_added_at (added_at),
    INDEX idx_channel (channel)
);

-- Trend analysis table
CREATE TABLE trend_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(100) NOT NULL,
    region VARCHAR(10) NOT NULL,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    results JSON NOT NULL, -- Store analysis results as JSON
    criteria JSON, -- Store analysis criteria as JSON
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_category (category),
    INDEX idx_region (region),
    INDEX idx_analyzed_at (analyzed_at)
);

-- View history table
CREATE TABLE view_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    video_id VARCHAR(20) NOT NULL,
    title VARCHAR(500) NOT NULL,
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    view_duration INT NOT NULL, -- Duration in seconds
    completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_video_id (video_id),
    INDEX idx_viewed_at (viewed_at),
    INDEX idx_completed (completed)
);

-- User preferences table
CREATE TABLE user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    genres JSON, -- Store genres as JSON array
    topics JSON, -- Store topics as JSON array
    languages JSON, -- Store languages as JSON array
    min_duration INT, -- Minimum duration in seconds
    max_duration INT, -- Maximum duration in seconds
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_preferences (user_id),
    INDEX idx_user_id (user_id)
);

-- Trending videos cache table (for storing YouTube trending data)
CREATE TABLE trending_videos_cache (
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

-- Video categories reference table
CREATE TABLE video_categories (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name)
);

-- Insert sample user for testing (with authentication)
INSERT INTO users (name, email, password_hash, salt, is_active, email_verified) 
VALUES ('Test User', 'test@example.com', 'NEEDS_RESET', 'NEEDS_RESET', TRUE, FALSE);

-- Insert default role for test user
INSERT INTO user_roles (user_id, role_name) VALUES (1, 'user');

-- Insert common video categories
INSERT INTO video_categories (id, name, description) VALUES
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