"""Market data and chart generation agent."""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool
from tools.market_data_tool import (
    fetch_price_history,
    compute_volatility,
    compute_returns,
)
from tools.chart_tool import generate_price_chart
from google.genai import types
from config.settings import (
    DEFAULT_MODEL,
    MAX_RETRY_ATTEMPTS,
    RETRY_EXP_BASE,
    RETRY_INITIAL_DELAY,
    RETRY_HTTP_STATUS_CODES,
    CHART_OUTPUT_DIR,
)


def create_market_agent() -> LlmAgent:
    """Create the market data agent.

    Returns:
        Configured LlmAgent for market data analysis
    """
    retry_config = types.HttpRetryOptions(
        attempts=MAX_RETRY_ATTEMPTS,
        exp_base=RETRY_EXP_BASE,
        initial_delay=RETRY_INITIAL_DELAY,
        http_status_codes=RETRY_HTTP_STATUS_CODES,
    )

    agent = LlmAgent(
        name="MarketAgent",
        model=Gemini(model=DEFAULT_MODEL, retry_options=retry_config),
        instruction="""You are a specialized market data analysis agent.

Your responsibilities:
1. Use fetch_price_history to get historical price data for the ticker
2. Use compute_volatility to calculate volatility metrics
3. Use compute_returns to calculate return metrics
4. Use generate_price_chart to create visualizations
5. Provide a comprehensive market analysis including:
   - Current price and recent trends
   - Volatility assessment
   - Return performance
   - Technical indicators (SMA, EMA)
   - Chart location for visualization

Always check the status field in tool responses for errors. If errors occur, report them clearly.
Default period is "1mo" unless user specifies otherwise.
""",
        tools=[
            FunctionTool(fetch_price_history),
            FunctionTool(compute_volatility),
            FunctionTool(compute_returns),
            FunctionTool(generate_price_chart),
        ],
        output_key="market_analysis",
    )

    return agent

