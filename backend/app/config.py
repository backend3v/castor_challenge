import os

class Config:
    # Database configuration
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    # External API configuration
    EXTERNAL_API_URL = os.getenv('EXTERNAL_API_URL')
    EXTERNAL_API_KEY = os.getenv('EXTERNAL_API_KEY')
    
    # YouTube API configuration
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY') 