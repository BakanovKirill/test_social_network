import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture(scope="session", autouse=True)
def celery_config():
    return {
        "task_always_eager": True,
        "broker_url": "amqp://",
        "result_backend": "redis://",
    }
