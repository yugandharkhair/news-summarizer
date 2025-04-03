from flask import Flask, render_template, request, jsonify
from news_fetcher import NewsFetcher
from summarizer import TextSummarizer
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize news fetcher and summarizer
news_fetcher = NewsFetcher()

# Initialize the summarizer lazily to speed up app startup
summarizer = None

def get_summarizer():
    """Lazy initialization of the summarizer"""
    global summarizer
    if summarizer is None:
        logger.info("Initializing summarizer...")
        summarizer = TextSummarizer()
    return summarizer

@app.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@app.route('/get_news')
def get_news():
    """Fetch news articles based on category and country"""
    category = request.args.get('category', 'technology')
    country = request.args.get('country', 'us')
    query = request.args.get('query', '')
    
    articles = news_fetcher.get_articles(country=country, category=category, query=query)
    
    return jsonify({
        'success': True,
        'articles': articles
    })

@app.route('/summarize', methods=['POST'])
def summarize_article():
    """Summarize an article from its URL"""
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({
            'success': False,
            'error': 'No URL provided'
        })
    
    # Get article details
    article = news_fetcher.get_article_details(url)
    
    if not article or not article.get('text'):
        return jsonify({
            'success': False,
            'error': 'Could not extract article content'
        })
    
    # Get summarizer
    summarizer = get_summarizer()
    
    # Generate summary
    start_time = time.time()
    summary = summarizer.summarize(article['text'])
    processing_time = time.time() - start_time
    
    return jsonify({
        'success': True,
        'title': article['title'],
        'original_text': article['text'][:500] + '...' if len(article['text']) > 500 else article['text'],
        'summary': summary,
        'url': url,
        'image': article.get('image', ''),
        'processing_time': f"{processing_time:.2f} seconds"
    })

@app.route('/summarize_text', methods=['POST'])
def summarize_text():
    """Summarize arbitrary text input"""
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({
            'success': False,
            'error': 'No text provided'
        })
    
    # Get summarizer
    summarizer = get_summarizer()
    
    # Generate summary
    start_time = time.time()
    summary = summarizer.summarize(text)
    processing_time = time.time() - start_time
    
    return jsonify({
        'success': True,
        'original_text': text[:500] + '...' if len(text) > 500 else text,
        'summary': summary,
        'processing_time': f"{processing_time:.2f} seconds"
    })

if __name__ == '__main__':
    app.run(debug=True)