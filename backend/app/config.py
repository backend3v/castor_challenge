import os

class Config:
    # Database configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'mydatabase')
    DB_USER = os.getenv('DB_USER', 'user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')

    # External API configuration
    EXTERNAL_API_URL = os.getenv('EXTERNAL_API_URL', 'https://api.example.com')
    EXTERNAL_API_KEY = os.getenv('EXTERNAL_API_KEY', 'your_api_key') 