from django.db import models
from django.utils.translation import gettext_lazy as _
class Mountain(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    region = models.CharField(max_length=150, default="Алматинская область")
    altitude = models.PositiveIntegerField(help_text="метров")
    difficulty = models.CharField(max_length=30, choices=[("easy", _("Лёгкий")), ("moderate", _("Средний")), ("hard", _("Сложный"))], default="moderate")
    duration = models.CharField(max_length=80, default="1 день")
    distance = models.CharField(max_length=50, blank=True)
    season = models.CharField(max_length=100, default="Июнь — сентябрь")
    description = models.TextField()
    safety = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    latitude = models.FloatField(default=43.0)
    longitude = models.FloatField(default=77.0)
    featured = models.BooleanField(default=False)
    def __str__(self): return self.name
