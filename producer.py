from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_order():
    order = {
        'user_id': random.randint(1, 100),
        'amount': round(random.uniform(10.0, 1000.0), 2),
        'timestamp': int(time.time())
    }
    return order

while True:
    order = generate_order()
    producer.send('orders', order)
    print(f"Produced: {order}")
    time.sleep(1)
