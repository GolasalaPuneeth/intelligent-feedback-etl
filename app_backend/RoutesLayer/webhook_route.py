from fastapi import APIRouter
from ValidationLayer import FeedbackHookValidation
from ServiceLayer import FeedBackProcessor
from CeleryLayer import test_task

FeedBackRoute = APIRouter(tags=["Feedback Webhooks"], prefix="/v1")
feedback_service = FeedBackProcessor()

@FeedBackRoute.post("/feedback")
async def test(feedbackdata:FeedbackHookValidation):
    res = test_task.delay(feedbackdata.model_dump())
    return res.id

@FeedBackRoute.get("/test")
async def test_cel():
    res = test_task.delay("sam")
    return "running.."