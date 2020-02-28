from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/<int:pk>/view-task', consumers.CommentConsumer),
]