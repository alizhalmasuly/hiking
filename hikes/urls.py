from django.urls import path
from .views import prepare
urlpatterns = [path("prepare/", prepare, name="prepare")]
