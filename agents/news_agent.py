"""News and sentiment analysis agent."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search, FunctionTool
from tools.sentiment_tool import analyze_news_sentiment
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
2. Use the analyze_news_sentiment tool to analyze the sentiment of the news articles
3. Extract key themes: regulation, earnings, risks, partnerships, product launches, etc.
4. Provide a structured summary with:
   - Overall sentiment (positive/neutral/negative)
   - Key themes identified
   - Most important news items
   - Sentiment score

Always check the status field in tool responses for errors. If errors occur, report them clearly.
""",
        tools=[
            google_search,
            FunctionTool(analyze_news_sentiment),
        ],
        output_key="news_analysis",
    )

    return agent

