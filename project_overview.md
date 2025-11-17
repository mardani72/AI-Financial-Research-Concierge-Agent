
# 📈 AI Financial Research Concierge Agent

### *Enterprise Track — Kaggle 5-Day AI Agents Intensive Capstone*

---

## 🧩 Project Summary

The **AI Financial Research Concierge Agent** is a multi-agent system that automates equity research for retail investors, analysts, and financial enthusiasts.
It collects real-time market data, summarizes news, computes financial ratios, analyzes volatility and trends, and generates a concise, research-style report while maintaining memory of the user’s tracked tickers and historical context.

This project demonstrates key agent engineering concepts:

* Multi-agent orchestration (Orchestrator → Sub-agents)
* Tooling (YFinance API, Google Search, Custom Python tools)
* Sessions & Memory (long-term user preferences)
* Context engineering & observability
* Optional deployment (local endpoint or Cloud Run)

---

# 🎯 Problem Statement

Financial research is time-consuming, fragmented across sources, and manually intensive. A user needs:

* market data
* valuation ratios
* news sentiment
* competitor comparisons
* volatility trends
* long-term context

This agent automates all of those steps and produces a **single unified research brief** customized to the user.

---

# 🚀 Solution Overview

A **multi-agent financial research assistant** that performs the following:

1. **Understands the user query** (e.g., “Compare Tesla and Ford”).
2. **Delegates tasks** to specialized sub-agents.
3. **Collects real-time data** using custom tools (YFinance, Python functions).
4. **Performs news & sentiment analysis** using Google Search + LLM.
5. **Calculates valuation & risk metrics.**
6. **Stores user preferences** (watched sectors, risk profile, past requests).
7. **Generates a polished research brief** with charts & tables.
8. **Supports session continuity** with memory.

---

# 🛠️ Core Components

## 1. **Orchestrator Agent**

* First agent invoked.
* Interprets user request.
* Determines subtasks.
* Delegates to News, Market Data, Valuation, and Report Agents.
* Tracks overall workflow state.

---

## 2. **News & Sentiment Agent**

* Uses **Google Search Tool** to gather recent financial news.
* Summaries and grades sentiment ("positive", "neutral", "negative").
* Extracts macro themes (regulation, earnings, risks).
* Returns structured JSON to orchestrator.

---

## 3. **Market Data Agent**

Custom Python tools:

* `fetch_price_history(ticker, period, interval)`
* `compute_volatility(ticker)`
* `compute_returns(ticker)`
* `generate_price_chart(ticker)`

Provides:

* Close, volume, SMA, EMA
* Volatility metrics
* Max drawdown
* Technical trend summary

---

## 4. **Valuation Agent**

Computes:

* P/E
* Forward P/E (if available)
* EV/EBITDA
* ROE, ROA
* Revenue growth (YoY)
* Free cash flow (if data provided)

Scores strength vs competitors.

---

## 5. **Comparison Agent**

Handles multi-ticker requests:

* Aligns sectors
* Benchmarks metrics
* Normalizes differences
* Produces competitor comparison table

---

## 6. **Memory Service**

Stores:

* User’s watched tickers
* Sectors of interest
* Long-term summaries
* Past reports for reference

Useful for “Follow up on the same companies from last week.”

---

## 7. **Final Report Agent**

Generates a research-style final document:

* Summary
* Market trends
* News sentiment
* Valuation table
* Price chart
* Volatility notes
* Recommendation-style narrative *(not investment advice)*

Output format: **Markdown** or **HTML**, ready for PDF export.

---

# 🧬 System Architecture

```
User Query
    ↓
Orchestrator Agent
    ↓ (delegates subtasks)
-------------------------------------------------------
| News Agent        | Market Data Agent | Valuation Agent |
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

---

# 🔧 Tools Used

### **Built-in Tools**

* Google Search
* Code Execution Tool (for Python charts / metrics)

### **Custom Tools**

| Tool Name            | Description                                   |
| -------------------- | --------------------------------------------- |
| `market_data_tool`   | Fetches prices, computes volatility & returns |
| `finance_ratio_tool` | Computes valuation metrics                    |
| `chart_tool`         | Generates candlestick & line charts           |
| `news_tool`          | Extracts structured news from search results  |
| `comparison_tool`    | Creates normalized ticker comparison tables   |

---

# 📦 Installation & Project Setup

Below is a recommended structure for Cursor:

```
financial-agent/
├── agents/
│   ├── orchestrator_agent.py
│   ├── news_agent.py
│   ├── market_agent.py
│   ├── valuation_agent.py
│   ├── comparison_agent.py
│   ├── report_agent.py
│
├── tools/
│   ├── market_data_tool.py
│   ├── ratio_tool.py
│   ├── chart_tool.py
│   ├── sentiment_tool.py
│
├── memory/
│   ├── session_store.py
│   ├── memory_bank.py
│
├── notebooks/
│   ├── data_experiments.ipynb
│
├── tests/
│
├── README.md
├── requirements.txt
└── main.py
```

---

# 🧪 Evaluation Strategy

To support Kaggle scoring requirements:

### **Category 1: Pitch**

* Clear problem, solution, value, and use-case communication.

### **Category 2: Implementation**

Includes:

* Multi-agent workflow
* Custom tools
* Memory + sessions
* Chart generation
* Logging & tracing
* Structured returns

### **Bonus**

* Uses Gemini for at least one agent
* Optional deployment
* 3-minute YouTube demo

---

# 📝 Example User Queries

* “Compare Tesla and Ford. Show trends, news, sentiment, and valuation.”
* “Give me a research brief on NVDA for the last 7 days.”
* “Track AAPL and send an update every morning.”
* “Explain why oil & gas stocks fell this week.”

---

# 🧠 Future Extensions

* Multi-day scheduled reporting
* Portfolio optimization (simulation only)
* Macro indicator integration
* Visual dashboards
* Slack or email alerts

---
