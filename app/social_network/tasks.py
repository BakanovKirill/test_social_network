import logging
from datetime import datetime
from random import randint

from django.conf import settings
from django.contrib.auth import get_user_model
from factory import faker

from app.celery import app
from app.clients import clearbit_client
from app.social_network.models import Bot, Like, Post
from app.social_network.utils import bulk_create_objects

User = get_user_model()
logger = logging.getLogger(__name__)


@app.task(name="app.social_network.test_task")
def debug_task() -> None:
    print("\n==========================")
    print("\nCelery beat is working....")
    print("\n==========================\n")


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


@app.task(name="app.social_network.launch_bots")
def launch_bots() -> None:
    current_users = []
    for i in range(0, settings.BOT_NUMBER_OF_USERS):
        user = User(username=f"bot_{i}_{datetime.now().isoformat()}")
        user.set_password(f"bot_{i}")
        user.save()
        Bot.objects.create(user=user)
        current_users.append(user)

    fake_title = faker.Faker("word")
    fake_text = faker.Faker("catch_phrase")

    posts = []
    for user in current_users:
        for i in range(0, randint(1, settings.BOT_MAX_POSTS_PER_USER)):
            posts.append(
                Post(
                    title=fake_title.generate(), text=fake_text.generate(), author=user
                )
            )

    bulk_create_objects(Post, posts)

    bot_posts = Post.objects.filter(author__bot__isnull=False)

    likes = []
    for user in current_users:
        posts_to_like = bot_posts.order_by("?")[
            : randint(1, settings.BOT_MAX_LIKES_PER_USER)
        ]
        for post in posts_to_like:
            likes.append(Like(post=post, author=user))

    bulk_create_objects(Like, likes)
