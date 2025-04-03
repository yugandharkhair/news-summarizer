document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const newsFilterForm = document.getElementById('newsFilterForm');
    const textSummarizationForm = document.getElementById('textSummarizationForm');
    const articlesList = document.getElementById('articlesList');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const errorAlert = document.getElementById('errorAlert');
    const errorMessage = document.getElementById('errorMessage');
    const summaryContainer = document.getElementById('summaryContainer');
    const textSummaryContainer = document.getElementById('textSummaryContainer');
    const closeSummary = document.getElementById('closeSummary');
    const closeTextSummary = document.getElementById('closeTextSummary');
    
    // On page load, fetch default news
    fetchNews();
    
    // Event listeners
    newsFilterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        fetchNews();
    });
    
    textSummarizationForm.addEventListener('submit', function(e) {
        e.preventDefault();
        summarizeText();
    });
    
    closeSummary.addEventListener('click', function() {
        summaryContainer.classList.add('d-none');
    });
    
    closeTextSummary.addEventListener('click', function() {
        textSummaryContainer.classList.add('d-none');
    });
    
    /**
     * Fetch news articles based on selected filters
     */
    function fetchNews() {
        // Show loading spinner
        loadingSpinner.classList.remove('d-none');
        articlesList.innerHTML = '';
        
        // Hide summary containers
        summaryContainer.classList.add('d-none');
        textSummaryContainer.classList.add('d-none');
        
        // Get filter values
        const category = document.getElementById('categorySelect').value;
        const country = document.getElementById('countrySelect').value;
        const query = document.getElementById('searchQuery').value;
        
        // Fetch news from API
        fetch(`/get_news?category=${category}&country=${country}&query=${query}`)
            .then(response => response.json())
            .then(data => {
                loadingSpinner.classList.add('d-none');
                
                if (data.success) {
                    displayArticles(data.articles);
                } else {
                    showError('Failed to fetch news articles');
                }
            })
            .catch(error => {
                loadingSpinner.classList.add('d-none');
                showError('Network error. Please try again later.');
                console.error('Error:', error);
            });
    }
    
    /**
     * Display articles in the UI
     */
    function displayArticles(articles) {
        if (articles.length === 0) {
            articlesList.innerHTML = `
                <div class="alert alert-info">
                    No articles found. Try different filters.
                </div>
            `;
            return;
        }
        
        let articlesHTML = '<div class="row">';
        
        articles.forEach(article => {
            // Default image if none is provided
            const imageUrl = article.urlToImage || 'https://via.placeholder.com/300x200?text=No+Image';
            
            // Truncate description if too long
            const description = article.description ? 
                (article.description.length > 120 ? article.description.substring(0, 120) + '...' : article.description) : 
                'No description available';
            
            articlesHTML += `
                <div class="col-md-6 mb-4">
                    <div class="card h-100 news-card" data-url="${article.url}">
                        <img src="${imageUrl}" class="card-img-top news-image" alt="${article.title}">
                        <div class="card-body">
                            <h5 class="card-title">${article.title}</h5>
                            <p class="card-text">${description}</p>
                        </div>
                        <div class="card-footer d-flex justify-content-between align-items-center">
                            <small class="text-muted">${formatDate(article.publishedAt)}</small>
                            <button class="btn btn-primary btn-sm summarize-btn" data-url="${article.url}">Summarize</button>
                        </div>
                    </div>
                </div>
            `;
        });
        
        articlesHTML += '</div>';
        articlesList.innerHTML = articlesHTML;
        
        // Add event listeners to summarize buttons
        document.querySelectorAll('.summarize-btn').forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                summarizeArticle(this.dataset.url);
            });
        });
        
        // Add event listeners to cards
        document.querySelectorAll('.news-card').forEach(card => {
            card.addEventListener('click', function(e) {
                // Open article in new tab when card is clicked
                if (!e.target.classList.contains('summarize-btn')) {
                    window.open(this.dataset.url, '_blank');
                }
            });
        });
    }
    
    /**
     * Summarize an article from its URL
     */
    function summarizeArticle(url) {
        // Show loading state
        summaryContainer.classList.remove('d-none');
        document.getElementById('summaryTitle').textContent = 'Generating summary...';
        document.getElementById('originalText').innerHTML = '<div class="placeholder-glow">Loading original text...</div>';
        document.getElementById('generatedSummary').innerHTML = '<div class="placeholder-glow">AI is summarizing the article...</div>';
        document.getElementById('processingTime').textContent = '';
        document.getElementById('articleLink').href = url;
        
        // Scroll to summary container
        summaryContainer.scrollIntoView({ behavior: 'smooth' });
        
        // Send request to backend
        fetch('/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update summary container
                document.getElementById('summaryTitle').textContent = data.title;
                document.getElementById('originalText').textContent = data.original_text;
                document.getElementById('generatedSummary').textContent = data.summary;
                document.getElementById('processingTime').textContent = `Processing time: ${data.processing_time}`;
            } else {
                showError(data.error || 'Failed to generate summary');
                summaryContainer.classList.add('d-none');
            }
        })
        .catch(error => {
            showError('Network error. Please try again later.');
            summaryContainer.classList.add('d-none');
            console.error('Error:', error);
        });
    }
    
    /**
     * Summarize text input directly
     */
    function summarizeText() {
        const text = document.getElementById('directText').value.trim();
        
        if (!text) {
            showError('Please enter text to summarize');
            return;
        }
        
        // Show loading state
        textSummaryContainer.classList.remove('d-none');
        document.getElementById('textOriginal').innerHTML = '<div class="placeholder-glow">Loading original text...</div>';
        document.getElementById('textSummary').innerHTML = '<div class="placeholder-glow">AI is summarizing the text...</div>';
        document.getElementById('textProcessingTime').textContent = '';
        
        // Scroll to summary container
        textSummaryContainer.scrollIntoView({ behavior: 'smooth' });
        
        // Send request to backend
        fetch('/summarize_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update summary container
                document.getElementById('textOriginal').textContent = data.original_text;
                document.getElementById('textSummary').textContent = data.summary;
                document.getElementById('textProcessingTime').textContent = `Processing time: ${data.processing_time}`;
            } else {
                showError(data.error || 'Failed to generate summary');
                textSummaryContainer.classList.add('d-none');
            }
        })
        .catch(error => {
            showError('Network error. Please try again later.');
            textSummaryContainer.classList.add('d-none');
            console.error('Error:', error);
        });
    }
    
    /**
     * Display error message
     */
    function showError(message) {
        errorMessage.textContent = message;
        errorAlert.classList.remove('d-none');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            errorAlert.classList.add('d-none');
        }, 5000);
    }
    
    /**
     * Format date string
     */
    function formatDate(dateString) {
        if (!dateString) return 'Unknown date';
        
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }
});