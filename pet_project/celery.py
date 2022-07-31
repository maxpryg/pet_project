import os

from celery import Celery

from django.conf import settings

# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_project.settings')

# you can change the name here
app = Celery("pet_project")

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# discover and load tasks.py in django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y
