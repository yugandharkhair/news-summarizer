import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# News API configuration
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "397de62e9d9847c2b51f6243e60f3950")
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
DEFAULT_COUNTRY = "us"
DEFAULT_CATEGORY = "technology"
ARTICLE_LIMIT = 10

# Model configuration
SUMMARIZATION_MODEL = "t5-small"  # Alternatives: "facebook/bart-large-cnn", "sshleifer/distilbart-cnn-12-6"
MAX_INPUT_LENGTH = 1024
MAX_SUMMARY_LENGTH = 150
MIN_SUMMARY_LENGTH = 30