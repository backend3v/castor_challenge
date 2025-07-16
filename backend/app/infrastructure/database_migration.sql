-- Database migration script for Castor Challenge application
-- This script adds new tables and fields to existing database

-- Add new indexes to existing tables
ALTER TABLE favorite_videos ADD INDEX idx_channel (channel);
ALTER TABLE trend_analysis ADD INDEX idx_region (region);

-- Create trending videos cache table (if not exists)
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

-- Create video categories reference table (if not exists)
CREATE TABLE IF NOT EXISTS video_categories (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name)
);

-- Insert common video categories (only if table is empty)
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

-- Add any missing columns to existing tables (safe operations)
-- Note: These operations will fail if columns already exist, which is safe

-- Add username field to users table if not exists
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = DATABASE() 
     AND TABLE_NAME = 'users' 
     AND COLUMN_NAME = 'username') = 0,
    'ALTER TABLE users ADD COLUMN username VARCHAR(255) UNIQUE AFTER email',
    'SELECT "username column already exists" as message'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add channel_id field to favorite_videos if not exists
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = DATABASE() 
     AND TABLE_NAME = 'favorite_videos' 
     AND COLUMN_NAME = 'channel_id') = 0,
    'ALTER TABLE favorite_videos ADD COLUMN channel_id VARCHAR(50) AFTER channel',
    'SELECT "channel_id column already exists" as message'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add view_count field to favorite_videos if not exists
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = DATABASE() 
     AND TABLE_NAME = 'favorite_videos' 
     AND COLUMN_NAME = 'view_count') = 0,
    'ALTER TABLE favorite_videos ADD COLUMN view_count BIGINT AFTER duration',
    'SELECT "view_count column already exists" as message'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add like_count field to favorite_videos if not exists
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
     WHERE TABLE_SCHEMA = DATABASE() 
     AND TABLE_NAME = 'favorite_videos' 
     AND COLUMN_NAME = 'like_count') = 0,
    'ALTER TABLE favorite_videos ADD COLUMN like_count INT AFTER view_count',
    'SELECT "like_count column already exists" as message'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt; 