import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True),
    CELERY_TASK_ALWAYS_EAGER=(bool, False),
    BOT_NUMBER_OF_USERS=(int, 5),
    BOT_MAX_POSTS_PER_USER=(int, 5),
    BOT_MAX_LIKES_PER_USER=(int, 5),
)
base = environ.Path(__file__) - 3
environ.Env.read_env(env_file=base(".env"))  # reading .env file
DEBUG = env("DEBUG")
