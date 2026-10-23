from .config import celery_app
# from sqlmodel import Session
from time import sleep
from AgentLayer import fb_agent
import asyncio

# Retry task failures with exponential backoff, up to five retries.
@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3
)
def test_task(self,data):
    res = asyncio.run(fb_agent(data['raw_text']))
    return res