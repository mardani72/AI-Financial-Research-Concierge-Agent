"""Final report generation agent."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from config.settings import (
    DEFAULT_MODEL,
    MAX_RETRY_ATTEMPTS,
    RETRY_EXP_BASE,
    RETRY_INITIAL_DELAY,
    RETRY_HTTP_STATUS_CODES,
)


def create_report_agent() -> LlmAgent:
    """Create the final report generation agent.

    Returns:
        Configured LlmAgent for report generation
    """
    retry_config = types.HttpRetryOptions(
        attempts=MAX_RETRY_ATTEMPTS,
        exp_base=RETRY_EXP_BASE,
        initial_delay=RETRY_INITIAL_DELAY,
        http_status_codes=RETRY_HTTP_STATUS_CODES,
    )

    agent = LlmAgent(
        name="ReportAgent",
        model=Gemini(model=DEFAULT_MODEL, retry_options=retry_config),
        instruction="""You are a specialized financial research report generator.

Your responsibilities:
1. Synthesize all analysis results from News, Market, Valuation, and Comparison agents
2. Generate a comprehensive research-style report in Markdown format
3. Structure the report with:
   - Executive Summary
   - Market Trends & Price Analysis
   - News & Sentiment Analysis
   - Valuation Metrics Table
   - Key Financial Ratios
   - Risk Assessment (volatility, drawdown)
   - Comparison Analysis (if multiple tickers)
   - Conclusion & Key Takeaways
4. Include references to charts when available
5. Use professional financial research language
6. Add disclaimers: "This is not investment advice. Do your own research."

Output format: Well-formatted Markdown that can be exported to PDF or HTML.
""",
        output_key="final_report",
    )

    return agent

