from django.urls import re_path
from . import views


urlpatterns = [
    re_path('^$', views.homepage, name="homepage"),
    re_path('^add-task', views.add_task, name="add_task"),
    re_path(r'^(?P<pk>\d+)/share-task$', views.share_task, name='share_task'),
    re_path(r'^(?P<pk>\d+)/edit-task$', views.edit_task, name='edit_task'),
]
