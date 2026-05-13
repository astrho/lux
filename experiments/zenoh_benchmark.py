import zenoh
import time
import statistics

ITERATIONS = 1000
latencies = []

print(f"Starting latency benchmark ({ITERATIONS} iterations)...")

# Peer-to-peer mode
config = zenoh.Config()
session = zenoh.open(config)

query_key = 'benchmark/ping'
reply_key = 'benchmark/pong'

# Set up responder
def responder(query):
    query.reply(query.key_expr, b'pong')

queryable = session.declare_queryable(query_key, responder)

print("Warming up...")
# Warmup runs
for _ in range(100):
    replies = session.get(query_key, timeout=1.0)
    for reply in replies:
        pass

print("Running benchmark...")
# Actual measurements
for i in range(ITERATIONS):
    start = time.perf_counter_ns()
    replies = session.get(query_key, timeout=1.0)
    for reply in replies:
        pass
    end = time.perf_counter_ns()
    latency_us = (end - start) / 1000  # Convert to microseconds
    latencies.append(latency_us)
    
    if i % 100 == 0:
        print(f"Progress: {i}/{ITERATIONS}")

# Calculate statistics
print("\n" + "="*60)
print("LATENCY RESULTS")
print("="*60)
print(f"Iterations: {ITERATIONS}")
print(f"Mean:   {statistics.mean(latencies):>8.2f} μs")
print(f"Median: {statistics.median(latencies):>8.2f} μs")
print(f"StdDev: {statistics.stdev(latencies):>8.2f} μs")
print(f"Min:    {min(latencies):>8.2f} μs")
print(f"Max:    {max(latencies):>8.2f} μs")

# Percentiles
sorted_latencies = sorted(latencies)
print(f"\nPercentiles:")
print(f"P50:  {sorted_latencies[int(0.50 * ITERATIONS)]:>8.2f} μs")
print(f"P95:  {sorted_latencies[int(0.95 * ITERATIONS)]:>8.2f} μs")
print(f"P99:  {sorted_latencies[int(0.99 * ITERATIONS)]:>8.2f} μs")
print(f"P99.9:{sorted_latencies[int(0.999 * ITERATIONS)]:>8.2f} μs")
print("="*60)

# Save raw data
with open('latency_results.csv', 'w') as f:
    f.write('iteration,latency_us\n')
    for i, lat in enumerate(latencies):
        f.write(f'{i},{lat}\n')

print("\nRaw data saved to: latency_results.csv")

queryable.undeclare()
session.close()
