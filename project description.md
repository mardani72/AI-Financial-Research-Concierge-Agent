**Project Description**

- **What it is**: AI Financial Research Concierge Agent — a multi-agent system that automates equity research for retail investors, analysts, and finance enthusiasts.  
- **Core value**: Transforms fragmented, manual research (prices, news, ratios, comparisons) into a single, personalized research brief with memory of past tickers and preferences.

**What it does**
- Understands user intent (e.g., “Compare Tesla and Ford”) and decomposes it into news, market data, valuation, and comparison tasks.
- Gathers real-time prices, history, volatility, returns, and generates charts.
- Analyzes recent news and grades sentiment, surfacing macro themes and risks.
- Calculates valuation and quality metrics: P/E, forward P/E, EV/EBITDA, ROE/ROA, revenue growth, free cash flow when available.
- Normalizes and benchmarks metrics across multiple tickers for fair comparisons.
- Remembers watched tickers, sectors, and prior summaries to maintain session continuity.
- Produces a concise research-style brief (Markdown or HTML) ready for PDF export, with a recommendation-style narrative (not investment advice).

**How it works (multi-agent workflow)**
- **Orchestrator Agent**: Interprets the query, plans subtasks, delegates to specialists, tracks state.
- **News & Sentiment Agent**: Uses Google Search, summarizes recent items, labels sentiment, extracts themes.
- **Market Data Agent**: Python tools for price history, volatility, returns, SMA/EMA, max drawdown, and chart generation.
- **Valuation Agent**: Computes valuation/quality ratios and scores strength versus peers.
- **Comparison Agent**: Aligns sectors, benchmarks, and outputs normalized comparison tables for multi-ticker requests.
- **Memory Service**: Persists user preferences, watched tickers, and past reports for follow-ups.
- **Final Report Agent**: Assembles summary, trends, sentiment, valuation tables, charts, and volatility notes into the final brief.

**Key tools**
- Built-in: Google Search, code execution for Python-based metrics/charts.
- Custom: `market_data_tool` (prices, volatility, returns), `finance_ratio_tool` (valuation metrics), `chart_tool` (candlestick/line charts), `news_tool` (structured news + sentiment), `comparison_tool` (normalized tables).

**Output and deployment**
- Output: Markdown or HTML research brief with tables, charts, sentiment summary, and narrative.
- Deployment: Local endpoint or optional Cloud Run; observability via structured returns and logging.
- Scoring fit: Clear pitch; multi-agent implementation with custom tools, memory, charts, and structured outputs; bonus-ready for Gemini use and a 3-minute demo.

**Example user flows**
- “Give me a research brief on NVDA for the last 7 days.”
- “Compare Tesla and Ford—trends, news, sentiment, valuation.”
- “Track AAPL and send an update every morning.”
- “Explain why oil and gas stocks fell this week.”

**Future extensions**
- Scheduled multi-day reporting; portfolio simulation (non-trading); macro indicator integration.
- Richer dashboards; Slack/email alerts; expanded long-term memory for investor profiles.
