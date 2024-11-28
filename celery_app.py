import logging
import time

from celery import Celery

CELERY_BROKER_URL = "sqla+postgresql://itzhak:12345@localhost:5432/itzhakdb"
CELERY_RESULT_BACKEND = "db+postgresql://itzhak:12345@localhost:5432/itzhakdb"

celery = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"]
)

@celery.task
def my_task(customer_name: str):
    logging.info(f"============================== task started =================================")
    logging.info(f"Processing customer: {customer_name}")
    time.sleep(10)
    logging.info(f"============================== task finished =================================")