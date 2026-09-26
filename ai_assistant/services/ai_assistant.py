import os

try:
    import requests
except ImportError:
    requests = None

GEAR = {
    "boots": ("Треккинговые ботинки", "Hiking boots", "Жаяу жүруге арналған етік", ("ботин", "треккинговая обувь", "hiking boot", "trekking shoe", "boots", "етік")),
    "backpack": ("Рюкзак", "Backpack", "Рюкзак", ("рюкзак", "backpack", "дорба")),
    "water": ("Вода", "Water", "Су", ("вода", "литр", "water", "hydration", "су")),
    "jacket": ("Непромокаемая куртка", "Waterproof jacket", "Су өткізбейтін күртеше", ("куртк", "дождевик", "ветровк", "rain jacket", "waterproof", "shell", "күртеше")),
    "warm": ("Тёплый слой одежды", "Warm mid-layer", "Жылы киім қабаты", ("термо", "флис", "тёпл", "тепл", "warm layer", "fleece", "жылы киім")),
    "navigation": ("Офлайн-карта или GPS", "Offline map or GPS", "Офлайн карта немесе GPS", ("карт", "компас", "gps", "навигац", "map", "compass", "navigation", "бағдар")),
    "first_aid": ("Аптечка", "First-aid kit", "Алғашқы көмек қобдишасы", ("аптеч", "первая помощь", "first aid", "first-aid", "дәрі қобдишасы")),
    "light": ("Налобный фонарь", "Headlamp", "Бас шамы", ("фонар", "налобн", "headlamp", "flashlight", "фонарик", "шам")),
    "food": ("Перекус и запас еды", "Snacks and food", "Жеңіл ас және азық", ("перекус", "еда", "снек", "батончик", "food", "snack", "азық", "тамақ")),
    "gloves": ("Перчатки", "Gloves", "Қолғап", ("перчат", "рукавиц", "glove", "қолғап")),
    "power": ("Заряженный телефон и power bank", "Charged phone and power bank", "Қуатталған телефон және power bank", ("power bank", "пауэрбанк", "повербанк", "заряженный телефон", "phone battery", "қуаттағыш")),
    "tent": ("Палатка", "Tent", "Шатыр", ("палат", "tent", "шатыр")),
    "sleeping": ("Спальный мешок и коврик", "Sleeping bag and mat", "Ұйықтайтын қап пен төсеніш", ("спальник", "спальный мешок", "sleeping bag", "sleeping mat", "ұйықтайтын қап")),
    "whistle": ("Свисток", "Emergency whistle", "Ысқырық", ("свисток", "whistle", "ысқырық")),
}


