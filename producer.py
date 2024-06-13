from kafka import KafkaProducer
import cv2
import base64
import time
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break
    
    _, buffer = cv2.imencode('.jpg', frame)
    frame_bytes = base64.b64encode(buffer).decode('utf-8')
    message = {'frame': frame_bytes, 'timestamp': int(time.time())}
    
    producer.send('frames', message)
    print(f"Produced: {message}")
    time.sleep(1)

cap.release()