import pandas as pd
import numpy as np
from collections import Counter
import re
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.model = None
        self.is_fitted = False
        self.positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'perfect', 'best', 'awesome', 'fantastic']
        self.negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'disappointing', 'poor']
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text
    
    def train(self, reviews_data):
        """Train sentiment analysis model (mock implementation)"""
        try:
            logger.info("Training sentiment analysis model...")

            # Preprocess text
            reviews_data['clean_text'] = reviews_data['review_text'].apply(self.preprocess_text)

            # Mock training - analyze word patterns
            self.model = self._create_word_based_model(reviews_data)
            self.is_fitted = True

            logger.info("Sentiment analysis model trained successfully (mock)")
            return self

        except Exception as e:
            logger.error(f"Error training sentiment model: {str(e)}")
            raise
    
    def analyze_sentiment(self, reviews_data):
        """Analyze sentiment of reviews"""
        try:
            if not self.is_fitted:
                return self._generate_mock_analysis(reviews_data)

            reviews_data['clean_text'] = reviews_data['review_text'].apply(self.preprocess_text)

            # Predict sentiments using word-based approach
            predictions = []
            probabilities = []

            for text in reviews_data['clean_text']:
                sentiment, prob = self._predict_sentiment(text)
                predictions.append(sentiment)
                probabilities.append(prob)

            # Calculate sentiment distribution
            sentiment_counts = Counter(predictions)
            total_reviews = len(predictions)
            sentiment_distribution = {
                sentiment: count / total_reviews
                for sentiment, count in sentiment_counts.items()
            }

            # Extract top words for each sentiment
            top_words = self._extract_top_words_simple(reviews_data, predictions)

            return {
                'sentiment_distribution': sentiment_distribution,
                'predictions': predictions,
                'probabilities': probabilities,
                'top_positive_words': top_words['positive'],
                'top_negative_words': top_words['negative'],
                'note': 'Mock sentiment analysis - install scikit-learn for advanced NLP'
            }

        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return self._generate_mock_analysis(reviews_data)
    
    def _create_word_based_model(self, reviews_data):
        """Create a simple word-based sentiment model"""
        return {
            'type': 'word_based',
            'positive_words': self.positive_words,
            'negative_words': self.negative_words
        }

    def _predict_sentiment(self, text):
        """Predict sentiment using word-based approach"""
        words = text.split()
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)

        if positive_count > negative_count:
            sentiment = 'positive'
            confidence = min(0.9, 0.5 + (positive_count - negative_count) * 0.1)
        elif negative_count > positive_count:
            sentiment = 'negative'
            confidence = min(0.9, 0.5 + (negative_count - positive_count) * 0.1)
        else:
            sentiment = 'neutral'
            confidence = 0.5

        # Return probabilities for positive, negative, neutral
        if sentiment == 'positive':
            probs = [confidence, 1-confidence, 0.0]
        elif sentiment == 'negative':
            probs = [1-confidence, confidence, 0.0]
        else:
            probs = [0.3, 0.3, 0.4]

        return sentiment, probs

    def _extract_top_words_simple(self, reviews_data, predictions, top_n=10):
        """Extract top words for each sentiment using simple frequency"""
        top_words = {'positive': [], 'negative': []}

        for sentiment in ['positive', 'negative']:
            sentiment_texts = reviews_data[np.array(predictions) == sentiment]['clean_text']
            if len(sentiment_texts) > 0:
                # Count word frequencies
                word_counts = Counter()
                for text in sentiment_texts:
                    words = text.split()
                    word_counts.update(words)

                # Get top words
                top_words[sentiment] = [
                    {'word': word, 'score': count / len(sentiment_texts)}
                    for word, count in word_counts.most_common(top_n)
                    if len(word) > 2  # Filter out short words
                ]

        return top_words

    def _generate_mock_analysis(self, reviews_data):
        """Generate mock sentiment analysis for demonstration"""
        try:
            num_reviews = len(reviews_data)

            # Generate random sentiments with realistic distribution
            np.random.seed(42)
            sentiments = np.random.choice(
                ['positive', 'negative', 'neutral'],
                size=num_reviews,
                p=[0.6, 0.25, 0.15]  # More positive reviews typically
            )

            # Generate mock probabilities
            probabilities = []
            for sentiment in sentiments:
                if sentiment == 'positive':
                    probs = [0.7, 0.2, 0.1]
                elif sentiment == 'negative':
                    probs = [0.1, 0.8, 0.1]
                else:
                    probs = [0.3, 0.3, 0.4]
                probabilities.append(probs)

            # Calculate distribution
            sentiment_counts = Counter(sentiments)
            sentiment_distribution = {
                sentiment: count / num_reviews
                for sentiment, count in sentiment_counts.items()
            }

            return {
                'sentiment_distribution': sentiment_distribution,
                'predictions': sentiments.tolist(),
                'probabilities': probabilities,
                'top_positive_words': [
                    {'word': word, 'score': 0.8} for word in self.positive_words[:5]
                ],
                'top_negative_words': [
                    {'word': word, 'score': 0.7} for word in self.negative_words[:5]
                ],
                'note': 'Mock data - train model for real sentiment analysis'
            }

        except Exception as e:
            logger.error(f"Error generating mock analysis: {str(e)}")
            return {
                'sentiment_distribution': {},
                'predictions': [],
                'probabilities': [],
                'top_positive_words': [],
                'top_negative_words': [],
                'error': str(e)
            }