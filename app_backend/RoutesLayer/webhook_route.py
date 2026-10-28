from fastapi import APIRouter
from ValidationLayer import FeedbackHookValidation
from ServiceLayer import FeedBackProcessor
from CeleryLayer import test_task
FeedBackRoute = APIRouter(tags=["Feedback Webhooks"], prefix="/v1")
feedback_service = FeedBackProcessor()

@FeedBackRoute.post(
    "/feedback",
    summary="Submit customer feedback",
    description=(
        "Accepts customer feedback and queues it for asynchronous processing. "
        "The request must include a source ID, channel, and raw feedback text. "
        "Duplicate feedback is detected by its payload hash.\n\n"
        "A newly queued request returns its task ID as a string. If the feedback "
        "was already persisted, the response is `{\"FOUND\": true}`."
    ),
    response_description="The Celery task ID, or a duplicate-record indicator.",
    response_model=str | dict[str, bool],
    responses={
        200: {
            "content": {
                "application/json": {
                    "examples": {
                        "queued": {
                            "summary": "Feedback queued",
                            "value": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                        },
                        "duplicate": {
                            "summary": "Feedback already persisted",
                            "value": {"FOUND": True},
                        },
                    }
                }
            }
        }
    },
)
async def test(feedbackdata: FeedbackHookValidation) -> str | dict[str, bool]:
    return await feedback_service.ProcessFeedBack(feedbackdata)

# @FeedBackRoute.post("/test")
# async def test_cel(feedbackdata:FeedbackHookValidation):
#     await feedback_service.ProcessFeedBack(feedbackdata)