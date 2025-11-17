"""Financial valuation and ratio analysis agent."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool
from tools.ratio_tool import calculate_valuation_metrics
from google.genai import types
from config.settings import (
    DEFAULT_MODEL,
    MAX_RETRY_ATTEMPTS,
    RETRY_EXP_BASE,
    RETRY_INITIAL_DELAY,
    RETRY_HTTP_STATUS_CODES,
)


def create_valuation_agent() -> LlmAgent:
    """Create the valuation analysis agent.

    Returns:
        Configured LlmAgent for valuation analysis
    """
    retry_config = types.HttpRetryOptions(
        attempts=MAX_RETRY_ATTEMPTS,
        exp_base=RETRY_EXP_BASE,
        initial_delay=RETRY_INITIAL_DELAY,
        http_status_codes=RETRY_HTTP_STATUS_CODES,
    )

    agent = LlmAgent(
        name="ValuationAgent",
        model=Gemini(model=DEFAULT_MODEL, retry_options=retry_config),
        instruction="""You are a specialized financial valuation analysis agent.

Your responsibilities:
1. Use calculate_valuation_metrics to get comprehensive financial ratios for the ticker
2. Analyze key valuation metrics:
   - P/E ratio and Forward P/E
   - EV/EBITDA
   - Price-to-Book and Price-to-Sales
   - Profitability ratios (ROE, ROA, margins)
   - Growth metrics (revenue growth, earnings growth)
   - Cash flow metrics
   - Debt ratios
3. Provide assessment of valuation:
   - Whether stock appears overvalued, undervalued, or fairly valued
   - Key strengths and weaknesses
   - Comparison context (if available)

Always check the status field in tool responses for errors. If errors occur, report them clearly.
""",
        tools=[
            FunctionTool(calculate_valuation_metrics),
        ],
        output_key="valuation_analysis",
    )

    return agent

