from fastapi import APIRouter
from ValidationLayer import FeedbackHookValidation,FeedbackHookValidation_200,FeedbackHookValidation_409
from ServiceLayer import FeedBackProcessor
from typing import Union

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
    response_model=FeedbackHookValidation_200 | FeedbackHookValidation_409,
    responses={
        200: {
            "description": "Successful operation / Feedback processed",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Valid feedback response",
                            "value": {
                                "hash": "abc123hashvalue",
                                "id": "task-uuid-or-id",
                                "message": "'ID' is valied only for 30mins for monitoring"
                            }
                        }
                    }
                }
            }
        },
        409: {
            "description": "Conflict / Track found using hash",
            "content": {
                "application/json": {
                    "examples": {
                        "duplicate": {
                            "summary": "Found track using hash",
                            "value": {
                                "hash": "abc123hashvalue",
                                "message": "Found track using 'hash'"
                            }
                        }
                    }
                }
            }
        }
    },
)
async def test(feedbackdata: FeedbackHookValidation) -> FeedbackHookValidation_200 | FeedbackHookValidation_409:
    return await feedback_service.ProcessFeedBack(feedbackdata)

# @FeedBackRoute.post("/test")
# async def test_cel(feedbackdata:FeedbackHookValidation):
#     await feedback_service.ProcessFeedBack(feedbackdata)