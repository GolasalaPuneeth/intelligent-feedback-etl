from pydantic_ai import Agent
from ValidationLayer import FeedbackAnalysis
from dotenv import load_dotenv
load_dotenv()


feedback_agent = Agent(
    model="google:gemini-3.1-flash-lite",
    output_type=FeedbackAnalysis,
    system_prompt=(
        "You are an expert AI data processing agent. Your tasks are:"
        "\n1. Strict PII Redaction: Mask all personal info (names, emails,"
        " phones) with [REDACTED]."
        "\n2. Categorization & Sentiment: Accurately categorize the text, pick"
        " the exact enum value for sentiment and urgency."
        "\n3. Keyword Extraction: Pull out key technical tags, error mentions,"
        " or feature components into the extracted_keywords list."
        "\n4. Adhere strictly to the defined output schema."
    ),
)

# Injection allows callers to substitute an agent with different settings.
async def fb_agent(raw_feedback,feedback_agent:Agent = feedback_agent):
    result:FeedbackAnalysis = await feedback_agent.run(raw_feedback)
    return result.output.model_dump()