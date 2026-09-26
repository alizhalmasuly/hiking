from django import forms
from .models import Hike
from django.utils.translation import gettext, gettext_lazy as _
class HikeForm(forms.ModelForm):
    class Meta:
        model = Hike
        fields = ["mountain", "date", "season", "duration_hours", "group_size", "equipment"]
        labels = {"mountain": _("Гора или маршрут"), "date": _("Дата похода"), "season": _("Сезон"), "duration_hours": _("Длительность, часов"), "group_size": _("Размер группы"), "equipment": _("Снаряжение")}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mountain"].label_from_instance = lambda mountain: gettext(mountain.name)
        self.fields["equipment"].label_from_instance = lambda item: gettext(item.name)
