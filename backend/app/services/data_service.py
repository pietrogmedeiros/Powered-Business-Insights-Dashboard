import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DataService:
    def __init__(self):
        self._sales_data = None
        self._customer_data = None
        self._reviews_data = None
        self._generate_sample_data()
    
    def _generate_sample_data(self):
        """Generate realistic sample data for demonstration"""
        # Generate sales data
        np.random.seed(42)
        random.seed(42)
        
        start_date = datetime.now() - timedelta(days=365)
        dates = [start_date + timedelta(days=x) for x in range(365)]
        
        sales_records = []
        customer_records = []
        review_records = []
        
        # Generate customers
        customer_ids = [f"CUST_{i:05d}" for i in range(1, 1001)]
        
        for customer_id in customer_ids:
            # Customer demographics
            age = np.random.randint(18, 70)
            gender = random.choice(['M', 'F'])
            location = random.choice(['New York', 'California', 'Texas', 'Florida', 'Illinois'])
            registration_date = start_date + timedelta(days=np.random.randint(0, 300))
            
            customer_records.append({
                'customer_id': customer_id,
                'age': age,
                'gender': gender,
                'location': location,
                'registration_date': registration_date
            })
        
        # Generate sales data
        order_id = 1
        for date in dates:
            # Seasonal patterns
            day_of_year = date.timetuple().tm_yday
            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * day_of_year / 365)
            
            # Weekend effect
            weekend_factor = 1.2 if date.weekday() >= 5 else 1.0
            
            # Number of orders per day
            base_orders = 50
            daily_orders = int(base_orders * seasonal_factor * weekend_factor * np.random.uniform(0.7, 1.3))
            
            for _ in range(daily_orders):
                customer_id = random.choice(customer_ids)
                
                # Order value based on customer behavior
                base_amount = np.random.lognormal(4, 0.8)  # Log-normal distribution
                total_amount = max(10, base_amount)  # Minimum order $10
                
                sales_records.append({
                    'order_id': f"ORD_{order_id:06d}",
                    'customer_id': customer_id,
                    'order_date': date,
                    'total_amount': round(total_amount, 2),
                    'product_category': random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports'])
                })
                order_id += 1
        
        # Generate reviews
        products = [f"Product_{i}" for i in range(1, 101)]
        sentiments = ['positive', 'negative', 'neutral']
        
        positive_words = ['excellent', 'amazing', 'great', 'love', 'perfect', 'outstanding', 'fantastic']
        negative_words = ['terrible', 'awful', 'hate', 'worst', 'disappointing', 'poor', 'bad']
        neutral_words = ['okay', 'average', 'decent', 'fine', 'acceptable']
        
        for i in range(2000):
            sentiment = np.random.choice(sentiments, p=[0.6, 0.25, 0.15])  # More positive reviews
            
            if sentiment == 'positive':
                words = random.sample(positive_words, random.randint(2, 4))
                rating = random.randint(4, 5)
            elif sentiment == 'negative':
                words = random.sample(negative_words, random.randint(2, 3))
                rating = random.randint(1, 2)
            else:
                words = random.sample(neutral_words, random.randint(1, 2))
                rating = 3
            
            review_text = f"This product is {' and '.join(words)}. " + random.choice([
                "Would recommend to others.",
                "Good value for money.",
                "Fast delivery.",
                "Quality could be better.",
                "Exactly as described."
            ])
            
            review_records.append({
                'review_id': f"REV_{i:05d}",
                'customer_id': random.choice(customer_ids),
                'product_id': random.choice(products),
                'rating': rating,
                'review_text': review_text,
                'sentiment': sentiment,
                'review_date': random.choice(dates)
            })
        
        # Convert to DataFrames
        self._sales_data = pd.DataFrame(sales_records)
        self._customer_data = pd.DataFrame(customer_records)
        self._reviews_data = pd.DataFrame(review_records)
        
        # Add churn labels to customer data
        self._add_churn_labels()
    
    def _add_churn_labels(self):
        """Add churn labels based on recent activity"""
        recent_date = self._sales_data['order_date'].max() - timedelta(days=60)
        recent_customers = self._sales_data[
            self._sales_data['order_date'] >= recent_date
        ]['customer_id'].unique()
        
        self._customer_data['is_churned'] = ~self._customer_data['customer_id'].isin(recent_customers)
        
        # Add customer features for churn prediction
        customer_stats = self._sales_data.groupby('customer_id').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'order_date': ['min', 'max']
        }).reset_index()
        
        customer_stats.columns = [
            'customer_id', 'total_spent', 'avg_order_value', 'order_count', 'first_order', 'last_order'
        ]
        
        # Calculate days since last order
        max_date = self._sales_data['order_date'].max()
        customer_stats['days_since_last_order'] = (max_date - customer_stats['last_order']).dt.days
        customer_stats['customer_lifetime_days'] = (customer_stats['last_order'] - customer_stats['first_order']).dt.days
        
        # Merge with customer data
        self._customer_data = self._customer_data.merge(customer_stats, on='customer_id', how='left')
        self._customer_data = self._customer_data.fillna(0)
    
    def get_sales_data(self):
        """Get sales data"""
        return self._sales_data.copy()
    
    def get_customer_data(self):
        """Get customer data"""
        return self._customer_data.copy()
    
    def get_reviews_data(self):
        """Get reviews data"""
        return self._reviews_data.copy()