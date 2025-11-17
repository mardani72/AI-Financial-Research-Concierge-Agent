"""Sentiment analysis tool for financial news."""

from typing import Dict, Any, List, Optional
from google.adk.models.google_llm import Gemini
from google.genai import types
import json


def analyze_news_sentiment(
    news_articles: List[Dict[str, Any]], api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Analyzes sentiment of financial news articles using LLM.

    Args:
        news_articles: List of news article dictionaries with 'title' and 'snippet' keys
        api_key: Optional API key (if not set, uses environment variable)

    Returns:
        Dictionary with status and sentiment analysis.
        Success: {"status": "success", "data": {...}}
        Error: {"status": "error", "error_message": "..."}
    """
    try:
        if not news_articles:
            return {
                "status": "error",
                "error_message": "No news articles provided",
            }

        # Prepare news text for analysis
        news_text = ""
        for i, article in enumerate(news_articles[:10], 1):  # Limit to 10 articles
            title = article.get("title", "")
            snippet = article.get("snippet", "")
            news_text += f"Article {i}:\nTitle: {title}\nSnippet: {snippet}\n\n"

        # Use Gemini to analyze sentiment
        model = Gemini(model="gemini-2.5-flash-lite")
        
        prompt = f"""Analyze the sentiment of the following financial news articles about stocks.
        
For each article, determine:
1. Overall sentiment: "positive", "neutral", or "negative"
2. Key themes: regulation, earnings, risks, partnerships, product launches, etc.
3. Confidence level: 1-10

Articles:
{news_text}

Provide your analysis in JSON format with this structure:
{{
    "overall_sentiment": "positive|neutral|negative",
    "sentiment_score": 0.0-1.0,
    "articles": [
        {{
            "article_number": 1,
            "sentiment": "positive|neutral|negative",
            "confidence": 1-10,
            "themes": ["theme1", "theme2"]
        }}
    ],
    "key_themes": ["theme1", "theme2", ...],
    "summary": "Brief summary of overall sentiment and key points"
}}
"""

        response = model.generate_content(prompt)
        
        # Extract text from response
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        # Try to parse JSON from response
        try:
            # Extract JSON if wrapped in markdown code blocks
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            
            sentiment_data = json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback: create structured response from text
            sentiment_data = {
                "overall_sentiment": "neutral",
                "sentiment_score": 0.5,
                "summary": response_text[:500],
                "articles": [],
                "key_themes": [],
            }

        data = {
            "total_articles": len(news_articles),
            "analyzed_articles": min(len(news_articles), 10),
            "sentiment_analysis": sentiment_data,
        }

        return {"status": "success", "data": data}

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error analyzing sentiment: {str(e)}",
        }

