from django.shortcuts import render
from .services import forecast_for
def dashboard(request):
    language = getattr(request, "LANGUAGE_CODE", "ru")
    location = request.GET.get("location") or ("Almaty" if language == "en" else "Алматы")
    return render(request, "weather/dashboard.html", {"weather": forecast_for(location, language), "location": location})
