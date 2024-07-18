from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Frame
import base64
import cv2
import numpy as np
import os
from datetime import datetime

class FrameListView(View):
    def get(self, request):
        frames = Frame.objects.all()
        return render(request, 'frames/frame_list.html', {'frames': frames})

class FrameDetailView(View):
    def get(self, request, frame_id):
        frame = get_object_or_404(Frame, pk=frame_id)
        img_base64 = frame.frame_data
        # frame_bytes = base64.b64decode(frame.frame_data)
        # nparr = np.frombuffer(frame_bytes, np.uint8)
        # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # _, img_encoded = cv2.imencode('.jpg', img)
        # img_base64 = base64.b64encode(img_encoded).decode('utf-8')
        return render(request, 'frames/frame_detail.html', {'frame': frame, 'img_base64': img_base64})

class VideoCreateView(View):
    def get(self, request):
        frames = Frame.objects.order_by('timestamp').all()
        if not frames:
            return render(request, 'frames/video_create.html', {'message': 'No frames found in the database.'})

        frame_list = []
        for frame in frames:
            frame_data = frame.frame_data
            frame_bytes = base64.b64decode(frame_data)
            nparr = np.frombuffer(frame_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            frame_list.append(img)

        height, width = frame_list[0].shape[:2]
        if not os.path.isdir('videos'):
            os.makedirs('videos')

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        video_path = os.path.join('videos', f'output_video_{timestamp}.mp4')
        out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))

        for frame in frame_list:
            out.write(frame)

        out.release()
        return render(request, 'frames/video_create.html', {'message': f'Video created at {video_path}'})
