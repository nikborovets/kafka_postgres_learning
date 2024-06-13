import psycopg2
import base64
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import os
from datetime import datetime

conn = psycopg2.connect(
    dbname='orders_db',
    user='user',
    password='password',
    host='localhost',
    port=5433
)
cursor = conn.cursor()

def list_frames():
    cursor.execute("SELECT frame_id, frame_data, timestamp FROM frames")
    rows = cursor.fetchall()
    
    for row in rows:
        new_row = []
        for value in row:
            if isinstance(value, str) and len(value) > 10:
                new_row.append(value[-10:] + "...")
            else:
                new_row.append(value)
        print(new_row)
    
    print("The number of frames: ", cursor.rowcount)
    
def display_frame(frame_id):
    cursor.execute("SELECT frame_data FROM frames WHERE frame_id = %s", (frame_id,))
    row = cursor.fetchone()
    
    if row is not None:
        frame_data = row[0]
        frame_bytes = base64.b64decode(frame_data)

        nparr = np.frombuffer(frame_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        
        img_pil.show()
    else:
        print("No frame found with the given frame_id")

def create_video_from_frames(output_path, fps=1):
    cursor.execute("SELECT frame_data FROM frames ORDER BY timestamp ASC")
    rows = cursor.fetchall()

    if not rows:
        print("No frames found in the database.")
        return

    frame_list = []
    for row in rows:
        frame_data = row[0]
        frame_bytes = base64.b64decode(frame_data)
        
        nparr = np.frombuffer(frame_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        frame_list.append(img)

    height, width = frame_list[0].shape[:2]
    # добавить когда-то проверку на размеры фреймов. если вдруг разные разрешения кадров будут
    # print(frame_list[1].shape)

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for frame in frame_list:
        out.write(frame)

    out.release()
    print(f"Video created at {output_path}")

def main():
    while True:
        print("Options: ")
        print("1. List frames")
        print("2. Display a frame")
        print("3. Create video from frames")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            list_frames()
        elif choice == '2':
            frame_id = input("Enter frame_id: ")
            display_frame(frame_id)
        elif choice == '3':
            if not os.path.isdir('videos'):
                os.makedirs('videos')
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            video_path = os.path.join(os.getcwd(), 'videos', f'output_video_{timestamp}.mp4')
            
            create_video_from_frames(video_path)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()