import random
import string
from datetime import datetime, timedelta, timezone

from app.services.ingest import insert_events

TENANTS = ["M001", "M002", "M003"]
EVENTS = ["click", "view", "purchase", "login", "logout"]

BATCH_SIZE = 10_000
TOTAL_EVENTS = 50_000_000  

def random_string(n=6):
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
        "campaign": random_string(),
    }

if __name__ == "__main__":
    rows = []

    for i in range(1, TOTAL_EVENTS + 1):
        rows.append((
            random.choice(TENANTS),
            random.choice(EVENTS),
            f"user_{random.randint(1, 5_000_000)}",
            random_timestamp(),
            random_attributes(),
        ))

        if len(rows) == BATCH_SIZE:
            insert_events(rows)
            print(f"Inserted {i} events")
            rows.clear()

    if rows:
        insert_events(rows)

    print("Done")

