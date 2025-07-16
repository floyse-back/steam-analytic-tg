from celery import Celery

from src.shared.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from celery.app.log import get_logger

app = Celery(
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

logger = get_logger("celery")

app.autodiscover_tasks(
    [
        'src.infrastructure.celery.tasks.news_tasks',
        'src.infrastructure.celery.tasks.subscribes_tasks',
    ]
)