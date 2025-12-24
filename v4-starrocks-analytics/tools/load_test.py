import time
import threading
import requests
import statistics

URL = "http://127.0.0.1:8003/api/v4/count"
PARAMS = {
    "tenant_id": "M001",
    "event_name": "click",
    "minutes": 30
}

THREADS = 10
DURATION = 30

latencies = []
lock = threading.Lock()

def worker():
    end = time.time() + DURATION
    while time.time() < end:
        start = time.time()
        requests.get(URL, params=PARAMS)
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

print("\n" + "=" * 60)
print("🚀 Load Test Results (StarRocks Analytics API)")
print("=" * 60)
print(f"Threads           : {THREADS}")
print(f"Test Duration     : {DURATION}s")
print(f"Total Requests    : {total}")
print(f"Requests/sec      : {total / DURATION:.2f}")

print("\n📊 Latency (milliseconds)")
print("-" * 60)
print(f"Average           : {statistics.mean(latencies):.2f} ms")
print(f"P50 (Median)      : {statistics.median(latencies):.2f} ms")
print(f"P95               : {latencies[int(0.95 * total)]:.2f} ms")
print(f"P99               : {latencies[int(0.99 * total)]:.2f} ms")
print(f"Max               : {max(latencies):.2f} ms")
