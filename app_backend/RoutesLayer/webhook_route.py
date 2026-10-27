from fastapi import APIRouter
from ValidationLayer import FeedbackHookValidation
from ServiceLayer import FeedBackProcessor
from CeleryLayer import test_task
from DatabaseLayer import Irepo,Repo
FeedBackRoute = APIRouter(tags=["Feedback Webhooks"], prefix="/v1")
feedback_service = FeedBackProcessor()
test_repo : Irepo = Repo()

@FeedBackRoute.post("/feedback")
async def test(feedbackdata:FeedbackHookValidation):
    res = test_task.delay(feedbackdata.model_dump())
    return res.id

@FeedBackRoute.post("/test")
async def test_cel(feedbackdata:FeedbackHookValidation):
    await feedback_service.ProcessFeedBack(feedbackdata)