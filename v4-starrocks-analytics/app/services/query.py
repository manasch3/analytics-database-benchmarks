from app.db.client import get_conn

def count_events(tenant_id, event_name, minutes):
    conn = get_conn()
    cursor = conn.cursor()

    sql = """
    SELECT COUNT(*)
    FROM events
    WHERE tenant_id = %s
      AND event_name = %s
      AND event_time >= NOW() - INTERVAL %s MINUTE
    """

    cursor.execute(sql, (tenant_id, event_name, minutes))
    result = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return result
