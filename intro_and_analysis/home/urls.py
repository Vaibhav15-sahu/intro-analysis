from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('home/', views.home, name='home'),
    path('all-videos/', views.all_videos, name='all_videos'),
    path('upload/', views.upload_video, name='upload_video')
]