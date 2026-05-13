import zenoh
import time

print("Starting Zenoh publisher...")
session = zenoh.open(zenoh.Config())
pub = session.declare_publisher('demo/hello')

print("Publishing messages (Ctrl+C to stop)...")
for i in range(100):
    msg = f'Hello Zenoh #{i}'
    pub.put(msg)
    print(f'Published: {msg}')
    time.sleep(1)

print("Publisher done!")
