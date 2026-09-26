from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import HikingStory
from .forms import StoryForm, CommentForm
def stories(request):
    return render(request, "community/list.html", {"stories": HikingStory.objects.select_related("author", "mountain").order_by("-created_at")})
def detail(request, pk):
    story = get_object_or_404(HikingStory.objects.select_related("author", "mountain"), pk=pk)
    form = CommentForm(request.POST or None)
    if request.method == "POST" and request.user.is_authenticated and form.is_valid():
        obj = form.save(commit=False)
        obj.story = story
        obj.author = request.user
        obj.save()
        return redirect("story_detail", pk=pk)
    return render(request, "community/detail.html", {"story": story, "form": form})
@login_required
def create(request):
    form = StoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()
        return redirect("stories")
    return render(request, "community/create.html", {"form": form})
@login_required
def like(request, pk):
    story = get_object_or_404(HikingStory, pk=pk)
    if request.user in story.likes.all():
        story.likes.remove(request.user)
    else:
        story.likes.add(request.user)
    return redirect("story_detail", pk=pk)
