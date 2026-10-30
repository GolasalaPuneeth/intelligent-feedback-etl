from abc import ABC, abstractmethod
from typing import Any
from .models import PayloadErrorLogs

class Irepo(ABC):
  @abstractmethod
  def save_feedback_record(self, data: dict[str, Any]) -> None:
    """Persists a processed feedback record into the database.

    Args:
        data (dict[str, Any]): A dictionary containing the sanitized feedback,
          classification metrics, extracted keywords, and payload metadata.

    Raises:
        NotImplementedError: If the concrete implementation does not override
        this method.
    """
    raise NotImplementedError

  @abstractmethod
  def check_record_persist(self, hash: str) -> bool:
    """Checks whether a feedback record with the given payload hash already exists.

    Used for enforcing pipeline idempotency by verifying if an incoming payload
    has previously been processed and persisted, preventing duplicate execution
    and redundant AI API calls.

    Args:
        hash (str): The unique SHA-256 payload hash representing the feedback.

    Returns:
        bool: True if the record exists in the database, False otherwise.

    Raises:
        NotImplementedError: If the concrete repository implementation does not
          override this method.
    """
    raise NotImplementedError

  @abstractmethod
  def add_error_log_info(self,data: PayloadErrorLogs):
    """Persists error details for a feedback payload.

    Args:
        data (PayloadErrorLogs): The payload metadata and error information to
          record.

    Raises:
        NotImplementedError: If the concrete repository does not override this
          method.
    """
    raise NotImplementedError