def _demo_analysis(message, context, history):
    language = context.get("language", "ru")
    conversation = " ".join([entry.get("content", "") for entry in history if entry.get("role") == "user"] + [message]).casefold()
    have = [key for key, (_, _, _, terms) in GEAR.items() if any(term in conversation for term in terms)]
    season = (context.get("season") or "Лето").casefold()
    duration = (context.get("duration") or "1 день").casefold()
    multi_day = any(word in duration for word in ("2 дня", "3 дня", "несколько", "multi", "2 day", "3 day", "бірнеше", "2 күн", "3 күн"))
    winter = any(word in season for word in ("зим", "winter", "қыс"))
    essentials = ["boots", "backpack", "water", "jacket", "warm", "navigation", "first_aid", "light", "food", "power"]
    if winter:
        essentials += ["gloves"]
    if multi_day:
        essentials += ["tent", "sleeping"]
    missing = [key for key in essentials if key not in have]
    score = round(100 * (len(essentials) - len(missing)) / max(1, len(essentials)))
    name_index = {"ru": 0, "en": 1, "kk": 2}.get(language, 0)
    label = lambda key: GEAR[key][name_index]
    route = context.get("mountain") or {"ru": "выбранный маршрут", "en": "your route", "kk": "таңдалған маршрут"}.get(language, "выбранный маршрут")
    if language == "en":
        reply = f"For {route} in {context.get('season', 'your selected season')}, I’ve noted {', '.join(label(key) for key in have) or 'no confirmed gear yet'}.\n\nStill to pack or confirm: {', '.join(label(key) for key in missing[:6]) or 'your core kit looks covered'}."
        if winter:
            reply += "\n\nWinter reminder: check snow and wind conditions, carry warm gloves and eye protection, and turn back if the route is unsafe."
        elif multi_day:
            reply += "\n\nFor an overnight trip, confirm your shelter, sleeping system, extra food and a way to keep your phone powered."
        reply += "\n\nCheck the official mountain forecast and share your route and return time with someone."
    elif language == "kk":
        reply = f"{route} бағытына {context.get('season', 'таңдалған маусым')} кезінде баруға дайындық. Белгілеген заттар: {', '.join(label(key) for key in have) or 'әзірге расталған жабдық жоқ'}.\n\nҚосу немесе тексеру керек: {', '.join(label(key) for key in missing[:6]) or 'негізгі жабдық толық сияқты'}."
        if winter:
            reply += "\n\nҚысқы ескерту: қар мен жел жағдайын тексеріп, жылы қолғап пен көзді қорғауды алыңыз. Бағыт қауіпті болса, кері қайтыңыз."
        elif multi_day:
            reply += "\n\nКөпкүндік сапарға шатырды, ұйықтайтын жабдықты, қосымша азықты және телефон қуатын тексеріңіз."
        reply += "\n\nРесми ауа райы болжамын қарап, бағытыңыз бен қайту уақытын жақындарыңызға хабарлаңыз."
    else:
        reply = f"Маршрут «{route}», сезон — {context.get('season', 'выбранный сезон')}. Учёл в списке: {', '.join(label(key) for key in have) or 'пока нет подтверждённых вещей'}.\n\nДобавьте или проверьте: {', '.join(label(key) for key in missing[:6]) or 'основной комплект выглядит полным'}."
        if winter:
            reply += "\n\nЗимой отдельно проверьте снег и ветер, возьмите тёплые перчатки и защиту для глаз. При небезопасных условиях откажитесь от выхода."
        elif multi_day:
            reply += "\n\nДля ночёвки проверьте палатку, спальную систему, запас еды и возможность зарядить телефон."
        reply += "\n\nПеред выходом сверьтесь с официальным прогнозом и сообщите близким маршрут и время возвращения."
    alerts = []
    if int(context.get("altitude_m") or 0) >= 3000:
        alerts.append({"ru": "На высоте выше 3000 м темп набора высоты особенно важен. Учитывайте акклиматизацию и самочувствие группы.", "en": "Above 3,000 m, pace your ascent carefully and monitor how everyone is feeling.", "kk": "3000 м-ден жоғарыда биіктікке біртіндеп көтеріліп, топ мүшелерінің жағдайын бақылаңыз."}.get(language, "На высоте выше 3000 м учитывайте акклиматизацию и самочувствие группы."))
    if "слож" in str(context.get("difficulty", "")).casefold() or "hard" in str(context.get("difficulty", "")).casefold():
        alerts.append({"ru": "Маршрут отмечен как сложный: проверьте опыт участников, запас времени и план безопасного разворота.", "en": "This route is marked difficult: check the group's experience, time reserve and turnaround plan.", "kk": "Бағыт күрделі деп белгіленген: топ тәжірибесін, уақыт қорын және кері қайту жоспарын тексеріңіз."}.get(language, "Маршрут отмечен как сложный: проверьте опыт группы и запас времени."))
    if alerts:
        reply += "\n\n" + "\n".join("⚠ " + alert for alert in alerts)
    return {"reply": reply, "have": [label(key) for key in have], "missing": [label(key) for key in missing], "score": score, "alerts": alerts, "mode": "demo"}


def get_recommendation(message, context=None, history=None):
    context = context or {}
    history = (history or [])[-10:]
    key = os.getenv("AI_API_KEY")
    if key and requests:
        try:
            messages = [
                {"role": entry["role"], "content": entry["content"]}
                for entry in history
                if entry.get("role") in ("user", "assistant") and entry.get("content")
            ]
            messages.append({"role": "user", "content": message})
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
                json={
                    "model": "claude-3-5-sonnet-20240620",
                    "max_tokens": 650,
                    "system": f"You are a careful hiking preparation assistant. Reply in language code {context.get('language', 'ru')}. Trip context: {context}. Remember gear the hiker already listed in this conversation. Separate confirmed gear from items still needed. Consider season and trip duration. Never invent live weather or claim a route is safe. Encourage checking official forecasts and sharing the itinerary.",
                    "messages": messages,
                },
                timeout=15,
            )
            response.raise_for_status()
            reply = response.json()["content"][0]["text"]
            analysis = _demo_analysis(message, context, history)
            analysis.update({"reply": reply, "mode": "ai"})
            return analysis
        except Exception:
            pass
    return _demo_analysis(message, context, history)
