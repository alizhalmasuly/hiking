from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileForm
from .models import Profile
def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        Profile.objects.get_or_create(user=user)
        login(request, user)
        return redirect("profile")
    return render(request, "accounts/signup.html", {"form": form})
@login_required
def profile(request):
    instance, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("profile")
    return render(request, "accounts/profile.html", {"form": form, "stories": request.user.stories.all(), "saved": request.user.savedhike_set.select_related("mountain")})
