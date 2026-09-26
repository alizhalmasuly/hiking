from django import forms
from .models import HikingStory, Comment
from django.utils.translation import gettext, gettext_lazy as _
class StoryForm(forms.ModelForm):
    class Meta:
        model = HikingStory
        fields = ["title", "mountain", "hike_date", "difficulty", "description", "tips", "equipment_used", "cover_url"]
        labels = {"title": _("Название истории"), "mountain": _("Гора"), "hike_date": _("Дата похода"), "difficulty": _("Сложность"), "description": _("История похода"), "tips": _("Полезные советы"), "equipment_used": _("Использованное снаряжение"), "cover_url": _("Ссылка на обложку")}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mountain"].label_from_instance = lambda mountain: gettext(mountain.name)
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": _("Ваш комментарий")}
