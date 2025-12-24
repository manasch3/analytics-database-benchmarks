from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import time

counters_bp = Blueprint("counters", __name__)

@counters_bp.get("/counters/<feature_name>")
def get_counter(feature_name):
    tenant_id = request.args["tenant_id"]
    entity_id = request.args["entity_id"]
    now = request.args.get("now")

    now_ts = (
        int(datetime.fromisoformat(now.replace("Z", "")).timestamp())
        if now
        else int(time.time())
    )

    value, is_fresh = current_app.counter_service.get_count(
        tenant_id, feature_name, entity_id, now_ts
    )

    return jsonify({
        "tenant_id": tenant_id,
        "feature_name": feature_name,
        "entity_id": entity_id,
        "now": now,
        "value": value,
        "is_fresh": is_fresh
    })
