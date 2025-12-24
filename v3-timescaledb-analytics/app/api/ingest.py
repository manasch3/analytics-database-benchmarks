from flask import Blueprint, request, jsonify
from app.services.ingest import IngestService

ingest_bp = Blueprint("ingest", __name__)
service = IngestService()

@ingest_bp.post("/ingest")
def ingest():
    events = request.json
    service.ingest_events(events)
    return jsonify({
        "status": "ok",
        "ingested": len(events)
    })
