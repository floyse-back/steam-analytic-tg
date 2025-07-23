import asyncio

from celery import Celery
from kombu import Queue, Exchange

from src.shared.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from celery.app.log import get_logger


app = Celery(
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)
app.conf.task_default_exchange = "analytic_tg_bot"
app.conf.task_default_queue = "analytic_tg_bot"
app.conf.task_default_routing_key = "analytic_tg_bot"

app.conf.task_queues = (
    Queue("subscribes_bot",Exchange("subscribes_bot"),routing_key="src.infrastructure.celery.tasks.subscribes_tasks"),
    Queue("news_bot",Exchange("news_bot"),routing_key="src.infrastructure.celery.tasks.news_tasks"),
)
app.conf.task_routes = {
    'src.infrastructure.celery.tasks.subscribes_tasks.*': {
        'queue': 'subscribes_bot',
        'routing_key': 'src.infrastructure.celery.tasks.subscribes_tasks',
    },
    'src.infrastructure.celery.tasks.news_tasks.*': {
        'queue': 'news_bot',
        'routing_key': 'src.infrastructure.celery.tasks.news_tasks',
    },
}

logger = get_logger("celery")

app.autodiscover_tasks(
    [
        'src.infrastructure.celery.tasks.news_tasks',
        'src.infrastructure.celery.tasks.subscribes_tasks',
    ]
)

def run_async(coro):
    import asyncio

    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError("Event loop is closed")
    except (RuntimeError, AssertionError):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(coro)
