from .config import celery_app
from sqlmodel import Session


# Retry task failures with exponential backoff, up to five retries.
@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=5
)

def test_task(self,data):
    return True