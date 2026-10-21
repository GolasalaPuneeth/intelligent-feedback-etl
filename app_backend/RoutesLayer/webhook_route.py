from fastapi import APIRouter
from ValidationLayer import FeedbackHookValidation

FeedBackRoute = APIRouter(tags=["Feedback Webhooks"], prefix="/v1")

@FeedBackRoute.post("/feedback")
def test(feedbackdata:FeedbackHookValidation):
    return feedbackdata