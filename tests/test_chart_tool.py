"""Unit tests for chart generation tools."""

import unittest
import os
from tools.chart_tool import generate_price_chart


class TestChartTool(unittest.TestCase):
    """Test cases for chart tools."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_output_dir = "test_charts"
        os.makedirs(self.test_output_dir, exist_ok=True)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)

    def test_generate_price_chart_success(self):
        """Test successful chart generation."""
        result = generate_price_chart("AAPL", period="5d", output_dir=self.test_output_dir)
        self.assertEqual(result["status"], "success")
        self.assertIn("chart_path", result)
        self.assertTrue(os.path.exists(result["chart_path"]))

    def test_generate_price_chart_invalid_ticker(self):
        """Test chart generation with invalid ticker."""
        result = generate_price_chart("INVALID_TICKER_XYZ123", output_dir=self.test_output_dir)
        self.assertEqual(result["status"], "error")
        self.assertIn("error_message", result)


if __name__ == "__main__":
    unittest.main()

