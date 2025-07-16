from flask import jsonify

def register_routes(app):
    @app.route("/test", methods=["GET"])
    def test():
        return jsonify({"project": "castor_challenge"}) 