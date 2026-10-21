from fastapi import APIRouter
from ValidationLayer import FeedbackHookValidation
from Apputils import hasher

FeedBackRoute = APIRouter(tags=["Feedback Webhooks"], prefix="/v1")

@FeedBackRoute.post("/feedback")
def test(feedbackdata:FeedbackHookValidation):
    return hasher.get_hash(feedbackdata)