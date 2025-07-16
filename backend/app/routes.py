from flask import jsonify
from .infrastructure.database import DatabaseConnection

def register_routes(app):
    @app.route("/test", methods=["GET"])
    def test():
        return jsonify({"project": "castor_challenge"})
    
    @app.route("/test_db", methods=["GET"])
    def test_db():
        """Test database connection endpoint"""
        try:
            db_connection = DatabaseConnection()
            result = db_connection.test_connection()
            return jsonify(result)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500 