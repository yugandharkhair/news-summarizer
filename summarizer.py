import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from config import SUMMARIZATION_MODEL, MAX_INPUT_LENGTH, MAX_SUMMARY_LENGTH, MIN_SUMMARY_LENGTH
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextSummarizer:
    """Class to summarize text using pre-trained models from Hugging Face"""
    
    def __init__(self, model_name=SUMMARIZATION_MODEL):
        logger.info(f"Initializing summarizer with model: {model_name}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        # Move model to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        logger.info(f"Model loaded. Using device: {self.device}")
        
    def summarize(self, text, max_length=MAX_SUMMARY_LENGTH, min_length=MIN_SUMMARY_LENGTH):
        """
        Summarize the given text
        
        Args:
            text (str): Text to summarize
            max_length (int): Maximum length of the summary
            min_length (int): Minimum length of the summary
            
        Returns:
            str: Generated summary
        """
        # Truncate input text if needed
        if len(text) > MAX_INPUT_LENGTH * 4:  # Rough character estimate
            text = text[:MAX_INPUT_LENGTH * 4]
            
        try:
            # Handle model-specific input formatting
            if "t5" in self.model.config._name_or_path:
                input_text = "summarize: " + text
            else:
                input_text = text
                
            # Tokenize and generate summary
            inputs = self.tokenizer(input_text, return_tensors="pt", max_length=MAX_INPUT_LENGTH, 
                                   truncation=True).to(self.device)
            
            # Generate summary
            summary_ids = self.model.generate(
                inputs["input_ids"],
                max_length=max_length,
                min_length=min_length,
                num_beams=4,
                length_penalty=2.0,
                early_stopping=True,
                no_repeat_ngram_size=2
            )
            
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Error generating summary."