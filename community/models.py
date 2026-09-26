from django.conf import settings
from django.db import models
from mountains.models import Mountain
from django.utils.translation import gettext_lazy as _
class HikingStory(models.Model):
    DIFFICULTY_CHOICES = [(value, _(value)) for value in ["Лёгкий", "Средний", "Сложный"]]
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stories")
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE, related_name="stories")
    title = models.CharField(max_length=200)
    hike_date = models.DateField()
    difficulty = models.CharField(max_length=30, choices=DIFFICULTY_CHOICES, default="Средний")
    description = models.TextField()
    tips = models.TextField(blank=True)
    equipment_used = models.CharField(max_length=400, blank=True)
    cover_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="liked_stories")
    def __str__(self): return self.title
class Comment(models.Model):
    story = models.ForeignKey(HikingStory, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.author}: {self.text[:40]}"
