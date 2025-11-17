"""Unit tests for market data tools."""

import unittest
from tools.market_data_tool import fetch_price_history, compute_volatility, compute_returns


class TestMarketDataTool(unittest.TestCase):
    """Test cases for market data tools."""

    def test_fetch_price_history_success(self):
        """Test successful price history fetch."""
        result = fetch_price_history("AAPL", period="5d")
        self.assertEqual(result["status"], "success")
        self.assertIn("data", result)
        self.assertIn("ticker", result["data"])
        self.assertEqual(result["data"]["ticker"], "AAPL")

    def test_fetch_price_history_invalid_ticker(self):
        """Test price history fetch with invalid ticker."""
        result = fetch_price_history("INVALID_TICKER_XYZ123")
        self.assertEqual(result["status"], "error")
        self.assertIn("error_message", result)

    def test_compute_volatility_success(self):
        """Test successful volatility computation."""
        result = compute_volatility("AAPL", period="1mo")
        self.assertEqual(result["status"], "success")
        self.assertIn("data", result)
        self.assertIn("volatility_percentage", result["data"])

    def test_compute_returns_success(self):
        """Test successful returns computation."""
        result = compute_returns("AAPL", period="1mo")
        self.assertEqual(result["status"], "success")
        self.assertIn("data", result)
        self.assertIn("total_return", result["data"])


if __name__ == "__main__":
    unittest.main()

