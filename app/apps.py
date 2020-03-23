from django.apps import AppConfig


class SocialNetworkAppConfig(AppConfig):
    name = "app"
    verbose_name = "app"

    def ready(self):
        import app.social_network.tasks
