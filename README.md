# ML-Powered News Summarizer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.2.3-green)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![NewsAPI](https://img.shields.io/badge/NewsAPI-API-orange)

A modern web application that uses machine learning to automatically summarize news articles from various categories. The application fetches the latest news from NewsAPI and provides concise, AI-generated summaries using Google's T5 transformer model.

## 🚀 Features

- **Real-time news fetching**: Retrieves the latest news articles from NewsAPI
- **Category filtering**: Filter news by categories like Technology, Business, Science, Health, etc.
- **Search functionality**: Find specific news articles using keywords
- **AI-powered summarization**: Automatically generates concise summaries of news articles
- **Direct text summarization**: Paste any text to get an AI-generated summary
- **Responsive design**: Works seamlessly on desktop and mobile devices
- **Pagination**: Load more articles as you scroll
- **Performance metrics**: Shows summarization processing time

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **News Source**: NewsAPI
- **NLP/Machine Learning**: 
  - HuggingFace Transformers
  - Google's T5 model for text summarization
- **Additional Libraries**:
  - newspaper3k for article extraction
  - PyTorch for deep learning
  - Python-dotenv for environment variables
 
## Screenshots
### Home
<img width="1345" alt="home" src="https://github.com/user-attachments/assets/5da1cd7f-aab7-49d9-ba3e-3cb61c436bed" />

### Summaries
<img width="931" alt="summary" src="https://github.com/user-attachments/assets/1de471b3-19f8-42c6-b6f0-4514eb6dd1e7" />



## 📋 Requirements

- Python 3.8+
- NewsAPI Key
- 2GB+ RAM (for running the ML model)
- Internet connection

## ⚙️ Installation

1. Clone the repository:
   ```
   git clone https://github.com/yugandharkhair/news-summarizer.git
   cd news-summarizer
   ```

2. Create a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your NewsAPI key:
   ```
   NEWS_API_KEY=your_news_api_key_here
   ```

5. Run the application:
   ```
   python3 app.py
   ```

6. Open your browser and navigate to `http://127.0.0.1:5000`

## 📱 Usage

1. **Browse News**: Select a category from the dropdown and optionally enter search keywords.
2. **Read Summaries**: Click the "Summarize" button on any article card to generate an AI summary.
3. **Direct Summarization**: Paste any text into the "Direct Text Summarization" section to get a summary.
4. **Full Articles**: Click on an article card (outside the Summarize button) to read the full article.

## 🧠 How It Works

1. The application fetches news articles from NewsAPI based on selected categories and search terms.
2. When a user requests a summary, the full article content is extracted using newspaper3k.
3. The extracted text is processed and fed into a pre-trained T5 model.
4. The model generates a concise summary highlighting the key points of the article.
5. Results are displayed to the user along with the original text for comparison.

## 🔄 Architecture

```
news-summarizer/
│
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── news_fetcher.py        # NewsAPI integration
├── summarizer.py          # ML model for summarization
│
├── static/
│   ├── css/
│   │   └── style.css      # Custom styling
│   └── js/
│       └── main.js        # Frontend functionality
│
├── templates/
│   └── index.html         # Main application page
│
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (not in repo)
```

## 📈 Future Improvements

- Multiple summarization models to choose from
- User accounts to save favorite articles and summaries
- Sentiment analysis of news articles
- Topic clustering to group related news
- Email digest of summarized news
- Expanded language support

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [NewsAPI](https://newsapi.org/) for providing news data
- [HuggingFace Transformers](https://huggingface.co/transformers/) for NLP models
- [Google's T5 Model](https://ai.googleblog.com/2020/02/exploring-transfer-learning-with-t5.html) for text summarization

---

Developed with ❤️ by [Your Name]
