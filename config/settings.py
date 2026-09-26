import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
try:
    from dotenv import load_dotenv
except ImportError:
    # Keep the prototype runnable even if optional environment helpers were not installed.
    load_dotenv = None
if load_dotenv:
    load_dotenv(BASE_DIR / ".env")
else:
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                name, value = line.split("=", 1)
                os.environ.setdefault(name.strip(), value.strip().strip("\"'"))
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    # Keep local setup convenient; production deployments must provide a private key.
    if os.environ.get("VERCEL"):
        raise RuntimeError("Set DJANGO_SECRET_KEY in the Vercel project environment variables.")
    SECRET_KEY = "local-development-only-do-not-use-in-production"
DEBUG = os.environ.get("DEBUG", "False").lower() in {"1", "true", "yes"}
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".vercel.app",
]
vercel_url = os.environ.get("VERCEL_URL")
if vercel_url:
    vercel_host = vercel_url.removeprefix("https://").removeprefix("http://")
    ALLOWED_HOSTS.append(vercel_host)
    CSRF_TRUSTED_ORIGINS = [f"https://{vercel_host}"]
else:
    CSRF_TRUSTED_ORIGINS = []
INSTALLED_APPS = ["django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles", "accounts", "mountains", "hikes", "community", "weather", "ai_assistant"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.locale.LocaleMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [BASE_DIR / "templates"], "APP_DIRS": True, "OPTIONS": {"context_processors": ["django.template.context_processors.request", "django.template.context_processors.i18n", "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
database_url = os.environ.get("DATABASE_URL")
if database_url:
    import dj_database_url

    DATABASES = {"default": dj_database_url.parse(database_url, conn_max_age=600, ssl_require=True)}
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "ru"
LANGUAGES = [("ru", "Русский"), ("kk", "Қазақша"), ("en", "English")]
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "Asia/Almaty"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "profile"
LOGOUT_REDIRECT_URL = "home"
