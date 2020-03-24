import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    CELERY_TASK_ALWAYS_EAGER=(bool, False),
)
base = environ.Path(__file__) - 3
environ.Env.read_env(env_file=base(".env"))  # reading .env file
DEBUG = env("DEBUG")
