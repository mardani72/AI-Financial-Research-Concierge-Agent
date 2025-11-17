"""Orchestrator agent that coordinates all sub-agents."""

from google.adk.agents import Agent, ParallelAgent, SequentialAgent, AgentTool
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


def create_orchestrator_agent() -> Agent:
    """Create the orchestrator agent that coordinates all sub-agents.

    Returns:
        Configured Agent that orchestrates the research workflow
    """
    retry_config = types.HttpRetryOptions(
        attempts=MAX_RETRY_ATTEMPTS,
        exp_base=RETRY_EXP_BASE,
        initial_delay=RETRY_INITIAL_DELAY,
        http_status_codes=RETRY_HTTP_STATUS_CODES,
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

    # Create sequential pipeline: Parallel Research → Comparison → Report
    # Comparison agent only runs if multiple tickers are provided
    sequential_pipeline = SequentialAgent(
        name="ResearchPipeline",
        sub_agents=[parallel_research_team, comparison_agent, report_agent],
    )

    # Root orchestrator agent
    orchestrator = Agent(
        name="OrchestratorAgent",
        model=Gemini(model=DEFAULT_MODEL, retry_options=retry_config),
        instruction="""You are the orchestrator for a financial research system.

Your role:
1. Understand the user's query (e.g., "Compare Tesla and Ford" or "Research NVDA")
2. Extract ticker symbols from the query
3. Determine if this is a single-ticker or multi-ticker request
4. Delegate to the ResearchPipeline which will:
   - Run News, Market, and Valuation analysis in parallel
   - Compare tickers if multiple are provided
   - Generate a final research report
5. Present the final report to the user in a clear, professional format

Workflow:
- For single ticker: ResearchPipeline → Final Report
- For multiple tickers: ResearchPipeline (includes comparison) → Final Report

Always provide clear, actionable financial research insights.
""",
        tools=[AgentTool(sequential_pipeline)],
    )

    return orchestrator

