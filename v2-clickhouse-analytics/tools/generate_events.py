import random
import string
from datetime import datetime, timedelta, timezone

from app.db.client import get_client

TENANTS = ["M001", "M002", "M003"]
EVENTS = ["click", "view", "purchase", "login", "logout"]

def random_string(n=8):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))


def random_timestamp():
    return datetime.now(timezone.utc) - timedelta(
        seconds=random.randint(0, 30 * 24 * 3600)
    )

def random_attributes():
    return {
        "browser": random.choice(["chrome", "firefox", "safari"]),
        "country": random.choice(["IN", "US", "DE", "SG"]),
        "device": random.choice(["mobile", "desktop"]),
        "campaign": random_string(6),
    }

if __name__ == "__main__":
    client = get_client()

    BATCH_SIZE = 100_000
    TOTAL_EVENTS = 50_000_000  

    rows = []

    for i in range(1, TOTAL_EVENTS + 1):
        rows.append(
            (
                random.choice(TENANTS),              
                random.choice(EVENTS),              
                f"user_{random.randint(1, 5_000_000)}", 
                random_attributes(),                
                random_timestamp(),                  
            )
        )

        if len(rows) == BATCH_SIZE:
            client.insert(
                "events",
                rows,
                column_names=[
                    "tenant_id",
                    "event_name",
                    "entity_id",
                    "attributes",
                    "event_time",
                ],
            )
            print(f"Inserted {i} events")
            rows.clear()

    if rows:
        client.insert(
            "events",
            rows,
            column_names=[
                "tenant_id",
                "event_name",
                "entity_id",
                "attributes",
                "event_time",
            ],
        )

    print("Done")
