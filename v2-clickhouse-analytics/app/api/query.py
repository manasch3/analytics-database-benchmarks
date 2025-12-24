from flask import Blueprint, request, jsonify
from app.services.analytics import AnalyticsService

query_bp = Blueprint("query", __name__)
service = AnalyticsService()

@query_bp.get("/count")
def count_events():
    tenant = request.args["tenant_id"]
    event_type = request.args["event_type"]
    minutes = int(request.args.get("minutes", 30))

    count = service.count_events(tenant, event_type, minutes)
    return jsonify({
        "tenant_id": tenant,
        "event_type": event_type,
        "count": count
    })
