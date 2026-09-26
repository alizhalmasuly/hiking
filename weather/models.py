from django.db import models
class WeatherCache(models.Model):
    location = models.CharField(max_length=150)
    payload = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return self.location
