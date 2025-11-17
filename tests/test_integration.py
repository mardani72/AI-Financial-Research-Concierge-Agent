"""Integration tests for agent workflows."""

import unittest
import asyncio
import os
from google.genai import types
from agents.orchestrator_agent import create_orchestrator_agent
from agents.news_agent import create_news_agent
from agents.market_agent import create_market_agent
from agents.valuation_agent import create_valuation_agent


class TestAgentIntegration(unittest.TestCase):
    """Integration tests for agents."""

    @classmethod
    def setUpClass(cls):
        """Set up test class."""
        # Check for API key
        if not os.getenv("GOOGLE_API_KEY"):
            raise unittest.SkipTest("GOOGLE_API_KEY not set")

    def test_create_orchestrator_agent(self):
        """Test orchestrator agent creation."""
        agent = create_orchestrator_agent()
        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, "OrchestratorAgent")

    def test_create_news_agent(self):
        """Test news agent creation."""
        agent = create_news_agent()
        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, "NewsAgent")

    def test_create_market_agent(self):
        """Test market agent creation."""
        agent = create_market_agent()
        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, "MarketAgent")

    def test_create_valuation_agent(self):
        """Test valuation agent creation."""
        agent = create_valuation_agent()
        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, "ValuationAgent")


if __name__ == "__main__":
    unittest.main()

