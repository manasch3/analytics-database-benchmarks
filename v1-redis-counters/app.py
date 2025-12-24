import os
from flask import Flask
from redis import Redis
from dotenv import load_dotenv

from app.registry.registry import FeatureRegistry
from app.counters.service import CounterService
from app.api.features import features_bp
from app.api.events import events_bp
from app.api.counters import counters_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    redis_client = Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )

    registry = FeatureRegistry()
    counter_service = CounterService(redis_client, registry)

    app.registry = registry
    app.counter_service = counter_service

    app.register_blueprint(features_bp, url_prefix="/api/v1")
    app.register_blueprint(events_bp, url_prefix="/api/v1")
    app.register_blueprint(counters_bp, url_prefix="/api/v1")

    @app.get("/health")
    def health():
        return {"status": "ok", "redis": "ok"}

    return app

if __name__ == "__main__":
    create_app().run(port=8000, debug=True)
