# config/settings.py
import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Environment settings
FASTAPI_ENV = os.getenv('FASTAPI_ENV', 'development')
DEBUG = FASTAPI_ENV == 'development'

# Installed apps (Django-like); each gets its own Tortoise "app" for per-app migrations
INSTALLED_APPS = [
    "apps.user",
]

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://db.sqlite3")
# Connection pool tuning (for PostgreSQL/MySQL; SQLite ignores these)
TORTOISE_ORM_POOL_MIN_SIZE = int(os.getenv("TORTOISE_ORM_POOL_MIN_SIZE", "5"))
TORTOISE_ORM_POOL_MAX_SIZE = int(os.getenv("TORTOISE_ORM_POOL_MAX_SIZE", "20"))
TORTOISE_ORM_COMMAND_TIMEOUT = int(os.getenv("TORTOISE_ORM_COMMAND_TIMEOUT", "30"))

# Tortoise ORM: one key per INSTALLED_APP for Django-like per-app migrations (Aerich)
# App label = last part of path (e.g. "apps.user" -> "user"); aerich.models only in first app
def _build_tortoise_apps():
    apps_config = {}
    for i, app_path in enumerate(INSTALLED_APPS):
        label = app_path.split(".")[-1]
        models_list = [f"{app_path}.models"]
        if i == 0:
            models_list.append("aerich.models")
        apps_config[label] = {
            "models": models_list,
            "default_connection": "default",
        }
    return apps_config


TORTOISE_ORM_CONFIG = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": _build_tortoise_apps(),
}

# Celery settings
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# JWT auth
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'change-me-in-production')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_ACCESS_EXPIRE_MINUTES = int(os.getenv('JWT_ACCESS_EXPIRE_MINUTES', '1440'))  # 1 day


# Logging settings (example)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'INFO',
    },
}
