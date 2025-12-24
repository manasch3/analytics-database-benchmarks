import time
from datetime import datetime

class CounterService:
    def __init__(self, redis_client, registry):
        self.redis = redis_client
        self.registry = registry

    def _parse_timestamp(self, value):
        """
        Accepts:
        - ISO 8601 string (e.g. 2025-01-01T10:15:00Z)
        - epoch seconds (int / float)
        Returns epoch seconds (int)
        """
        if isinstance(value, str):
            return int(datetime.fromisoformat(value.replace("Z", "")).timestamp())
        return int(value)

    def ingest_event(self, event):
        feature = self.registry.get(event["tenant_id"], event["feature_name"])
        if not feature:
            return 0

        window = feature["window_seconds"]
        ts = self._parse_timestamp(event["timestamp"])

        key = (
            f"features:{event['tenant_id']}:"
            f"{event['entity_id']}:"
            f"{event['feature_name']}:txns"
        )

        # Insert event
        member = event.get("event_id", f"{ts}-{time.time_ns()}")
        self.redis.zadd(key, {member: ts})

        # Sliding window cleanup
        self.redis.zremrangebyscore(key, 0, ts - window)

        # Key-level TTL 
        self.redis.expire(key, int(window * 1.5))

        return self.redis.zcount(key, ts - window, ts)

    def get_count(self, tenant_id, feature_name, entity_id, now):
        feature = self.registry.get(tenant_id, feature_name)
        if not feature:
            return 0, False

        now_ts = self._parse_timestamp(now)

        key = (
            f"features:{tenant_id}:"
            f"{entity_id}:"
            f"{feature_name}:txns"
        )

        window = feature["window_seconds"]
        cutoff = now_ts - window

        count = self.redis.zcount(key, cutoff, now_ts)

        if count == 0:
            return feature["default"], False

        return count, True
