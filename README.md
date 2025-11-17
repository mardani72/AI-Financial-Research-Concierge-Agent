# AI Financial Research Concierge Agent

**Enterprise Track — Kaggle 5-Day AI Agents Intensive Capstone**

## Project Summary

The **AI Financial Research Concierge Agent** is a multi-agent system that automates equity research for retail investors, analysts, and financial enthusiasts. It collects real-time market data, summarizes news, computes financial ratios, analyzes volatility and trends, and generates a concise, research-style report while maintaining memory of the user's tracked tickers and historical context.

This project demonstrates key agent engineering concepts:
- Multi-agent orchestration (Orchestrator → Sub-agents)
- Tooling (YFinance API, Google Search, Custom Python tools)
- Sessions & Memory (long-term user preferences)
- Context engineering & observability
- Optional deployment (local endpoint or Cloud Run)

## Problem Statement

Financial research is time-consuming, fragmented across sources, and manually intensive. A user needs:
- Market data
- Valuation ratios
- News sentiment
- Competitor comparisons
- Volatility trends
- Long-term context

This agent automates all of those steps and produces a **single unified research brief** customized to the user.

## Solution Overview

A **multi-agent financial research assistant** that performs the following:

1. **Understands the user query** (e.g., "Compare Tesla and Ford")
2. **Delegates tasks** to specialized sub-agents
3. **Collects real-time data** using custom tools (YFinance, Python functions)
4. **Performs news & sentiment analysis** using Google Search + LLM
5. **Calculates valuation & risk metrics**
6. **Stores user preferences** (watched sectors, risk profile, past requests)
7. **Generates a polished research brief** with charts & tables
8. **Supports session continuity** with memory

## System Architecture

```
User Query
    ↓
Orchestrator Agent
    ↓ (delegates subtasks)
-------------------------------------------------------
|| News Agent        | Market Data Agent | Valuation Agent ||
-------------------------------------------------------
    ↓
Comparison Agent (if multiple tickers)
    ↓
Memory Service (store context)
    ↓
Final Report Agent
    ↓
Research Brief (Markdown + Charts)
```

### Agent Components

1. **Orchestrator Agent**: Main coordinator that interprets user requests and delegates to sub-agents
2. **News & Sentiment Agent**: Gathers financial news using Google Search and analyzes sentiment
3. **Market Data Agent**: Fetches price history, computes volatility and returns, generates charts
4. **Valuation Agent**: Calculates financial ratios (P/E, EV/EBITDA, ROE, ROA, etc.)
5. **Comparison Agent**: Handles multi-ticker requests and creates comparison tables
6. **Report Agent**: Synthesizes all analysis into a comprehensive research report

### Tools

**Built-in Tools:**
- `google_search`: For gathering financial news
- `BuiltInCodeExecutor`: For calculations and data processing

**Custom Tools:**
- `market_data_tool`: Fetches prices, computes volatility & returns
- `ratio_tool`: Computes valuation metrics
- `chart_tool`: Generates candlestick & line charts
- `sentiment_tool`: Extracts structured news from search results

## Installation & Setup

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/api-keys))

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd my_capstone_project
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```
GOOGLE_API_KEY=your_api_key_here
DB_URL=sqlite:///financial_agent_data.db
```

### Step 4: Verify Installation

```bash
python -m pytest tests/ -v
```

## Usage

### Interactive Mode

Run the agent in interactive mode:

```bash
python main.py
```

Then enter your queries:

```
Query > Compare Tesla and Ford. Show trends, news, sentiment, and valuation.
Query > Give me a research brief on NVDA for the last 7 days.
Query > Track AAPL and send an update every morning.
```

### Single Query Mode

Run a single query:

```bash
python main.py "Research AAPL stock"
```

### With Session Management

```bash
python main.py "Research TSLA" --session-id my_session_001
python main.py "What did I ask about earlier?" --session-id my_session_001
```

## Example Queries

- "Compare Tesla and Ford. Show trends, news, sentiment, and valuation."
- "Give me a research brief on NVDA for the last 7 days."
- "Track AAPL and send an update every morning."
- "Explain why oil & gas stocks fell this week."
- "What are the key financial metrics for Microsoft?"

## Project Structure

