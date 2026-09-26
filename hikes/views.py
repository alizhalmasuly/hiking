from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Equipment, Hike
from .forms import HikeForm
@login_required
def prepare(request):
    form = HikeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        hike = form.save(commit=False)
        hike.user = request.user
        hike.save()
        form.save_m2m()
        return redirect("prepare")
    return render(request, "hikes/prepare.html", {"form": form, "equipment": Equipment.objects.all(), "hikes": Hike.objects.filter(user=request.user).select_related("mountain")})
