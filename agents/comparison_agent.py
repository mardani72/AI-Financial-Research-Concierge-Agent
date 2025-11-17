"""Multi-ticker comparison agent."""

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


def create_comparison_agent() -> LlmAgent:
    """Create the comparison agent for multi-ticker analysis.

    Returns:
        Configured LlmAgent for comparison analysis
    """
    retry_config = types.HttpRetryOptions(
        attempts=MAX_RETRY_ATTEMPTS,
        exp_base=RETRY_EXP_BASE,
        initial_delay=RETRY_INITIAL_DELAY,
        http_status_codes=RETRY_HTTP_STATUS_CODES,
    )

    agent = LlmAgent(
        name="ComparisonAgent",
        model=Gemini(model=DEFAULT_MODEL, retry_options=retry_config),
        instruction="""You are a specialized comparison analysis agent for multiple tickers.

Your responsibilities:
1. Receive analysis results from News, Market, and Valuation agents for multiple tickers
2. Create normalized comparison tables for:
   - Valuation metrics (P/E, EV/EBITDA, etc.)
   - Market performance (returns, volatility)
   - News sentiment scores
   - Key financial ratios
3. Identify relative strengths and weaknesses
4. Provide sector/industry context when available
5. Highlight key differentiators between tickers

Input format: You will receive structured data with analysis for each ticker.
Output format: Provide a clear comparison table and narrative analysis.
""",
        output_key="comparison_analysis",
    )

    return agent

