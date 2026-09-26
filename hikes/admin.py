from django.contrib import admin
from .models import Equipment, Hike, SavedHike
admin.site.register([Equipment, Hike, SavedHike])
