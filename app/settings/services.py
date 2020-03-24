from datetime import timedelta

CLEARBIT_API_KEY = "sk_5b52080c7dc3dfeaff1ea98709fd7989"
PYHUNTER_API_KEY = "5364c3d05e43112352f98d529e300d39caea022e"

CELERY_BROKER_URL = "redis://redis:6379/"
CELERY_RESULT_BACKEND = "redis://redis:6379/"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
