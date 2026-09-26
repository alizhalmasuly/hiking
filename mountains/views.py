from django.shortcuts import render, get_object_or_404
from .models import Mountain
def home(request):
    mountains = Mountain.objects.filter(featured=True)[:6]
    return render(request, "home.html", {"mountains": mountains or Mountain.objects.all()[:6]})
def mountain_list(request):
    return render(request, "mountains/list.html", {"mountains": Mountain.objects.all()})
def detail(request, slug):
    return render(request, "mountains/detail.html", {"mountain": get_object_or_404(Mountain, slug=slug)})
