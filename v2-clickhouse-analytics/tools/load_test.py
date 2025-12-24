import time
import threading
import requests
import statistics

URL = "http://127.0.0.1:8000/api/v2/count"
PARAMS = {
    "tenant_id": "T1",
    "event_type": "event_5",
    "minutes": 30
}

THREADS = 10
DURATION = 30

latencies = []
lock = threading.Lock()

def worker():
    end = time.time() + DURATION
    session = requests.Session()

    while time.time() < end:
        start = time.time()
        r = session.get(URL, params=PARAMS)
        elapsed = (time.time() - start) * 1000
        with lock:
            latencies.append(elapsed)

threads = []
for _ in range(THREADS):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

latencies.sort()

total = len(latencies)
avg = statistics.mean(latencies)
p50 = statistics.median(latencies)
p95 = latencies[int(0.95 * total)]
p99 = latencies[int(0.99 * total)]
max_latency = max(latencies)

rps = total / DURATION

print("\n" + "=" * 60)
print("🚀 Load Test Results (ClickHouse Analytics API)")
print("=" * 60)

print(f"Threads           : {THREADS}")
print(f"Test Duration     : {DURATION}s")
print(f"Total Requests    : {total}")
print(f"Requests/sec      : {rps:.2f}")

print("\n📊 Latency (milliseconds)")
print("-" * 60)
print(f"Average           : {avg:.2f} ms")
print(f"P50 (Median)      : {p50:.2f} ms")
print(f"P95               : {p95:.2f} ms")
print(f"P99               : {p99:.2f} ms")
print(f"Max               : {max_latency:.2f} ms")
