from pydantic import BaseModel, Field

class FeedbackHookValidation(BaseModel):
    source_id:str
    channel:str
    raw_text:str

class FeedbackHookValidation_200(BaseModel):
    hash : str
    id: str
    message: str = Field(default= "'ID' is valied only for 30mins for monitoring")

class FeedbackHookValidation_409(BaseModel):
    hash : str
    message: str = Field(default="Found track using 'hash'")