from pathlib import Path
from datetime import timedelta
from decouple import config
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY", default="change-me")
DEBUG = config("DEBUG", cast=bool, default=False)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sites",

    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "drf_spectacular",
    "channels",

    "apps.core",
    "apps.accounts",
    "apps.rbac",
    "apps.org",
    "apps.people",
    "apps.projects",
    "apps.communications",
    "apps.cybergrc",

    "apps.core.files",
    "apps.hr",
    "apps.volunteers",
    "apps.requests",
    "apps.inventory",
    "apps.assets",
    "apps.fleet",
    "apps.procurement",
    "apps.documents",
    "apps.reporting",
    "apps.finance",
    "apps.budgets",
    "apps.memberships",
    "apps.alerts",
    "apps.shelters",
    "apps.case_management",
    "apps.health_facilities",
    "apps.patients",
    "apps.medical",
    "apps.epidemiology",
    "apps.events",
    "apps.missing_persons",
    "apps.victim_identification",
    "apps.locations",
    "apps.content",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="relief_db"),
        "USER": config("DB_USER", default="relief_user"),
        "PASSWORD": config("DB_PASSWORD", default="relief_pass"),
        "HOST": config("DB_HOST", default="db"),
        "PORT": config("DB_PORT", cast=int, default=5432),
    }
}

AUTH_USER_MODEL = "accounts.User"
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Africa/Douala"
USE_I18N = True
USE_TZ = True
SITE_ID = 1

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@opengrc.local")
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=25)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=False)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False)
EMAIL_TIMEOUT = config("EMAIL_TIMEOUT", cast=int, default=10)

CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="http://localhost:5173").split(",")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.StandardResultsSetPagination",
    "PAGE_SIZE": 20,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Relief Platform API",
    "DESCRIPTION": "Starter professionnel humanitaire et opérationnel.",
    "VERSION": "4.3.0",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=config("ACCESS_TOKEN_LIFETIME_MINUTES", cast=int, default=60)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=config("REFRESH_TOKEN_LIFETIME_DAYS", cast=int, default=7)),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

REDIS_URL = config("REDIS_URL", default="redis://redis:6379/1")
CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="redis://redis:6379/2")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="redis://redis:6379/3")
CHANNEL_REDIS_URL = config("CHANNEL_REDIS_URL", default="redis://redis:6379/4")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Africa/Douala"
CELERY_BEAT_SCHEDULE = {
    "daily-cleanup-soft-deleted": {
        "task": "apps.core.tasks.cleanup_soft_deleted_records",
        "schedule": crontab(hour=2, minute=0),
    },
    "daily-generate-summary-notifications": {
        "task": "apps.projects.tasks.generate_daily_reporting_snapshot",
        "schedule": crontab(hour=6, minute=0),
    },
    "consultation-meeting-reminders": {
        "task": "apps.cybergrc.tasks.send_consultation_reminders",
        "schedule": crontab(minute="*/15"),
    },
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [CHANNEL_REDIS_URL]},
    }
}
