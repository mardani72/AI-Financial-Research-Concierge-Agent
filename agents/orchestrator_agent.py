"""Orchestrator agent that coordinates all sub-agents."""

from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from agents.news_agent import create_news_agent
from agents.market_agent import create_market_agent
from agents.valuation_agent import create_valuation_agent
from agents.comparison_agent import create_comparison_agent
from agents.report_agent import create_report_agent
from google.genai import types
from config.settings import (
    DEFAULT_MODEL,
    MAX_RETRY_ATTEMPTS,
    RETRY_EXP_BASE,
    RETRY_INITIAL_DELAY,
    RETRY_HTTP_STATUS_CODES,
)


def create_orchestrator_agent() -> SequentialAgent:
    """Create the orchestrator agent that coordinates all sub-agents.

    Returns:
        Configured SequentialAgent that orchestrates the research workflow.
    """
    retry_config = types.HttpRetryOptions(
        attempts=MAX_RETRY_ATTEMPTS,
        exp_base=RETRY_EXP_BASE,
        initial_delay=RETRY_INITIAL_DELAY,
        http_status_codes=RETRY_HTTP_STATUS_CODES,
    )

    # Create query understanding agent
    query_agent = LlmAgent(
        name="QueryAgent",
        model=Gemini(model=DEFAULT_MODEL, retry_options=retry_config),
        instruction="""You are a query understanding agent for a financial research system.

Your role:
1. Understand the user's query (e.g., "Compare Tesla and Ford" or "Research NVDA")
2. Extract ticker symbols from the query
3. Determine if this is a single-ticker or multi-ticker request
4. Pass the ticker information clearly to the next agents in the pipeline

Output format: Provide a clear summary with:
- Extracted ticker symbols
- Whether this is a single or multi-ticker request
- Any specific requirements mentioned (e.g., "show trends", "valuation", etc.)
""",
        output_key="query_analysis",
    )

    # Create specialized agents
    news_agent = create_news_agent()
    market_agent = create_market_agent()
    valuation_agent = create_valuation_agent()
    comparison_agent = create_comparison_agent()
    report_agent = create_report_agent()

    # Create parallel research team (News, Market, Valuation run simultaneously)
    parallel_research_team = ParallelAgent(
        name="ParallelResearchTeam",
        sub_agents=[news_agent, market_agent, valuation_agent],
    )

    # Create sequential pipeline: Query -> Parallel Research -> Comparison -> Report
    # Comparison agent will process results when multiple tickers are detected
    orchestrator_agent = SequentialAgent(
        name="OrchestratorAgent",
        sub_agents=[
            query_agent,
            parallel_research_team,
            comparison_agent,
            report_agent,
        ],
    )

    return orchestrator_agent
