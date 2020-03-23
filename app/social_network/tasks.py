import logging

from app.celery import app
from app.clients import clearbit_client
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)


@app.task(name="app.social_network.enrich_user")
def enrich_user(user_id: int):
    logger.info("Enrich user %s", user_id)
    user = User.objects.get(id=user_id)

    result = clearbit_client.get_enrichment(user.email)
    if result is not None:
        # Clearbit overrides default dict.get() method.
        # https://github.com/clearbit/clearbit-python/issues/8
        if dict.get(result, "person"):
            user.first_name, user.last_name = result["person"]["name"][
                "fullName"
            ].split(" ", 1)
        if dict.get(result, "company"):
            user.first_name = result["company"]["name"]

        user.save()


@app.task(name="app.social_network.test_task")
def debug_task():
    print("\n==========================")
    print("\nCelery beat is working....")
    print("\n==========================\n")
