from pydantic import BaseModel, Field
from enum import Enum

class Sentiment(str, Enum):
  POSITIVE = "Positive"
  NEUTRAL = "Neutral"
  NEGATIVE = "Negative"

class Urgency(str, Enum):
  LOW = "Low"
  MEDIUM = "Medium"
  HIGH = "High"
  CRITICAL = "Critical" 

class FeedbackAnalysis(BaseModel):
  sanitized_text: str = Field(
      description=(
          "The raw text with all PII (names, emails, phone numbers) replaced"
          " with [REDACTED]."
      )
  )
  category: str = Field(
      description=(
          "Classified category, e.g., Billing, Bug, Account, or Feature Request"
      )
  )
  sentiment: Sentiment = Field(
      description="Overall sentiment: Positive, Neutral, or Negative"
  )
  urgency: Urgency = Field(
      description="Urgency level: Low, Medium, High, or Critical"
  )