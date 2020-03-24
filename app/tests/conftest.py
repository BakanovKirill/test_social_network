import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture(scope="session")
def celery_config():
    return {"task_always_eager": True}
