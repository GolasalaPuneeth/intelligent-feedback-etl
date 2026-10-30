from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, JSON
from datetime import datetime, timezone
from typing import Optional


class FeedbackRecord(SQLModel, table=True):
  __tablename__ = "feedback_records"

  # Primary Key & Idempotency Hash (Prevents duplicate webhook processing)
  payload_hash: str = Field(primary_key=True, index=True, max_length=64)

  # Ingestion Metadata
  source_id: str = Field(index=True, nullable=False)
  channel: str = Field(index=True, nullable=False)
  raw_text: str = Field(nullable=False)

  # AI Extracted & Redacted Output Fields
  sanitized_text: str = Field(nullable=False)
  category: str = Field(index=True, nullable=False)
  sentiment: str = Field(index=True, nullable=False)
  urgency: str = Field(index=True, nullable=False)

  # Stored as a native PostgreSQL JSON array for clean list querying
  extracted_keywords: list[str] = Field(
      default_factory=list, sa_column=Column(JSON, nullable=False)
  )

  # Audit Timestamp
  created_at: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )

class PayloadErrorLogs(SQLModel, table=True):
    __tablename__ = "payload_error_logs"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    payload_hash: str
    source_id: str
    channel: str
    raw_text: str
    error_info:str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
        )