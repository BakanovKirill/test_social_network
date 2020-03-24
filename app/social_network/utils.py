from itertools import islice
from typing import Optional

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def get_tokens_for_user(user: User) -> dict:
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def chunks(lst: list, n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def bulk_create_objects(
    model_cls, objects: list, batch_size: Optional[int] = 100
) -> None:
    for chunk in chunks(objects, batch_size):
        if not chunk:
            break
        model_cls.objects.bulk_create(chunk, batch_size)
