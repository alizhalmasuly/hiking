import os
try:
    import requests
except ImportError:
    requests = None
def forecast_for(location="Almaty", language="ru"):
    key = os.getenv("WEATHER_API_KEY")
    if key and requests:
        try:
            api_language = {"ru": "ru", "kk": "kk", "en": "en"}.get(language, "ru")
            response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params={"q": location, "appid": key, "units": "metric", "lang": api_language}, timeout=5)
            response.raise_for_status()
            data = response.json()
            current = data["list"][0]
            return {"location": data["city"]["name"], "temp": round(current["main"]["temp"]), "feels": round(current["main"]["feels_like"]), "condition": current["weather"][0]["description"].title(), "wind": current["wind"]["speed"], "humidity": current["main"]["humidity"], "forecast": data["list"][1:6]}
        except Exception:
            pass
    demo = {
        "ru": ("Переменная облачность", "Завтра", "Лёгкий дождь", "Послезавтра", "Ясно"),
        "en": ("Partly cloudy", "Tomorrow", "Light rain", "Day after tomorrow", "Clear"),
        "kk": ("Ала бұлтты", "Ертең", "Сәл жаңбыр", "Бүрсігүні", "Ашық"),
    }.get(language, ("Переменная облачность", "Завтра", "Лёгкий дождь", "Послезавтра", "Ясно"))
    condition, tomorrow, rain, later, clear = demo
    return {"location": location, "temp": 12, "feels": 9, "condition": condition, "wind": 4, "humidity": 48, "forecast": [{"dt_txt": tomorrow, "main": {"temp": 10}, "weather": [{"description": rain}]}, {"dt_txt": later, "main": {"temp": 14}, "weather": [{"description": clear}]}]}
