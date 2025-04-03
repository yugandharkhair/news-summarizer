import requests
from config import NEWS_API_KEY, NEWS_API_URL, DEFAULT_COUNTRY, DEFAULT_CATEGORY, ARTICLE_LIMIT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsFetcher:
    """Class to fetch news articles from News API"""
    
    def __init__(self, api_key=NEWS_API_KEY):
        self.api_key = api_key
        self.base_url = NEWS_API_URL
        
    def get_articles(self, country=DEFAULT_COUNTRY, category=DEFAULT_CATEGORY, query=None, page_size=ARTICLE_LIMIT):
        """
        Fetch articles from News API
        
        Args:
            country (str): 2-letter ISO 3166-1 country code
            category (str): News category (business, entertainment, health, science, sports, technology)
            query (str, optional): Keywords to search for
            page_size (int): Number of articles to return
            
        Returns:
            list: List of article dictionaries
        """
        params = {
            'apiKey': self.api_key,
            'country': country,
            'pageSize': page_size
        }
        
        if category:
            params['category'] = category
            
        if query:
            params['q'] = query
            
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get('articles', [])
            
            # Clean up articles - remove those without content
            valid_articles = [article for article in articles if article.get('content')]
            
            logger.info(f"Fetched {len(valid_articles)} valid articles")
            return valid_articles
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching articles: {e}")
            return []
            
    def get_article_details(self, url):
        """
        Get full article content using newspaper3k library
        This is useful because News API often truncates content
        
        Args:
            url (str): URL of the article
            
        Returns:
            dict: Article details including full text
        """
        try:
            from newspaper import Article
            
            article = Article(url)
            article.download()
            article.parse()
            
            return {
                'title': article.title,
                'text': article.text,
                'url': url,
                'image': article.top_image
            }
            
        except Exception as e:
            logger.error(f"Error extracting article details: {e}")
            return None