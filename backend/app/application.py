from flask import Flask
from .config import Config
from .routes import register_routes

class Application:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        register_routes(self.app)

    def run(self):
        self.app.run() 