from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
import myapp.services as services


my_service = services.MyCustomService()

# Get a logger for this module.
logger = get_task_logger(__name__)

@shared_task(name='my_task_service', queue='high')
def my_task_service(x, *args, **kwargs):
    logger.info(f'Executing my task service.')
    return my_service.execute(x)