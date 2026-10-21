from pydantic import BaseModel

class FeedbackHookValidation(BaseModel):
    source_id:str
    channel:str
    raw_text:str