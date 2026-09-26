from django.conf import settings
from django.db import models
from mountains.models import Mountain
from django.utils.translation import gettext_lazy as _
class Equipment(models.Model):
    CATEGORY_CHOICES = [(value, _(value)) for value in ["Одежда", "Навигация", "Еда и вода", "Безопасность", "Кемпинг"]]
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    essential = models.BooleanField(default=True)
    description = models.CharField(max_length=240, blank=True)
    def __str__(self): return self.name
class Hike(models.Model):
    SEASON_CHOICES = [(value, _(value)) for value in ["Весна", "Лето", "Осень", "Зима"]]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hikes")
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE, related_name="hikes")
    date = models.DateField(null=True, blank=True)
    season = models.CharField(max_length=40, choices=SEASON_CHOICES, default="Лето")
    duration_hours = models.PositiveSmallIntegerField(default=6)
    group_size = models.PositiveSmallIntegerField(default=1)
    equipment = models.ManyToManyField(Equipment, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.mountain} — {self.user}"
class SavedHike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE)
    class Meta: unique_together = ("user", "mountain")
