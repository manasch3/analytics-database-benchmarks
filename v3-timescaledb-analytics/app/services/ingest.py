import json
from app.db.client import get_conn

class IngestService:
    def ingest_events(self, events):
        conn = get_conn()
        cur = conn.cursor()

        query = """
        INSERT INTO events
        (tenant_id, event_name, entity_id, attributes, event_time)
        VALUES (%s, %s, %s, %s, %s)
        """

        rows = [
            (
                e["tenant_id"],
                e["event_name"],
                e.get("entity_id"),
                json.dumps(e.get("attributes", {})),
                e["event_time"]
            )
            for e in events
        ]

        cur.executemany(query, rows)
        conn.commit()

        cur.close()
        conn.close()
