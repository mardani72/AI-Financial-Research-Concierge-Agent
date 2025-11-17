"""News and sentiment analysis agent."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.genai import types
from config.settings import (
    DEFAULT_MODEL,
    MAX_RETRY_ATTEMPTS,
    RETRY_EXP_BASE,
    RETRY_INITIAL_DELAY,
    RETRY_HTTP_STATUS_CODES,
)


def create_news_agent() -> LlmAgent:
    """Create the news and sentiment analysis agent.

    Returns:
        Configured LlmAgent for news analysis
    """
    retry_config = types.HttpRetryOptions(
        attempts=MAX_RETRY_ATTEMPTS,
        exp_base=RETRY_EXP_BASE,
        initial_delay=RETRY_INITIAL_DELAY,
        http_status_codes=RETRY_HTTP_STATUS_CODES,
    )

    agent = LlmAgent(
        name="NewsAgent",
        model=Gemini(model=DEFAULT_MODEL, retry_options=retry_config),
        instruction="""You are a specialized financial news and sentiment analysis agent.

Your responsibilities:
1. Use the google_search tool to find recent financial news articles about the given ticker(s)
2. Analyze the sentiment and tone of the retrieved news
3. Extract key themes: regulation, earnings, risks, partnerships, product launches, etc.
4. Provide a structured summary with:
   - Overall sentiment (positive/neutral/negative)
   - Key themes identified
   - Most important news items
   - Sentiment score (0.0 to 1.0 where higher is more positive)

If tools are unavailable or return limited results, fall back to your general financial knowledge while clearly stating any limitations.
""",
        tools=[
            google_search,
        ],
        output_key="news_analysis",
    )

    return agent

