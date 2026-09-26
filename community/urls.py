from django.urls import path
from . import views
urlpatterns = [path("", views.stories, name="stories"), path("new/", views.create, name="story_create"), path("<int:pk>/", views.detail, name="story_detail"), path("<int:pk>/like/", views.like, name="story_like")]
