import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext

from mountains.models import Mountain
from .models import ChatMessage
from .services.ai_assistant import get_recommendation


def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body or "{}")
            if data.get("action") == "reset":
                request.session.pop("ai_assistant_history", None)
                request.session.pop("ai_assistant_context", None)
                return JsonResponse({"ok": True})
            message = data.get("message", "")
            if not isinstance(message, str):
                invalid_message = {"ru": "Сообщение должно быть текстом.", "kk": "Хабарлама мәтін болуы керек.", "en": "Message must be text."}.get(getattr(request, "LANGUAGE_CODE", "ru"), "Message must be text.")
                return JsonResponse({"error": invalid_message}, status=400)
            message = message[:2000]
            if not message.strip():
                empty_message = {"ru": "Введите вопрос или список снаряжения.", "kk": "Сұрақты немесе жабдық тізімін енгізіңіз.", "en": "Enter a question or list the gear you have."}.get(getattr(request, "LANGUAGE_CODE", "ru"), "Enter a question or list the gear you have.")
                return JsonResponse({"error": empty_message}, status=400)

            history = request.session.get("ai_assistant_history", [])[-10:]
            context = request.session.get("ai_assistant_context", {})
            context.update(data.get("context") or {})
            context["language"] = getattr(request, "LANGUAGE_CODE", "ru")
            mountain_name = context.get("mountain")
            if mountain_name:
                mountain = Mountain.objects.filter(name=mountain_name).first()
                if mountain:
                    context["altitude_m"] = mountain.altitude
                    context["difficulty"] = mountain.get_difficulty_display()
                    context["route_duration"] = mountain.duration
            allowed_context = {"mountain", "season", "duration", "language", "altitude_m", "difficulty", "route_duration"}
            context = {key: value for key, value in context.items() if key in allowed_context}

            assistant_context = context.copy()
            if assistant_context.get("mountain"):
                assistant_context["mountain"] = gettext(assistant_context["mountain"])
            for key in ("season", "duration", "route_duration"):
                if assistant_context.get(key):
                    assistant_context[key] = gettext(assistant_context[key])
            result = get_recommendation(message, assistant_context, history)
            reply = result["reply"]
            history.extend([{"role": "user", "content": message}, {"role": "assistant", "content": reply}])
            request.session["ai_assistant_history"] = history[-12:]
            request.session["ai_assistant_context"] = context
            if request.user.is_authenticated:
                ChatMessage.objects.create(user=request.user, role="user", content=message)
                ChatMessage.objects.create(user=request.user, role="assistant", content=reply)
            analysis = {key: result[key] for key in ("have", "missing", "score", "alerts", "mode")}
            return JsonResponse({"reply": reply, "analysis": analysis})
        except (ValueError, TypeError):
            error = {"ru": "Некорректный запрос.", "kk": "Сұрау қате.", "en": "Invalid request."}.get(getattr(request, "LANGUAGE_CODE", "ru"), "Invalid request.")
            return JsonResponse({"error": error}, status=400)

    return render(request, "ai_assistant/chat.html", {
        "mountains": Mountain.objects.all(),
        "history": request.session.get("ai_assistant_history", [])[-12:],
        "saved_context": request.session.get("ai_assistant_context", {}),
    })
