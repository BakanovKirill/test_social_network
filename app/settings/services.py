from datetime import timedelta

from .env import env

# DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}

# djangorestframework_simplejwt
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
}

# drf-yasg
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    }
}


# Celery
CELERY_TASK_ALWAYS_EAGER = env("CELERY_TASK_ALWAYS_EAGER")
CELERY_BROKER_URL = "redis://redis:6379/"
CELERY_RESULT_BACKEND = "redis://redis:6379/"

# Clearbit
CLEARBIT_API_KEY = "sk_5b52080c7dc3dfeaff1ea98709fd7989"

# pyhunter
PYHUNTER_API_KEY = "5364c3d05e43112352f98d529e300d39caea022e"

# Automatic bots
BOT_NUMBER_OF_USERS = int(env("BOT_NUMBER_OF_USERS"))
BOT_MAX_POSTS_PER_USER = int(env("BOT_MAX_POSTS_PER_USER"))
BOT_MAX_LIKES_PER_USER = int(env("BOT_MAX_LIKES_PER_USER"))
