from django.urls import path
from . import views
urlpatterns = [path("", views.mountain_list, name="mountain_list"), path("<slug:slug>/", views.detail, name="mountain_detail")]
