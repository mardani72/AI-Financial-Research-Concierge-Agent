"""Chart generation tools for financial data visualization."""

from typing import Dict, Any, Optional
import yfinance as yf
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os
from datetime import datetime


def generate_price_chart(
    ticker: str,
    period: str = "1mo",
    interval: str = "1d",
    chart_type: str = "line",
    output_dir: str = "charts",
) -> Dict[str, Any]:
    """Generates a price chart for a given ticker.

    Args:
        ticker: Stock ticker symbol
        period: Time period for the chart
        interval: Data interval
        chart_type: Type of chart ("line" or "candlestick")
        output_dir: Directory to save the chart

    Returns:
        Dictionary with status and chart file path.
        Success: {"status": "success", "chart_path": "...", "data": {...}}
        Error: {"status": "error", "error_message": "..."}
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Fetch data
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)

        if hist.empty:
            return {
                "status": "error",
                "error_message": f"No data found for ticker {ticker}",
            }

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))

        if chart_type.lower() == "candlestick":
            # Simple candlestick-like visualization using actual dates on x-axis
            for ts, row in hist.iterrows():
                color = "green" if row["Close"] >= row["Open"] else "red"
                ax.plot(
                    [ts, ts],
                    [row["Low"], row["High"]],
                    color=color,
                    linewidth=1,
                )
                ax.plot(
                    [ts, ts],
                    [row["Open"], row["Close"]],
                    color=color,
                    linewidth=3,
                )
        else:
            # Line chart
            ax.plot(hist.index, hist["Close"], label="Close Price", linewidth=2)
            ax.fill_between(hist.index, hist["Low"], hist["High"], alpha=0.3, label="Range")

        # Add moving averages if enough data
        if len(hist) >= 20:
            hist["SMA_20"] = hist["Close"].rolling(window=20).mean()
            ax.plot(hist.index, hist["SMA_20"], label="SMA 20", linestyle="--", alpha=0.7)

        # Formatting
        ax.set_title(f"{ticker} Price Chart ({period})", fontsize=14, fontweight="bold")
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price ($)", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save chart
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{ticker}_{period}_{timestamp}.png"
        chart_path = os.path.join(output_dir, filename)
        plt.savefig(chart_path, dpi=150, bbox_inches="tight")
        plt.close()

        data = {
            "ticker": ticker,
            "period": period,
            "chart_type": chart_type,
            "data_points": len(hist),
            "price_range": {
                "high": float(hist["High"].max()),
                "low": float(hist["Low"].min()),
                "current": float(hist["Close"].iloc[-1]),
            },
        }

        return {
            "status": "success",
            "chart_path": chart_path,
            "data": data,
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error generating chart for {ticker}: {str(e)}",
        }

