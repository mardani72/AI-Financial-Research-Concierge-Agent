"""Financial ratio calculation tools."""

from typing import Dict, Any
import yfinance as yf


def calculate_valuation_metrics(ticker: str) -> Dict[str, Any]:
    """Calculates key financial valuation metrics for a ticker.

    Computes P/E, Forward P/E, EV/EBITDA, ROE, ROA, Revenue Growth, and Free Cash Flow.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Dictionary with status and valuation metrics.
        Success: {"status": "success", "data": {...}}
        Error: {"status": "error", "error_message": "..."}
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info:
            return {
                "status": "error",
                "error_message": f"No data found for ticker {ticker}",
            }

        # Extract key metrics
        metrics = {}

        # Valuation ratios
        metrics["pe_ratio"] = info.get("trailingPE")
        metrics["forward_pe"] = info.get("forwardPE")
        metrics["peg_ratio"] = info.get("pegRatio")
        metrics["ev_to_ebitda"] = info.get("enterpriseToEbitda")
        metrics["price_to_book"] = info.get("priceToBook")
        metrics["price_to_sales"] = info.get("priceToSalesTrailing12Months")

        # Profitability ratios
        metrics["roe"] = info.get("returnOnEquity")
        metrics["roa"] = info.get("returnOnAssets")
        metrics["profit_margin"] = info.get("profitMargins")
        metrics["operating_margin"] = info.get("operatingMargins")

        # Growth metrics
        metrics["revenue_growth"] = info.get("revenueGrowth")
        metrics["earnings_growth"] = info.get("earningsGrowth")
        metrics["earnings_quarterly_growth"] = info.get("earningsQuarterlyGrowth")

        # Cash flow
        metrics["free_cash_flow"] = info.get("freeCashflow")
        metrics["operating_cash_flow"] = info.get("operatingCashflow")

        # Debt metrics
        metrics["debt_to_equity"] = info.get("debtToEquity")
        metrics["current_ratio"] = info.get("currentRatio")
        metrics["quick_ratio"] = info.get("quickRatio")

        # Market cap and enterprise value
        metrics["market_cap"] = info.get("marketCap")
        metrics["enterprise_value"] = info.get("enterpriseValue")

        # Clean up None values and convert to float where possible
        cleaned_metrics = {}
        for key, value in metrics.items():
            if value is not None:
                try:
                    cleaned_metrics[key] = float(value)
                except (ValueError, TypeError):
                    cleaned_metrics[key] = value
            else:
                cleaned_metrics[key] = None

        data = {
            "ticker": ticker,
            "company_name": info.get("longName", ticker),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "metrics": cleaned_metrics,
        }

        return {"status": "success", "data": data}

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error calculating valuation metrics for {ticker}: {str(e)}",
        }

