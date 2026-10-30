from .config import celery_app
from time import sleep
from AgentLayer import fb_agent
import asyncio
from DatabaseLayer import Repo,PayloadErrorLogs

@celery_app.task(
    bind=True,
    autoretry_for=(TimeoutError,ConnectionError),
    retry_backoff=True,
    max_retries=3
)
def process_feedback_analysis_task(self, data, hash):
    try:
        repo: Repo = Repo()
        res = asyncio.run(fb_agent(data["raw_text"]))
        record_data = {
            "payload_hash": hash,
            "source_id": data["source_id"],
            "channel": data["channel"],
            "raw_text": data["raw_text"],
            "sanitized_text": res["sanitized_text"],
            "category": res["category"],
            "sentiment": res["sentiment"],
            "urgency": res["urgency"],
            "extracted_keywords": res["extracted_keywords"],
        }
        repo.save_feedback_record(record_data)
        return record_data
    except Exception as exc:
        print(f"Error processing feedback analysis task: {exc}")
        repo.add_error_log_info(PayloadErrorLogs(
            payload_hash=hash,
            source_id=data["source_id"],
            channel=data["channel"],
            raw_text=data["raw_text"],
            error_info=str(exc)
        ))
        raise