from fastapi import APIRouter
from ValidationLayer import FeedbackHookValidation
from ServiceLayer import FeedBackProcessor

FeedBackRoute = APIRouter(tags=["Feedback Webhooks"], prefix="/v1")
feedback_service = FeedBackProcessor()

@FeedBackRoute.post("/feedback")
def test(feedbackdata:FeedbackHookValidation):
    return feedback_service.ProcessFeedBack(feedbackdata)