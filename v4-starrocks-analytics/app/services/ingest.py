from app.db.client import get_conn

def insert_events(rows):
    conn = get_conn()
    cursor = conn.cursor()

    sql = """
    INSERT INTO events
    (tenant_id, event_name, entity_id, event_time, attributes)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.executemany(sql, [
        (t, e, u, ts, str(attrs))
        for (t, e, u, ts, attrs) in rows
    ])

    cursor.close()
    conn.close()

