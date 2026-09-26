# Деплой на Vercel

Проект автоматически распознаётся Vercel как Django-приложение. При сборке запускаются миграции и команда `seed_data` из `pyproject.toml`.

## Переменные окружения

В настройках проекта Vercel → **Settings → Environment Variables** добавьте `DJANGO_SECRET_KEY` со случайным секретом. Создать его локально можно командой:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Добавьте ключ в Production и Preview, затем сделайте новый деплой. Приложение также принимает стандартное имя `SECRET_KEY`.

Для сохранения пользовательских данных подключите в Vercel постоянную PostgreSQL-базу и передайте её строку подключения как `DATABASE_URL`. Если переменная отсутствует, сборка использует SQLite с демо-данными; SQLite в serverless-среде не подходит для постоянных пользовательских записей.

`VERCEL_URL` автоматически добавляется Vercel. Настройки используют его для разрешённых хостов и CSRF.
