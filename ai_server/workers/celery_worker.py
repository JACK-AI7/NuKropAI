from celery import Celery

celery = Celery(
    "nukropai",
    broker="redis://localhost:6379/0"
)
