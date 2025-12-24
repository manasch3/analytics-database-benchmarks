from flask import Blueprint, request, jsonify
from app.services.query import count_events

bp = Blueprint("query", __name__, url_prefix="/api/v4")

@bp.route("/count", methods=["GET"])
def count():
    tenant_id = request.args.get("tenant_id")
    event_name = request.args.get("event_name")
    minutes = int(request.args.get("minutes", 30))

    count = count_events(tenant_id, event_name, minutes)
    return jsonify({"count": count})
