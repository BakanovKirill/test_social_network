from django.apps import AppConfig


class SocialNetworkAppConfig(AppConfig):
    name = "app.social_network"
    verbose_name = "app.social_network"

    def ready(self):
        import app.social_network.tasks
