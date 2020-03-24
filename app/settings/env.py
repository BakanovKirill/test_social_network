import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    CELERY_TASK_ALWAYS_EAGER=(bool, True),
)
base = environ.Path(__file__) - 3
environ.Env.read_env(env_file=base(".env"))  # reading .env file

DEBUG = env("DEBUG")

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    "default": env.db(
        default="postgres://social_network:social_network@db:5432/social_network"
    )
}
CELERY_TASK_ALWAYS_EAGER = env("CELERY_TASK_ALWAYS_EAGER")
