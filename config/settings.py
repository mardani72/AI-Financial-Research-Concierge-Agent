"""Configuration settings for the financial research agent."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Database configuration
DB_URL = os.getenv("DB_URL", "sqlite:///financial_agent_data.db")

# Application configuration
APP_NAME = "financial_research_agent"
DEFAULT_USER_ID = "default_user"

# Model configuration
DEFAULT_MODEL = "gemini-2.5-flash-lite"

# Retry configuration
MAX_RETRY_ATTEMPTS = 5
RETRY_EXP_BASE = 7
RETRY_INITIAL_DELAY = 1
RETRY_HTTP_STATUS_CODES = [429, 500, 503, 504]

# Chart configuration
CHART_OUTPUT_DIR = "charts"
CHART_FORMAT = "png"

# Memory configuration
MEMORY_COMPACTION_INTERVAL = 5
MEMORY_OVERLAP_SIZE = 2

