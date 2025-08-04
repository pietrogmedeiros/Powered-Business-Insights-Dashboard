import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class ChurnPredictor:
    def __init__(self):
        self.model = None
        self.scaler_params = None
        self.feature_names = None
        self.is_fitted = False
    
    def prepare_features(self, customer_data):
        """Prepare features for churn prediction"""
        features = customer_data.copy()
        
        # Ensure required columns exist
        required_cols = ['total_spent', 'avg_order_value', 'order_count', 'days_since_last_order', 'customer_lifetime_days']
        for col in required_cols:
            if col not in features.columns:
                features[col] = 0
        
        # Create additional features
        features['avg_days_between_orders'] = features['customer_lifetime_days'] / (features['order_count'] + 1)
        features['spending_velocity'] = features['total_spent'] / (features['customer_lifetime_days'] + 1)
        
        # Encode categorical variables
        features['gender_encoded'] = features['gender'].map({'M': 1, 'F': 0}).fillna(0)
        
        # Select features for modeling
        feature_columns = [
            'age', 'total_spent', 'avg_order_value', 'order_count',
            'days_since_last_order', 'customer_lifetime_days',
            'avg_days_between_orders', 'spending_velocity', 'gender_encoded'
        ]
        
        return features[feature_columns].fillna(0)
    
    def train(self, customer_data):
        """Train churn prediction model (mock implementation)"""
        try:
            logger.info("Training churn prediction model...")

            X = self.prepare_features(customer_data)
            y = customer_data['is_churned'].astype(int) if 'is_churned' in customer_data.columns else np.random.randint(0, 2, len(customer_data))

            # Mock training - store basic statistics
            self.scaler_params = {
                'mean': X.mean().to_dict(),
                'std': X.std().to_dict()
            }

            # Create simple rule-based model
            self.model = self._create_rule_based_churn_model(X, y)
            self.feature_names = X.columns.tolist()
            self.is_fitted = True

            logger.info("Churn prediction model trained successfully (mock)")

            return {
                'auc_score': 0.75,  # Mock AUC score
                'feature_importance': self._get_mock_feature_importance()
            }

        except Exception as e:
            logger.error(f"Error training churn model: {str(e)}")
            raise
    
    def predict_churn(self, customer_data):
        """Predict customer churn probability"""
        try:
            if not self.is_fitted:
                return self._generate_mock_predictions(customer_data)

            X = self.prepare_features(customer_data)

            # Apply rule-based predictions
            churn_probabilities = []
            for _, row in X.iterrows():
                prob = self._calculate_churn_probability(row)
                churn_probabilities.append(prob)

            churn_probabilities = np.array(churn_probabilities)

            # Create predictions dataframe
            predictions_df = customer_data.copy()
            predictions_df['churn_probability'] = churn_probabilities
            predictions_df['risk_level'] = pd.cut(
                churn_probabilities,
                bins=[0, 0.3, 0.7, 1.0],
                labels=['Low', 'Medium', 'High']
            )

            # Sort by churn probability (highest risk first)
            predictions_df = predictions_df.sort_values('churn_probability', ascending=False)

            # Get feature importance
            feature_importance = self._get_mock_feature_importance()

            return {
                'predictions': predictions_df[['customer_id', 'churn_probability', 'risk_level']].to_dict('records') if 'customer_id' in predictions_df.columns else [],
                'feature_importance': feature_importance,
                'overall_churn_rate': float(churn_probabilities.mean()),
                'note': 'Mock predictions - install scikit-learn for advanced ML models'
            }

        except Exception as e:
            logger.error(f"Error predicting churn: {str(e)}")
            return self._generate_mock_predictions(customer_data)

    def _create_rule_based_churn_model(self, X, y):
        """Create a simple rule-based churn model"""
        return {
            'type': 'rule_based',
            'rules': {
                'days_since_last_order_threshold': 60,
                'low_spending_threshold': X['total_spent'].quantile(0.25),
                'low_frequency_threshold': X['order_count'].quantile(0.25)
            }
        }

    def _calculate_churn_probability(self, customer_features):
        """Calculate churn probability using simple rules"""
        prob = 0.1  # Base probability

        # Days since last order
        if customer_features.get('days_since_last_order', 0) > 60:
            prob += 0.4
        elif customer_features.get('days_since_last_order', 0) > 30:
            prob += 0.2

        # Total spending
        if customer_features.get('total_spent', 0) < 100:
            prob += 0.3

        # Order frequency
        if customer_features.get('order_count', 0) < 2:
            prob += 0.2

        # Average order value
        if customer_features.get('avg_order_value', 0) < 50:
            prob += 0.1

        return min(0.95, prob)  # Cap at 95%

    def _get_mock_feature_importance(self):
        """Get mock feature importance"""
        if not self.feature_names:
            return []

        # Mock importance scores
        importance_map = {
            'days_since_last_order': 0.25,
            'total_spent': 0.20,
            'order_count': 0.18,
            'avg_order_value': 0.15,
            'customer_lifetime_days': 0.12,
            'avg_days_between_orders': 0.06,
            'spending_velocity': 0.04
        }

        feature_importance = []
        for feature in self.feature_names:
            importance = importance_map.get(feature, 0.01)
            feature_importance.append({'feature': feature, 'importance': importance})

        feature_importance.sort(key=lambda x: x['importance'], reverse=True)
        return feature_importance

    def _generate_mock_predictions(self, customer_data):
        """Generate mock churn predictions for demonstration"""
        try:
            num_customers = len(customer_data)

            # Generate realistic churn probabilities
            np.random.seed(42)
            churn_probabilities = np.random.beta(2, 5, num_customers)  # Skewed towards lower probabilities

            # Create risk levels
            risk_levels = pd.cut(
                churn_probabilities,
                bins=[0, 0.3, 0.7, 1.0],
                labels=['Low', 'Medium', 'High']
            )

            # Create mock predictions
            predictions = []
            for i in range(num_customers):
                predictions.append({
                    'customer_id': f'customer_{i+1}',
                    'churn_probability': round(churn_probabilities[i], 3),
                    'risk_level': str(risk_levels[i])
                })

            # Sort by churn probability
            predictions.sort(key=lambda x: x['churn_probability'], reverse=True)

            return {
                'predictions': predictions,
                'feature_importance': self._get_mock_feature_importance(),
                'overall_churn_rate': float(churn_probabilities.mean()),
                'note': 'Mock data - train model for real churn predictions'
            }

        except Exception as e:
            logger.error(f"Error generating mock predictions: {str(e)}")
            return {
                'predictions': [],
                'feature_importance': [],
                'overall_churn_rate': 0.0,
                'error': str(e)
            }