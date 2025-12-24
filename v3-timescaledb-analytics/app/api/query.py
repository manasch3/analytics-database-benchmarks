from flask import Blueprint, request, jsonify
from app.services.query import QueryService

query_bp = Blueprint("query", __name__)
service = QueryService()

@query_bp.get("/count")
def count():
    tenant_id = request.args["tenant_id"]
    event_name = request.args["event_name"]
    minutes = int(request.args.get("minutes", 30))

    count = service.count_events(tenant_id, event_name, minutes)

    return jsonify({
        "tenant_id": tenant_id,
        "event_name": event_name,
        "count": count
    })
