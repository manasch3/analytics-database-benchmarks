from flask import Flask
from app.api.ingest import ingest_bp
from app.api.query import query_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(ingest_bp, url_prefix="/api/v3")
    app.register_blueprint(query_bp, url_prefix="/api/v3")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=8001)

