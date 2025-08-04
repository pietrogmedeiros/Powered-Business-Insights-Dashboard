import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SalesForecaster:
    def __init__(self):
        self.model = None
        self.is_fitted = False
        self.training_data = None

    def prepare_data(self, df):
        """Prepare data for forecasting model"""
        try:
            df_prepared = df.copy()
            if 'ds' not in df_prepared.columns and 'date' in df_prepared.columns:
                df_prepared['ds'] = pd.to_datetime(df_prepared['date'])
            if 'y' not in df_prepared.columns and 'sales' in df_prepared.columns:
                df_prepared['y'] = df_prepared['sales']

            df_prepared['ds'] = pd.to_datetime(df_prepared['ds'])
            return df_prepared[['ds', 'y']].dropna()
        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            raise

    def train(self, sales_data):
        """Train the forecasting model (mock implementation)"""
        try:
            logger.info("Training sales forecasting model...")

            # Prepare data
            df = self.prepare_data(sales_data)

            if len(df) < 2:
                raise ValueError("Need at least 2 data points to train the model")

            # Store training data and basic statistics
            self.training_data = df
            self.model = {
                'mean': df['y'].mean(),
                'std': df['y'].std(),
                'trend': (df['y'].iloc[-1] - df['y'].iloc[0]) / len(df) if len(df) > 1 else 0,
                'last_date': df['ds'].max(),
                'data_points': len(df),
                'min_value': df['y'].min(),
                'max_value': df['y'].max()
            }

            self.is_fitted = True
            logger.info("Sales forecasting model trained successfully (mock)")
            return self

        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise

    def forecast(self, periods=30):
        """Generate forecast for specified periods"""
        try:
            if not self.is_fitted:
                return self._generate_mock_forecast(periods)

            # Use stored statistics to generate forecast
            base_sales = self.model['mean']
            trend = self.model['trend']
            std = self.model['std']
            last_date = self.model['last_date']

            # Generate forecast based on trend and seasonality
            forecast_data = []
            for i in range(1, periods + 1):
                forecast_date = last_date + timedelta(days=i)

                # Add trend
                value = base_sales + (trend * i)

                # Add seasonal component (weekly pattern)
                day_of_week = forecast_date.weekday()
                seasonal = 0.1 * base_sales * np.sin(2 * np.pi * day_of_week / 7)

                # Add some controlled noise
                noise = np.random.normal(0, std * 0.05) if std > 0 else 0

                forecast_value = max(0, value + seasonal + noise)  # Ensure non-negative

                forecast_data.append({
                    'ds': forecast_date.strftime('%Y-%m-%d'),
                    'yhat': round(forecast_value, 2),
                    'yhat_lower': round(forecast_value - std * 0.5, 2),
                    'yhat_upper': round(forecast_value + std * 0.5, 2)
                })

            return {
                'forecast': forecast_data,
                'components': self._generate_components(forecast_data),
                'note': 'Mock forecast - install Prophet for advanced forecasting'
            }

        except Exception as e:
            logger.error(f"Error generating forecast: {str(e)}")
            return self._generate_mock_forecast(periods)

    def _generate_components(self, forecast_data):
        """Generate mock components data"""
        components = []
        for item in forecast_data:
            components.append({
                'ds': item['ds'],
                'trend': item['yhat'] * 0.8,
                'yearly': item['yhat'] * 0.1,
                'weekly': item['yhat'] * 0.1
            })
        return components

    def _generate_mock_forecast(self, periods=30):
        """Generate mock forecast data for demonstration"""
        try:
            base_date = datetime.now()
            forecast_data = []

            # Generate realistic-looking sales data
            base_sales = 1000

            for i in range(1, periods + 1):
                forecast_date = base_date + timedelta(days=i)

                # Add trend
                trend = i * 2

                # Add seasonality
                seasonality = 100 * np.sin(2 * np.pi * i / 7)  # Weekly pattern

                # Add noise
                noise = np.random.normal(0, 50)

                forecast_value = base_sales + trend + seasonality + noise

                forecast_data.append({
                    'ds': forecast_date.strftime('%Y-%m-%d'),
                    'yhat': round(forecast_value, 2),
                    'yhat_lower': round(forecast_value - 100, 2),
                    'yhat_upper': round(forecast_value + 100, 2)
                })

            return {
                'forecast': forecast_data,
                'components': self._generate_components(forecast_data),
                'note': 'Mock data - install Prophet for real forecasting'
            }

        except Exception as e:
            logger.error(f"Error generating mock forecast: {str(e)}")
            return {
                'forecast': [],
                'components': [],
                'error': str(e)
            }

    def save_model(self, path):
        """Save model (mock implementation)"""
        logger.info(f"Mock save to {path}")
        return True

    def load_model(self, path):
        """Load model (mock implementation)"""
        logger.info(f"Mock load from {path}")
        return True