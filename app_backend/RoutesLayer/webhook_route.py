from fastapi import APIRouter
from ValidationLayer import FeedbackHookValidation
from ServiceLayer import FeedBackProcessor
from CeleryLayer import test_task
FeedBackRoute = APIRouter(tags=["Feedback Webhooks"], prefix="/v1")
feedback_service = FeedBackProcessor()

@FeedBackRoute.post("/feedback")
async def test(feedbackdata:FeedbackHookValidation):
    return await feedback_service.ProcessFeedBack(feedbackdata)

@FeedBackRoute.post("/test")
async def test_cel(feedbackdata:FeedbackHookValidation):
    await feedback_service.ProcessFeedBack(feedbackdata)