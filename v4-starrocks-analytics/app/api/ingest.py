from flask import Blueprint, request, jsonify
from app.services.ingest import insert_events

bp = Blueprint("ingest", __name__, url_prefix="/api/v4")

@bp.route("/ingest", methods=["POST"])
def ingest():
    data = request.json
    insert_events(data["rows"])
    return jsonify({"status": "ok"})
