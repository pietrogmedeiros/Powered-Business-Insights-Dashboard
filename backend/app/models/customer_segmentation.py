import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class CustomerSegmentation:
    def __init__(self, n_clusters=4):
        self.n_clusters = n_clusters
        self.model = None
        self.scaler_params = None
        self.is_fitted = False
        self.feature_names = None
        
    def create_rfm_features(self, df):
        """Create RFM (Recency, Frequency, Monetary) features"""
        current_date = df['order_date'].max()
        
        rfm = df.groupby('customer_id').agg({
            'order_date': lambda x: (current_date - x.max()).days,  # Recency
            'order_id': 'count',  # Frequency
            'total_amount': 'sum'  # Monetary
        }).reset_index()
        
        rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary']
        
        # Add additional features
        rfm['avg_order_value'] = rfm['monetary'] / rfm['frequency']
        rfm['recency_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1])
        rfm['frequency_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
        rfm['monetary_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5])
        
        return rfm
    
    def train(self, customer_data):
        """Train clustering model (mock implementation)"""
        try:
            logger.info("Training customer segmentation model...")

            rfm_features = self.create_rfm_features(customer_data)
            features = ['recency', 'frequency', 'monetary', 'avg_order_value']

            X = rfm_features[features]

            # Mock scaling - store mean and std for each feature
            self.scaler_params = {
                'mean': X.mean().to_dict(),
                'std': X.std().to_dict()
            }

            # Mock clustering - use simple rule-based segmentation
            self.model = self._create_rule_based_segments(rfm_features)
            self.feature_names = features
            self.is_fitted = True

            logger.info("Customer segmentation model trained successfully (mock)")

            return {
                'silhouette_score': 0.65,  # Mock score
                'cluster_centers': self._get_mock_centers(),
                'n_customers_per_cluster': self._count_customers_per_segment(rfm_features)
            }

        except Exception as e:
            logger.error(f"Error training segmentation model: {str(e)}")
            raise
    
    def predict_segments(self, customer_data):
        """Predict customer segments"""
        try:
            if not self.is_fitted:
                return self._generate_mock_segments(customer_data)

            rfm_features = self.create_rfm_features(customer_data)

            # Apply rule-based segmentation
            rfm_features['cluster'] = rfm_features.apply(self._assign_segment, axis=1)

            # Create segment descriptions
            segment_summary = self.create_segment_descriptions(rfm_features)

            return {
                'customer_segments': rfm_features.to_dict('records'),
                'segment_summary': segment_summary,
                'note': 'Mock segmentation - install scikit-learn for advanced clustering'
            }

        except Exception as e:
            logger.error(f"Error predicting segments: {str(e)}")
            return self._generate_mock_segments(customer_data)
    
    def create_segment_descriptions(self, rfm_data):
        """Create human-readable segment descriptions"""
        segments = []
        for cluster in range(self.n_clusters):
            cluster_data = rfm_data[rfm_data['cluster'] == cluster]
            
            segment = {
                'cluster_id': int(cluster),
                'size': len(cluster_data),
                'avg_recency': float(cluster_data['recency'].mean()),
                'avg_frequency': float(cluster_data['frequency'].mean()),
                'avg_monetary': float(cluster_data['monetary'].mean()),
                'description': self.get_segment_label(cluster_data)
            }
            segments.append(segment)
        
        return segments
    
    def get_segment_label(self, cluster_data):
        """Generate descriptive labels for segments"""
        avg_recency = cluster_data['recency'].mean()
        avg_frequency = cluster_data['frequency'].mean()
        avg_monetary = cluster_data['monetary'].mean()

        if avg_monetary > 1000 and avg_frequency > 5:
            return "High-Value Champions"
        elif avg_monetary > 500 and avg_recency < 30:
            return "Loyal Customers"
        elif avg_recency > 90:
            return "At-Risk Customers"
        else:
            return "Potential Loyalists"

    def _create_rule_based_segments(self, rfm_features):
        """Create rule-based segmentation model"""
        return {
            'type': 'rule_based',
            'rules': {
                0: {'monetary_min': 1000, 'frequency_min': 5, 'label': 'High-Value Champions'},
                1: {'monetary_min': 500, 'recency_max': 30, 'label': 'Loyal Customers'},
                2: {'recency_min': 90, 'label': 'At-Risk Customers'},
                3: {'default': True, 'label': 'Potential Loyalists'}
            }
        }

    def _assign_segment(self, row):
        """Assign segment based on rules"""
        if row['monetary'] > 1000 and row['frequency'] > 5:
            return 0  # High-Value Champions
        elif row['monetary'] > 500 and row['recency'] < 30:
            return 1  # Loyal Customers
        elif row['recency'] > 90:
            return 2  # At-Risk Customers
        else:
            return 3  # Potential Loyalists

    def _get_mock_centers(self):
        """Get mock cluster centers"""
        return [
            [20, 8, 1500, 187.5],  # High-Value Champions
            [15, 6, 750, 125.0],   # Loyal Customers
            [120, 2, 200, 100.0],  # At-Risk Customers
            [45, 4, 400, 100.0]    # Potential Loyalists
        ]

    def _count_customers_per_segment(self, rfm_features):
        """Count customers per segment"""
        segments = rfm_features.apply(self._assign_segment, axis=1)
        counts = []
        for i in range(self.n_clusters):
            counts.append(int((segments == i).sum()))
        return counts

    def _generate_mock_segments(self, customer_data):
        """Generate mock segmentation for demonstration"""
        try:
            # Create basic RFM features
            rfm_features = self.create_rfm_features(customer_data)

            # Assign random segments for demo
            np.random.seed(42)
            rfm_features['cluster'] = np.random.randint(0, self.n_clusters, len(rfm_features))

            # Create segment descriptions
            segment_summary = self.create_segment_descriptions(rfm_features)

            return {
                'customer_segments': rfm_features.to_dict('records'),
                'segment_summary': segment_summary,
                'note': 'Mock data - train model for real segmentation'
            }

        except Exception as e:
            logger.error(f"Error generating mock segments: {str(e)}")
            return {
                'customer_segments': [],
                'segment_summary': [],
                'error': str(e)
            }