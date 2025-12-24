from flask import Blueprint, request, jsonify, current_app

features_bp = Blueprint("features", __name__)


def parse_duration(value: str) -> int:
    """
    Parses duration strings like:
    10m -> 600
    1h  -> 3600
    30s -> 30
    """
    if not isinstance(value, str):
        raise ValueError("Duration must be a string")

    value = value.strip().lower()

    if value.endswith("m"):
        return int(value[:-1]) * 60
    if value.endswith("h"):
        return int(value[:-1]) * 3600
    if value.endswith("s"):
        return int(value[:-1])

    raise ValueError("Invalid duration format. Use s, m, or h.")


@features_bp.post("/features")
def create_feature():
    data = request.json

    required_fields = [
        "tenant_id",
        "name",
        "description",
        "window",
        "ttl",
        "default",
        "type"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        window_seconds = parse_duration(data["window"])
        ttl_seconds = parse_duration(data["ttl"])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    feature = {
        "name": data["name"],
        "description": data["description"],
        "window_seconds": window_seconds,
        "ttl_seconds": ttl_seconds,
        "default": data["default"],
        "type": data["type"],
        "entity_type": data.get("entity_type"),
    }

    current_app.registry.add(data["tenant_id"], feature)

    return jsonify(feature), 201


@features_bp.get("/features")
def list_features():
    tenant_id = request.args.get("tenant_id")

    if not tenant_id:
        return jsonify({"error": "tenant_id is required"}), 400

    return jsonify(current_app.registry.list(tenant_id)), 200
