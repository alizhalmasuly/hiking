from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {"username": _("Имя пользователя"), "email": _("Электронная почта"), "password1": _("Пароль"), "password2": _("Повторите пароль")}
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "avatar_url", "home_region"]
        labels = {"bio": _("О себе"), "avatar_url": _("Ссылка на аватар"), "home_region": _("Ваш регион")}
