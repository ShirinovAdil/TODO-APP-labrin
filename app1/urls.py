from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path('^$', views.homepage, name="homepage"),
    re_path('^add-task', views.add_task, name="add_task"),
    path('<int:pk>/share-task', views.share_task, name='share_task'),
    path('<int:pk>/edit-task', views.edit_task, name='edit_task'),
    path('<int:pk>/view-task', views.view_task, name='view_task'),
]
