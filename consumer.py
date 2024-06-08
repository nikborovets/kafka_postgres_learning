from kafka import KafkaConsumer
import json
import psycopg2

consumer = KafkaConsumer(
    'orders',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='order-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

conn = psycopg2.connect(
    dbname='orders_db',
    user='user',
    password='password',
    host='localhost',
    port=5433
)
cursor = conn.cursor()

def save_order(order):
    cursor.execute(
        "INSERT INTO orders (user_id, amount, timestamp) VALUES (%s, %s, %s)",
        (order['user_id'], order['amount'], order['timestamp'])
    )
    conn.commit()

for message in consumer:
    order = message.value
    save_order(order)
    print(f"Consumed: {order}")
