"""Unit tests for financial ratio tools."""

import unittest
from tools.ratio_tool import calculate_valuation_metrics


class TestRatioTool(unittest.TestCase):
    """Test cases for ratio tools."""

    def test_calculate_valuation_metrics_success(self):
        """Test successful valuation metrics calculation."""
        result = calculate_valuation_metrics("AAPL")
        self.assertEqual(result["status"], "success")
        self.assertIn("data", result)
        self.assertIn("ticker", result["data"])
        self.assertIn("metrics", result["data"])

    def test_calculate_valuation_metrics_invalid_ticker(self):
        """Test valuation metrics with invalid ticker."""
        result = calculate_valuation_metrics("INVALID_TICKER_XYZ123")
        self.assertEqual(result["status"], "error")
        self.assertIn("error_message", result)


if __name__ == "__main__":
    unittest.main()

