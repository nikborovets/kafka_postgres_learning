from django.urls import path
from .views import FrameListView, FrameDetailView, VideoCreateView

urlpatterns = [
    path('', FrameListView.as_view(), name='frame_list'),
    path('frame/<int:frame_id>/', FrameDetailView.as_view(), name='frame_detail'),
    path('create_video/', VideoCreateView.as_view(), name='create_video'),
]
