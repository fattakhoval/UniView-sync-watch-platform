from django.urls import path
from .views import video_page, test_video_page

urlpatterns = [
    path('', video_page, name='video_page'),
    path('test_video/', test_video_page, name='test_page_video')
]