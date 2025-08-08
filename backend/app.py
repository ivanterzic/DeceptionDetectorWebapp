from flask import Flask
from flask_cors import CORS
from config import API_HOST, API_PORT, DEBUG_MODE
from routes import register_routes


def create_app():
    app = Flask(__name__)
    CORS(app)
    register_routes(app)    
    return app


def main():
    app = create_app()
    print("Starting Deception Detector API...")
    print(f"Server will run on http://{API_HOST}:{API_PORT}")
    app.run(debug=DEBUG_MODE, host=API_HOST, port=API_PORT)


if __name__ == '__main__':
    main()
