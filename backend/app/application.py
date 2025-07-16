from flask import Flask
from flask_cors import CORS
from .config import Config
from .routes import register_routes

class Application:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        
        # Enable CORS for all routes
        CORS(self.app, resources={r"/*": {"origins": "*"}})
        
        register_routes(self.app)

    def run(self):
        self.app.run() 