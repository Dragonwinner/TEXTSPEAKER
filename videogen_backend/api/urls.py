from django.urls import path
from .views import GenerateVideoView

urlpatterns = [
    path('generatevideo/', GenerateVideoView.as_view(), name='generatevideo'),
]
