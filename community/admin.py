from django.contrib import admin
from .models import HikingStory, Comment
admin.site.register([HikingStory, Comment])
