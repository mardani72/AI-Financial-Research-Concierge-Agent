"""Market data tools for fetching stock prices, volatility, and returns."""

from typing import Dict, Any, Optional
import yfinance as yf
import pandas as pd
import numpy as np


def fetch_price_history(
    ticker: str, period: str = "1mo", interval: str = "1d"
) -> Dict[str, Any]:
    """Fetches historical price data for a given ticker.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "TSLA")
        period: Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        interval: Valid intervals: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

    Returns:
        Dictionary with status and price history data.
        Success: {"status": "success", "data": {...}}
        Error: {"status": "error", "error_message": "..."}
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)

        if hist.empty:
            return {
                "status": "error",
                "error_message": f"No data found for ticker {ticker}",
            }

        # Calculate moving averages
        hist["SMA_20"] = hist["Close"].rolling(window=20).mean()
        hist["EMA_12"] = hist["Close"].ewm(span=12, adjust=False).mean()

        # Prepare response data
        latest = hist.iloc[-1]
        data = {
            "ticker": ticker,
            "period": period,
            "interval": interval,
            "latest_price": float(latest["Close"]),
            "latest_volume": int(latest["Volume"]),
            "sma_20": float(latest["SMA_20"]) if not pd.isna(latest["SMA_20"]) else None,
            "ema_12": float(latest["EMA_12"]) if not pd.isna(latest["EMA_12"]) else None,
            "high": float(hist["High"].max()),
            "low": float(hist["Low"].min()),
            "data_points": len(hist),
            "price_history": hist[["Close", "Volume", "High", "Low", "Open"]].tail(10).to_dict("records"),
        }

        return {"status": "success", "data": data}

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching price history for {ticker}: {str(e)}",
        }


def compute_volatility(ticker: str, period: str = "1mo") -> Dict[str, Any]:
    """Computes volatility metrics for a given ticker.

    Args:
        ticker: Stock ticker symbol
        period: Time period for volatility calculation

    Returns:
        Dictionary with status and volatility metrics.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            return {
                "status": "error",
                "error_message": f"No data found for ticker {ticker}",
            }

        # Calculate daily returns
        hist["Returns"] = hist["Close"].pct_change()

        # Volatility metrics
        daily_volatility = hist["Returns"].std()
        annualized_volatility = daily_volatility * np.sqrt(252)  # Trading days per year

        # Max drawdown
        cumulative = (1 + hist["Returns"]).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()

        data = {
            "ticker": ticker,
            "period": period,
            "daily_volatility": float(daily_volatility),
            "annualized_volatility": float(annualized_volatility),
            "max_drawdown": float(max_drawdown),
            "volatility_percentage": float(annualized_volatility * 100),
        }

        return {"status": "success", "data": data}

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error computing volatility for {ticker}: {str(e)}",
        }


def compute_returns(ticker: str, period: str = "1mo") -> Dict[str, Any]:
    """Computes return metrics for a given ticker.

    Args:
        ticker: Stock ticker symbol
        period: Time period for return calculation

    Returns:
        Dictionary with status and return metrics.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            return {
                "status": "error",
                "error_message": f"No data found for ticker {ticker}",
            }

        # Calculate returns
        hist["Returns"] = hist["Close"].pct_change()
        total_return = (hist["Close"].iloc[-1] / hist["Close"].iloc[0]) - 1
        average_daily_return = hist["Returns"].mean()

        # Annualized return
        days = len(hist)
        annualized_return = ((1 + total_return) ** (252 / days)) - 1 if days > 0 else 0

        data = {
            "ticker": ticker,
            "period": period,
            "total_return": float(total_return),
            "total_return_percentage": float(total_return * 100),
            "average_daily_return": float(average_daily_return),
            "annualized_return": float(annualized_return),
            "annualized_return_percentage": float(annualized_return * 100),
        }

        return {"status": "success", "data": data}

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error computing returns for {ticker}: {str(e)}",
        }

