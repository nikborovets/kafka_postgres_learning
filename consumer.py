from kafka import KafkaConsumer
import cv2
import base64
import json
import numpy as np
import psycopg2
from io import BytesIO

consumer = KafkaConsumer(
    'frames',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='frame-group',
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

def save_frame(frame_data, timestamp):
    cursor.execute(
        "INSERT INTO frames (frame_data, timestamp) VALUES (%s, %s)",
        (frame_data, timestamp)
    )
    conn.commit()

for message in consumer:
    frame_str = message.value['frame']
    frame_bytes = base64.b64decode(frame_str)
    
    nparr = np.frombuffer(frame_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    _, buffer = cv2.imencode('.jpg', gray_img)
    frame_data = base64.b64encode(buffer).decode('utf-8')
    timestamp = message.value['timestamp']
    
    save_frame(frame_data, timestamp)
    # save_frame(frame_str, timestamp)
    
    print(f"Consumed and saved frame with timestamp: {timestamp}")