```
financial-agent/
├── agents/
│   ├── __init__.py
│   ├── orchestrator_agent.py      # Root coordinator
│   ├── news_agent.py              # News & sentiment analysis
│   ├── market_agent.py            # Market data & charts
│   ├── valuation_agent.py         # Financial ratios
│   ├── comparison_agent.py       # Multi-ticker comparison
│   └── report_agent.py           # Final report generation
├── tools/
│   ├── __init__.py
│   ├── market_data_tool.py       # yfinance integration
│   ├── ratio_tool.py             # Financial metrics
│   ├── chart_tool.py             # Visualization generation
│   └── sentiment_tool.py         # News sentiment analysis
├── memory/
│   ├── __init__.py
│   ├── session_store.py          # Session management
│   └── memory_bank.py            # Memory utilities
├── config/
│   ├── __init__.py
│   └── settings.py               # Configuration management
├── utils/
│   ├── __init__.py
│   ├── logging_config.py         # Logging setup
│   ├── tracing.py                # Tracing utilities
│   └── metrics.py                # Metrics collection
├── tests/
│   ├── __init__.py
│   ├── test_market_data_tool.py
│   ├── test_ratio_tool.py
│   ├── test_chart_tool.py
│   └── test_integration.py
├── charts/                       # Generated charts (created automatically)
├── main.py                       # Entry point
├── requirements.txt              # Dependencies
└── README.md                    # This file
```

## Technical Implementation

### Multi-Agent System

The system uses Google ADK (Agent Development Kit) with:
- **Orchestrator Pattern**: LLM-based coordinator using `AgentTool` to delegate
- **Parallel Execution**: News, Market Data, and Valuation agents run simultaneously
- **Sequential Pipeline**: Comparison → Memory Storage → Report generation

### Sessions & Memory

- **Sessions**: `DatabaseSessionService` (SQLite) for persistence across restarts
- **Memory**: `InMemoryMemoryService` (can be swapped to Vertex AI Memory Bank)
- **Automation**: `after_agent_callback` to auto-save sessions to memory
- **Retrieval**: `preload_memory` tool for proactive memory loading

### Error Handling

All tools follow a structured error pattern:
```python
{
    "status": "success" | "error",
    "data": {...} | None,
    "error_message": "..." | None
}
```

## Testing

Run all tests:

```bash
python -m pytest tests/ -v
```

Run specific test file:

```bash
python -m pytest tests/test_market_data_tool.py -v
```

## Logging & Observability

The system includes:
- **Logging**: Configurable logging to console and files
- **Tracing**: Operation tracing with duration tracking
- **Metrics**: Collection of timing and error metrics

Enable logging:

```python
from utils.logging_config import setup_logging
setup_logging(log_level="DEBUG", log_file="logs/agent.log")
```

## Memory Management

The agent automatically:
1. Saves conversation sessions to memory after each turn
2. Retrieves relevant past conversations using semantic search
3. Maintains user preferences (watched tickers, risk profile)

Memory is stored persistently and can be searched:

```python
from memory.memory_bank import search_memory
results = await search_memory(memory_service, app_name, user_id, "AAPL research")
```

## Deployment

### Local Deployment

The agent runs locally using SQLite for session storage. Charts are saved to the `charts/` directory.

### Cloud Deployment (Optional)

For production deployment:
1. Replace `InMemoryMemoryService` with `VertexAiMemoryBankService`
2. Use Cloud SQL or PostgreSQL for session storage
3. Deploy to Cloud Run or similar platform
4. Set up environment variables in cloud console

## Evaluation Criteria Met

### Category 1: Pitch ✅
- Clear problem statement
- Well-defined solution
- Value proposition articulated

### Category 2: Implementation ✅
- **Multi-agent workflow**: Orchestrator + 5 specialized agents
- **Custom tools**: 4 custom FunctionTools
- **Built-in tools**: google_search, BuiltInCodeExecutor
- **Memory + sessions**: DatabaseSessionService + InMemoryMemoryService
- **Chart generation**: Matplotlib-based chart generation
- **Logging & tracing**: Comprehensive observability
- **Structured returns**: Consistent error handling patterns

### Bonus Points ✅
- **Gemini**: All agents use Gemini models
- **Deployment**: Ready for Cloud Run deployment
- **Documentation**: Comprehensive README and code comments

## Future Extensions

- Multi-day scheduled reporting
- Portfolio optimization (simulation only)
- Macro indicator integration
- Visual dashboards
- Slack or email alerts
- Integration with Vertex AI Memory Bank for production

## Contributing

This is a capstone project for the Kaggle 5-Day AI Agents Intensive course. Contributions and improvements are welcome!

## License

This project is part of the Kaggle 5-Day AI Agents Intensive course and follows the course guidelines.

## Acknowledgments

- Google ADK (Agent Development Kit) team
- Kaggle for hosting the course
- YFinance for market data access

## Support

For issues or questions:
1. Check the [ADK Documentation](https://google.github.io/adk-docs/)
2. Review course materials in `project_resources/`
3. Ask questions on Kaggle Discord

---

**Note**: This agent provides research assistance only. It does not provide investment advice. Always do your own research and consult with financial advisors before making investment decisions.

