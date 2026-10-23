from pydantic_ai import Agent
from ValidationLayer import FeedbackAnalysis
from dotenv import load_dotenv
load_dotenv()


feedback_agent = Agent(
    model="google:gemini-3.1-flash-lite",
    output_type=FeedbackAnalysis,
    system_prompt=(
        "You are an expert AI data processing agent. Your task is to:"
        "\n1. Strict PII Redaction: Mask all personal info (names, emails,"
        " phones) with [REDACTED]."
        "\n2. Categorization & Sentiment: Accurately categorize the text and"
        " gauge sentiment."
        "\n3. Adhere strictly to the defined output schema."
    ),
)

async def fb_agent(raw_feedback,feedback_agent:Agent = feedback_agent):
    result = await feedback_agent.run(raw_feedback)
    return result.output.model_dump_json()