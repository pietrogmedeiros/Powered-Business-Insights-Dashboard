import asyncio
import pandas as pd
import numpy as np
from app.models.sales_forecasting import SalesForecaster
from app.models.customer_segmentation import CustomerSegmentation
from app.models.sentiment_analysis import SentimentAnalyzer
from app.models.churn_prediction import ChurnPredictor
from app.services.data_service import DataService
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self):
        self.data_service = DataService()
        self.sales_forecaster = SalesForecaster()
        self.customer_segmentation = CustomerSegmentation()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.churn_predictor = ChurnPredictor()
        self._models_trained = False
        
    async def get_business_overview(self):
        """Get high-level business metrics"""
        try:
            # Get sample data
            sales_data = self.data_service.get_sales_data()
            customer_data = self.data_service.get_customer_data()
            
            total_revenue = sales_data['total_amount'].sum()
            active_customers = customer_data['customer_id'].nunique()
            total_orders = len(sales_data)
            
            # Calculate satisfaction score (mock)
            satisfaction_score = np.random.uniform(75, 95)
            
            return {
                "total_revenue": float(total_revenue),
                "active_customers": int(active_customers),
                "total_orders": int(total_orders),
                "satisfaction_score": round(satisfaction_score, 1)
            }
        except Exception as e:
            logger.error(f"Error getting business overview: {e}")
            raise
    
    async def generate_sales_forecast(self, periods=30):
        """Generate sales forecast"""
        try:
            sales_data = self.data_service.get_sales_data()
            
            # Prepare data for forecasting
            daily_sales = sales_data.groupby('order_date')['total_amount'].sum().reset_index()
            
            if not self.sales_forecaster.is_fitted:
                self.sales_forecaster.train(daily_sales)
            
            forecast_result = self.sales_forecaster.forecast(periods)
            
            return {
                "forecast": forecast_result['forecast'],
                "components": forecast_result['components'],
                "insights": self._generate_forecast_insights(forecast_result)
            }
        except Exception as e:
            logger.error(f"Error generating sales forecast: {e}")
            raise
    
    async def analyze_customer_segments(self):
        """Analyze customer segments"""
        try:
            customer_data = self.data_service.get_customer_data()
            
            if not self.customer_segmentation.is_fitted:
                training_result = self.customer_segmentation.train(customer_data)
            
            segmentation_result = self.customer_segmentation.predict_segments(customer_data)
            
            return {
                "segments": segmentation_result['segment_summary'],
                "customer_data": segmentation_result['customer_segments'][:100],  # Limit for performance
                "insights": self._generate_segmentation_insights(segmentation_result)
            }
        except Exception as e:
            logger.error(f"Error analyzing customer segments: {e}")
            raise
    
    async def analyze_sentiment(self):
        """Analyze product review sentiment"""
        try:
            reviews_data = self.data_service.get_reviews_data()
            
            if not self.sentiment_analyzer.is_fitted:
                self.sentiment_analyzer.train(reviews_data)
            
            sentiment_result = self.sentiment_analyzer.analyze_sentiment(reviews_data)
            
            return {
                "sentiment_distribution": sentiment_result['sentiment_distribution'],
                "top_positive_words": sentiment_result['top_positive_words'],
                "top_negative_words": sentiment_result['top_negative_words'],
                "insights": self._generate_sentiment_insights(sentiment_result)
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            raise
    
    async def predict_churn(self):
        """Predict customer churn"""
        try:
            customer_data = self.data_service.get_customer_data()
            
            if not self.churn_predictor.is_fitted:
                self.churn_predictor.train(customer_data)
            
            churn_result = self.churn_predictor.predict_churn(customer_data)
            
            return {
                "churn_predictions": churn_result['predictions'][:50],  # Top 50 at-risk
                "feature_importance": churn_result['feature_importance'],
                "churn_rate": churn_result['overall_churn_rate'],
                "insights": self._generate_churn_insights(churn_result)
            }
        except Exception as e:
            logger.error(f"Error predicting churn: {e}")
            raise
    
    def _generate_forecast_insights(self, forecast_result):
        """Generate insights from forecast results"""
        forecast_data = forecast_result['forecast']
        avg_forecast = np.mean([f['yhat'] for f in forecast_data])
        
        return [
            f"Predicted average daily sales: ${avg_forecast:,.2f}",
            "Sales trend shows seasonal patterns",
            "Consider inventory planning for peak periods"
        ]
    
    def _generate_segmentation_insights(self, segmentation_result):
        """Generate insights from segmentation results"""
        segments = segmentation_result['segment_summary']
        high_value_segment = max(segments, key=lambda x: x['avg_monetary'])
        
        return [
            f"'{high_value_segment['description']}' segment generates highest revenue",
            f"Focus retention efforts on {high_value_segment['size']} high-value customers",
            "Implement targeted marketing campaigns per segment"
        ]
    
    def _generate_sentiment_insights(self, sentiment_result):
        """Generate insights from sentiment analysis"""
        sentiment_dist = sentiment_result['sentiment_distribution']
        negative_pct = sentiment_dist.get('negative', 0) * 100
        
        return [
            f"Customer satisfaction: {100-negative_pct:.1f}% positive sentiment",
            "Monitor negative feedback trends closely",
            "Address common complaints to improve satisfaction"
        ]
    
    def _generate_churn_insights(self, churn_result):
        """Generate insights from churn prediction"""
        churn_rate = churn_result['overall_churn_rate'] * 100
        
        return [
            f"Current churn risk: {churn_rate:.1f}% of customers",
            "Implement retention campaigns for at-risk customers",
            "Focus on improving key satisfaction drivers"
        ]
    
    async def retrain_all_models(self):
        """Retrain all ML models with latest data"""
        try:
            logger.info("Starting model retraining...")
            
            # Get fresh data
            sales_data = self.data_service.get_sales_data()
            customer_data = self.data_service.get_customer_data()
            reviews_data = self.data_service.get_reviews_data()
            
            # Retrain models
            daily_sales = sales_data.groupby('order_date')['total_amount'].sum().reset_index()
            self.sales_forecaster.train(daily_sales)
            self.customer_segmentation.train(customer_data)
            self.sentiment_analyzer.train(reviews_data)
            self.churn_predictor.train(customer_data)
            
            self._models_trained = True
            logger.info("Model retraining completed successfully")
            
        except Exception as e:
            logger.error(f"Error during model retraining: {e}")
            raise