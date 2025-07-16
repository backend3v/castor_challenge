from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../env')

def create_app():
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Import and register routes
    from .routes import register_routes
    register_routes(app)
    
    return app 