import zenoh

print("Starting Zenoh subscriber...")

def listener(sample):
    print(f'Received: {bytes(sample.payload).decode("utf-8")}')

session = zenoh.open(zenoh.Config())
sub = session.declare_subscriber('demo/hello', listener)

print("Listening for messages (Press Enter to quit)...")
input()
print("Subscriber done!")
