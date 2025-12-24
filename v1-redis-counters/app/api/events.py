from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

events_bp = Blueprint("events", __name__)

@events_bp.post("/events")
def ingest_event():
    data = request.json
    data["timestamp"] = int(datetime.fromisoformat(data["timestamp"].replace("Z","")).timestamp())

    count = current_app.counter_service.ingest_event(data)
    return jsonify({"current_count": count})
