from workers.celery_worker import celery


@celery.task
def test_task():
    return "NuKropAI task working"
