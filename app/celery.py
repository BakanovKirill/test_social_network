from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")

from django.conf import settings

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    # 'test-task': {
    #     'task': 'app.social_network.test_task',
    #     'schedule': 60,
    # }
}
