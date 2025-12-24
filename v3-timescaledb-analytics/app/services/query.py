from app.db.client import get_conn

class QueryService:
    def count_events(self, tenant_id, event_name, minutes):
        conn = get_conn()
        cur = conn.cursor()

        query = """
        SELECT COUNT(*)
        FROM events
        WHERE tenant_id = %s
          AND event_name = %s
          AND event_time >= now() - interval '%s minutes'
        """

        cur.execute(query, (tenant_id, event_name, minutes))
        count = cur.fetchone()[0]

        cur.close()
        conn.close()

        return count
