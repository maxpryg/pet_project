# from django.core.mail import send_mail
#
# from pet_project.celery import app
#
#
# @app.task
# def send_mail_to(datatuple):
#     send_mail(datatuple)

from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task
def sample_task():
    logger.info("The sample task just ran.")

