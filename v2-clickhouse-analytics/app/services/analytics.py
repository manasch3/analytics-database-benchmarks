from app.db.client import get_client

class AnalyticsService:
    def __init__(self):
        self.client = get_client()

    def count_events(self, tenant_id, event_type, since_minutes):
        query = """
        SELECT count()
        FROM events
        WHERE tenant_id = %(tenant)s
          AND event_name = %(etype)s
          AND event_time >= now() - INTERVAL %(mins)s MINUTE
        """
        result = self.client.query(
            query,
            parameters={
                "tenant": tenant_id,
                "etype": event_type,
                "mins": since_minutes
            }
        )
        return result.result_rows[0][0]

